# A1TV_EPG
EPG to XMLTV via A1 TV Mobile API

Works with python 2.7 and 3 (Tested on Bionic Beaver and MacOS Mojave)

v.01 Very early version. Only for testing

Usage:

python a1tv_epg.py (-o FILE | -d)

Possible command Line options:
"-d" Imports directly into tvheadend via socket.

"-f" FILE Outputs a XML File. Specify path + filename

Using no command line options will default in writing "xmltv.xml" to the directory relative to the script.
