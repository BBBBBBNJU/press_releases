import cPickle
houseTypeTwoDict_1 = cPickle.load(open('housePressReleaseArticleUrlDict_type2_part1','rb'))
houseTypeTwoDict_2 = cPickle.load(open('housePressReleaseArticleUrlDict_type2_part2','rb'))
houseTypeTwpDict = {}
for name, urlList in houseTypeTwoDict_1.iteritems():
	if len(urlList) > 0:
		houseTypeTwpDict[name] = urlList
	elif len(houseTypeTwoDict_2[name]) > 0:
		houseTypeTwpDict[name] = houseTypeTwoDict_2[name]
	else:
		houseTypeTwpDict[name] = []

cPickle.dump(houseTypeTwpDict,open('housePressReleaseArticleUrlDict_type1','wb'))
writer = open('output_2.log','w')
for name, urlList in houseTypeTwpDict.iteritems():
	writer.write(name+' , ')
	if len(urlList) != 0:
		writer.write(str(len(urlList))+' article found\n')
	else:
		writer.write('no article list found\n')
writer.close()


