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

senateUrlDict = cPickle.load(open('senateUrlDict','rb'))
for name, homeUrls in senateUrlDict.iteritems():
	PR_homeUrl = homeUrls[1] + '/'
	homeUrl = homeUrls[0]


