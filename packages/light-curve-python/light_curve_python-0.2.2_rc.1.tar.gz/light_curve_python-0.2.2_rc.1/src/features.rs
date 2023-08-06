use crate::arr_wrapper::ArrWrapper;
use crate::sorted::is_sorted;
use light_curve_feature as lcf;
use numpy::{IntoPyArray, PyArray1};
use pyo3::exceptions::{PyNotImplementedError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyTuple;

type F = f64;
type Arr<T> = PyArray1<T>;

#[pyclass(subclass, name = "_FeatureEvaluator")]
pub struct PyFeatureEvaluator {
    feature_evaluator: Box<dyn lcf::FeatureEvaluator<F>>,
}

#[pymethods]
impl PyFeatureEvaluator {
    #[call]
    #[args(t, m, sigma = "None", sorted = "None", fill_value = "None")]
    fn __call__<'py>(
        &self,
        py: Python<'py>,
        t: &Arr<F>,
        m: &Arr<F>,
        sigma: Option<&Arr<F>>,
        sorted: Option<bool>,
        fill_value: Option<F>,
    ) -> PyResult<&'py PyArray1<F>> {
        if t.len() != m.len() {
            return Err(PyValueError::new_err("t and m must have the same size"));
        }
        if let Some(sigma) = sigma {
            if t.len() != sigma.len() {
                return Err(PyValueError::new_err("t and sigma must have the same size"));
            }
        }
        if t.len() < self.feature_evaluator.min_ts_length() {
            return Err(PyValueError::new_err(format!(
                "input arrays must have size not smaller than {}, but having {}",
                self.feature_evaluator.min_ts_length(),
                t.len()
            )));
        }

        let is_t_required = match (
            self.feature_evaluator.is_t_required(),
            self.feature_evaluator.is_sorting_required(),
            sorted,
        ) {
            // feature requires t
            (true, _, _) => true,
            // t is required because sorting is required and data can be unsorted
            (false, true, Some(false)) | (false, true, None) => true,
            // sorting is required but user guarantees that data is already sorted
            (false, true, Some(true)) => false,
            // neither t or sorting is required
            (false, false, _) => false,
        };
        let t = ArrWrapper::new(t, is_t_required);
        match sorted {
            Some(true) => {}
            Some(false) => {
                return Err(PyNotImplementedError::new_err(
                    "sorting is not implemented, please provide time-sorted arrays",
                ))
            }
            None => {
                if self.feature_evaluator.is_sorting_required() & !is_sorted(&t) {
                    return Err(PyValueError::new_err("t must be in ascending order"));
                }
            }
        }

        let m = ArrWrapper::new(m, self.feature_evaluator.is_m_required());

        let w = sigma.and_then(|sigma| {
            if self.feature_evaluator.is_w_required() {
                let mut w = sigma.to_owned_array();
                w.mapv_inplace(|x| x.powi(-2));
                Some(ArrWrapper::Owned(w))
            } else {
                None
            }
        });

        let mut ts = lcf::TimeSeries::new(&t, &m, w.as_deref());

        let result = match fill_value {
            Some(x) => self.feature_evaluator.eval_or_fill(&mut ts, x),
            None => self
                .feature_evaluator
                .eval(&mut ts)
                .map_err(|e| PyValueError::new_err(e.to_string()))?,
        };
        Ok(result.into_pyarray(py))
    }

    /// Feature names
    #[getter]
    fn names(&self) -> Vec<&str> {
        self.feature_evaluator.get_names()
    }

    /// Feature descriptions
    #[getter]
    fn descriptions(&self) -> Vec<&str> {
        self.feature_evaluator.get_descriptions()
    }
}

/// Features extractor
///
/// Extract multiple features simultaneously, which should be more
/// performant than calling them separately
///
/// Parameters
/// ----------
/// *features : iterable
///     Feature objects
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(*args)"]
pub struct Extractor {}

#[pymethods]
impl Extractor {
    #[new]
    #[args(args = "*")]
    fn __new__(args: &PyTuple) -> PyResult<(Self, PyFeatureEvaluator)> {
        let evals = args
            .iter()
            .map(|arg| {
                arg.downcast::<PyCell<PyFeatureEvaluator>>()
                    .map(|fe| fe.borrow().feature_evaluator.clone())
            })
            .collect::<Result<Vec<_>, _>>()?;
        Ok((
            Self {},
            PyFeatureEvaluator {
                feature_evaluator: Box::new(lcf::FeatureExtractor::new(evals)),
            },
        ))
    }
}

macro_rules! evaluator {
    ($name: ident, $eval: ty $(,)?) => {
        #[pyclass(extends = PyFeatureEvaluator)]
        #[text_signature = "()"]
        pub struct $name {}

        #[pymethods]
        impl $name {
            #[new]
            fn __new__() -> (Self, PyFeatureEvaluator) {
                (
                    Self {},
                    PyFeatureEvaluator {
                        feature_evaluator: Box::new(<$eval>::new()),
                    },
                )
            }
        }
    };
}

evaluator!(Amplitude, lcf::Amplitude);

evaluator!(AndersonDarlingNormal, lcf::AndersonDarlingNormal);

/// Fraction of observations beyond N*std from mean
///
/// Parameters
/// ----------
/// nstd : positive float
///     N
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(nstd, /)"]
pub struct BeyondNStd {}

#[pymethods]
impl BeyondNStd {
    #[new]
    fn __new__(nstd: F) -> (Self, PyFeatureEvaluator) {
        (
            Self {},
            PyFeatureEvaluator {
                feature_evaluator: Box::new(lcf::BeyondNStd::new(nstd)),
            },
        )
    }
}

#[cfg(feature = "nonlinear-fit")]
evaluator!(BazinFit, lcf::BazinFit);

/// Binned time-series
///
/// Parameters
/// ----------
/// features : iterable
///     Features to extract from binned time-series
/// window : positive float
///     Width of binning interval in units of time
/// offset : float
///     Zero time moment
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(features, window, offset)"]
pub struct Bins {}

#[pymethods]
impl Bins {
    #[new]
    #[args(features, window, offset)]
    fn __new__(
        py: Python,
        features: PyObject,
        window: F,
        offset: F,
    ) -> PyResult<(Self, PyFeatureEvaluator)> {
        let mut eval = lcf::Bins::default();
        for x in features.extract::<&PyAny>(py)?.iter()? {
            let feature = x?
                .downcast::<PyCell<PyFeatureEvaluator>>()?
                .borrow()
                .feature_evaluator
                .clone();
            eval.add_feature(feature);
        }
        eval.set_window(window);
        eval.set_offset(offset);
        Ok((
            Self {},
            PyFeatureEvaluator {
                feature_evaluator: Box::new(eval),
            },
        ))
    }
}

evaluator!(Cusum, lcf::Cusum);

evaluator!(Eta, lcf::Eta);

evaluator!(EtaE, lcf::EtaE);

evaluator!(ExcessVariance, lcf::ExcessVariance);

/// Inner percentile range
///
/// Parameters
/// ----------
/// quantile : positive float
///     Range is (100% * quantile, 100% * (1 - quantile))
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(quantile)"]
pub struct InterPercentileRange {}

#[pymethods]
impl InterPercentileRange {
    #[new]
    #[args(quantile)]
    fn __new__(quantile: f32) -> (Self, PyFeatureEvaluator) {
        (
            Self {},
            PyFeatureEvaluator {
                feature_evaluator: Box::new(lcf::InterPercentileRange::new(quantile)),
            },
        )
    }
}

evaluator!(Kurtosis, lcf::Kurtosis);

evaluator!(LinearFit, lcf::LinearFit);

evaluator!(LinearTrend, lcf::LinearTrend);

/// Ratio of two inter-percentile ranges
///
/// Parameters
/// ----------
/// quantile_numerator: positive float
///     Numerator is inter-percentile range (100% * q, 100% (1 - q))
/// quantile_denominator: positive float
///     Denominator is inter-percentile range (100% * q, 100% (1 - q))
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(quantile_numerator, quantile_denominator)"]
pub struct MagnitudePercentageRatio {}

#[pymethods]
impl MagnitudePercentageRatio {
    #[new]
    #[args(quantile_numerator, quantile_denominator)]
    fn __new__(
        quantile_numerator: f32,
        quantile_denominator: f32,
    ) -> PyResult<(Self, PyFeatureEvaluator)> {
        if !(0.0..0.5).contains(&quantile_numerator) {
            return Err(PyValueError::new_err(
                "quantile_numerator must be between 0.0 and 0.5",
            ));
        }
        if !(0.0..0.5).contains(&quantile_denominator) {
            return Err(PyValueError::new_err(
                "quantile_denumerator must be between 0.0 and 0.5",
            ));
        }
        Ok((
            Self {},
            PyFeatureEvaluator {
                feature_evaluator: Box::new(lcf::MagnitudePercentageRatio::new(
                    quantile_numerator,
                    quantile_denominator,
                )),
            },
        ))
    }
}

evaluator!(MaximumSlope, lcf::MaximumSlope);

evaluator!(Mean, lcf::Mean);

evaluator!(MeanVariance, lcf::MeanVariance);

evaluator!(Median, lcf::Median);

evaluator!(MedianAbsoluteDeviation, lcf::MedianAbsoluteDeviation,);

/// Median Buffer Range Percentage
///
/// Parameters
/// ----------
/// quantile : positive float
///     Relative range size
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(quantile)"]
pub struct MedianBufferRangePercentage {}

#[pymethods]
impl MedianBufferRangePercentage {
    #[new]
    #[args(quantile)]
    fn __new__(quantile: F) -> (Self, PyFeatureEvaluator) {
        (
            Self {},
            PyFeatureEvaluator {
                feature_evaluator: Box::new(lcf::MedianBufferRangePercentage::new(quantile)),
            },
        )
    }
}

evaluator!(PercentAmplitude, lcf::PercentAmplitude);

/// Percent Difference Magnitude Percentile
///
/// Parameters
/// ----------
/// quantile : positive float
///     Relative range size
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(quantile)"]
pub struct PercentDifferenceMagnitudePercentile {}

#[pymethods]
impl PercentDifferenceMagnitudePercentile {
    #[new]
    #[args(quantile)]
    fn __new__(quantile: f32) -> (Self, PyFeatureEvaluator) {
        (
            Self {},
            PyFeatureEvaluator {
                feature_evaluator: Box::new(lcf::PercentDifferenceMagnitudePercentile::new(
                    quantile,
                )),
            },
        )
    }
}

/// Periodogram-based features
///
/// Parameters
/// ----------
/// peaks : int or None, optional
///     Number of peaks to find
///
/// resolution : float or None, optional
///     Resolution of frequency grid
///
/// max_freq_factor : float or None, optional
///     Mulitplier for Nyquist frequency
///
/// nyquist : str or float or None, optional
///     Type of Nyquist frequency. Could be one of:
///      - 'average': "Average" Nyquist frequency
///      - 'median': Nyquist frequency is defined by median time interval
///         between observations
///      - float: Nyquist frequency is defined by given quantile of time
///         intervals between observations
///
/// fast : bool or None, optional
///     Use "Fast" (approximate and FFT-based) or direct periodogram algorithm
///
/// features : iterable or None, optional
///     Features to extract from periodogram considering it as a time-series
///
#[pyclass(extends = PyFeatureEvaluator)]
#[text_signature = "(peaks=None, resolution=None, max_freq_factor=None, nyquist=None, fast=None, features=None)"]
pub struct Periodogram {
    eval: lcf::Periodogram<F>,
}

impl Periodogram {
    fn create_eval(
        py: Python,
        peaks: Option<usize>,
        resolution: Option<f32>,
        max_freq_factor: Option<f32>,
        nyquist: Option<PyObject>,
        fast: Option<bool>,
        features: Option<PyObject>,
    ) -> PyResult<lcf::Periodogram<F>> {
        let mut eval = match peaks {
            Some(peaks) => lcf::Periodogram::new(peaks),
            None => lcf::Periodogram::default(),
        };
        if let Some(resolution) = resolution {
            eval.set_freq_resolution(resolution);
        }
        if let Some(max_freq_factor) = max_freq_factor {
            eval.set_max_freq_factor(max_freq_factor);
        }
        if let Some(nyquist) = nyquist {
            let nyquist_freq: Box<dyn lcf::NyquistFreq<F>> =
                if let Ok(s) = nyquist.extract::<&str>(py) {
                    match s {
                        "average" => Box::new(lcf::AverageNyquistFreq {}),
                        "median" => Box::new(lcf::MedianNyquistFreq {}),
                        _ => return Err(PyValueError::new_err(
                            "nyquist must be one of: None, 'average', 'median' or quantile value",
                        )),
                    }
                } else if let Ok(quantile) = nyquist.extract::<f32>(py) {
                    Box::new(lcf::QuantileNyquistFreq { quantile })
                } else {
                    return Err(PyValueError::new_err(
                        "nyquist must be one of: None, 'average', 'median' or quantile value",
                    ));
                };
            eval.set_nyquist(nyquist_freq);
        }
        if let Some(fast) = fast {
            if fast {
                eval.set_periodogram_algorithm(Box::new(lcf::PeriodogramPowerFft::new()));
            } else {
                eval.set_periodogram_algorithm(Box::new(lcf::PeriodogramPowerDirect {}));
            }
        }
        if let Some(features) = features {
            for x in features.extract::<&PyAny>(py)?.iter()? {
                let feature = x?
                    .downcast::<PyCell<PyFeatureEvaluator>>()?
                    .borrow()
                    .feature_evaluator
                    .clone();
                eval.add_feature(feature);
            }
        }
        Ok(eval)
    }
}

#[pymethods]
impl Periodogram {
    #[new]
    #[args(
        peaks = "None",
        resolution = "None",
        max_freq_factor = "None",
        nyquist = "None",
        fast = "None",
        features = "None"
    )]
    fn __new__(
        py: Python,
        peaks: Option<usize>,
        resolution: Option<f32>,
        max_freq_factor: Option<f32>,
        nyquist: Option<PyObject>,
        fast: Option<bool>,
        features: Option<PyObject>,
    ) -> PyResult<(Self, PyFeatureEvaluator)> {
        Ok((
            Self {
                eval: Self::create_eval(
                    py,
                    peaks,
                    resolution,
                    max_freq_factor,
                    nyquist.as_ref().map(|x| x.clone_ref(py)),
                    fast,
                    features.as_ref().map(|x| x.clone_ref(py)),
                )?,
            },
            PyFeatureEvaluator {
                feature_evaluator: Box::new(Self::create_eval(
                    py,
                    peaks,
                    resolution,
                    max_freq_factor,
                    nyquist,
                    fast,
                    features,
                )?),
            },
        ))
    }

    /// Angular frequencies and periodogram values
    #[text_signature = "(t, m)"]
    fn freq_power<'py>(
        &self,
        py: Python<'py>,
        t: &Arr<F>,
        m: &Arr<F>,
    ) -> (&'py PyArray1<F>, &'py PyArray1<F>) {
        let t = ArrWrapper::new(t, true);
        let m = ArrWrapper::new(m, true);
        let mut ts = lcf::TimeSeries::new(&t, &m, None);
        let (freq, power) = self.eval.freq_power(&mut ts);
        (freq.into_pyarray(py), power.into_pyarray(py))
    }
}

evaluator!(ReducedChi2, lcf::ReducedChi2);

evaluator!(Skew, lcf::Skew);

evaluator!(StandardDeviation, lcf::StandardDeviation);

evaluator!(StetsonK, lcf::StetsonK);

evaluator!(WeightedMean, lcf::WeightedMean);

evaluator!(Duration, lcf::antifeatures::Duration);

evaluator!(MaximumTimeInterval, lcf::antifeatures::MaximumTimeInterval);

evaluator!(MinimumTimeInterval, lcf::antifeatures::MinimumTimeInterval);

evaluator!(ObservationCount, lcf::antifeatures::ObservationCount);

evaluator!(TimeMean, lcf::antifeatures::TimeMean);

evaluator!(
    TimeStandardDeviation,
    lcf::antifeatures::TimeStandardDeviation
);

/// Features highly dependent on time-series cadence
///
/// See feature interface documentation in the top-level module
#[pymodule]
pub fn antifeatures(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Duration>()?;
    m.add_class::<MaximumTimeInterval>()?;
    m.add_class::<MinimumTimeInterval>()?;
    m.add_class::<ObservationCount>()?;
    m.add_class::<TimeMean>()?;
    m.add_class::<TimeStandardDeviation>()?;

    Ok(())
}
