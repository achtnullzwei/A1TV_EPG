# General functions

# Global imports
import time
from xml.etree import ElementTree as ET
from io import BytesIO
import socket

# A1TV_EPG imports
from api.api import *

# Functions start

def load_epg_light(station_list, hours=26):
    query = request_station_details(station_list, hours)
#    query = request_station_details(station_list)

    programme = []
    channel = []

    if query:
        for stations in query:
            channel.append({'id': stations[1],'display-name': stations[1],
                            'icon': 'http://epggw.a1.net/img/station-globalid/darkbg/300x160/'
                            + str(stations[0]) + '.png'})

            for events in stations[2]:

                if events[4] == None:
                    sub_title = '--'
                else:
                    sub_title = events[4]

                start_time = time.strftime('%Y%m%d%H%M%S %z', time.localtime(events[1]))
                end_time = time.strftime('%Y%m%d%H%M%S %z', time.localtime(events[2]))

                programme.append({'channel': stations[1], 'episode-num': events[0],
                                  'title': events[3], 'sub-title': sub_title,
                                  'category': events[5], 'date': events[7],
                                  'start': start_time, 'stop': end_time})

    tv = {'channel': channel, 'programme': programme}

    return tv



def generate_xmltv(station_list, hours):

    tv_data = load_epg_light(station_list, hours)

    tv = ET.Element('tv', {'source-info-url': 'https://epggw.a1.net', 'source-info-name': 'A1 TV EPG'})

    for tv_channel in tv_data['channel']:
        xml_channel = ET.SubElement(tv, 'channel', {'id': tv_channel['id']} )
        ET.SubElement(xml_channel, 'display-name', {'lang': 'en'}).text = tv_channel['display-name']
        ET.SubElement(xml_channel, 'icon', {'src': tv_channel['icon']})

    for tv_programme in tv_data['programme']:
        xml_programme = ET.SubElement(tv, 'programme', {'start': tv_programme['start'], 'stop': tv_programme['stop'], 'channel': tv_programme['channel']})
        ET.SubElement(xml_programme, 'title', {'lang': 'en'}).text = tv_programme['title']
        ET.SubElement(xml_programme, 'sub-title', {'lang': 'en'}).text = tv_programme['sub-title']
        #ET.SubElement(xml_programme, 'date').text = tv_programme['date']

        for tv_category in tv_programme['category']:
            ET.SubElement(xml_programme, 'category', {'lang': 'en'}).text = tv_category

    return ET.tostring(tv, encoding='utf8', method='xml').decode()



def send_to_tvheadend(message):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    socket_address = '/home/hts/.hts/tvheadend/epggrab/xmltv.sock'
    sock.connect()
    sock.sendall(message)
    sock.close()
