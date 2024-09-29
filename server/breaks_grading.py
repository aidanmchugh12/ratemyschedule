import pandas as pd
import numpy as np
from walktime import getWalkTime

def class_breaks(schedule): #arg: schedule.csv file
    
    breaksDf = pd.read_csv(schedule)

    #set break lengths as index
    breaksDf['break_length'] = pd.to_timedelta(breaksDf['time_between']).dt.total_seconds()/60
    breaksDf['break_length'] = breaksDf['break_length'].astype(int)
    breaksDf = breaksDf.set_index('break_length')
    breaksDf.index.name = 'break_length'

    #create 2nd columns for class identifiers as the start and end points of the break
    breaksDf['class_id2']=breaksDf['class_id'].iloc[1:].tolist()+[np.nan]
    breaksDf['location2']=breaksDf['location'].iloc[1:].tolist()+[np.nan]
    breaksDf['class_name2']=breaksDf['class_name'].iloc[1:].tolist()+[np.nan]

    #create new columns cutting off classroom number
    breaksDf['location_clean'] = breaksDf['location'].fillna('').apply(lambda x: ' '.join(x.split(' ')[1:])).tolist()
    breaksDf['location2_clean'] = breaksDf['location2'].fillna('').apply(lambda x: ' '.join(x.split(' ')[1:])).tolist()
    
    #drop unnecessary columns/values
    breaksDf.drop(columns=['duration','credits','professor'], inplace=True)
    breaksDf.drop(index=0, inplace=True)

    breaksDf['walk_time'] = breaksDf.apply(lambda row: getWalkTime(row['location_clean'], row['location2_clean']), axis=1).astype(int)
    breaksDf['break_walk_diff'] = breaksDf.index - breaksDf['walk_time']

    # Define a function for the case switch for scoring the break
    def score(x):
        if x < 2:
            return 1
        elif x < 4:
            return 2
        elif x < 6:
            return 3
        elif x < 10:
            return 4
        else:
            return 5

    breaksDf['break_diff_score'] = breaksDf['break_walk_diff'].apply(score)

    #print(breaksDf)

    breaksDf.to_csv('breaks.csv', index=False)
    return breaksDf['break_diff_score'].mean().astype(int)

#test
#class_breaks('schedule.csv')