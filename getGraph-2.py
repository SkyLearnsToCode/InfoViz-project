inp = "FUND-all.txt"
try:
	file = open(inp)
except:
	print 'File not found'
	exit()

#['"RECORD #(BIBLIO)"', '"TITLE"', '"AUTHOR"', '"PUB INFO"', '"CALL #(BIBLIO)"', 
#'"ODATE"', '"RDATE"', '"FUND"', '"TOT CHKOUT"', '"LOUTDATE"']
#all should -2 because of ""
#title max = 1106
#title min = 6

data = []
nodesarray = "\"nodes\": [\n"
purecodes = []
nodenames = []
nodevalues = {}

#get pure fund codes
for i in file:
	data.append(i)
	j = i.strip().split(',')
	if j[0].split('-')[0] not in purecodes:
		purecodes.append(j[0].split('-')[0])
	nodevalues[j[0]] = int(j[1].strip('\n'))+1

for fund in purecodes:
	for year in range(2005,2016):
		before = fund+"-"+str(year)
		nodenames.append(before)
		nodesarray = nodesarray + "{\"name\":\"" + before + "\"},\n"

nodesarray += "]}"

for node in nodenames:
	if node not in nodevalues.keys():
		nodevalues[node] = 1

linksarray = "{\n\"links\": [\n"

for fund in purecodes:
	for year in range(2005,2016):
		before = fund+"-"+str(year)
		if year < 2015:
			after = fund+"-"+str(year+1)
			linksarray = linksarray + "{\"source\":\""+before+"\",\"target\":\""+after+"\",\"value\":\""+str(nodevalues[before])+"\"},\n"

linksarray += "],\n"

wfile = open("graph-2.json",'w')
wfile.write(linksarray+nodesarray)