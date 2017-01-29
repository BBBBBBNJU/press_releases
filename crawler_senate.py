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
    unicodePage = html_contents.decode("utf-8",'ignore')
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
		congressPeopleHomeUrlDict[temp_name] = temp_url
	return congressPeopleHomeUrlDict

senateHomeUrlDict = getSenateHomeUrl()
print senateHomeUrlDict
 