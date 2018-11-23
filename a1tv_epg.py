# Global imports
import sys

#A1TV_EPG imports
from stations import *
from api.functions import generate_xmltv, send_to_tvheadend

data = generate_xmltv(station_list,25)


#save to xml file
#with open('xmltv.xml', 'w') as xmlfile:
#    xmlfile.write(str(data))

# use socket to load directly into tvheadend
send_to_tvheadend(str(data))
