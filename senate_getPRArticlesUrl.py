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
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	page = requests.get(Url,headers=headers)
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


def oneTypeArticleUrlCrawler(articleUrlList, PR_homeUrl, senateHomeUrl, pageIndex):
	try:
		temp_url = PR_homeUrl + "?page=" + pageIndex
		unicodePage=getunicodePage(temp_url)
		if 'WEBSITE TEMPORARILY UNAVAILABLE DUE TO MAINTENANCE' in unicodePage:
			unicodePage=getunicodePage(temp_url)
		target='<td class="recordListTitle"><a href="(.*?)"'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		tempUrlList = []
		for eachitem in myItems:
			tempUrlList.append(eachitem)
		target='page=(.*?)"(.*?)>Next'
		myItems = re.findall(target,unicodePage,re.IGNORECASE)
		print myItems
		if len(myItems) == 0:
			return articleUrlList + tempUrlList
		else:
			return oneTypeArticleUrlCrawler(articleUrlList + tempUrlList, PR_homeUrl, senateHomeUrl, myItems[0][0])
	except:
		return articleUrlList

def twoTypeArticleUrlCrawler(articleUrlList, PR_homeUrl, senateHomeUrl, pageIndex):
	try:
		temp_url = PR_homeUrl + "?PageNum_rs=" + pageIndex + '&'
		unicodePage=getunicodePage(temp_url)
		startIndex = PR_homeUrl.index('gov/')
		temp_pattern = PR_homeUrl[startIndex + 4 : len(PR_homeUrl)]
		target = temp_pattern + '/(.*?)"'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		tempUrlList = []
		for eachitem in myItems:
			tempUrlList.append(PR_homeUrl + '/' + eachitem.strip())
		target='\?PageNum_rs=(.*?)&">next'
		myItems = re.findall(target,unicodePage,re.IGNORECASE)
		print myItems
		if len(myItems) == 0:
			return articleUrlList + tempUrlList
		else:
			return twoTypeArticleUrlCrawler(articleUrlList + tempUrlList, PR_homeUrl, senateHomeUrl, myItems[0])
	except:
		return articleUrlList

chosen_type = sys.argv[1]
senateUrlDict = cPickle.load(open('senateUrlDict','rb'))
senatePressReleaseArticleUrlDict = {}
for name, homeUrls in senateUrlDict.iteritems():
	PR_homeUrl = homeUrls[1]
	if not PR_homeUrl.endswith('/'):
		PR_homeUrl += '/'
	homeUrl = homeUrls[0]
	if not homeUrl.endswith('/'):
		homeUrl += '/'
	tempUnicode = getunicodePage(PR_homeUrl)
	# type 1, similar to the list one in house
	if 'index.cfm/' in PR_homeUrl and chosen_type == '1':
		senateArticleUrlList = oneTypeArticleUrlCrawler([], PR_homeUrl[0:len(PR_homeUrl)-1], homeUrl , '1')
		print name,
		if len(senateArticleUrlList) == 0:
			print ", no article list found"
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type +", no article list found\" | mail -s \"update\" haoyan.wustl@gmail.com")
		else:
			print ", " + str(len(senateArticleUrlList)) + ' article found'
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type + ", " + str(len(senateArticleUrlList)) + "article found\" | mail -s \"update\" haoyan.wustl@gmail.com")
			senatePressReleaseArticleUrlDict[name] = senateArticleUrlList
	
	# type 2, url start with the PR_homeUrl-homeUrl, probably has something in middle, next page is ?PageNum_rs=2&
	if '?PageNum_rs=' in tempUnicode and chosen_type == '2':
		senateArticleUrlList = twoTypeArticleUrlCrawler([], PR_homeUrl[0:len(PR_homeUrl)-1], homeUrl , '1')
		print name,
		if len(senateArticleUrlList) == 0:
			print ", no article list found"
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type +", no article list found\" | mail -s \"update\" haoyan.wustl@gmail.com")
		else:
			print ", " + str(len(senateArticleUrlList)) + ' article found'
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type + ", " + str(len(senateArticleUrlList)) + "article found\" | mail -s \"update\" haoyan.wustl@gmail.com")
			senatePressReleaseArticleUrlDict[name] = senateArticleUrlList
		print senateArticleUrlList

	# # type 3, url start with the PR_homeUrl-homeUrl, probably has something in middle, next page is ?page=1


	cPickle.dump(senatePressReleaseArticleUrlDict,open('senatePressReleaseArticleUrlDict_type' + chosen_type,'wb'))



