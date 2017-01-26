import cPickle
import sys
DictFile_1 = sys.argv[1]
DictFile_2 = sys.argv[2]
OutFile_1 = sys.argv[3]
OutFile_2 = sys.argv[4]

newDictFile = sys.argv[5]
newOutFile = sys.argv[6]
houseDict_1 = cPickle.load(open(DictFile_1,'rb'))
houseDict_2 = cPickle.load(open(DictFile_2,'rb'))
houseDict = {}
for name, urlList in houseDict_1.iteritems():
	if len(urlList) > 0:
		houseDict[name] = urlList
	elif len(houseTypeTwoDict_2[name]) > 0:
		houseDict[name] = houseDict_2[name]
	else:
		houseDict[name] = []

cPickle.dump(houseDict,open(newDictFile,'wb'))
writer = open(newOutFile,'w')
for name, urlList in houseDict.iteritems():
	writer.write(name+' , ')
	if len(urlList) != 0:
		writer.write(str(len(urlList))+' article found\n')
	else:
		writer.write('no article list found\n')
writer.close()


