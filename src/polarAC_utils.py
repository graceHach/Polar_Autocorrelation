import glob
import os
import pandas as pd
import copy
import numpy as np
from scipy import stats

def autocorrelate(vector):
    """
    Simple autocorrelation function, first point is self-comparison, and therefore equal to 1
    Input:
    vector - (int or floats) list-like collection of
    Output:
    """
    denominator = 0
    numerator = 0
    n = len(vector)
    mean = sum(vector)/n
    result = [0]*n
    for i in range(n):
        denominator += (vector[i]-mean)**2
    for k in range(n):
        for i in range(n-k):
            numerator += (vector[i]-mean)*(vector[i+k]-mean)
        result[k] = numerator/denominator
        numerator = 0
    return result


def sort_CCW(points):
    """
    Takes a pointcloud and sorts it in counterclockwise order, starting with a top point
    Input: a list of points where each point is a tuple
    Output: The same list of points, sorted in CCW order
    """
    points_copy = copy.deepcopy(points)
    x_only, y_only = [x for x, y in points], [y for x, y in points]
    sorta = []
    max_y = max(y_only)
    # select point at top of point cloud
    # POTENTIAL ISSUE HERE IF THERE ARE REDUNDANT Y VALUES
    sorta.append([x for x in points if x[1] == max_y][0])  # add point with maximum y coordinate, as tuple, to sorta
    points_copy.remove(sorta[0])  # remove max y point from points list
    p1, p2 = return_two_closest(sorta[0], points_copy)
    if p1[0] < p2[0]:  # if p1 is the leftmost point
        sorta.append(p1)  # add it to sorta
        sorta.append(p2)
    else:
        sorta.append(p2)
        sorta.append(p1)
    points_copy.remove(p1)
    points_copy.remove(p2)
    # Iterate through each point
    while len(points_copy) > 0:
        p1 = return_closest(sorta[len(sorta) - 1], points_copy)
        sorta.append(p1)
        points_copy.remove(p1)
    return sorta


def return_two_closest(point_, points_list):
    """
    Returns two points closest to point_
    Input:
    point_ - list or tuple-like collection of two floats
    points_list - list of similarly formatted points:
    Output:
    Closest point and second-closest point
    """
    x, y = point_[0], point_[1]
    points_tuples_with_distance = []
    for current_point in points_list:
        distance = ((x - current_point[0]) ** 2 + (y - current_point[1]) ** 2) ** 0.5
        points_tuples_with_distance.append((current_point[0], current_point[1], distance))

    # sorts points in ascending order of distance
    sorted_tuple_list = sorted(points_tuples_with_distance, key=lambda x: x[2])
    point1 = (sorted_tuple_list[0][0], sorted_tuple_list[0][1])
    point2 = (sorted_tuple_list[1][0], sorted_tuple_list[1][1])
    return point1, point2


def return_closest(point_, points_list):
    """
    Returns point closest to point_
    Input:
    point_ - list or tuple-like collection of two floats
    points_list - list of similarly formatted points:
    Output:
    Closest point
    """
    x, y = point_[0], point_[1]
    points_tuples_with_distance = []
    for current_point in points_list:
        distance = ((x - current_point[0]) ** 2 + (y - current_point[1]) ** 2) ** 0.5
        points_tuples_with_distance.append((current_point[0], current_point[1], distance))
    min_dist = min([z for x, y, z in points_tuples_with_distance])
    closest_point = [(x, y) for x, y, z in points_tuples_with_distance if z == min_dist]
    closest_point_tuple = closest_point[0]
    return closest_point_tuple


def count_sign_changes(dataset):
    """
    Counts the number of times a 1D list of numbers changes sign
    Input: dataset, list of numbers
    Output: # of sign changes of dataset
    """
    sign_changes = 0
    for i in range(len(dataset)-1):
        if dataset[i]*dataset[i+1] <= 0:
            sign_changes = sign_changes+1
    return sign_changes

def third_derivative_test(dataset):
    """
    Number of times dataset changes concavity (second derivative changes sign)
    Input: dataset, list of numbers
    Output: number of sign changes of second derivative
    """
    derivative = []
    second_derivative = []
    third_derivative = []
    for i in range(len(dataset)-1):
        dx = dataset[i+1]-dataset[i]
        derivative.append(dx)
    for i in range(len(derivative)-1):
        d2x = derivative[i+1]-derivative[i]
        second_derivative.append(d2x)
    for i in range(len(second_derivative)-1):
        d3x = derivative[i+1]-derivative[i]
        third_derivative.append(d2x)
    return count_sign_changes(third_derivative)


def second_derivative_test(dataset):
    """
    Number of times dataset changes concavity (second derivative changes sign)
    Input: dataset, list of numbers
    Output: number of sign changes of second derivative
    """
    derivative = []
    second_derivative = []
    for i in range(len(dataset)-1):
        dx = dataset[i+1]-dataset[i]
        derivative.append(dx)
    for i in range(len(derivative)-1):
        d2x = derivative[i+1]-derivative[i]
        second_derivative.append(d2x)
    return count_sign_changes(second_derivative)

def first_derivative_test(dataset):
    """
    Number of times dataset changes concavity (first derivative changes sign)
    Input: dataset, list of numbers
    Output: number of sign changes of first derivative
    """
    derivative = []
    second_derivative = []
    for i in range(len(dataset)-1):
        dx = dataset[i+1]-dataset[i]
        derivative.append(dx)
    return count_sign_changes(derivative)


def add_radial_distance(points_df):
    """
    Returns a copy of points dataframe with radial distance column added
    """
    points_df_copy = points_df
    points_df_copy['r'] = 0
    x_bar = sum(points_df['x'])/len(points_df['x'])
    y_bar = sum(points_df['y'])/len(points_df['y'])
    for i in range(len(points_df)):
        points_df_copy.loc[i, 'r'] = ((points_df.loc[i, 'x'] - x_bar) ** 2 + (points_df.loc[i, 'y'] - y_bar) ** 2)**0.5
    return points_df_copy


def add_arc_length_parameterization(points_df):
    """
    Returns a copy of points_df with arc length column added
    """
    points_df_copy = points_df
    points_df_copy['arc_length'] = 0
    distance = 0
    for i in range(len(points_df)-1):
        distance += ((points_df.loc[i, 'x'] - points_df.loc[i+1, 'x'])**2 + (points_df.loc[i, 'y'] - points_df.loc[i+1, 'y'])**2)**0.5
    cumulative_distance = 0
    for i in range(len(points_df)-1):
        cumulative_distance += ((points_df.loc[i, 'x'] - points_df.loc[i+1, 'x'])**2 + (points_df.loc[i, 'y']-points_df.loc[i+1, 'y'])**2)**0.5
        points_df_copy.loc[i, 'arc_length'] = cumulative_distance/distance*360
    return points_df_copy

def arc_length_remapping(points_df):
    """
    Takes the arc length column of points_df and returns a copy with it
    remapped such that the angular zero is the maximum radial coordiante
    """
    points_df_copy = points_df
    points_r = list(points_df['r'])
    points_arc = list(points_df['arc_length'])
    max_r_index = points_r.index(max(points_r))
    # slices and recombines radial and arc length coordinates
    points_r = points_r[max_r_index:len(points_r)] + points_r[0:max_r_index]
    points_arc = points_arc[max_r_index:len(points_r)] + points_arc[0:max_r_index]

    # re-zeros the arc length coordinate such that first point (maximum r) is 0 degrees
    new_arc = []
    for i in points_arc:
        if i >= points_arc[0]:
            new_arc.append(i - points_arc[0])
        else:
            new_arc.append(i + 360 - points_arc[0])
    points_df_copy['r'] = points_r
    points_df_copy['arc_length'] = new_arc

    return points_df_copy

def get_csvs_from_directory(data_directory):
    """
    Input: the directory in which data, in xy format may be found.
    Output: the list of all csvs within this directory
    """
    csv_files = glob.glob(os.path.join(data_directory, "*.csv"))  # What's the deal with OS module?
    return csv_files

def get_csvs_from_directories(data_directory):
    """
    Input: the directory in which data, in xy format may be found.
    Output: the list of all csvs within this directory
    """
    csv_files = []
    # Use os.path.abspath to ensure we're using absolute path of the data directory
    data_directory = os.path.abspath(data_directory)
    for root, dirs, files in os.walk(data_directory):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files





def read_csv(csv_filename):
    """
    Input: name of a csv file
    Output: datafrane
    """
    # add error handling for permission error
    csv_df = pd.read_csv(csv_filename)
    return csv_df

def create_export_df(include_ac_curve, points_df):
    """
    Input:
    include_AC_curve - bool, if true includes autocorreation as a function of arc length displacement
    points_df
    Output: dataframe with autocorreation/feature detection results
    """
    # Calculate autocorrelation and extract feature number
    autocorrelation_vector = autocorrelate(points_df['r'])
    # Feature extraction is int(# sign changes/2) or int(# sign changes of second derivative/2)
    num_features_sign_change = count_sign_changes(autocorrelation_vector)//2
    if include_ac_curve:
        result_df = pd.DataFrame(columns=['r_autocorrelation', 'arc_length', 'num_features_sign_change'])
        result_df['arc_length'] = points_df['arc_length']
        result_df['r_autocorrelation'] = autocorrelation_vector
    else:
        result_df = pd.DataFrame(columns=['num_features_sign_change'])
    result_df.loc[0, 'num_features_sign_change'] = num_features_sign_change

    return result_df

def create_export_df_derivatives(include_ac_curve, points_df):
    """
    Input:
    include_AC_curve - bool, if true includes autocorreation as a function of arc length displacement
    points_df
    Output: dataframe with autocorreation/feature detection results
    """
    # Calculate autocorrelation and extract feature number
    autocorrelation_vector = autocorrelate(points_df['r'])
    # Feature extraction is int(# sign changes/2) or int(# sign changes of second derivative/2)
    num_features_sign_change = count_sign_changes(autocorrelation_vector)//2
    num_features_2nd_deriv = second_derivative_test(autocorrelation_vector)//2
    num_features_1st_deriv = first_derivative_test(autocorrelation_vector)//2
    if include_ac_curve:
        result_df = pd.DataFrame(columns=['r_autocorreation', 'arc_length', 'num_features_sign_change', 'num_features_1st_deriv', 'num_features_2nd_deriv', ])
        result_df['arc_length'] = points_df['arc_length']
        result_df['r_autocorreation'] = autocorrelation_vector
    else:
        result_df = pd.DataFrame(columns=['num_features_sign_change', 'num_features_1st_derivative', 'num_features_2nd_deriv'])
    result_df.loc[0, 'num_features_sign_change'] = num_features_sign_change
    result_df.loc[0, 'num_features_1st_deriv'] = num_features_1st_deriv
    result_df.loc[0, 'num_features_2nd_deriv'] = num_features_2nd_deriv

    return result_df


def export_df(result_df, data_filename):
    result_df.to_csv(data_filename, index=False)
    return
