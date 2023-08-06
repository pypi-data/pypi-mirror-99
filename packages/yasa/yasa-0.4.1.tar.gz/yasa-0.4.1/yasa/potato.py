"""Re-implementation of pyRiemann's Potato Class for artefact detection.

The pyRiemann package, which is used in the yasa.art_detect function, is no
longer maintained (https://github.com/alexandrebarachant/pyRiemann/issues/92),
and as a consequence breaks with newer versions of scikit-learn. I therefore
decided to re-implement the Potato class directly in YASA.

All credits goes to Alexandra Barachant for writing the original code:
https://github.com/alexandrebarachant/pyRiemann
"""
import scipy
import numpy as np
from scipy.linalg import eigvalsh
from sklearn.utils.extmath import softmax
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin

# from .utils.mean import mean_covariance
from numpy.core.numerictypes import typecodes

###############################################################################
# COVARIANCE
###############################################################################


def _matrix_operator(Ci, operator):
    """Matrix equivalent of an operator."""
    if Ci.dtype.char in typecodes['AllFloat'] and not np.isfinite(Ci).all():
        raise ValueError(
            "Covariance matrices must be positive definite. ",
            "Add regularization to avoid this error.")
    eigvals, eigvects = scipy.linalg.eigh(Ci, check_finite=False)
    eigvals = np.diag(operator(eigvals))
    Out = np.dot(np.dot(eigvects, eigvals), eigvects.T)
    return Out


def sqrtm(Ci):
    """Return the matrix square root of a covariance matrix.
    """
    return _matrix_operator(Ci, np.sqrt)


def logm(Ci):
    """Return the matrix logarithm of a covariance matrix.
    """
    return _matrix_operator(Ci, np.log)


def expm(Ci):
    """Return the matrix exponential of a covariance matrix.
    """
    return _matrix_operator(Ci, np.exp)


def invsqrtm(Ci):
    """Return the inverse matrix square root of a covariance matrix.
    """

    def isqrt(x):
        return 1. / np.sqrt(x)

    return _matrix_operator(Ci, isqrt)


def _get_sample_weight(sample_weight, data):
    """Get the sample weights.
    If none provided, weights init to 1. otherwise, weights are normalized.
    """
    if sample_weight is None:
        sample_weight = np.ones(data.shape[0])
    if len(sample_weight) != data.shape[0]:
        raise ValueError("len of sample_weight must be equal to len of data.")
    sample_weight /= np.sum(sample_weight)
    return sample_weight


def mean_riemann(covmats, tol=10e-9, maxiter=50, init=None,
                 sample_weight=None):
    """Return the mean covariance matrix according to the Riemannian metric.
    """
    # init
    sample_weight = _get_sample_weight(sample_weight, covmats)
    Nt, Ne, Ne = covmats.shape
    if init is None:
        C = np.mean(covmats, axis=0)
    else:
        C = init
    k = 0
    nu = 1.0
    tau = np.finfo(np.float64).max
    crit = np.finfo(np.float64).max
    # stop when J<10^-9 or max iteration = 50
    while (crit > tol) and (k < maxiter) and (nu > tol):
        k = k + 1
        C12 = sqrtm(C)
        Cm12 = invsqrtm(C)
        J = np.zeros((Ne, Ne))

        for index in range(Nt):
            tmp = np.dot(np.dot(Cm12, covmats[index, :, :]), Cm12)
            J += sample_weight[index] * logm(tmp)

        crit = np.linalg.norm(J, ord='fro')
        h = nu * crit
        C = np.dot(np.dot(C12, expm(nu * J)), C12)
        if h < tau:
            nu = 0.95 * nu
            tau = h
        else:
            nu = 0.5 * nu

    return C


def mean_covariance(covmats, metric='riemann', sample_weight=None, *args):
    """Return the mean covariance matrix according to the metric.
    """
    return mean_riemann(covmats, sample_weight=sample_weight, *args)


###############################################################################
# DISTANCE
###############################################################################

def distance_riemann(A, B):
    """Riemannian distance between two covariance matrices A and B.
    """
    return np.sqrt((np.log(eigvalsh(A, B))**2).sum())


def distance(A, B):
    """Distance between two covariance matrices A and B according to the metric.
    """
    if len(A.shape) == 3:
        d = np.empty((len(A), 1))
        for i in range(len(A)):
            d[i] = distance_riemann(A[i], B)
    else:
        d = distance_riemann(A, B)
    return d


###############################################################################
# MINIMUM DISTANCE TO MEAN
###############################################################################


class MDM(BaseEstimator, ClassifierMixin, TransformerMixin):
    """Classification by Minimum Distance to Mean.

    Classification by nearest centroid. For each of the given classes, a
    centroid is estimated according to the chosen metric. Then, for each new
    point, the class is affected according to the nearest centroid.

    Parameters
    ----------
    metric : string | dict (default: 'riemann')
        The type of metric used for centroid and distance estimation.
        see `mean_covariance` for the list of supported metric.
        the metric could be a dict with two keys, `mean` and `distance` in
        order to pass different metric for the centroid estimation and the
        distance estimation. Typical usecase is to pass 'logeuclid' metric for
        the mean in order to boost the computional speed and 'riemann' for the
        distance in order to keep the good sensitivity for the classification.

    Attributes
    ----------
    covmeans_ : list
        the class centroids.
    classes_ : list
        list of classes.

    References
    ----------
    [1] A. Barachant, S. Bonnet, M. Congedo and C. Jutten, "Multiclass
    Brain-Computer Interface Classification by Riemannian Geometry," in IEEE
    Transactions on Biomedical Engineering, vol. 59, no. 4, p. 920-928, 2012.
    [2] A. Barachant, S. Bonnet, M. Congedo and C. Jutten, "Riemannian geometry
    applied to BCI classification", 9th International Conference Latent
    Variable Analysis and Signal Separation (LVA/ICA 2010), LNCS vol. 6365,
    2010, p. 629-636.
    """

    def __init__(self, metric='riemann'):
        """Init."""
        # store params for cloning purpose
        self.metric = metric

        if isinstance(metric, str):
            self.metric_mean = metric
            self.metric_dist = metric

        elif isinstance(metric, dict):
            # check keys
            for key in ['mean', 'distance']:
                if key not in metric.keys():
                    raise KeyError('metric must contain "mean" and "distance"')

            self.metric_mean = metric['mean']
            self.metric_dist = metric['distance']

        else:
            raise TypeError('metric must be dict or str')

    def fit(self, X, y, sample_weight=None):
        """Fit (estimates) the centroids.

        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels, n_channels)
            ndarray of SPD matrices.
        y : ndarray shape (n_trials, 1)
            labels corresponding to each trial.
        sample_weight : None | ndarray shape (n_trials, 1)
            the weights of each sample. if None, each sample is treated with
            equal weights.

        Returns
        -------
        self : MDM instance
            The MDM instance.
        """
        self.classes_ = np.unique(y)

        if sample_weight is None:
            sample_weight = np.ones(X.shape[0])

        self.covmeans_ = [mean_covariance(
            X[y == a], metric=self.metric_mean,
            sample_weight=sample_weight[y == a]) for a in self.classes_]

        return self

    def _predict_distances(self, covtest):
        """Helper to predict the distance. equivalent to transform."""
        Nc = len(self.covmeans_)
        dist = [distance(covtest, self.covmeans_[m], self.metric_dist)
                for m in range(Nc)]
        dist = np.concatenate(dist, axis=1)
        return dist

    def predict(self, covtest):
        """Get the predictions.

        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels, n_channels)
            ndarray of SPD matrices.

        Returns
        -------
        pred : ndarray of int, shape (n_trials, 1)
            the prediction for each trials according to the closest centroid.
        """
        dist = self._predict_distances(covtest)
        return self.classes_[dist.argmin(axis=1)]

    def transform(self, X):
        """Get the distance to each centroid.

        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels, n_channels)
            ndarray of SPD matrices.

        Returns
        -------
        dist : ndarray, shape (n_trials, n_classes)
            the distance to each centroid according to the metric.
        """
        return self._predict_distances(X)

    def fit_predict(self, X, y):
        """Fit and predict in one function."""
        self.fit(X, y)
        return self.predict(X)

    def predict_proba(self, X):
        """Predict proba using softmax.

        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels, n_channels)
            ndarray of SPD matrices.
        Returns
        -------
        prob : ndarray, shape (n_trials, n_classes)
            the softmax probabilities for each class.
        """
        return softmax(-self._predict_distances(X))


###############################################################################
# POTATO ALGORITHM
###############################################################################

class Potato(BaseEstimator, TransformerMixin, ClassifierMixin):
    """Artefact detection with the Riemannian Potato.

    The Riemannian Potato [1] is a clustering method used to detect artifact in
    EEG signals. The algorithm iteratively estimate the centroid of clean
    signal by rejecting every trial that have a distance greater than several
    standard deviation from it.

    Parameters
    ----------
    metric : string (default 'riemann')
        The type of metric used for centroid and distance estimation.
    threshold : int (default 3)
        The number of standard deviation to reject artifacts.
    n_iter_max : int (default 100)
        The maximum number of iteration to reach convergence.
    pos_label: int (default 1)
        The positive label corresponding to clean data
    neg_label: int (default 0)
        The negative label corresponding to artifact data

    References
    ----------
    [1] A. Barachant, A. Andreev and M. Congedo, "The Riemannian Potato: an
    automatic and adaptive artifact detection method for online experiments
    using Riemannian geometry", in Proceedings of TOBI Workshop IV, p. 19-20,
    2013.
    """

    def __init__(self, metric='riemann', threshold=3, n_iter_max=100,
                 pos_label=1, neg_label=0):
        """Init."""
        self.metric = metric
        self.threshold = threshold
        self.n_iter_max = n_iter_max
        if pos_label == neg_label:
            raise(ValueError("Positive and Negative labels must be different"))
        self.pos_label = pos_label
        self.neg_label = neg_label

    def fit(self, X, y=None):
        """Fit the potato from covariance matrices.

        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels, n_channels)
            ndarray of SPD matrices.
        y : ndarray | None (default None)
            Not used, here for compatibility with sklearn API.

        Returns
        -------
        self : Potato instance
            The Potato instance.
        """
        self._mdm = MDM(metric=self.metric)

        if y is not None:
            if len(y) != len(X):
                raise ValueError('y must be the same lenght of X')

            classes = np.int32(np.unique(y))

            if len(classes) > 2:
                raise ValueError('number of classes must be maximum 2')

            if self.pos_label not in classes:
                raise ValueError('y must contain a positive class')

            y_old = np.int32(np.array(y) == self.pos_label)
        else:
            y_old = np.ones(len(X))
        # start loop
        for n_iter in range(self.n_iter_max):
            ix = (y_old == 1)
            self._mdm.fit(X[ix], y_old[ix])
            y = np.zeros(len(X))
            d = np.squeeze(np.log(self._mdm.transform(X[ix])))
            self._mean = np.mean(d)
            self._std = np.std(d)
            y[ix] = self._get_z_score(d) < self.threshold

            if np.array_equal(y, y_old):
                break
            else:
                y_old = y
        return self

    def transform(self, X):
        """Return the normalized log-distance to the centroid (z-score).
        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels, n_channels)
            ndarray of SPD matrices.
        Returns
        -------
        z : ndarray, shape (n_epochs, 1)
            the normalized log-distance to the centroid.
        """
        d = np.squeeze(np.log(self._mdm.transform(X)))
        z = self._get_z_score(d)
        return z

    def predict(self, X):
        """Predict artefact from data.
        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels, n_channels)
            ndarray of SPD matrices.
        Returns
        -------
        pred : ndarray of bool, shape (n_epochs, 1)
            the artefact detection. True if the trial is clean, and False if
            the trial contain an artefact.
        """
        z = self.transform(X)
        pred = z < self.threshold
        out = np.zeros_like(z) + self.neg_label
        out[pred] = self.pos_label
        return out

    def _get_z_score(self, d):
        """Get z score from distance."""
        z = (d - self._mean) / self._std
        return z
