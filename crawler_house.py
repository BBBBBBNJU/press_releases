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
commonPattern = ['media-center/press-releases','media/press-releases','press-releases','press','newsroom/press-releases','news/documentquery.aspx?DocumentTypeID']

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
		unicodePage = unicodePage.lower()
		target='<a href="/news/documentquery\.aspx\?documenttypeid=(\d+?)".{0,20}press releases'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		return temp_url + '=' + myItems[0]
	except:
		return 'null'

def getHousePressReleasePageUrl(congressPeopleHomeUrlDict):
	# first try some common pattern
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
				congressPeoplePressReleasePageDict[name] = str(i) + '|' + temp_url
				break
			except urllib2.HTTPError as err:
					if str(err.code) == '404':
						continue
					else:
						print "parse personal page error code " + str(err.code) + ": " + homepage
		if succeedFlag == False:
			congressPeoplePressReleasePageDict[name] = 'null'
		print "finish: " + name
	return congressPeoplePressReleasePageDict


# houseHomeUrlDict = getHouseRepresenUrl()
# housePressReleasePageDict = getHousePressReleasePageUrl(houseHomeUrlDict)
# cPickle.dump(houseHomeUrlDict,open('houseHomeUrlDict','wb'))
# cPickle.dump(housePressReleasePageDict,open('housePressReleasePageDict','wb'))

# housePressReleasePageDict = cPickle.load(open('housePressReleasePageDict','rb'))
# writer = open('urlTypeFile.csv','w')
# writer.write('lastname,firstname,type,url\n')
# for name,name_url in housePressReleasePageDict.iteritems():
# 	if name_url != 'null':
# 		[temp_type,temp_url] = name_url.split('|')
# 		writer.write(name+','+temp_type+','+temp_url+'\n')
# writer.close()

# def checkUrl(tempUrl):
#     response = urllib2.urlopen(tempUrl)
#     redirected = response.geturl() == tempUrl
#     return redirected,response.geturl()

# housePressReleasePageDict = cPickle.load(open('housePressReleasePageDict','rb'))
# for name,name_url in housePressReleasePageDict.iteritems():
# 	if name_url != 'null':
# 		[temp_type,temp_url] = name_url.split('|')
# 		if temp_url != 'null':
# 			checkResult, trueUrl = checkUrl(temp_url)
# 			if not checkResult:
# 				print name
# 				print temp_url
# 				print trueUrl
# 				print '====='

housePressReleasePageDict = cPickle.load(open('housePressReleasePageDict','rb'))
houseHomeUrlDict = cPickle.load(open('houseHomeUrlDict','rb'))

def typeZerosArticleUrlCrawler(articleUrlList, name, articleMenuPage, pageIndex):
	try:
		if pageIndex == '0':
			temp_url = articleMenuPage
		else:
			temp_url = articleMenuPage + "?page=" + pageIndex
		unicodePage=getunicodePage(temp_url)
		target='<a href="/media-center/press-releases/(.*?)">(.*?)</a>'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		tempUrlList = []
		for eachitem in myItems:
			tempUrlList.append(houseHomeUrlDict[name] + 'media-center/press-releases/' + eachitem[0])
		
		target='page=(\d{1,2})">next'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		if len(myItems) == 0:
			return articleUrlList + tempUrlList
		else:
			return typeZerosArticleUrlCrawler(articleUrlList + tempUrlList, name, articleMenuPage, myItems[0])
	except:
		return articleUrlList


housePressReleaseArticleUrlDict = {}
for name,name_url in housePressReleasePageDict.iteritems():
	if name_url != 'null':
		[temp_type,temp_url] = name_url.split('|')
		if temp_url != 'null':
			if temp_type == '0':
				typeZerosArticleUrlList = typeZerosArticleUrlCrawler([], name, temp_url, '0')
				housePressReleaseArticleUrlDict[name] = typeZerosArticleUrlList
				print name
				if len(typeZerosArticleUrlList) == 0:
					print ", no article list found"
				else:
					print ", " + len(typeZerosArticleUrlList) + ' article found'
cPickle.dump(housePressReleaseArticleUrlDict,open('housePressReleaseArticleUrlDict','wb'))



