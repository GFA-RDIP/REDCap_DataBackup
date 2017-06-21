#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-----------------------     REDCap_DataBackup()    --------------------------

This script is used to extract the data from an instrument from a REDCap 
project using the API.

The main reason is that real data may be entered into a project being
developed and there is a potential that data could be lost as the project
is worked on my various people or move to production.

This routine extracts that data being entered as effortlessly as possible 
to ensure that the work is not lost. The idea is to reimport into the 
production version once the project is moved over.

Programmed by Simon Christopher Cropper 26/5/2017
(c) Murdoch Childrens Research Institute

"""

#***********************************************************************
#***********************     GPLv3 License      ************************
#***********************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************

# import modules required to have python do what is required
import os                   # access to general operating system stuff
import platform             # access to platform details
import argparse
import csv                  # access to CSV library
import urllib.parse
import urllib.request
import time
import pandas as pd

def extract_data_redcap(url, edrlist):

    """
    This function allows you to poll the REDCap API. The examples
    provided on the API Playground don't work in Python 3.
    """

    data = urllib.parse.urlencode(edrlist)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        response_buffer = response.read()

    # REDCap exports data with LF for line ending and CRLF for inrecord 
    # line breaks in note fields. This confuses the sit out of Python. 
    # These lines replaces CRLF with '. ' and collapses the notes fields
    # into a paragraph.
    response_text = response_buffer.decode('UTF-8').replace('\r\n', '. ')
    response_text = response_text.replace('. . ', '. ')   
    response_text = response_text.replace('..', '.')   
    response_text = response_text.replace('  ', ' ')   
    response_buffer = response_text.encode('UTF-8')
    return response_buffer

def main():

    """
    This is the main routine that calls all the relevant modules in sequence.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("redcap_server", help="Enter the URL for the REDCap \
                        Server API, e.g. https://redcap.vanderbilt.edu/api")
    parser.add_argument("user_token", help="Enter the USER token provided by \
                        your REDCap Administrator, \
                        e.g. A945062DEAB165F74FC5C5E0BA14A265")
    parser.add_argument("primarykey", help="Enter the primary key for the \
                        person. e.g. RecordID")
    parser.add_argument("instrument", help="Enter name of instrument in \
                        REDCap to backup the data")
    parser.add_argument("output_dir", help="directory where data should be \
                        saved. e.g. C:\Data (don't include backslash). ")
    args = parser.parse_args()

    print("Extracting the data from the '" + args.instrument + "'")

    
    # What platform are we on?
    if platform.system() == 'Windows':
        dirsymbol = '\\'
    else:
        dirsymbol = '/'

    savepath = args.output_dir + dirsymbol
    timestr = time.strftime("%Y%m%d-%H%M%S")
    savefile = args.instrument.upper() + "_DATA_" + timestr + ".csv"

    # When exporting forms it is important to include the 
    # primary key field for the database, otherwise you can't
    # reimport
    data = {
        'token': args.user_token,
        'content': 'record',
        'format': 'csv',
        'type': 'flat',
        'fields': args.primarykey,
        'forms[0]': args.instrument,
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'csv'
    }

    mydata = extract_data_redcap(args.redcap_server, data)

    # Save cleaned buffer to local directory
    with open(savepath + savefile, 'wb') as f:
        f.write(mydata)

    # imports into pandas and removes records with no data
    df = pd.read_csv(savepath + savefile, dtype=str, index_col=0)
    df = df[pd.notnull(df['cceg_accelidrecorded'])]
    df.to_csv(savepath + savefile, index=True)
    
    print("CSV list saved to " + savepath + savefile)
    
if __name__ == "__main__":

    main()

