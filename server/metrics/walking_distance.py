import requests
import math
import pandas as pd
from dotenv import load_dotenv
import os

HERE_API_KEY = os.getenv("HERE_API_KEY")

#get the walk time between 2 buildings
def getWalkTime(building1, building2):
    building1coords = get_building_coords(building1)
    building2coords = get_building_coords(building2)
    #print(building1coords, " ",building2coords)
    walkTime = (get_walking_distance(HERE_API_KEY, building1coords, building2coords))
    return walkTime

#retrieve coordinates of buildings from csv file
def get_building_coords(building):
    coordsdf = pd.read_csv("./utils/building_coords.csv")
    #print(coordsdf['building'].tolist())
    #print(f"Looking for: '{building}'")
    row = coordsdf.loc[coordsdf['building'] == building]
    if row.empty:
        return None  # or raise an error
    lat = row.iloc[0]['lat']
    long = row.iloc[0]['long']
    return f"{lat},{long}"  # HERE API expects "lat,long" as a string

#using HERE Routing API, calculate walking distance between 2 coordinates
def get_walking_distance(api_key, origin, destination):
    # HERE Routing API endpoint
    url = "https://router.hereapi.com/v8/routes"
    
    # Prepare the parameters for the API request
    params = {
        'transportMode': 'pedestrian',
        'origin': origin,
        'destination': destination,
        'return': 'summary',
        'apikey': api_key
    }
    
    # Make the request to the HERE Routing API
    response = requests.get(url, params=params)
    #print("API response:", response.status_code, response.text)  # Debug
    
    # Check for a successful response
    if response.status_code == 200:
        data = response.json()
        
        # Extract walking distance from the response
        try:
            walking_distance = math.ceil((data['routes'][0]['sections'][0]['summary']['length'] / 1000)*12.6)  # Convert to kilometers
            return walking_distance
        except (IndexError, KeyError):
            return 0
    else:
        return 0
