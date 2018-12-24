# Functions to query the A1 EPG API

#General imports
import requests, time, json
from xml.etree import ElementTree as ET

#Fix for Python2/3 Urllib issues
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

# Start requests session
rs = requests.session()



# Fake the headers to be from A1 TV Mobile App (iOS in this case)
# Function then queries the url and gets JSON Data

def query_url (get_url, type='epg'):
    add_headers = {'User-Agent': 'A1TV/3.9 (iPhone; iOS 12.1; Scale/3.00)', 'Accept-Language': 'en-AT;q=1, de-AT;q=0.9'}

    if type == 'epg':
        query_data = rs.get(get_url, headers=add_headers).json()
    elif type == 'stations':
        query_data = rs.get(get_url, headers=add_headers)
        query_data = query_data.content
    else:
        raise ValueError('Wrong query type provided: ' + str(type))

    return query_data



# Function to query the station details for a given period starting with current time.
# Returns list of events for the specific station(s) and period as JSON data

def request_station_details(station_id,hours):

    # Define period in relation to current time. 28H ensures 4h overlap when run as service
    datetime_to_load =  str(time.strftime('%Y%m%dT%H%M', time.localtime(time.time())))
    period = datetime_to_load + "/" + str(hours) + "H"


    # Check if multiple of only one station is queried and encode url properly
    api_root = "https://epggw.a1.net/a/api.mobile.event.hour?"

    if isinstance(station_id,list):
        query_params = {'period': period, 'stationId': ','.join(str(i) for i in station_id), 'type': 'JSON.6'}
    else:
        query_params = {'period': period, 'stationId': station_id, 'type': 'JSON.6'}


    # Encode Url and query the API
    url = api_root + urlencode(query_params)
    data = query_url(url)


    # Check status and raise exception if not 200
    status = data[0][0]
    if status != 200:
        raise ValueError('Station details query did not return status code 200. Status Code: ' + str(status))

    return data[1]



# Get all station IDs and pretty names. Necessary to get the correct channel icons
# There are some issues when using the stationuid. Not all channel icons are correct
# then

def request_station_ids():

    url = "https://epggw.a1.net/a/api.mobile.start?type=JSON.3"

    data = {}

    query_response = query_url(url)

    # Check status and raise exception if not 200
    status = query_response[0][0]
    if status != 200:
        raise ValueError('Station IDs query did not return status code 200. Status Code: ' + str(status))

    for station in query_response[3]:
        data[station[2]] = str(station[0])

    return data



# request stations from XSPF playlist from A1

def request_stations(type='plus'):

    if type == 'basic':
        url = 'https://epggw.a1.net/a/service.fta.xspf'
    elif type == 'plus':
        url = 'https://epggw.a1.net/a/service.plus.xspf'
    else:
        raise ValueError('Wrong type for Playlist provided')

    query_response = query_url(url,'stations')

    # Initiate station settings JSON file
    stations = {}
    stations['type'] = type
    stations['data'] = []
    stations['ids'] = []
    stations['last_update'] = time.mktime(time.localtime(time.time()))

    # Request all stations with IDs
    station_ids = request_station_ids()

    # Request current playlist based on type to generate match station IDs & Names
    xspf = ET.ElementTree(ET.fromstring(query_response))
    root = xspf.getroot()

    # Compose station list (name + ID) based on playlist & type
    for title in root[1].findall('{http://xspf.org/ns/0/}track'):
        station_name = title.find('{http://xspf.org/ns/0/}title').text
        stations['data'].append({'id': station_ids[station_name], 'name': station_name})
        stations['ids'].append(station_ids[station_name])

    return stations
