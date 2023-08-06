# XamPy
## Links
- [Code of Conduct](https://github.com/XamNalpak/xampy/blob/main/CODE-OF-CONDUCT.md)
- [Contributing](https://github.com/XamNalpak/xampy/blob/main/CONTRIBUTING.md)
- [Issues](https://github.com/XamNalpak/xampy/issues)
- [License](https://github.com/XamNalpak/xampy/blob/main/LICENSE)
- [Current Functions](https://github.com/XamNalpak/xampy/blob/main/FUNCTIONS.md)



# _Information_


XamPy is a Data Science Package written in Python. 
## Features

- Simplifying the process of analyzing data
- User-Friendly command based sripting package

## Packages Used

XamPy uses a number of open source projects to work properly:

- Pandas - Data manipulation tool for python
- Numpy - awesome tool for matrix/array mathmatics
- MatPlotLib - tool for graphing in python
- vaderSenitment - tool for senitment anaylsis of social media
- nltk - natural language processing and text mining
- textblob - sentiment analysis on a larger size of text
- datetime for date manipulation

# Installation
```
pip install xampy
or
pip3 install xampy
```

# Contributors and Contributions
IF YOU ARE A CONTRIBUTOR AND ARE NOT LISTED PLEASE EMAIL [Max Paul](mailto:maxkpaul21@gmail.com) or submit a new issue.

 - Max Paul 
   - Lead Contributor/Founder
   - Bachelor Of Science In Data Science from Bryant Unversity.
   - Software engineer by day for TJX.

# Example Use
RECOMMENDED USE WITH A VIRTUAL ENV
```
pip install virtualenv

python -m virtualenv venv

venv\Scripts\activate

pip install xampy
```
```
import xampy as xp

# reading data and showing information
data = xp.makeData('topcsv.csv')
xp.showInfo(data)

# dropping all the rows that contain nulls get dropped
data = xp.dropnaDim(data,'row')

#counting missing data to show all values have been dropped
xp.countMissing(data)

#conducting sentiment analysis on the text data
data = xp.socialSentiment(data,'Content')

#showing the new dataframe
data.head(10)





```

## License

MIT

**Free Software, Hell Yeah!**

