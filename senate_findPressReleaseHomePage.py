# -*- coding: utf-8 -*- 
import cPickle
import urllib2
import urllib  
import re  
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import thread  
import requests
import time
import codecs
import os
import sys
htmlentities = ["&quot;","&nbsp;","&amp;","&lt;","&gt;","&OElig;","&oelig;","&Scaron;","&scaron;","&Yuml;","&circ;","&tilde;","&ensp;","&emsp;","&thinsp;","&zwnj;","&zwj;","&lrm;","&rlm;","&ndash;","&mdash;","&lsquo;","&rsquo;","&sbquo;","&ldquo;","&rdquo;","&bdquo;","&dagger;","&Dagger;","&permil;","&lsaquo;"]
def getunicodePage(Url):
    page = requests.get(Url)
    html_contents = page.text
    unicodePage = ""
    for eachElement in html_contents:
    	try:
    		eachElement.decode("ascii",'ignore')
    		unicodePage += eachElement
    	except:
    		continue
    return unicodePage

def checkUrl(tempUrl):
    response = urllib2.urlopen(tempUrl)
    redirected = response.geturl() == tempUrl
    return redirected,response.geturl()


def getSenatePRHomeUrl(tempUrl):
	pressReleaseHomeUrl = ""
	unicodePage = getunicodePage(tempUrl)
	allLines = unicodePage.split('\n')
	for i in range(len(allLines)):
		lower_line = allLines[i].lower()
		if 'press' in lower_line and 'release' in lower_line and 'href' in lower_line:
			target='<a href="(.*?)press(.{3,10})">'
			myItems = re.findall(target,lower_line,re.DOTALL)
			if len(myItems) > 0:
				pressReleaseHomeUrl = myItems[0][0] + 'press' + myItems[0][1]
				break

	return pressReleaseHomeUrl

# senatePressReleaseHomePageDict_update = {}
# senatePressReleaseHomePageDict = {}
# senateHomeUrlDict = cPickle.load(open('senateHomeUrlDict','rb'))
# for name, homePage in senateHomeUrlDict.iteritems():
# 	pressReleaseHomePageUrl = getSenatePRHomeUrl(homePage)
# 	if len(pressReleaseHomePageUrl) > 0:
# 		senatePressReleaseHomePageDict[name] = pressReleaseHomePageUrl
# for name, pressReleaseHomePage in senatePressReleaseHomePageDict.iteritems():
# 	if '<' not in pressReleaseHomePage:
# 		if 'http' in pressReleaseHomePage:
# 			senatePressReleaseHomePageDict_update[name] = pressReleaseHomePage
# 		else:
# 			senatePressReleaseHomePageDict_update[name] = senateHomeUrlDict[name] + pressReleaseHomePage[1:len(pressReleaseHomePage)]
# 	if 'href="/press-releases"' in pressReleaseHomePage:
# 		senatePressReleaseHomePageDict_update[name] =  senateHomeUrlDict[name]+ "/press-releases/"
# senatePressReleaseHomePageDict_update['Inhofe, James M.'] = 'http://www.inhofe.senate.gov/newsroom/press-releases/'

# cPickle.dump(senatePressReleaseHomePageDict_update,open('senatePRHomePageDict','wb'))

senateHomeUrlDict = cPickle.load(open('senateHomeUrlDict','rb'))
senatePRHomePageDict = cPickle.load(open('senatePRHomePageDict','rb'))
for name, homeurl in senateHomeUrlDict.iteritems():
	if not senatePRHomePageDict.has_key(name):
		print name
		print homeurl
		print '========'




