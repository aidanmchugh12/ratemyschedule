from datetime import datetime, timedelta
import pandas as pd
from icalendar import Calendar
import re


# define a function to parse through the .ICS file
def parse_ics(file_path):
    with open(file_path, 'r') as file:
        calendar = Calendar.from_ical(file.read()) # opens the .ICS and starts reading it

    events = []
    # get each component in the .ICS file
    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {}
            event['summary'] = component.get('SUMMARY')
            event['location'] = component.get('LOCATION')
            event['dtstart'] = component.get('DTSTART').dt
            event['dtend'] = component.get('DTEND').dt
            event['description'] = component.get('DESCRIPTION')

            # extract BYDAY rule from RRULE in order to get duplicate classes
            rrule = component.get('RRULE')
            event['byday'] = rrule.get('BYDAY') if rrule and 'BYDAY' in rrule else None
            
            # add the original event to the list
            events.append(event)

            # check for BYDAY combinations
            if event['byday']:
                byday_str = ','.join(event['byday'])  # Create a string representation of BYDAY

                if byday_str == "MO,WE":
                    # duplicate for wednesday
                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=2)  # move to wednesday
                    new_event['dtend'] += timedelta(days=2)
                    events.append(new_event)

                elif byday_str == "TU,TH":
                    # duplicate for thursday
                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=2)  # move to thursday
                    new_event['dtend'] += timedelta(days=2)
                    events.append(new_event)

                elif byday_str == "MO,WE,FR":
                    # duplicate for wednesday and friday
                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=2)  # move to wednesday
                    new_event['dtend'] += timedelta(days=2)
                    events.append(new_event)

                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=4)  # move to friday
                    new_event['dtend'] += timedelta(days=4)
                    events.append(new_event)

    return events

# function to parse the .CSV file

def make_csv(SAVE_LOCATION, output_csv_path='schedule.csv'):
    events = parse_ics(SAVE_LOCATION)

    # create dataframe from events
    data = {
        'dstart': [event['dtstart'] for event in events],
        'dend': [event['dtend'] for event in events],
        'class_id': [event['summary'] for event in events],
        'location': [event['location'] for event in events],
        'class_name': [event['description'] for event in events],
    }

    df = pd.DataFrame(data)

    df['credits'] = None  # first empty column
    df['professor'] = None  # second empty column

    # converting dstart & dend column to datetime in order to split the date and time
    df['dstart'] = pd.to_datetime(df['dstart']) 
    df['dend'] = pd.to_datetime(df['dend']) # only need time from dend



    # split dstart column into date & time
    df['day'] = df["dstart"].dt.date # add the date from dstart to a date column
    df['timeStart'] = df["dstart"].dt.time # add the time from dstart into a timeStart column
    df['timeEnd'] = df["dend"].dt.time # add the time from dend into a timeEnd column

    # calculate duration by subtracting dend and dstart
    df['duration'] = df['dend'] - df['dstart']


    # format the duration into a more readable time
    df['duration'] = df['duration'].apply(lambda x: f"{int(x.total_seconds() // 3600):02}:{int((x.total_seconds() % 3600) // 60):02}:{int(x.total_seconds() % 60):02}")


    # converts date column to a datetime column so we can switch from dates into day
    df['day'] = pd.to_datetime(df['day']) 
    df = df.sort_values(by=['day','timeStart']) # sort the dates before turning into days
    df['day'] = df['day'].dt.day_name() # turn dates into day names

    # initialize a list to hold the times between classes
    time_between_classes = []

    # loop to calculate the time between classes
    for i in range(len(df) - 1):

        # get the endTime of the first class and startTime of the next class
        curr_endTime = df['dend'].iloc[i]
        curr_startTime = df['dstart'].iloc[i + 1]

        # calculate the time difference
        time_difference = curr_startTime - curr_endTime

        # appen the appropriate value to the time_between_classes list
        if time_difference >= pd.Timedelta(hours=12):
            time_between_classes.append(pd.Timedelta(0))  # append 0 if the gap is 12 hours or more (means that the class is for the next day)
        else:
            time_between_classes.append(time_difference)  # append the actual time difference if less than 12 hours

    # append a placeholder for the last class
    time_between_classes.append(pd.Timedelta(0))

    # make sure the list length matches the dataframe length before assigning
    if len(time_between_classes) == len(df):
        df['time_between'] = time_between_classes
    else:
        print("Warning: Length mismatch. Length of time_between_classes:", len(time_between_classes), "Length of df:", len(df))

    # add the list to the time_between column
    df['time_between'] = time_between_classes

    # format the time for time_between classes
    df['time_between'] = df['time_between'].apply(lambda x: f"{int(x.total_seconds() // 3600):02}:{int((x.total_seconds() % 3600) // 60):02}:{int(x.total_seconds() % 60):02}")

    # save the DataFrame to a new .CSV file
    df.drop(columns=['dstart','dend','timeStart','timeEnd']).to_csv(output_csv_path, index=False)


