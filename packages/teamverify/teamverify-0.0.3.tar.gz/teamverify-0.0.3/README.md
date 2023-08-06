# TeamVerify : A Team Analysis tool for Competitive Pokemon

TeamVerify is a Competitive Pokemon teambuilding companion tool based on automated reasoning. 

## Installation

TeamVerify is listed on the PyPI repository. Therefore, it is an easy install for anyone already running Python. Ensure you have a working distribution of Python 3.6 or higher then run the following command in a terminal window:
```
pip install teamverify
```
TeamVerify also needs to run a first-time setup script to populate its knowledge base. Once TeamVerify is installed simply run this command in a terminal window.
```
teamverify-fts
```
We also advise that you re-run this command whenever Smogon implements a major tier shift. TeamVerify's knowledge base only contains a subset of all Pokemon, so it may fall out-of-date as Pokemon shift into and out of OU.


## Usage
```
teamverify {txt/pokepaste} {outputfile}
```
Once installed, teamVerify can be invoked with the above command to the command line. TeamVerify works on one OU team at a time and produces console output as well as output to a text file. {txt/pokepaste} is a mandatory argument and should be the filename of a .txt file containing the team or a link to pokepast.es. {outputfile} is also a mandatory argument and should be the name of the output file you want created (output will have .txt appended to it, so don't include a file extension).
