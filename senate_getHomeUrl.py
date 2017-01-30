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

def getSenateHomeUrl():
	reader = open('senate_home_page.html','r')
	unicodePage = ""
	for eachline in reader:
		unicodePage += eachline
	congressPeopleHomeUrlDict = {}
	target='contenttext" align="left"><a href="(.*?)">(.*?)\n(.*?)</a>'
	myItems = re.findall(target,unicodePage,re.DOTALL)
	for i in range(len(myItems)):
		temp_url = myItems[i][0]
		temp_name = myItems[i][1].strip()
		if not temp_url.endswith('/'):
			temp_url += '/'
		if temp_url[0:4] != 'http':
			temp_url = 'http:' + temp_url
		temp_url_https = 'https://' + temp_url[7:len(temp_url)]
		temp_url_public = temp_url + 'public/'
		congressPeopleHomeUrlDict[temp_name] = [temp_url_public,temp_url,temp_url_https]
	return congressPeopleHomeUrlDict

def correctUrl(tempUrl):
	unicodePage = getunicodePage(tempUrl)
	if "WEBSITE TEMPORARILY UNAVAILABLE DUE TO MAINTENANCE" in unicodePage:
		return False
	if 'http-equiv="refresh"' in unicodePage:
		return False
	return True

senateHomeUrlDict_updated = {}
senateHomeUrlDict = getSenateHomeUrl()

for name, senator_home_pages in senateHomeUrlDict.iteritems():	
	tempLabelList = []
	for i in range(3):
		tempLabel = correctUrl(senator_home_pages[i])
		tempLabelList.append(tempLabel)
	if tempLabelList[0]:
		senateHomeUrlDict_updated[name] = senator_home_pages[0]
		continue
	if tempLabelList[2]:
		senateHomeUrlDict_updated[name] = senator_home_pages[2]
		continue
	if tempLabelList[1]:
		senateHomeUrlDict_updated[name] = senator_home_pages[1]
		continue

cPickle.dump(senateHomeUrlDict_updated,open('senateHomeUrlDict','wb'))

