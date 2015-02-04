'''
#--Title:  extract_trip_features.py
#--Author:  Geoff Ryder
#--Version: 0.1
#--Date:  1/31/15
#--Input:  Kaggle contest trip data files of x and y vehicle coordinates
#--You can download the data from:  http://www.kaggle.com/c/axa-driver-telematics-analysis
#
#--Output:  Metrics of how similar one trip is to another, across all trips
#--Requirements:  imported modules shown below; preloaded local MongoDB database
#--Notes:
Take special care with pandas data frame specifications--slicing, etc.
http://pandas.pydata.org/
Similar to others (native python, numpy, Matlab, R), but some differences
'''
import os, os.path #--for database setup
import sys
import pickle
import numpy as np 
import sklearn
import pandas  #--use pandas data frames for statistical analysis
import TripPhysics as TP


#--Import data saved as a python pickle file, and load it into a pandas data frame (df) for processing
df_in = pandas.DataFrame(pickle.load(open("tripsamples.p","rb")))

#--Discovery:  pickle turned all the values to type string when we saved the data.
#--Need to convert them back to numbers.  
x_arr = np.array(df_in["x"]).astype(float)
y_arr = np.array(df_in["y"]).astype(float)
id_arr = np.array(df_in["trip_id"]).astype(float)

#--Here's a list of hundreds of unique trips, each with 500 - 1000 data points (rows)
trip_id_list = list(set(df_in['trip_id']))

#--It would be great to stick with pandas data frames as much as possible.
#--Turning this from numpy arrays back to a d.f.
df = pandas.DataFrame({"trip_id": id_arr, "x" : x_arr, "y" : y_arr })

trip_phy = TP.Trip_Physics() #--new Trip_Physics object to process data

analysis_array = np.array(range(9))*0.0 #--create an empty dictionary (to be a data frame) for analysis



#########################
#--Loop over each "trip" in the data set, and compute features of interest
for trip_id in trip_id_list:

	#--Extract the records for this trip
	df_this_trip = df[ df['trip_id'] == trip_id]

	print "trip_id ", trip_id

	#--Call the TripPhysics.py library to calculate feature values
	try:
		crows_flight = trip_phy.crows_flight_distance(df_this_trip)
		am_dict = trip_phy.total_angular_motion(df_this_trip)
		dist_dict = trip_phy.total_distance_metrics(df_this_trip)

	except ValueError:
		print "Check for pandas value error, python dict key error."

	#--Store the featues in data structure "analysis_array"	
	new_row_array = np.array([trip_id, crows_flight, am_dict['abs_sum_angles'],
					am_dict['net_sum_angles'], am_dict['mean_angular_motion'],
					am_dict['median_angular_motion'], dist_dict['total_distance'],
					dist_dict['mean_distance'], dist_dict['median_distance']])

	analysis_array = np.vstack((analysis_array, new_row_array))

#########################

#--TODO:  recover column names automatically from the function calls
#--These column names are hard coded for now--ADDRESS THIS when extending TripPhysics
col_names = ['trip_id', 'crows_flight_distance','abs_sum_angles','net_sum_angles',
					'mean_angular_motion','median_angular_motion','total_distance',
					'mean_distance','median_distance']
aa_df = pandas.DataFrame(analysis_array)
aa_df.columns = col_names

print aa_df

#--save as a csv file for ML analysis later
aa_df.to_csv("analysis_mtx.csv")

#--try plotting data
import matplotlib.pyplot as plt 
from pylab import *
figure()
title(r'Distance as a Crow Flies, vs. Total Distance Traveled')
xval = list(aa_df["crows_flight_distance"])
yval = list(aa_df["total_distance"])
plt.plot(xval,yval,'o')
plt.plot(xval,xval,'-',label='Line is Crows Flight Dist.')
plt.show()





