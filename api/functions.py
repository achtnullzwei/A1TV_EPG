# General functions

# Global imports
import time, json, socket, os
from xml.etree import ElementTree as ET

# A1TV_EPG imports
from .api import *


# Functions start

# Queries API and loads EPG data in JSON format
def load_epg(stations, hours=26):

    # Requesting station details from api for processing
    query = request_station_details(stations['ids'], hours)

    # Initiating collection to store programs and channels
    tv = {}
    programme = []
    channel = []

    # Use data queried from api to generate data for the collection. Used to ease compilation of XML data
    if query:
        for station in query:
            channel.append({'id': station[1],'display-name': station[1],
                            'icon': 'http://epggw.a1.net/img/station-globalid/darkbg/500x300/'
                            + str(station[0]) + '.png'})

            for event in station[2]:
                if not station[2][0]:
                    break
                elif event[4] == None:
                    sub_title = '--'
                else:
                    sub_title = event[4]

                start_time = time.strftime('%Y%m%d%H%M%S %z', time.localtime(event[1]))
                end_time = time.strftime('%Y%m%d%H%M%S %z', time.localtime(event[2]))

                programme.append({'channel': station[1], 'episode-num': event[0],
                                  'title': event[3], 'sub-title': sub_title,
                                  'category': event[5], 'date': event[7],
                                  'start': start_time, 'stop': end_time})

    tv = {'channel': channel, 'programme': programme}

    return tv


# Generates XML tv format from EPG data loaded
def generate_xmltv(stations, hours):

    # Load EPG data
    tv_data = load_epg(stations, hours)

    # Initiae XML structure
    tv = ET.Element('tv', {'source-info-url': 'https://epggw.a1.net', 'source-info-name': 'A1 TV EPG'})

    # Add XML elements for channels
    for tv_channel in tv_data['channel']:
        xml_channel = ET.SubElement(tv, 'channel', {'id': tv_channel['id']} )
        ET.SubElement(xml_channel, 'display-name', {'lang': 'en'}).text = tv_channel['display-name']
        ET.SubElement(xml_channel, 'icon', {'src': tv_channel['icon']})

    # Add XML elements for programs
    for tv_programme in tv_data['programme']:
        xml_programme = ET.SubElement(tv, 'programme', {'start': tv_programme['start'], 'stop': tv_programme['stop'], 'channel': tv_programme['channel']})
        ET.SubElement(xml_programme, 'title', {'lang': 'en'}).text = tv_programme['title']
        ET.SubElement(xml_programme, 'sub-title', {'lang': 'en'}).text = tv_programme['sub-title']
        ET.SubElement(xml_programme, 'date').text = tv_programme['date']

        for tv_category in tv_programme['category']:
            ET.SubElement(xml_programme, 'category', {'lang': 'en'}).text = tv_category

    return ET.tostring(tv, encoding='utf8', method='xml').decode('utf8')

# Sends XMLTV data directly to the UNIX socket presented by TVHeadend
def send_to_tvheadend(message):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    socket_address = '/home/hts/.hts/tvheadend/epggrab/xmltv.sock'
    sock.connect(socket_address)
    sock.sendall(message.encode('utf-8'))
    sock.close()

# Saves XMLTV as file. Overwrites existing file!
def save_to_file(data, filename='xmltv.xml'):
    with open(filename, 'wb') as file:
        file.write(data.encode('utf-8'))

# Writes new version of the station list as JSON data
def write_stations(type='plus'):
    data = request_stations(type)
    with open('stations.json', 'w') as file:
        json.dump(data,file)

# Loads the station list stored as JSON data
def load_stations():
    with open('stations.json') as file:
        data = json.load(file)
    return data

# Checks the station list file. If not found it is created. Default is always A1TV Plus.
# Also updates the station list of it is older than 7 days.
def check_stations_file():

    # Check if station file exists, if not, load & create
    if os.path.isfile('./stations.json') == False:
        write_stations()

    # Check time difference. If more than 7 days, reload station filename
    stations = load_stations()
    last_update = stations['last_update']
    time_diff = time.mktime(time.localtime(time.time())) - last_update
    if time_diff > 604800:
        write_stations(stations['type'])
