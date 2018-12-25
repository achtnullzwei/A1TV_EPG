## A1TV_EPG

### Description
This tool queries the API provided by A1 for their TV Program App and it's written in Python. It uses their API to query for channel information and program information. It then either generates an XMLTV formatted XML file, or sends the information directly to TVHeadend via UNIX socket (separate settings in TVHeadend required). A channel list is retrieved upon first start. It defaults to A1TV Plus (includes HD channels). It can be switched to basic also, to avoid loading unnecessary data. The station list is updated every 7 days automatically (can be updated manually). The default hours of EPG data to be loaded is set to 26. The maximum time period is set to 48 hours to avoid stressing the API too much. Also the channel details are filled with the naming etc. directly from A1. This is helpful when using their M3U for TVHeadend since it automatically matches the EPG to the channels.

Currently it does not support loading a description for a selected program. The API does not provide the possibility to query for a bulk of programs in order to retrieve the description details. Working around this limitation would result in the script running for a very long time (approx. 3-5h when querying the API with a maximum of 10-20 calls per minute).

** Use this tool at you own risk and and to net stress the API too much. We are thankful that A1 provides it and we should not risk getting banned, or force them to restrict this somehow **

### Requirements
The tool itself is written to be compatible with Python 2.7 & Python 3.7. It has been tested and works in at least the following setups:
- Raspbian Stretch (Python 2.7)
- Ubuntu Bionic Beaver (Python 2.7)
- MacOS Mojave (Python 2.7 & Python 3.7, both with miniconda envs)

Apart from the standard python installation that comes with the distributions the only requirement is the module "Requests".

It can be installed either via:
    sudo apt-get install python-requests

or:
    pip install requests

### Installation
Installation is pretty straight forward.

Choose or create a directory of your choice to save and run the script.
    Example:
    mkdir /opt
    cd /opt

Git clone the repository to this directory.
    git clone https://github.com/achtnullzwei/A1TV_EPG.git

Change to the directory to run the script
    cd /opt/A1TV_EPG

### Usage
The script accepts some command line arguments. The full list can be retrieved starting the tool with *-h* or *--help*

Output of this command:
''''
usage: a1tv_epg.py [-h] [-o Filename | -d] [-t [Time in hours]] [-u]
                   [-c basic, plus]

Load EPG data from A1 TV official api and convert to XMLTV. Tool is able to
load directly into TVHeadend via Socket or output as XML file.

optional arguments:
  -h, --help          show this help message and exit
  -o Filename         Specify valid path and filename. Example:
                      /some/path/filename.xml
  -d                  Send directly to TVheadend via Socket. Must be set up
                      first in TVheadend first!
  -t [Time in hours]  Enter how many hours of epg to load. USE WITH CAUTION!
                      Excessive use may leads to API ban!!! Default: 26, Max:
                      48
  -u                  Update the channel list JSON file. Calling with -u will
                      not load XMLTV data!
  -c basic, plus      Change channels to A1TV basic or A1TV plus. Default is
                      A1TV plus. Loads new EPG data. Change is stored in JSON
                      file and persistent.
''''
