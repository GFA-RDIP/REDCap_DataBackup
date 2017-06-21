# REDCap DataBackup

## Overview

This script is used to extract the data from an instrument from a REDCap 
project using the API.

The main reason is that real data may be entered into a project being
developed and there is a potential that data could be lost as the project
is worked on my various people or move to production.

This routine extracts that data being entered as effortlessly as possible 
to ensure that the work is not lost. The idea is to reimport into the 
production version once the project is moved over.

## To Run

A batch/bash script needs to be created by the individual user using their user token. The script's one line includes...

    python [path]REDCap_Query.py REDCapServerAPI_URL USER_Token PrimaryKey Instrument Output_Directory

>**[path]** = optional path to directory where routine is present

>**REDCapServerAPI_URL** = URL for the REDCap Server API, e.g. https://redcap.vanderbilt.edu/api

>**USER_Token** = USER token provided by your REDCap Administrator, e.g. A945062DEAB165F74FC5C5E0BA14A265

>**PrimaryKey** = The primary key of the database, e.g. RecordID

>**Instrument** = Name of instrument or form

>**Output_Directory** = Full path to the output directory where the data is stored.

## Output

The output data file name is automatically generated and includes the instrument name followed by a datatime stamp. The actual data is stored in CSV format, encoded in UTF-8 and with Windows (CRLF) line endings. A header row is included so the information can be readily imported back into REDCap once the project moves from development into production. 

## License

This library is released under [GPLv3 Licence](https://github.com/GFA-RDIP/REDCap_DataBackup/blob/master/licenses/GPL_v3.txt "GPLv3 License").