import requests
import math
import pandas as pd

#get the walk time between 2 buildings
def getWalkTime(building1, building2):

    building1coords = getBuildingCoords(building1)
    building2coords = getBuildingCoords(building2)

    api_key = "KR_zu2-V5a95QdwF4WTRXpZingouudhSV1F92OzB64s"
    walkTime = (get_walking_distance(api_key, building1coords, building2coords))
    return walkTime

#retrieve coordinates of buildings from csv file
def getBuildingCoords(building):

    coordsdf=pd.read_csv('building_coords.csv')
    coords = coordsdf.loc[coordsdf['building'] == building, 'coordinates (lat,long)'].values
    return coords

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
