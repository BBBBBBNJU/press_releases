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

def thirdTypeUrlProcess(temp_url):
	try:
		unicodePage=getunicodePage(temp_url)
		unicodePage = unicodePage.lower()
		target='<a href="/news/documentquery\.aspx\?documenttypeid=(.*?)">press releases'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		return temp_url + '=' + myItems[0]
	except:
		return 'null'

def getCongressPeoplePressReleasePageUrl(congressPeopleHomeUrlDict):
	# first try some common pattern
	commonPattern = ['press-releases','media-center/press-releases','media/press-releases','news/documentquery.aspx?DocumentTypeID']
	congressPeoplePressReleasePageDict = {}
	for name, homepage in congressPeopleHomeUrlDict.iteritems():
		try:
			succeedFlag = False
			for i in range(len(commonPattern)):
				temp_url = homepage + commonPattern[i]
				unicodePage=getunicodePage(temp_url)
				if "PAGE NOT FOUND" not in unicodePage.upper():
					succeedFlag = True
					if i == 3:
						temp_url = thirdTypeUrlProcess(temp_url)
					congressPeoplePressReleasePageDict[name] = temp_url
					break
			if succeedFlag == False:
				congressPeoplePressReleasePageDict[name] = 'null'
		except:
			print "parse personal page error: " + homepage
			congressPeoplePressReleasePageDict[name] = 'null'
	return congressPeoplePressReleasePageDict

congressPeopleHomeUrlDict = getHouseRepresenUrl()
congressPeoplePressReleasePageDict = getCongressPeoplePressReleasePageUrl(congressPeopleHomeUrlDict)
cPickle.dump(congressPeopleHomeUrlDict,open('congressPeopleHomeUrlDict','wb'))
cPickle.dump(congressPeoplePressReleasePageDict,open('congressPeoplePressReleasePageDict','wb'))
