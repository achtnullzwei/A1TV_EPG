## A1TV_EPG

### Description
This tool queries the API provided by A1 for their TV Program App and it's written in Python. It uses their API to query for channel information and program information. It then either generates an XMLTV formatted XML file, or sends the information directly to TVHeadend via UNIX socket (separate settings in TVHeadend required). A channel list is retrieved upon first start from the XSPF playlists provided by A1. It defaults to A1TV Plus (includes HD channels). It can be switched to basic also, to avoid loading unnecessary data. The station list is updated every 7 days automatically (can be updated manually). The default hours of EPG data to be loaded is set to 26. The maximum time period is set to 48 hours to avoid stressing the API too much. Also the channel details are filled with the naming etc. directly from A1. This is helpful when using their M3U for TVHeadend since it automatically matches the EPG to the channels. Furthermore it also automatically adds channel icon URLs to the XMLTV file (500x300px).

Currently it does not support loading a description for a selected program. The API does not provide the possibility to query for a bulk of programs in order to retrieve the description details. Working around this limitation would result in the script running for a very long time (approx. 3-5h when querying the API with a maximum of 10-20 calls per minute).

**Use this tool at you own risk and and to net stress the API too much. We are thankful that A1 provides it and we should not risk getting banned, or force them to restrict this somehow**

### Requirements
The tool itself is written to be compatible with Python 2.7 & Python 3.7. It has been tested and works with, at least, the following setups:
- Raspbian Stretch (Python 2.7)
- Ubuntu Bionic Beaver (Python 2.7)
- MacOS Mojave (Python 2.7 & Python 3.7, both with miniconda envs)

Apart from the standard python installation that comes with the distributions the only requirement is the module "Requests".

It can be installed either via:
```
sudo apt-get install python-requests
```

or:
```
pip install requests
```

### Installation
Installation is pretty straight forward.

Install git if not installed:
```
sudo apt-get install git
```

Choose or create a directory of your choice to save and run the script (Example).
```
mkdir /opt
cd /opt
```

Git clone the repository to this directory.
```
git clone https://github.com/achtnullzwei/A1TV_EPG.git
```

Change to the directory to run the script
```
cd /opt/A1TV_EPG
```

### Usage
The script accepts some command line arguments. The full list can be retrieved starting the tool with *-h* or *--help*

Output of this command:
```
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
```

#### Eaxmple for using UNIX socket import on TVHeadend:
```
python /opt/A1TV_EPG/a1tv_epg.py -d
```
This command loads 26 hours of EPG data for A1TV Plus channels and sends them directly to TVHeadend.

In order to use this feature activate the following in TVHeadend:
1. Login to TVHeadend as admin.
2. Go to Configuration --> Channel / EPG --> EPG-Grabber-Modules
3. Click on "External: XMLTV"
4. Activate the checkbox "Enabled" and click "Save"
This will activate the UNIX socket for XMLTV import.

#### Example for saving to a file:
```
python /opt/A1TV_EPG/a1tv_epg.py -o /home/hts/xmltv.xml
```
This will save the XMLTV file to the location */home/hts/xmltv.xml*

#### Default behaviour:
Starting the script simply without any commandline arguments will result in an xmltv.file saved next to the script. It contains 26h of EPG data for A1TV Plus channels.
```
python /opt/A1TV_EPG/a1tv_epg.py
```

#### Updating channel list or change to another type of channel list (basic, plus):
##### Updating the channel list:
```
python /opt/A1TV_EPG/a1tv_epg.py -u
```
This will not result in an updated XMLTV file. The channel list is automatically updated every 7 days **before** loading the EPG.

##### Changing the channel list:
```
python /opt/A1TV_EPG/a1tv_epg.py -c basic
```
Changes the channel list to A1TV basic and reloads updates XMLTV data via socket or replaces the file specified.

#### Automation of the script
Simplest solution to run it every night:
```
sudo crontab -e
```
Add the following line for sending directly to the UNIX socket every night (just change the command line arguments to your needs):
```
5 */12 * * * /usr/bin/python /opt/A1TV_EPG/a1tv_epg.py -d
```
*Don't forget to run the script initially so it retrieves the first hours of EPG data.*

Another option would be to use timers with systemctl. How to set this up can easily be found via Google.
