from datetime import datetime, timedelta
from csv_ical import Convert
import pandas as pd
from icalendar import Calendar
import re


#Define a function to parse the ICS file
def parse_ics(file_path):
    with open(file_path, 'r') as file:
        calendar = Calendar.from_ical(file.read())

    events = []
    #Get each component in the .ICS file
    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {}
            event['summary'] = component.get('SUMMARY')
            event['location'] = component.get('LOCATION')
            event['dtstart'] = component.get('DTSTART').dt
            event['dtend'] = component.get('DTEND').dt
            event['description'] = component.get('DESCRIPTION')

            # Extract BYDAY rule from RRULE
            rrule = component.get('RRULE')
            event['byday'] = rrule.get('BYDAY') if rrule and 'BYDAY' in rrule else None
            
            # Add the original event to the list
            events.append(event)

            # Check for BYDAY combinations
            if event['byday']:
                byday_str = ','.join(event['byday'])  # Create a string representation of BYDAY

                if byday_str == "MO,WE":
                    # Duplicate for Wednesday and Friday
                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=2)  # Move to Wednesday
                    new_event['dtend'] += timedelta(days=2)
                    events.append(new_event)

                elif byday_str == "TU,TH":
                    # Duplicate for Thursday
                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=2)  # Move to Thursday
                    new_event['dtend'] += timedelta(days=2)
                    events.append(new_event)

                elif byday_str == "MO,WE,FR":
                    # Duplicate for Wednesday and Thursday
                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=2)  # Move to Wednesday
                    new_event['dtend'] += timedelta(days=2)
                    events.append(new_event)

                    new_event = event.copy()
                    new_event['dtstart'] += timedelta(days=4)  # Move to Friday
                    new_event['dtend'] += timedelta(days=4)
                    events.append(new_event)

    return events

#Function to parse the CSV File
def make_csv(SAVE_LOCATION, CSV_FILE_LOCATION):
    events = parse_ics(SAVE_LOCATION)
    # Create DataFrame from events
    data = {
        'dstart': [event['dtstart'] for event in events],
        'dend': [event['dtend'] for event in events],
        'class_id': [event['summary'] for event in events],
        'location': [event['location'] for event in events],
        'class_name': [event['description'] for event in events],
    }


    df = pd.DataFrame(data)

    df['credits'] = None  # First empty column
    df['professor'] = None  # Second empty column

    # Save DataFrame to CSV
    #df.to_csv(CSV_FILE_LOCATION, index=False)

    #Converting dstart & dend column to datetime in order to split the date and time
    df['dstart'] = pd.to_datetime(df['dstart']) 
    df['dend'] = pd.to_datetime(df['dend']) # only need time from dend



    #Split DSTART column into date & time
    df['day'] = df["dstart"].dt.date #Adds the date from dstart to a date column
    df['timeStart'] = df["dstart"].dt.time #Adds the time from dstart into a timeStart column
    df['timeEnd'] = df["dend"].dt.time #Adds the time from dend into a timeEnd column

    #Calculate duration by subtracting dend and dstart
    df['duration'] = df['dend'] - df['dstart']


    #Format the duration into a more readable time
    df['duration'] = df['duration'].apply(lambda x: f"{int(x.total_seconds() // 3600):02}:{int((x.total_seconds() % 3600) // 60):02}:{int(x.total_seconds() % 60):02}")


    #Converts date column to a datetime column so we can switch from dates into day
    df['day'] = pd.to_datetime(df['day']) 
    df = df.sort_values(by=['day','timeStart']) #Sort the dates before turning into days=
    df['day'] = df['day'].dt.day_name() #Turn dates into day names

    # Initialize a list to hold the times between classes
    time_between_classes = []

    # Loop to calculate the time between classes
    for i in range(len(df) - 1):
        # Get the endTime of the first class and startTime of the next class
        curr_endTime = df['dend'].iloc[i]
        curr_startTime = df['dstart'].iloc[i + 1]

        # Calculate the time difference
        time_difference = curr_startTime - curr_endTime

        # Append the appropriate value to the time_between_classes list
        if time_difference >= pd.Timedelta(hours=12):
            time_between_classes.append(pd.Timedelta(0))  # Append 0 if the gap is 12 hours or more
        else:
            time_between_classes.append(time_difference)  # Append the actual time difference if less than 12 hours

    # Append a placeholder for the last class
    time_between_classes.append(pd.Timedelta(0))  # or any other logic you want to use for the last entry

    # Make sure the list length matches the DataFrame length before assigning
    if len(time_between_classes) == len(df):
        df['time_between'] = time_between_classes
    else:
        print("Warning: Length mismatch. Length of time_between_classes:", len(time_between_classes), "Length of df:", len(df))

    #Add the list to the time_between column
    df['time_between'] = time_between_classes

    # Format the time for time_between classes
    df['time_between'] = df['time_between'].apply(lambda x: f"{int(x.total_seconds() // 3600):02}:{int((x.total_seconds() % 3600) // 60):02}:{int(x.total_seconds() % 60):02}")

    new_csv_file_location = r'C:\Users\James Toscano\Desktop\School\final_schedule.csv'

    # Save the DataFrame to a new CSV file
    df.drop(columns=['dstart','dend','timeStart','timeEnd']).to_csv(new_csv_file_location, index=False)

    print(df.drop(columns=['dstart', 'dend', 'timeStart', 'timeEnd',]).to_string(index=False)) #Print the dataframe without dstart and dend



