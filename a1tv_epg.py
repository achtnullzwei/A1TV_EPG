# Global imports
import argparse

#A1TV_EPG imports
from api import *

if __name__ == "__main__":

    # Use arguments/options from command line

    parser = argparse.ArgumentParser(description='Load EPG data from A1 TV official api and convert to XMLTV. Tool is able to load directly into TVHeadend via Socket or output as XML file.')
    parser_group = parser.add_mutually_exclusive_group()
    parser_group.add_argument('-o', metavar='Filename', type=argparse.FileType('wt'), help="Specify valid path and filename. Example: /some/path/filename.xml", dest="o")
    parser_group.add_argument('-s', metavar='Filename', type=argparse.FileType('wt'), help="Send directly to TVheadend via defined Socket path. Example: /some/path/socketname.sock", dest="s")
    parser_group.add_argument('-d', action="store_true", help="Send directly to TVheadend via Socket. Must be set up first in TVheadend first!", dest="d")
    parser.add_argument('-t', metavar='Time in hours', type=int, help="Enter how many hours of epg to load. USE WITH CAUTION! Excessive use may leads to API ban!!! Default: 26, Max: 48", nargs='?', choices=range(1, 49), const=26, default=26, dest="t")
    parser.add_argument('-u', action="store_true", help="Update the channel list JSON file. Calling with -u will not load XMLTV data!", dest="u")
    parser.add_argument('-c', metavar='basic, plus', action="store", help="Change channels to A1TV basic or A1TV plus. Default is A1TV plus. Loads new EPG data. Change is stored in JSON file and persistent.", dest="c")



    # Main application. Selection between Arguments/Options parsed from Command Line
    try:
        arguments = parser.parse_args()

        #Check Channel List JSON FileType. Update if older than 7 days.
        check_stations_file()



        # Swtich station list type
        if arguments.c:
            if arguments.c == 'basic':
                write_stations(arguments.c)
            elif arguments.c == 'plus':
                write_stations(arguments.c)
            else:
                raise ValueError('Wrong entry for Playlist type!')

        # Load stations and generate XMLTV Data or update station list
        stations = load_stations()
        data = generate_xmltv(stations,arguments.t)
        if arguments.u:
            stations = write_stations()
        elif arguments.d == True:
            send_to_tvheadend(data)
        elif arguments.o != None:
            save_to_file(data, arguments.o.name)
        elif arguments.s != None:
            send_to_tvheadend(data, arguments.s.name)
        else:
            save_to_file(data, 'xmltv.xml')

    except IOError as msg:
        parser.error(str(msg))
