import numpy as np
import pandas as pd
import os
import time
import glob

startTime = time.time()

# updated and corrected
def angle(x_bar, y_bar, y, x, r):
    if(y>=y_bar):#quadrants I and II
        theta = np.arccos((x-x_bar)/r)
    elif(x>=x_bar):#quadrant IV
        theta = np.arcsin((y-y_bar)/r) + np.pi*2
    else:#quadrant III
        theta = 2*np.pi - np.arccos((x-x_bar)/r)
    return theta*180.0/np.pi

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
    return sign_changes

def tiebreaker(dataset):
    derivative = []
    second_derivative = []
    for i in range(len(dataset)-1):
        dx = dataset[i+1]-dataset[i]
        derivative.append(dx)
    for i in range(len(derivative)-1):
        d2x = derivative[i+1]-derivative[i]
        second_derivative.append(d2x)
    return sign_change(second_derivative)

# Does this make the result folder if not present? (no)
bit = "beans"
data_directory = "C:\\Users\\graci\\OneDrive\\Documents\\Lab\\Polar AC\\"+bit
result_directory = "C:\\Users\\graci\\OneDrive\\Documents\\Lab\\Polar AC\\"+bit+"\\results"
csv_files = glob.glob(os.path.join(data_directory, "*.csv"))


#Iterative processing of numbered images, starting with 1.csv
for j in csv_files:
    os.chdir(data_directory)
    fileName = j.split("\\")[-1]
    points = pd.read_csv(j)
    points.columns=['x','y']
    points['r']=0
    points["theta"]=0

    #adding points converted to polar

    x_bar=np.mean(points['x'])
    y_bar=np.mean(points['y'])
    for i in range(len(points)):
        points.iloc[i,2]= np.sqrt((points.iloc[i,0]-x_bar)**2+(points.iloc[i,1]-y_bar)**2)
        points.iloc[i,3] = angle(x_bar,y_bar, points.iloc[i,1],points.iloc[i,0],points.iloc[i,2])

    # First, points are sorted by theta from 0-360 degrees
    points.sort_values(by=["theta"],inplace=True,ascending=True)
    # Then they are re-sorted such that the first point is the one with the largest radial coordiante
    points_theta = list(points['theta'])
    points_r = list(points['r'])
    max_r_index = points_r.index(max(points_r))
    points_r = points_r[max_r_index:len(points_r)]+points_r[0:max_r_index] # slices and recombines 
    points_theta = points_theta[max_r_index:len(points_r)]+points_theta[0:max_r_index]
    points['r'] = points_r
    
    #angular remapping, sets the angular zero to be the max radial coordinate 
    new_theta = []
    for i in points_theta:
        if i>=points_theta[0]:
            new_theta.append(i-points_theta[0])
        else:
            new_theta.append(i+360-points_theta[0])
    
    points['theta'] = new_theta
    
    #Initialize results vector
    result = pd.DataFrame(columns=['theta','r_cor','num_features'])
    result['theta']=points['theta']
    result['r_cor']=autocorrelate(points['r'])
    result_vector = list(result['r_cor']) # Sack up and use Pandas for the whole thing 
    
    # Dimensional Reduction
    result.iloc[0,2] = int(sign_change(result_vector)/2)

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
    result.to_csv("!"+fileName[0:-4]+"_PolarAC.csv",index=False)
    print(fileName+" processed,", int(sign_change(result_vector)/2), "features")

finishTime = time.time()

print("The program took ",np.floor(finishTime-startTime)," seconds")