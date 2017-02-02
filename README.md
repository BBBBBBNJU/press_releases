# Congress People Press Releases Crawler
## Overview
This project is a crawler for the press release articles. 
## Requirements
Python 2.7 and [NLTK](http://www.nltk.org/)
## How to use
The crawlers for house and senate are seperated. 
### Senate
The organization of senate websites [senate.gov](https://www.senate.gov/) are highly inconsistency. Since there are only 100 senators, I manually get their home page urls and press releases home page urls. Please see `senateUrl.csv`. Then use `senate_getHomeUrls.py` to transfer this file to python dictionary `senateUrlDict`. And use `senate_getPRArticlesUrl.py` to get a the urls for all press releases. Finally use `senate_getArticles.py` to get press releases article text data.