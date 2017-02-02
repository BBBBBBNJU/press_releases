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

def oneTypeGetArticle(tempUrl):
	try:
		unicodePage = getunicodePage(tempUrl)
		cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
		cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
		cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
		cleanPage = re.sub(r'“','"',cleanPage)
		cleanPage = re.sub(r'”','"',cleanPage)
		for h in htmlentities:
			cleanPage = cleanPage.replace(h, " ")
		cleanArticle = ""
		for eachline in cleanPage.split('\n'):
			if len(eachline.split()) > 30 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
				target = '<!--(.*?)-->'
				myItems = re.findall(target,eachline,re.DOTALL)
				if len(myItems) == 0:
					cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
		errorFreeArticle = ""
		for eachElement in cleanArticle:
			try:
				eachElement.encode('ascii')
				errorFreeArticle += eachElement
			except:
				continue
		return errorFreeArticle
	except:
		return ""

def twoTypeGetArticle(tempUrl):
	try:
		unicodePage = getunicodePage(tempUrl)
		cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
		cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
		cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
		cleanPage = re.sub(r'“','"',cleanPage)
		cleanPage = re.sub(r'”','"',cleanPage)
		for h in htmlentities:
			cleanPage = cleanPage.replace(h, " ")
		cleanArticle = ""
		for eachline in cleanPage.split('\n'):
			if len(eachline.split()) > 30 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
				target = '<!--(.*?)-->'
				myItems = re.findall(target,eachline,re.DOTALL)
				if len(myItems) == 0:
					cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
		errorFreeArticle = ""
		for eachElement in cleanArticle:
			try:
				eachElement.encode('ascii')
				errorFreeArticle += eachElement
			except:
				continue
		return errorFreeArticle
	except:
		return ""

def threeTypeGetArticle(tempUrl):
	try:
		unicodePage = getunicodePage(tempUrl)
		cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
		cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
		cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
		cleanPage = re.sub(r'“','"',cleanPage)
		cleanPage = re.sub(r'”','"',cleanPage)
		for h in htmlentities:
			cleanPage = cleanPage.replace(h, " ")
		cleanArticle = ""
		for eachline in cleanPage.split('\n'):
			if len(eachline.split()) > 30 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
				target = '<!--(.*?)-->'
				myItems = re.findall(target,eachline,re.DOTALL)
				if len(myItems) == 0:
					cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
		errorFreeArticle = ""
		for eachElement in cleanArticle:
			try:
				eachElement.encode('ascii')
				errorFreeArticle += eachElement
			except:
				continue
		return errorFreeArticle
	except:
		return ""



def fourTypeGetArticle(tempUrl):
	try:
		unicodePage = getunicodePage(tempUrl)
		cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
		cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
		cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
		cleanPage = re.sub(r'“','"',cleanPage)
		cleanPage = re.sub(r'”','"',cleanPage)
		for h in htmlentities:
			cleanPage = cleanPage.replace(h, " ")
		cleanArticle = ""
		for eachline in cleanPage.split('\n'):
			if len(eachline.split()) > 30 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
				target = '<!--(.*?)-->'
				myItems = re.findall(target,eachline,re.DOTALL)
				if len(myItems) == 0:
					cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
		errorFreeArticle = ""
		for eachElement in cleanArticle:
			try:
				eachElement.encode('ascii')
				errorFreeArticle += eachElement
			except:
				continue
		return errorFreeArticle
	except:
		return ""

chosen_type = sys.argv[1]
senatePressReleaseArticleUrlDict = cPickle.load(open('senatePressReleaseArticleUrlDict_type' + chosen_type,'rb'))
senatePressReleaseArticleDict = {}
for name, articleUrlList in senatePressReleaseArticleUrlDict.iteritems():
	count = 0
	articleUrlList = list(set(articleUrlList))
	senatePressReleaseArticleDict[name] = []
	if chosen_type == '1':
		for eachUrl in articleUrlList:	
			temp_article = threeTypeGetArticle(eachUrl)
			if len(temp_article) > 0:
				senatePressReleaseArticleDict[name].append(temp_article)
			
	elif chosen_type == '2':
		for eachUrl in articleUrlList:	
			temp_article = threeTypeGetArticle(eachUrl)
			if len(temp_article) > 0:
				senatePressReleaseArticleDict[name].append(temp_article)
			
	elif chosen_type == '3':
		for eachUrl in articleUrlList:	
			temp_article = threeTypeGetArticle(eachUrl)
			if len(temp_article) > 0:
				senatePressReleaseArticleDict[name].append(temp_article)
	elif chosen_type == '4':
		for eachUrl in articleUrlList:
			temp_article = fourTypeGetArticle(eachUrl)
			if len(temp_article) > 0:
				senatePressReleaseArticleDict[name].append(temp_article)
						
cPickle.dump(senatePressReleaseArticleDict,open('senatePressReleaseArticleDict_type' + chosen_type,'wb'))


