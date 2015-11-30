import operator
inp = "FUND-all.txt"
try:
	file = open(inp)
except:
	print 'File not found'
	exit()

class Link(object):
	def __init__(self, source, target, value):
		self.source = source
		self.target = target
		self.value = value

def getKey(link):
	return int(link.value)

purecodes = []
fullnodenames = []
nodevalues = {}

nodesarray = "\"nodes\": [\n"
nodesbyyear = "\"by-year\": [\n"

for i in file:
	j = i.strip().split(',')
	if j[0].split('-')[0] not in purecodes:
		purecodes.append(j[0].split('-')[0])
	nodevalues[j[0]] = int(j[1].strip('\n'))+1

for fund in purecodes:
	for year in range(2005,2016):
		before = fund+"-"+str(year)
		fullnodenames.append(before)
		#nodesarray = nodesarray + "{\"name\":\"" + before + "\"},\n"
		#nodesbyyear = nodesbyyear + "\t{\n\t\"year\": \"" + str(year) + "\",\n\t\"codenodes\": [\n";
		#for code in purecodes:
		#	nodesbyyear += "\t\t{\"name\":\"" + before + "\"},\n";
		#nodesbyyear = nodesbyyear[0:-2];
		#nodesbyyear += "]\n\t},\n"

for node in fullnodenames:
	if node not in nodevalues.keys():
		nodevalues[node] = 1

sorted_nodes = sorted(nodevalues,key=operator.itemgetter(1))

for node in sorted_nodes:
	year = node.split('-')[1]
	nodesarray = nodesarray + "{\"name\":\"" + node + "\",\n\"value\":" + str(nodevalues[node]) +"},\n"
	nodesbyyear = nodesbyyear + "\t{\n\t\"year\": \"" + year + "\",\n\t\"codenodes\": [\n";
	for code in purecodes:
		nodesbyyear += "\t\t{\"name\":\"" + code + "-" + year + "\"},\n";
	nodesbyyear = nodesbyyear[0:-2];
	nodesbyyear += "]\n\t},\n"

nodesbyyear = nodesbyyear[0:-2]
nodesbyyear += "]}"		
nodesarray = nodesarray[0:-2]
nodesarray += "]}"

linksarray = "{\n\"links\": [\n"
linklist = []
for fund in purecodes:
	for year in range(2005,2016):
		before = fund+"-"+str(year)
		value = str(nodevalues[before])
		if year < 2015:
			after = fund+"-"+str(year+1)
			linklist.append(Link(before, after, value))
#linksarray = linksarray + "{\"source\":\""+before+"\",\"target\":\""+after+"\",\"value\":\""+value+"\"},\n"
linklist = sorted(linklist, key=getKey)
for link in linklist:
	linksarray = linksarray + "{\"source\":\""+link.source+"\",\"target\":\""+link.target+"\",\"value\":\""+link.value+"\"},\n"
linksarray = linksarray[0:-2]
linksarray += "],\n"

wfile = open("graph-1.json",'w')
wfile.write(linksarray+nodesarray)