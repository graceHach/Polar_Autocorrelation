import numpy as np
from scipy import stats



def confidence_interval(data, confidence=0.95):
    """
    :param data: list of datapoints
    :param confidence: confidence level (named variable)
    :return: lower bound, upper bound of CI=confidence
    """
    n = len(data)
    mean, se = np.mean(data), stats.sem(data)
    # Uses the t distribution, which is the normal distribution set to zero
    # Unlike z dist, uses sample standard deviation
    interval = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return mean - interval, mean + interval



def area_between_curves(x1, y1, x2, y2):
    """
    :param x1: dataset1 x values (list or array like)
    :param y1: dataset1 y values (list or array like)
    :param x2: dataset2 x values (list or array like)
    :param y2: dataset2 y values (list or array like)
    :return: approximate area between curves of the
    """
    # Check if the input arrays have the same length
    if len(x1) != len(y1) or len(x2) != len(y2):
        raise ValueError("The lengths of x and y must be the same.")
    else:
        a1 = np.trapz(y1,x1)
        a2 = np.trapz(y2,x2)
    return abs(a1-a2)
