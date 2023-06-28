# analyseMethod.py
#
# prick methods, help find optimal rotation of PN, heatmap for bell proximity, analyse music
#


# roundsDefault = "12345678"
# methodStage = 8
# pn = ["x", "18", "x", "18","x", "18","x", "18","x", "18", "x", "18", "x", "18", "x", "12"];

roundsDefault = "123456789"
methodStage = 9
pn = ['349', '7', '349', '167', '3', '167'];

dudChange = roundsDefault[-1:] + roundsDefault[-2:-1] 

desirableMusic = ['123456789', '987654321', '135246', '13572468', '12753468', '1526374859']

def bellToInt(bellString):
    if bellString == "0":
        return 10
    if bellString == "E" or bellString == "e":
        return 11
    if bellString == "T" or bellString == "t":
        return 12
        
    return int(bellString)

def doChange(str, placeNotation):
    result = ""
    i = 1
    
    while (i <= len(str)):
        if (placeNotation.find(repr(i)) >= 0):
            result += str[i-1]
            i += 1
        else:
            result += str[i]
            result += str[i-1]
            i += 2

    return result

def generateMethod(pn):
	pnOffset = 0
	lastChange = roundsDefault
	changes = []

	while True:
		change = doChange(lastChange, pn[pnOffset])

		changes.append(change)
		# print("Generated change: ", change)

		if change == roundsDefault:
		    break

		lastChange = change

		pnOffset = (pnOffset + 1) % len(pn)
	return changes



def doStats(method, bell1, bell2):
	distances = []

	bell1str = str(bell1)
	bell2str = str(bell2)

	maxDist = 0
	minDist = 100

	musicNotes = ""

	print "STATS FOR BELLS %d, %d:" % (bell1, bell2)

	isHandstroke = True

	dudChangeCount = 0

	for change in method[0:-1]:
		idx1 = change.index(bell1str)
		idx2 = change.index(bell2str)

		dist = abs(idx2 - idx1)

		maxDist = max(maxDist, dist)
		minDist = min(minDist, dist)

		distances.append(dist)

		print "handstroke, change, part = %d, %s, %s" % (isHandstroke, change, change[-2:])
		if (not isHandstroke) and change[-2:] == dudChange:
			dudChangeCount += 1

		# music
		foundMusicInChange = []
		for music in desirableMusic:
			print music
			musicPart = music

			while len(musicPart) > 3:
				# print "musicPart A " + musicPart
				if change.find(musicPart) >= 0:
					if not musicPart in foundMusicInChange:
						foundMusicInChange.append(musicPart)
						musicNotes += "Music: %s<p/>" % musicPart
						break
				musicPart = musicPart[:-1]

			musicPart = music

			while len(musicPart) > 3:
				# print "musicPart B " + musicPart
				if change.find(musicPart) >= 0:
					if not musicPart in foundMusicInChange:
						foundMusicInChange.append(musicPart)
						musicNotes += "Music: %s<p/>" % musicPart
						break
				musicPart = musicPart[1:]

		# print "For change %s, dist is %d" % (change, dist)

		isHandstroke = not isHandstroke

	averageDist = float(reduce(lambda x, y: x + y, distances)) / float(len(distances))

	if dudChangeCount > 0:
		musicNotes += "<b>Nasty: Got %d x 98s at backstroke</b><p/>" % dudChangeCount
	else:
		musicNotes += "(No 98s at backstroke)<p/>"

	return (minDist, maxDist, averageDist, musicNotes)

def appendHtmlForMethod(pn):
	global html

	method = generateMethod(pn)

	print method

	html = html + "<h2>%s</h2>" % pn

	html = html + '<table border="1" padding="4" cellspacing="0">'

	musicNotes = ""

	for bellA in range (0, methodStage):
		html = html + "<tr>"
		for bellB in range (0, methodStage + 1):

			if (bellA == 0 and bellB == 0): 
				html = html + "<td></td>"
			elif (bellA == 0): 
				# header
				html = html + '<td bgcolor="#ddd">%d</td>' % bellB
			elif (bellB == 0):
				# header
				html = html + '<td bgcolor="#ddd">%d</td>' % bellA
			else:
				if (bellB <= bellA): 
					html = html + "<td></td>"
					continue

				# analyze distances
				(minDist, maxDist, avgDist, musicNotes) = doStats(method, bellA, bellB)

				colour = 15.0 * float(maxDist) / (methodStage - 1)
				print colour

				hexVal = hex(int(15.0 - colour))[2:]
				hexValOpposite = hex(int(colour))[2:]

				hexStr = '#%s%s%s' % ('f', hexVal, hexVal)
				print "hexStr: ", hexStr
				html = html + '<td bgcolor="%s">%d, %s</td>' % (hexStr, maxDist, str(round(avgDist, 1)))


			# print bellA, bellB
		html = html + "</tr>\n"
	html = html + "</table><p/>"

	html += '<p>%s</p>' % musicNotes

html = ""

html = html + "<h3>For each pair of bells, the cells show (max distance, avg distance)</h3>"
	


for rotatePnIdx in range(0, len(pn)):
	appendHtmlForMethod(pn)
	pn = pn[1:] + pn[0:1]

# print html

htmlFile = open("report.html", "w")
htmlFile.write(html)
htmlFile.close()

# for bellA in range (1, methodStage):
# 	for bellB in range (bellA + 1, methodStage+1):
# 		print bellA, bellB
# print(method)
