import cPickle
reader = open('senateHomeUrl.csv','r')
senateUrlDict = {}
for eachline in reader:
	if '==' not in eachline:
		if 'http' not in eachline:
			allitems = eachline.split()
			temp_name = allitems[0] +  allitems[1]
			senateUrlDict[temp_name] = []
		else:
			tempLine = eachline.strip()
			senateUrlDict[temp_name].append(tempLine[0:len(tempLine)-2])

print senateUrlDict
cPickle.dump(senateUrlDict,open('senateUrlDict','wb'))