# Global imports
import sys

#A1TV_EPG imports
from stations import station_list
from api import *

data = generate_xmltv(station_list,25)


#save to xml file
with open('xmltv.xml', 'w') as xmlfile:
    xmlfile.write(str(data))

# use socket to load directly into tvheadend
# send_to_tvheadend(str(data))
