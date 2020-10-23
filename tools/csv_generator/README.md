# OpenPAYGO Token - CSV Generator

## Installation

Nothing special to do, just make sure you have Python version 3.6 or above installed and setup in your path. 

## Usage

1. In a command line window, go to the csv_generator folder and run: **python openpaygo_csv_generator.py**
2. At the first run, you will be prompted to setup some parameters (e.g. manufacturer prefix, hardware model, etc.) 
If you wish to change them later you can directly edit the openpaygo_csv_generator.conf file. 
3. You will be prompted for the last serial number that was generated in order to avoid two devices having the same serial number. 
The latest serial number from the last batch will be shown to you if it was generated on the same computer and the config file was kept. 
For your first batch you can use 0.  
4. You will then be prompted for the number of devices for which you want to generate the CSV for.
5. You will then find the CSV file generated in the same folder with the name "openpaygo_batch_XXX-YYY.csv" 
with XXX being the first serial number in the batch and YYY the last serial number in the batch. 
