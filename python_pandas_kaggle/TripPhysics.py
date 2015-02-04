'''
#--Title:  TripPhysics.py
#--Author:  Geoff Ryder
#--Version: 0.1
#--Date:  1/31/15
#--Input:  Kaggle contest trip data files of x and y vehicle coordinates
#--You can download the data from:  http://www.kaggle.com/c/axa-driver-telematics-analysis
#
#--Output:  Metrics of how similar one trip is to another, across all trips
#--Requirements:  imported modules shown below; preloaded local MongoDB database
#--Notes:

'''
import numpy as np 
import unittest
import pytest  #--try this paradigm if easier
import pandas
import math

class Trip_Physics:
    '''
    Input:  arrays of the following
    + trip ids
    + x coordinates for each trip 
    + y coordinates for each trip 
    OUtput:  
    + turn fingerprints: turn ids, avg radial vel., max radial velocity
    + trip fingerprints:  # sharp turns, trip distance, max/med/avg speed
    Then go cluster the trips based on these outputs  
    '''
    def __init__(self):
        pass
    
    def distance_two_points(self,x1,y1,x2,y2):
        '''Compute Euclidean distance between two points.
           The data set has no time stamps, so assume there is a 
           fixed sampling time between (x,y) pairs.  Thus the
           speed is defined by (distance / constant_value), with
           constant_value the same everywhere, so it can be factored out.
           So use this value for both distance and speed.'''
        delta_x = float(x2 - x1)
        delta_y = float(y2 - y1)
        Euclidean_distance = math.hypot( delta_x, delta_y )
        return Euclidean_distance

    def angular_velocity_two_points(self,x1,y1,x2,y2):
        '''Compute angular velocity between two points in the data set.
           Value is returned as dtheta/dt, in radians per time.
           The data set has no time stamps, so assume there is a 
           fixed sampling time dt between (x,y) pairs.
           NOTE:  this introduces roundoff error to prevent divide by zero.'''
        delta_x = float(x2 - x1)
        delta_y = float(y2 - y1)
        if math.fabs(delta_x) < 0.000001:
            safe_delta_x = math.copysign(0.000001,delta_x)
        else:
            safe_delta_x = delta_x
        theta = math.atan(delta_y / safe_delta_x)    

        if ((y2==y1) and (x2==x1)):
            return 0.0
        else:
            return theta

    def crows_flight_distance(self,trip_data_frame):
        '''Straight distance as a crow flies between start and end points.
        It assumes a pandas data frame as input, that includes
        at least an "x" column and a "y" column of numeric values.'''
        try:
          df = trip_data_frame
          #x1 = float(df['x'][:1])
          temp = list(df['x'][:])
          x1 = temp[0]
          y1 = float(df['y'][:1])
          x2 = float(df['x'][-1:])
          y2 = float(df['y'][-1:])
          crows_flight_dist = round(self.distance_two_points(x1,y1,x2,y2),6)
          return crows_flight_dist
        finally:
          pass

    def total_angular_motion(self,trip_data_frame):
        '''Sum up the angular motion, for the entire trip.
        It assumes a pandas data frame as input, that includes
        at least an "x" column and a "y" column of numeric values.'''
        df = trip_data_frame
        quartets = zip(df['x'][:-1],df['y'][:-1],df['x'][1:],df['y'][1:])
        angular_motion_list = [self.angular_velocity_two_points(x1,y1,x2,y2) for x1,y1,x2,y2 in quartets]
        return {'abs_sum_angles': round(np.sum(np.abs(angular_motion_list)),6), 
                'net_sum_angles': round(np.sum(angular_motion_list),6), 
                'mean_angular_motion': round(np.mean(np.abs(angular_motion_list)),6),
                'median_angular_motion': round(np.median(np.abs(angular_motion_list)),6)}

    def total_distance_metrics(self,trip_data_frame):
        '''Sum up the distance for the entire trip.
        It assumes a pandas data frame as input, that includes
        at least an "x" column and a "y" column of numeric values.'''
        df = trip_data_frame
        x_diff = np.diff(df['x'])
        y_diff = np.diff(df['y'])
        distance_list = [math.hypot(x,y) for x,y in zip(x_diff,y_diff)]
        return {'total_distance': round(np.sum(distance_list),6), 
                'mean_distance': round(np.mean(distance_list),6),
                'median_distance': round(np.median(distance_list),6)}


