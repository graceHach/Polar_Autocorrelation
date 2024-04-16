import numpy as np
from scipy import stats


def get_numerical_tangent_x_intercept(x, y, degrees_to_sample=20):
    """
    fits a numerical tangent line based on a short subset at the start of the dataset. Get the x value where it intersects
    the x axis
    :param x: ALL x data (arc length parameterization
    :param y: all y data (R AC)
    :param degrees_to_sample: end point of interval used to calculate tangent line
    if 5, makes tangent line based on first 5 degrees of x coordiante
    :return:
    """
    x_trunc = []
    for i in x:
        if i <= degrees_to_sample:
            x_trunc.append(i)
        else:
            break
    y_trunc = y[:len(x_trunc)]

    # If there aren't enough datapoints in the first part of the dataset, the fitting operations are undefined
    if len(y_trunc) <= 1:
        return None
    else:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_trunc, y_trunc)
        x_inter = -1*intercept/slope
        return x_inter

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

def absolute_AUC(x,y):
    """
    Gets area under the curve, treating area under x axis as positive
    :param x: x values of dataset
    :param y: y values of dataset
    :return: Total AUC, treating all area as positive
    """
    y_pos = [abs(i) for i in y]
    # Check if the input arrays have the same length
    if len(x) != len(y):
        raise ValueError("The lengths of x and y must be the same.")
    else:
        area = np.trapz(y_pos, x)
        return area

def area_between_curves(x1, y1, x2, y2):
    """
    Gets area between two curves. Order doesn't matter
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
