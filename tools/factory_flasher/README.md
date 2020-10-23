# OpenPAYGO Token - Factory Flashing Tool

## Installation

1. Make sure you have Python version 2.7 or above installed and setup in your path. 
2. Run **pip install -r requirements.txt**
3. Make sure you have a Serial interface with the correct drivers installed on your system (e.g. FTDI USB to UART adapter)

## Usage

1. In a command line window, go to the csv_generator folder and run: **python factory_flashing_tool.py**
2. At the first run, you will be prompted to enter the Serial port you want to use (this depends)
3. You will be prompted for the CSV file you want to use for this batch. Enter the path to the CSV file 
(you can drag and drop the file to the terminal window and press enter on most system)
4. You will then repeatedly be prompted for the serial numbers of the device you want to flash. 
Make sure that the device is connected to the serial interface before continuing. 
You can enter this serial number manually or use an HID barcode scanners if the devices have barcodes with the serial number. 
Make sure the barcode scanner is configured to enter a carriage return after reading the barcode to save time. 
5. Wait for the device to be flashed and continue to the next one or press Ctrl+C to quit.
