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

def getName(unicodePage):
	target='https://www.congress.gov/(.*?)">(.*?)</a>'
	myItems = re.findall(target,unicodePage,re.DOTALL)
	job_name = myItems[0][1].split()
	name = job_name[1:len(job_name)].join(' ')
	return name

def getParty(unicodePage):
	target='Party:(.*?)<span>(.*?)</span>'
	myItems = re.findall(target,unicodePage,re.DOTALL)
	party = myItems[0][1]
	return party

def getServeTime(unicodePage):
	target='<li>(.*?)</li>'
	myItems = re.findall(target,unicodePage,re.DOTALL)
	serveTime = myItems[0]
	return serveTime

def getCongressPeopleData(baseUrl, pageIndex):
	congressPeopleDict = {}
	try:
		temp_url = baseUrl + pageIndex
		unicodePage=getunicodePage(temp_url)
		target='<span class="result-heading"><a href="(.*?)</ul>'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		myItems = list(set(myItems))
		for eachitem in myItems:
			tempName = getName(eachitem)
			tempParty = getParty(eachitem)
			tempServeTime = getServeTime(eachitem)
			congressPeopleDict[tempName] = [tempParty, tempServeTime]
		return congressPeopleDict
	except:
		return congressPeopleDict


congressNumber = sys.argv[1]
baseUrl = 'https://www.congress.gov/members?q={"congress":"'+congressNumber+'"}&page='
congressPeopleDict = {}
for i in range(6):
	congressPeopleDict.update(getCongressPeopleData(baseUrl, str(i)))
cPickle.dump(congressPeopleDict,open('congressPeopleDict_'+congressNumber,'wb'))
print len(congressPeopleDict)
print congressPeopleDict['Thune, John']
