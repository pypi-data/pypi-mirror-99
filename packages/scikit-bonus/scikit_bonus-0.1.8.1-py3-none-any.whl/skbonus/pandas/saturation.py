"""Saturation classes."""

from abc import ABC, abstractmethod

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted, check_array


class Saturation(BaseEstimator, TransformerMixin, ABC):
    """
    Base class for all saturations, such as Box-Cox, Adbudg, ...
    """

    def fit(self, X: np.array, y: None = None) -> "Saturation":
        """
        Fit the transformer.

        In this special case, nothing is done.

        Parameters
        ----------
        X : Ignored
            Not used, present here for API consistency by convention.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        Saturation
            Fitted transformer.
        """
        X = check_array(X)
        self.n_features_in_ = X.shape[1]

        return self

    def transform(self, X: np.array) -> np.array:
        """
        Apply the saturation effect.

        Parameters
        ----------
        X : np.array
            Data to be transformed.

        Returns
        -------
        np.array
            Data with saturation effect applied.
        """
        check_is_fitted(self)

        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"The dimension during fit time was {self.n_features_in_} and now it is {X.shape[1]}. They should be the same, however."
            )

        return self._transformation(X)

    @abstractmethod
    def _transformation(self, X: np.array) -> np.array:
        """The transformation formula."""


class BoxCoxSaturation(Saturation):
    """
    Apply the Box-Cox saturation.

    The formula is ((x + shift) ** exponent-1) / exponent if exponent!=0, else ln(x+shift).

    Parameters
    ----------
    exponent: float, default=1.0
        The exponent.

    shift : float, default=1.0
        The shift.

    Examples
    --------
    >>> import pandas as pd
    >>> X = pd.DataFrame([[1, 1000], [2, 1000], [3, 1000]], columns=["A", "B"])
    >>> BoxCoxSaturation(exponent=0.5).fit_transform(X)
              A          B
    0  0.828427  61.277168
    1  1.464102  61.277168
    2  2.000000  61.277168
    """

    def __init__(self, exponent: float = 1.0, shift: float = 1.0) -> None:
        """Initialize."""
        self.exponent = exponent
        self.shift = shift

    def _transformation(self, X: np.array) -> np.array:
        """The transformation formula."""
        if self.exponent != 0:
            return ((X + self.shift) ** self.exponent - 1) / self.exponent
        else:
            return np.log(X + self.shift)


class AdbudgSaturation(Saturation):
    """
    Apply the Adbudg saturation.

    The formula is x ** exponent / (denominator_shift + x ** exponent).

    Parameters
    ----------
    exponent : float, default=1.0
        The exponent.

    denominator_shift : float, default=1.0
        The shift in the denominator.

    Notes
    -----
    This version produces saturated values in the interval [0, 1]. You can use `LinearShift` from the shift module to
    bring it between some interval [a, b].

    Examples
    --------
    >>> import pandas as pd
    >>> X = pd.DataFrame([[1, 1000], [2, 1000], [3, 1000]], columns=["A", "B"])
    >>> AdbudgSaturation().fit_transform(X)
              A         B
    0  0.500000  0.999001
    1  0.666667  0.999001
    2  0.750000  0.999001
    """

    def __init__(self, exponent: float = 1.0, denominator_shift: float = 1.0) -> None:
        """Initialize."""
        self.exponent = exponent
        self.denominator_shift = denominator_shift

    def _transformation(self, X: np.array) -> np.array:
        """The transformation formula."""
        return X ** self.exponent / (self.denominator_shift + X ** self.exponent)


class HillSaturation(Saturation):
    """
    Apply the Hill saturation.

    The formula is 1 / (1 + (half_saturation / x) ** exponent).

    Parameters
    ----------
    exponent : float, default=1.0
        The exponent.

    half_saturation : float, default=1.0
        The point of half saturation, i.e. Hill(half_saturation) = 0.5.

    Examples
    --------
    >>> import pandas as pd
    >>> X = pd.DataFrame([[1, 1000], [2, 1000], [3, 1000]], columns=["A", "B"])
    >>> HillSaturation().fit_transform(X)
              A         B
    0  0.500000  0.999001
    1  0.666667  0.999001
    2  0.750000  0.999001
    """

    def __init__(self, exponent: float = 1.0, half_saturation: float = 1.0) -> None:
        """Initialize."""
        self.half_saturation = half_saturation
        self.exponent = exponent

    def _transformation(self, X: np.array) -> np.array:
        """The transformation formula."""
        return 1 / (1 + (self.half_saturation / X) ** self.exponent)


class ExponentialSaturation(Saturation):
    """
    Apply exponential saturation.

    The formula is 1 - exp(-exponent * x).

    Parameters
    ----------
    exponent : float, default=1.0
        The exponent.

    Notes
    -----
    This version produces saturated values in the interval [0, 1]. You can use `LinearShift` from the shift module to
    bring it between some interval [a, b].

    Examples
    --------
    >>> import pandas as pd
    >>> X = pd.DataFrame([[1, 1000], [2, 1000], [3, 1000]], columns=["A", "B"])
    >>> ExponentialSaturation().fit_transform(X)
              A    B
    0  0.632121  1.0
    1  0.864665  1.0
    2  0.950213  1.0
    """

    def __init__(self, exponent: float = 1.0) -> None:
        """Initialize."""
        self.exponent = exponent

    def _transformation(self, X: np.array) -> np.array:
        """The transformation formula."""
        return 1 - np.exp(-self.exponent * X)
