# Functions to query the A1 EPG API

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import requests
import time
import stations

rs = requests.session()

# Fake the headers to be from A1 TV Mobile App (iOS in this case)
# Function then queries the url and gets JSON Data

def query_url (get_url):
    add_headers = {'User-Agent': 'A1TV/3.9 (iPhone; iOS 12.1; Scale/3.00)', 'Accept-Language': 'en-AT;q=1, de-AT;q=0.9'}
    query_data = rs.get(get_url, headers=add_headers).json()
    return query_data


# Function to query the A1 EPG API.
# Accepts, Querytype, Station ID, Event ID
# Returns all stations as JSON Data
# Atm not used. Only stations defined in the stations.py settings file are queried
# In this case stations are only A1 TV Plus

def request_stations():

    url = "https://epggw.a1.net/a/api.mobile.start?type=JSON.6"
    data = query_url(url)

    # Check status and raise exception if not 200
    status = data[0][0]
    if status != 200:
        raise ValueError('Station Query did not return status code 200. Status Code: ' + str(status))

    return data[3]



# Function to query the station details for a given period starting with current timeself.
# Returns list of events for the specific station and period as JSON data

def request_station_details(station_id,hours):

    # Define period in relation to current time. 28H ensures 4h overlap when run as service
    datetime_to_load =  str(time.strftime('%Y%m%dT%H%M', time.localtime(time.time())))
    period = datetime_to_load + "/" + str(hours) + "H"


    # Check if multiple of only one station is queried and encode url properly
    api_root = "https://epggw.a1.net/a/api.mobile.event.hour?"

    if isinstance(station_id,list):
        query_params = {'period': period, 'stationuid': ','.join(str(i) for i in station_id), 'type': 'JSON.5'}
    else:
        query_params = {'period': period, 'stationuid': station_id, 'type': 'JSON.5'}


    # Encode Url and query the API
    url = api_root + urllib.parse.urlencode(query_params)
    data = query_url(url)


    # Check status and raise exception if not 200
    status = data[0][0]
    if status != 200:
        raise ValueError('Event List Query did not return status code 200. Status Code: ' + str(status))

    return data[1]



# Function to query to details of a certain event. Referenced by the id of the events
# Returns details of the event as JSON data

def request_event_desc(event_id):

    # Check if multiple of only one station is queried and encode url properly
    api_root = "https://epggw.a1.net/a/api.mobile.event.get?"

    data = []

    query_params = {'evid': event_id, 'type': 'JSON.3'}
    url = api_root + urllib.parse.urlencode(query_params)
    query_response = query_url(url)
    # Check status and raise exception if not 200
    status = query_response['head']['Status']
    if status != 200:
        raise ValueError('Event Detail Query did not return status code 200. Status Code: ' + str(status))

    data = query_response['data'][0]['Event']['Description']


    return data
