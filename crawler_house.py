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
commonPattern = ['media-center/press-releases','media/press-releases','press-releases','news/documentquery.aspx?DocumentTypeID','press','newsroom/press-releases']

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
				if i == 3:
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

def ordinaryTypeArticleUrlCrawler(articleUrlList, name, articleMenuPage, pageIndex, pageType):
	try:
		if pageIndex == '0':
			temp_url = articleMenuPage
		else:
			temp_url = articleMenuPage + "?page=" + pageIndex
		unicodePage=getunicodePage(temp_url)
		if pageType != 2:
			page_pattern = commonPattern[pageType]
		else:
			page_pattern = 'press-release' # the pattern for type 2 could be press-releases or press-release
		target='<a href="/' + page_pattern + '/(.*?)">(.*?)</a>'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		tempUrlList = []
		for eachitem in myItems:
			tempUrlList.append(houseHomeUrlDict[name] + page_pattern + '/' + eachitem[0])
		target='page=(\d{1,3})">next'
		myItems = re.findall(target,unicodePage,flags=re.IGNORECASE)
		if len(myItems) == 0:
			return articleUrlList + tempUrlList
		else:
			return ordinaryTypeArticleUrlCrawler(articleUrlList + tempUrlList, name, articleMenuPage, myItems[0], pageType)
	except:
		return articleUrlList

def listTypeArticleUrlCrawler(articleUrlList, name, articleMenuPage, pageIndex):
	try:
		temp_url = articleMenuPage + "&Page=" + pageIndex
		unicodePage=getunicodePage(temp_url)
		target='<a href="/news/documentsingle\.aspx\?DocumentID=(\d{1,10})">'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		tempUrlList = []
		for eachitem in myItems:
			tempUrlList.append(houseHomeUrlDict[name] + 'news/documentsingle.aspx?DocumentID=' + eachitem)
		target='Page=(\d{1,2})">Next'
		myItems = re.findall(target,unicodePage,re.DOTALL)
		if len(myItems) == 0:
			return articleUrlList + tempUrlList
		else:
			return listTypeArticleUrlCrawler(articleUrlList + tempUrlList, name, articleMenuPage, myItems[0])
	except:
		return articleUrlList


# chosen_type = sys.argv[1]
# housePressReleaseArticleUrlDict = {}
# for name,name_url in housePressReleasePageDict.iteritems():
# 	# os.system("echo \"Now processing: "+name+"\" | mail -s \"update\" haoyan.wustl@gmail.com")
# 	if name_url != 'null':
# 		[temp_type,temp_url] = name_url.split('|')
# 		if temp_url != 'null' and temp_type == chosen_type:
# 			houseArticleUrlList = []
# 			if temp_type in ['0','1','2','4','5']:
# 				houseArticleUrlList = ordinaryTypeArticleUrlCrawler([], name, temp_url, '0', int(temp_type))
# 			else:
# 				houseArticleUrlList = listTypeArticleUrlCrawler([], name, temp_url, '1')
# 			housePressReleaseArticleUrlDict[name] = houseArticleUrlList
# 			print name,
# 			if len(houseArticleUrlList) == 0:
# 				print ", no article list found"
# 				os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type +", no article list found\" | mail -s \"update\" haoyan.wustl@gmail.com")
# 			else:
# 				print ", " + str(len(houseArticleUrlList)) + ' article found'
# 				os.system("echo \"Finish processing: "+ name + ", " + "type: "+ chosen_type + ", " + str(len(houseArticleUrlList)) + "article found\" | mail -s \"update\" haoyan.wustl@gmail.com")
# cPickle.dump(housePressReleaseArticleUrlDict,open('housePressReleaseArticleUrlDict_type' + chosen_type,'wb'))

def getCleanPage_typeZero(unicodePage):
	cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
	cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
	cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
	for h in htmlentities:
		cleanPage = cleanPage.replace(h, " ")
	cleanPage = re.sub(r'“','"',cleanPage)
	cleanPage = re.sub(r'”','"',cleanPage)
	cleanArticle = ""
	for eachline in cleanPage.split('\n'):
		if len(eachline.split()) > 20 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
			cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
	errorFreeArticle = ""
	for eachElement in cleanArticle:
		try:
			eachElement.encode('ascii')
			errorFreeArticle += eachElement
		except:
			continue
	return errorFreeArticle

def zeroTypeGetArticle(oneUrl):
	try:
		unicodePage=getunicodePage(oneUrl)
		article = getCleanPage_typeZero(unicodePage)
		return article
	except:
		return ""

def getCleanPage_typeOne(unicodePage):
	cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
	cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
	cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
	for h in htmlentities:
		cleanPage = cleanPage.replace(h, " ")
	cleanPage = re.sub(r'“','"',cleanPage)
	cleanPage = re.sub(r'”','"',cleanPage)
	cleanArticle = ""
	for eachline in cleanPage.split('\n'):
		if len(eachline.split()) > 20 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
			cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
	errorFreeArticle = ""
	for eachElement in cleanArticle:
		try:
			eachElement.encode('ascii')
			errorFreeArticle += eachElement
		except:
			continue
	return errorFreeArticle

def oneTypeGetArticle(oneUrl):
	try:
		unicodePage=getunicodePage(oneUrl)
		article = getCleanPage_typeOne(unicodePage)
		return article
	except:
		return ""

def getCleanPage_typeTwo(unicodePage):
	cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
	cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
	cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
	for h in htmlentities:
		cleanPage = cleanPage.replace(h, " ")
	cleanPage = re.sub(r'“','"',cleanPage)
	cleanPage = re.sub(r'”','"',cleanPage)
	cleanArticle = ""
	for eachline in cleanPage.split('\n'):
		if len(eachline.split()) > 20 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
			cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
	errorFreeArticle = ""
	for eachElement in cleanArticle:
		try:
			eachElement.encode('ascii')
			errorFreeArticle += eachElement
		except:
			continue
	return errorFreeArticle

def getCleanPage_typeTwo_oneParagraph(unicodePage):
	target='class="contentdata">(.*?)<div class="push">'
	myItems = re.findall(target,unicodePage,re.DOTALL)
	cleanArticle = myItems[0]
	cleanArticle = re.sub(r'</?\w+[^>]*>','',cleanArticle)
	for h in htmlentities:
		cleanArticle = cleanArticle.replace(h, " ")
	cleanArticle = re.sub(r'“','"',cleanArticle)
	cleanArticle = re.sub(r'”','"',cleanArticle)
	errorFreeArticle = ""
	for eachElement in cleanArticle:
		try:
			eachElement.encode('ascii')
			errorFreeArticle += eachElement
		except:
			continue
	return errorFreeArticle

def twoTypeGetArticle(oneUrl):
	try:
		unicodePage=getunicodePage(oneUrl)
		if len(unicodePage.split('\n')) > 10:
			article = getCleanPage_typeTwo(unicodePage)
		else:
			article = getCleanPage_typeTwo_oneParagraph(unicodePage)
		return article
	except:
		return ""

def getCleanPage_typeThree(unicodePage):
	cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
	cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
	cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
	for h in htmlentities:
		cleanPage = cleanPage.replace(h, " ")
	cleanPage = re.sub(r'“','"',cleanPage)
	cleanPage = re.sub(r'”','"',cleanPage)
	cleanArticle = ""
	for eachline in cleanPage.split('\n'):
		if len(eachline.split()) > 20 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
			cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
	errorFreeArticle = ""
	for eachElement in cleanArticle:
		try:
			eachElement.encode('ascii')
			errorFreeArticle += eachElement
		except:
			continue
	return errorFreeArticle

def threeTypeGetArticle(oneUrl):
	try:
		unicodePage=getunicodePage(oneUrl)
		article = getCleanPage_typeThree(unicodePage)
		return article
	except:
		return ""

def getCleanPage_typeFourFive(unicodePage):
	cleanPage = re.sub(r'<li>','xxxxxxxxxxxxxx',unicodePage)
	cleanPage = re.sub(r'<br/>','xxxxxxxxxxxxxx',cleanPage)
	cleanPage = re.sub(r'</?\w+[^>]*>','',cleanPage)
	for h in htmlentities:
		cleanPage = cleanPage.replace(h, " ")
	cleanPage = re.sub(r'“','"',cleanPage)
	cleanPage = re.sub(r'”','"',cleanPage)
	cleanArticle = ""
	for eachline in cleanPage.split('\n'):
		if len(eachline.split()) > 20 and ('jQuery' not in eachline) and ('http' not in eachline) and ('{' not in eachline) and ('}' not in eachline) and ('xxxxxxxxxxxxxx' not in eachline):
			cleanArticle +=  re.sub(r'</?\w+[^>]*>','',eachline)
	errorFreeArticle = ""
	for eachElement in cleanArticle:
		try:
			eachElement.encode('ascii')
			errorFreeArticle += eachElement
		except:
			continue
	return errorFreeArticle

def fourFiveTypeGetArticle(oneUrl):
	try:
		unicodePage=getunicodePage(oneUrl)
		article = getCleanPage_typeFourFive(unicodePage)
		return article
	except:
		return ""

chosen_type = sys.argv[1]
housePressReleaseArticleUrlDict = cPickle.load(open('./results/housePressReleaseArticleUrlDict_type'+chosen_type,'rb'))
housePressReleaseArticleDict = {}
for name, urlList in housePressReleaseArticleUrlDict.iteritems():
	if len(urlList) > 0:
		housePressReleaseArticleDict[name] = []
		urlList = list(set(urlList))
		for eachurl in urlList:
			if chosen_type == '0':
				tempArticle = zeroTypeGetArticle(eachurl)
			elif chosen_type == '1':
				tempArticle = oneTypeGetArticle(eachurl)
			elif chosen_type == '2':
				tempArticle = twoTypeGetArticle(eachurl)
			elif chosen_type == '3':
				tempArticle = threeTypeGetArticle(eachurl)
			elif chosen_type == '4' or chosen_type == '5':
				tempArticle = fourFiveTypeGetArticle(eachurl)

			if len(tempArticle) > 0:
				housePressReleaseArticleDict[name].append(tempArticle)

		os.system("echo \"Finish processing: "+ name + ", " + str(len(housePressReleaseArticleDict[name])) + "articles\" | mail -s \"update\" haoyan.wustl@gmail.com")
		
cPickle.dump(housePressReleaseArticleDict,open('housePressReleaseArticleDict_type' + chosen_type,'wb'))





