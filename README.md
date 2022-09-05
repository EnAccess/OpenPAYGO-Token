# OpenPAYGO Token v2

This project is supported by the EnAccess Foundation (https://enaccess.org/)

Hardware implementation with generic C version + Arduino + schematics: https://github.com/EnAccess/OpenPAYGO-HW


## GETTING STARTED

1. Have a look at the general documentation: https://github.com/EnAccess/OpenPAYGO/blob/master/documentation/general_documentation.pdf

2. The source code of the example implementation into a device (including an example for begginers implemented on Arduino): https://github.com/EnAccess/OpenPAYGO-HW

3. The guide for the example, including a quick test to see if you have implemented the code properly into your system: https://github.com/EnAccess/OpenPAYGO/blob/master/documentation/example_implementation_documentation.pdf


## NOTE 
If you have pulled or downloaded this implementation before the official OpenPAYGO Token release on the 10th of October 2019, 
please make sure to update to the latest version before using in production. 


## CHANGELOG

2022-09-05: v2.2.0 release
- Packaged into a PIP package (thanks to the work of @wan5xp)
- Folder structure cleanup
- Tests improvements

2021-06-24: v2.1.5 release
- Added padding of tokens with 0 directly to the generator
- Modified tests to work with recommended settings for unordered token entry

2021-05-04: v2.1.4 release
- Added tool to automatically generate spreadsheets with tokens for the test procedure
- Clarify ambiguity about the re-enabling of PAYG
- Ensured the example implementations used the recommended values
- Added full test procedure for the device simulator
- Clarified UI to differentiate between invalid and already used

2020-10-23: v2.1.1 release
- Added tool to generate CSV files with device data; the data can then be used for factory setup and software setup
- Added a tool to flash device data onto devices in factory (from the CSV file); it is compatible with the Arduino examples of the hardware repository

2019-11-15: v2.1.0 release
- Added documentation about how to allow entry of slightly older tokens on device (unordered token entry)
- Added an example of unordered token entry (with test scenario) on the Python implementation
- Ensured compatibility of the Python code with Python v2.7+ (in addition to Python 3+ already supported).

**Note:** This version is fully retro-compatible with the v2.0, the tokens themselves do not change. Changes can be implemented on devices that wish to support unordered token entry but are not required. No change is required on servers. 

2019-10-10: v2.0.0 release
- Improved the test suite
- Added an extra example in the implementation documentation
- Bugfix in the example server implementation leading to count not always being updated correctly
- Bugfix in the update of count in the python device simulator

2019-09-27:
- Added signed independent security audit
- Added documentation as PDF

2019-09-06: v2.0 rc1
- Added extended token example implementation

2019-08-28: v2.0 beta
- Fully functional version with all v2.0 features

2019-07-19: v2.0 alpha
- First functional pre-release version

**Note:** The v1.0 version was only provided to a few partners for a limited beta test and to gather feedback useful to make the v2.0, it is not published here, is not compatible with the v2.0 and should not be used in production. 
