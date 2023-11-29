# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 14:30:11 2023

@author: graci
"""

import numpy as np
import pandas as pd
import os
import time
import glob

startTime = time.time()

# updated and corrected
def arc_length(out_pd1):
    """
    Modifies arc length dataframe in place to
    """
    distance = 0
    for i in range(len(out_pd1)-1):
        distance += ((out_pd1['x'][i]-out_pd1['x'][i+1])**2+(out_pd1['y'][i]-out_pd1['y'][i+1])**2)**0.5
    distance_progress = 0
    for i in range(len(out_pd1)-1):
        distance_progress += ((out_pd1['x'][i]-out_pd1['x'][i+1])**2+(out_pd1['y'][i]-out_pd1['y'][i+1])**2)**0.5
        #out_pd1['arc_length'][i+1] = distance_progress/distance*360
        out_pd1.iloc[i, 3] = distance_progress/distance*360
        #print(distance_progress/distance*360)
    #out_pd1['arc_length'][len(out_pd1)-1] = 360
    #print(distance,distance_progress)
    return

def autocorrelate(vector):
    denominator = 0
    numerator = 0
    result = [0]*len(vector)
    for i in range(len(vector)):
       denominator += (vector.iloc[i]-np.mean(vector))**2
    for k in range(len(vector)):
        for i in range(len(vector)-k):
            numerator += (vector.iloc[i]-np.mean(vector))*(vector.iloc[i+k]-np.mean(vector))
        result[k]=numerator/denominator
        numerator=0
    return result

def sign_change(list_):
    sign_changes = 0
    for i in range(len(list_)-1):
        if list_[i]*list_[i+1]<=0:
            sign_changes=sign_changes+1
    return sign_changes//2

def tiebreaker(dataset):
    derivative = []
    second_derivative = []
    for i in range(len(dataset)-1):
        dx = dataset[i+1]-dataset[i]
        derivative.append(dx)
    for i in range(len(derivative)-1):
        d2x = derivative[i+1]-derivative[i]
        second_derivative.append(d2x)
    return sign_change(second_derivative)//2

def return_two_closest(point_,points_list):
    x, y = point_[0], point_[1]
    # gets smallest distance between point and minimum distance point
    min_dist = min([((x-s[0])**2+(y-s[1])**2)**0.5 for s in points_list])
    # first 
    min_index = points_list.index([s for s in points_list if ((x-s[0])**2+(y-s[1])**2)**0.5==min_dist][0])
    point1 = points_list[min_index]
    # removes the point from both the local and global variable points list
    points_list.remove(point1)
    min_dist = min([((x-s[0])**2+(y-s[1])**2)**0.5 for s in points_list])
    # gets index of point with the minimum distance 
    min_index = points_list.index([s for s in points_list if ((x-s[0])**2+(y-s[1])**2)**0.5==min_dist][0])
    point2 = points_list[min_index]
    points_list.remove(point2)
    return point1, point2

def return_closest(point_,points_list):
    x, y = point_[0], point_[1]
    # gets smallest distance between point and minimum distance point
    min_dist = min([((x-s[0])**2+(y-s[1])**2)**0.5 for s in points_list])
    # first 
    min_index = points_list.index([s for s in points_list if ((x-s[0])**2+(y-s[1])**2)**0.5==min_dist][0])
    point1 = points_list[min_index]
    points_list.remove(point1)
    return point1

def sort_CCW(points_pd):
    ''''
    '''
    points_pd.columns = ['x','y']
    points = list(zip(list(points_pd['x']),list(points_pd['y'])))
    sorta = []
    max_y = max(list(points_pd['y']))
    points = list(zip(list(points_pd['x']),list(points_pd['y'])))
    # select point with maximum y coordinate 
    sorta.append([x for x in points if x[1]==max_y][0]) # add point with maximum y coordinate, as tuple, to sorta
    points.remove(sorta[0]) # remove max y point from points list
    p1,p2 = return_two_closest(sorta[0],points)
    if p1[0]<p2[0]:   # if p1 is the leftmost point
        sorta.append(p1) # add it to sorta
    else:
        sorta.append(p2)
# Iterate through each point 
    while len(points)>0:
        p1 = return_closest(sorta[len(sorta)-1],points)
        sorta.append(p1)
    return sorta


# Does this make the result folder if not present? (no)
bit = "beans"
data_directory = "C:\\Users\\graci\\OneDrive\\Documents\\Lab\\Polar AC\\"+bit
result_directory = "C:\\Users\\graci\\OneDrive\\Documents\\Lab\\Polar AC\\"+bit+"\\results_arc"
csv_files = glob.glob(os.path.join(data_directory, "*.csv"))


# Iterative processing of numbered images, starting with 1.csv
for j in csv_files:
    os.chdir(data_directory)
    fileName = j.split("\\")[-1]
    points_pd = pd.read_csv(j)
    points_pd.columns = ['x', 'y']
    points_pd = pd.DataFrame(sort_CCW(points_pd))
    points_pd.columns = ['x', 'y']
    points_pd['r'] = 0
    points_pd['arc_length'] = 0

    # adding points converted to polar

    x_bar=np.mean(points_pd['x'])
    y_bar=np.mean(points_pd['y'])
    for i in range(len(points_pd)):
        points_pd.iloc[i,2]= np.sqrt((points_pd.iloc[i,0]-x_bar)**2+(points_pd.iloc[i,1]-y_bar)**2)
    # Adding arc length
    arc_length(points_pd) # points_pd is now in terms of arc length 
        

    # First, points are sorted by theta from 0-360 degrees
    # points.sort_values(by=["theta"],inplace=True,ascending=True)
    # Then they are re-sorted such that the first point is the one with the largest radial coordiante
    points_arc = list(points_pd['arc_length'])
    points_r = list(points_pd['r'])
    max_r_index = points_r.index(max(points_r))
    points_r = points_r[max_r_index:len(points_r)]+points_r[0:max_r_index] # slices and recombines 
    points_arc = points_arc[max_r_index:len(points_r)]+points_arc[0:max_r_index]
    points_pd['r'] = points_r
    points_pd['arc_length']= points_arc
    
    #angular remapping, sets the zero of arc length to be the max radial coordinate 
    new_arc = []
    for i in points_arc:
        if i>=points_arc[0]:
            new_arc.append(i-points_pd['arc_length'][0])
        else:
            new_arc.append(i+360-points_pd['arc_length'][0])
    
    points_pd['arc_length'] = new_arc
    #points_arc = new_arc
    #When do I last use/need the points DF?
    
    # Make list of points 
    
    # new_theta, points_x, points_y and points_r are lists of points
    
    
    
    
    
    #OLD
    result = pd.DataFrame(columns=['arc_length','r_cor','num_features','num_features_2nd'])
    result['arc_length']=points_pd['arc_length']
    result['r_cor']=autocorrelate(points_pd['r'])
    result_vector = list(result['r_cor']) # Sack up and use Pandas for the whole thing 
    
    # Dimensional Reduction
    result.iloc[0,2] = sign_change(result_vector)
    result.iloc[0,3] = tiebreaker(result_vector)
    # Dimensional Reduction by way of scipy maxima detection
    '''
    numpy_result = result['r_cor'].to_numpy()
    
    print(fileName,"maxima: ",len(argrelextrema(numpy_result, np.greater)[0]),"minima: ",len(argrelextrema(numpy_result, np.less)[0]))
    indecies_of_maxima = argrelextrema(numpy_result, np.greater)[0]
    indecies_of_minima = argrelextrema(numpy_result, np.less)[0]
    num_maxima = len(indecies_of_maxima)
    if num_maxima == 2: # This part of the control flow deals with the tiebreaker case of two features
       num_maxima_2 = tiebreaker(numpy_result) # num maxima 2 is feature number returned by second derivative test
       if not (num_maxima_2 == 2 or num_maxima_2 == 3):
           result.iloc[0,2] = "inconclusive"
       else:
           result.iloc[0,2] = num_maxima_2
    else:
        result.iloc[0,2] = num_maxima
    '''
    # Change current directory
    os.chdir(result_directory)
    result.to_csv("!"+fileName[0:-4]+"_PolarAC.csv", index=False)
    #print(fileName+" processed,", "features")
    print(fileName+" processed,", sign_change(result_vector), "features",tiebreaker(result_vector))

finishTime = time.time()

print("The program took ", np.floor(finishTime-startTime), " seconds")
