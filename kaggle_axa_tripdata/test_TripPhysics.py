'''
#--Title:  test_TripPhysics.py
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
from TripPhysics import *

#+++++++++++++++++++++++++++++++++++++++++++++
  
class trip_physics_test(unittest.TestCase):

    def setUp(self):
        '''Can load pickled data, or database connection here.'''
        print 'In setUp():'
        pass

    def tearDown(self):
        '''Later, close db connections, etc. here.'''
        print 'In tearDown():'
        pass

    def test_distance_two_points(self):
        '''Test:  can we compute a 3-4-5 triangle hypotenuse correctly?'''
        trip_physics = Trip_Physics()
        try:
            attempted_calculation = trip_physics.distance_two_points(0.0,0.0,3.0,4.0)
            self.assertEqual(attempted_calculation,5.0)
        finally:
            pass


    def test_angular_velocity_two_points(self):
        '''Test:  can we compute arctan(3/4) correctly?'''
        trip_physics = Trip_Physics()
        try:
            attempted_calculation = trip_physics.angular_velocity_two_points(0.0,0.0,4.0,3.0)
            self.assertEqual(attempted_calculation,math.atan(3.0/4.0))
        finally:
            pass

    def test_crows_flight_distance(self):
        '''Test:  compute crow's flight distance for this trip.'''
        trip_physics = Trip_Physics()
        
        trip_data_frame = pandas.DataFrame( {'_id':[1,2,3,4,5,6,7,8,9,10],
            'trip_id':[1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3],
            'x':[557.9,560.1,565.1,569.2,573.7,578.3,582.8,588.5,593.3,599.0],
            'y':[-41.3,-45.2,-48.3,-49.9,-50.7,-51.2,-51.6,-52.1,-52.2,-52.5] })

        try:
            attempted_calculation = trip_physics.crows_flight_distance(trip_data_frame)
            self.assertEqual(attempted_calculation, 42.598709)
        finally:
            pass   

    def test_total_angular_motion(self):
        '''Test:  compute ang. velocity between all the 2-point distances in this trip'''
        trip_physics = Trip_Physics()
        
        trip_data_frame = pandas.DataFrame( {'_id':[1,2,3,4,5,6,7,8,9,10],
            'trip_id':[1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3],
            'x':[557.9,560.1,565.1,569.2,573.7,578.3,582.8,588.5,593.3,599.0],
            'y':[-41.3,-45.2,-48.3,-49.9,-50.7,-51.2,-51.6,-52.1,-52.2,-52.5] })

        try:
            attempted_calculation = trip_physics.total_angular_motion(trip_data_frame)
            precomputed_answer = {'abs_sum_angles': 2.518029,
                'mean_angular_motion': 0.279781,
                'median_angular_motion': 0.108271,
                'net_sum_angles': -2.518029}
            self.assertAlmostEqual(attempted_calculation, precomputed_answer,places=6)
        finally:
            pass   

    def test_total_distance_metrics(self):
        '''Test:  compute sum, mean & median of all the 2-point distances in this trip'''
        trip_physics = Trip_Physics()
        
        trip_data_frame = pandas.DataFrame( {'_id':[1,2,3,4,5,6,7,8,9,10],
            'trip_id':[1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3],
            'x':[557.9,560.1,565.1,569.2,573.7,578.3,582.8,588.5,593.3,599.0],
            'y':[-41.3,-45.2,-48.3,-49.9,-50.7,-51.2,-51.6,-52.1,-52.2,-52.5] })

        try:
            attempted_calculation = trip_physics.total_distance_metrics(trip_data_frame)
            precomputed_answer = {'total_distance': 44.708099,
                'mean_distance': 4.967567,
                'median_distance': 4.627094}
            self.assertAlmostEqual(attempted_calculation, precomputed_answer,places=6)
        finally:
            pass   



if __name__ == '__main__':
    unittest.main()
