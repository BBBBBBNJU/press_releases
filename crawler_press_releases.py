# -*- coding: utf-8 -*- 
import cPickle
import urllib2
import urllib  
import re  
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import thread  
import time
import codecs
import os
import sys
htmlentities = ["&quot;","&nbsp;","&amp;","&lt;","&gt;","&OElig;","&oelig;","&Scaron;","&scaron;","&Yuml;","&circ;","&tilde;","&ensp;","&emsp;","&thinsp;","&zwnj;","&zwj;","&lrm;","&rlm;","&ndash;","&mdash;","&lsquo;","&rsquo;","&sbquo;","&ldquo;","&rdquo;","&bdquo;","&dagger;","&Dagger;","&permil;","&lsaquo;"]

def getunicodePage(Url):
    req = urllib2.Request(Url)
    myResponse = urllib2.urlopen(req)
    myPage = myResponse.read()
    unicodePage = myPage.decode("utf-8",'ignore')
    return unicodePage

def getHouseRepresenUrl():
	unicodePage=getunicodePage("http://www.house.gov/representatives/")
	congressPeopleHomeUrlDict = {}
	target='<td><a href="(.*?)">\n(.*?)</a>'
	myItems = re.findall(target,unicodePage,re.DOTALL)
	for i in range(len(myItems)):
		temp_name = myItems[i][1].strip()
		temp_url = myItems[i][0]
		if not temp_url.endswith('/'):
			temp_url += '/'
		congressPeopleHomeUrlDict[temp_name] = temp_url
	return congressPeopleHomeUrlDict

def tableTypeUrlProcess(temp_url):
	try:
		unicodePage=getunicodePage(temp_url)
		# unicodePage = unicodePage.lower()
		target='<a href="/news/documentquery\.aspx\?DocumentTypeID=(\d+?)">\s{0,2}Press Releases'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		return temp_url + '=' + myItems[0]
	except:
		return 'null'

def getCongressPeoplePressReleasePageUrl(congressPeopleHomeUrlDict):
	# first try some common pattern
	commonPattern = ['press-releases','media-center/press-releases','media/press-releases','newsroom/press-releases','press','news/documentquery.aspx?DocumentTypeID']
	congressPeoplePressReleasePageDict = {}
	for name, homepage in congressPeopleHomeUrlDict.iteritems():
		succeedFlag = False
		for i in range(len(commonPattern)):
			temp_url = homepage + commonPattern[i]
			try:
				unicodePage=getunicodePage(temp_url)
				succeedFlag = True
				if i == 5:
					temp_url = tableTypeUrlProcess(temp_url)
				congressPeoplePressReleasePageDict[name] = temp_url
				break
			except urllib2.HTTPError as err:
					if err.code != 404:
						continue
					else:
						print "parse personal page error code " + str(err.code) + ": " + homepage
		if succeedFlag == False:
			congressPeoplePressReleasePageDict[name] = 'null'
	return congressPeoplePressReleasePageDict


congressPeopleHomeUrlDict = getHouseRepresenUrl()
congressPeoplePressReleasePageDict = getCongressPeoplePressReleasePageUrl(congressPeopleHomeUrlDict)
cPickle.dump(congressPeopleHomeUrlDict,open('congressPeopleHomeUrlDict','wb'))
cPickle.dump(congressPeoplePressReleasePageDict,open('congressPeoplePressReleasePageDict','wb'))
