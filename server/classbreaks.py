import pandas as pd
import numpy as np

def class_breaks(schedule): #arg: schedule.csv file
    
    breaksDf = pd.read_csv(schedule)

    #set break lengths as index
    breaksDf = breaksDf.set_index('time_between') 
    breaksDf.index.name = 'break_length'

    #create 2nd columns for class identifiers as the start and end points of the break
    breaksDf['class_id2']=breaksDf['class_id'][1:].tolist()+[np.nan]
    breaksDf['location2']=breaksDf['location'][1:].tolist()+[np.nan]
    breaksDf['class_name2']=breaksDf['class_name'][1:].tolist()+[np.nan]

    #drop unnecessary columns/values
    breaksDf.drop(columns=['duration','credits','professor'], inplace=True)
    breaksDf = breaksDf.loc[breaksDf.index != '00:00:00']

