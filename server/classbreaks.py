import pandas as pd
import numpy as np

from rmp_grading import getProfGrade

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
    
def sum_credits(csvFile):
    # read the csv file 
    df = pd.read_csv(csvFile)
    
    # get the sum and skip the Nan values
    total_credits = df['credits'].sum(skipna = True)
    
    print(total_credits)
    # match case to determine credit rating
    match total_credits:
        case _ if total_credits > 18:
            return 1
        case _ if total_credits == 18:
            return 2
        case _ if total_credits == 17:
            return 3
        case _ if total_credits == 16:
            return 4
        case _ if total_credits <= 15:
            return 5
        
def prof_rating():
    # read the dataframe but only get the professors column
    df = pd.read_csv('schedule.csv', usecols=['professor'])
    
    # make a new column for averaged professor rating
    df['average_rating'] = None
    
    # loop through the professors and assign their average rating in the column
    for index, professor in enumerate(df['professor']):
        df.at[index, 'average_rating'] = getProfGrade(professor)
        
    return df

