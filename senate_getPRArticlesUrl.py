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

def threeTypeArticleUrlCrawler(articleUrlList, PR_homeUrl, senateHomeUrl, pageIndex): 
	try:
		temp_url = PR_homeUrl + "?page=" + pageIndex
		unicodePage=getunicodePage(temp_url)
		if 'href="/content/' in unicodePage:
			target = '<h\d><a href="/content/(.*?)"'
			myItems = re.findall(target,unicodePage,re.DOTALL)
			tempUrlList = []
			for eachitem in myItems:
				tempUrlList.append(senateHomeUrl + 'content/' + eachitem.strip())
		else:
			startIndex = PR_homeUrl.index('gov/')
			temp_pattern = PR_homeUrl[startIndex + 4 : len(PR_homeUrl)]
			target = temp_pattern + '/(.*?)"'
			if 'scott.senate' in PR_homeUrl:
				target = temp_pattern[0:len(temp_pattern)-1] + '/(.*?)"'
			myItems = re.findall(target,unicodePage,re.DOTALL)
			tempUrlList = []
			for eachitem in myItems:
				if 'scott.senate' not in PR_homeUrl:
					if not ('billnelson' in PR_homeUrl and '-' not in eachitem):
						tempUrlList.append(PR_homeUrl + '/' + eachitem.strip())
				else:
					tempUrlList.append(PR_homeUrl[0:len(PR_homeUrl)-1] + '/' + eachitem.strip())
		target='\?page=(\d{1,10})">next'
		myItems = re.findall(target,unicodePage,re.IGNORECASE)
		print myItems
		if len(myItems) == 0:
			return articleUrlList + tempUrlList
		else:
			return threeTypeArticleUrlCrawler(articleUrlList + tempUrlList, PR_homeUrl, senateHomeUrl, myItems[0])
	except:
		return articleUrlList

def fourTypeArticleUrlCrawler(articleUrlList, PR_homeUrl, senateHomeUrl, pageIndex):
	try:
		temp_url = senateHomeUrl + "index.cfm?p=press_releases&pg=" + pageIndex
		unicodePage=getunicodePage(temp_url)
		target='\?p=press_release&amp;id=(\d{1,10})"'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		myItems = list(set(myItems))
		tempUrlList = []
		for eachitem in myItems:
			tempUrlList.append(PR_homeUrl[0:len(PR_homeUrl)-1] + '&id=' + eachitem)
		target='&pg=(.*?)">next'
		myItems = re.findall(target,unicodePage,re.IGNORECASE)
		print myItems
		if len(myItems) == 0:
			return articleUrlList + tempUrlList
		else:
			return fourTypeArticleUrlCrawler(articleUrlList + tempUrlList, PR_homeUrl, senateHomeUrl, myItems[0])
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

	# type 3, url start with the PR_homeUrl-homeUrl, probably has something in middle, next page is ?page=1
	if '?page=' in tempUnicode and 'index.cfm' not in tempUnicode and chosen_type == '3':
		senateArticleUrlList = threeTypeArticleUrlCrawler([], PR_homeUrl[0:len(PR_homeUrl)-1], homeUrl , '0')
		print name,
		if len(senateArticleUrlList) == 0:
			print ", no article list found"
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type +", no article list found\" | mail -s \"update\" haoyan.wustl@gmail.com")
		else:
			print ", " + str(len(senateArticleUrlList)) + ' article found'
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type + ", " + str(len(senateArticleUrlList)) + "article found\" | mail -s \"update\" haoyan.wustl@gmail.com")
			senatePressReleaseArticleUrlDict[name] = senateArticleUrlList

	# type 4, url start with the PR_homeUrl-homeUrl, followed by &amp;id=595, next page is ?pg=1
	if '.gov/?p=press_releases' in PR_homeUrl and chosen_type == '4':
		senateArticleUrlList = fourTypeArticleUrlCrawler([], PR_homeUrl[0:len(PR_homeUrl)-1], homeUrl , '1')
		print name,		
		if len(senateArticleUrlList) == 0:
			print ", no article list found"
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type +", no article list found\" | mail -s \"update\" haoyan.wustl@gmail.com")
		else:
			print ", " + str(len(senateArticleUrlList)) + ' article found'
			os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type + ", " + str(len(senateArticleUrlList)) + "article found\" | mail -s \"update\" haoyan.wustl@gmail.com")
			senatePressReleaseArticleUrlDict[name] = senateArticleUrlList
		

	cPickle.dump(senatePressReleaseArticleUrlDict,open('senatePressReleaseArticleUrlDict_type' + chosen_type,'wb'))



