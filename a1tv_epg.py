# Global imports
import argparse

#A1TV_EPG imports
from stations import station_list
from api import *

if __name__ == "__main__":

    # Use arguments/options from command line

    parser = argparse.ArgumentParser(description='Load EPG data from A1 TV official api and convert to XMLTV. Tool is able to load directly into TVHeadend via Socket or output as XML file.')
    parser_group = parser.add_mutually_exclusive_group()
    parser_group.add_argument('-o', metavar='Filename', type=argparse.FileType('wt'), help="Specify valid path and filename. Example: /some/path/filename.xml")
    parser_group.add_argument('-d', action="store_true", help="Send directly to TVheadend via Socket. Must be set up first in TVheadend first!")


    # Main application. Selection between Arguments/Options parsed from Command Line
    try:
        arguments = parser.parse_args()

        data = generate_xmltv(station_list,25)

        if arguments.d == True:
            send_to_tvheadend(data)
        elif arguments.o != None:
            sate_to_file(data, arguments.o.name)
        else:
            sate_to_file(data, 'xmltv.xml')

    except IOError as msg:
        parser.error(str(msg))
