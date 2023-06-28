# splicedPricker.py
#

import sys
import pprint

# Name,plain,bob,single

# map from the method to (plain, bob, single) perms.
methodPerms = {
	'C' : ['15738264', '13578264', '15378264'],
	'Y' : ['15738264', '13578264', '15378264'],
	'S' : ['15738264', '13578264', '15378264'],
	'B' : ['14263857', '14235678', '12435678'], 
	'E' : ['14263857', '18642735', '14623857'],
	'W' : ['16482735', '16423857', '14623857']
}


# do a perm (including treble in the row). 
# e.g. ("ABCDEFGH", "21435678") --> "BADCEFGH"
def doPerm(row, perm):
	newRow = ""
	for num in perm:
		newRow += row[int(num) - 1]

	return newRow

# testy = doPerm("ABCDEFGH", "21435678")
# print(testy)
# sys.exit(1)

# Bobs: Y,S
# Singles: S,B,E,W

# Comp: 3x

# CY.ECS.WS.S.E.
# BB.YW.B.

# each item in the list is one course. So we expect tenor to end in
# home position after each item.
# - = bob
# _ = single (underscore char)
compositionCoursesRaw = ['CY-ECS_WS_S-E_', 'BB_YW_B_']
# compositionCoursesRaw = ['B_', 'B_']

# compositionCoursesRaw = ['B_B_']
# compositionCoursesRaw = ['CCCCCCC-', 'SSSSSSS-', 'YYYYYYY-']


# facts on this comp:
#
# the part has single lead each of E and W, like so: E, W, E, W.
# they only follow a Y or a S.

callChars = ['-', '_']

# split comp courses into individual strings, e.g. 'C', "Y-", "B_", "S", etc.
compositionCourses = []

for course in compositionCoursesRaw:
	splitItemsForThisCourse = []

	currCourseRemaining = course
	while course:
		numCharsToExtract = 1
		if (len(course) > 1 and course[1] in callChars):
			numCharsToExtract = 2

		splitItemsForThisCourse.append(course[0:numCharsToExtract])
		course = course[numCharsToExtract:]

	compositionCourses.append(splitItemsForThisCourse)

# print('\n\nDONE SPLITTING - we have ', compositionCourses, '\n\n')
# sys.exit(1)

partNumber = 1

row = "12345678"

stats = {}


def registerPlacebellRung(method, bell, placebellRung):
	print('register: bell = %d, pb rung = %d' % (bell, placebellRung))

	if method in stats:
		methodInfo = stats[method]
	else:
		methodInfo = {}
		stats[method] = methodInfo

	if bell in methodInfo:
		info = methodInfo[bell]
	else:
		info = {}
		methodInfo[bell] = info

	if placebellRung in info:
		numTimesPBRung = info[placebellRung] + 1
	else:
		numTimesPBRung = 1

	info[placebellRung] = numTimesPBRung

# record for each bell how many times it rings each lead
def recordStatsForLeadStarting(method, row):
	for pos in range(2, 9):
		registerPlacebellRung(method, bell=int(row[pos - 1]), placebellRung=pos)
	pass

recordStatsForLeadStarting('C', row)
# print row

while True:
	courseNumber = 1

	# print('======================================= part start %d' % partNumber)
	print('\n\n=======================================')
	for course in compositionCourses:
		print('\nPart %d, course %d: %s' % (partNumber, courseNumber, course))


		# leadMethodAndCall examples: 'S', 'B-', "S_"
		for leadMethodAndCall in course:
			permIndex = 0
			leadType = ''
			if len(leadMethodAndCall) > 1:
				permIndex = 1 + callChars.index(leadMethodAndCall[1])
				# print('found a perm index = ', permIndex)

			methodStr = leadMethodAndCall[0]
			
			permToUse = methodPerms[methodStr][permIndex]
	
			debugStr = '           permToUse = %s, permIndex = %s' % (permToUse, permIndex)

			prettyMethodStr = leadMethodAndCall.replace('-', ' -');
			prettyMethodStr = prettyMethodStr.replace('_', ' s');

			oldRow = row
			row = doPerm(row, permToUse)

			# print("%s  %s            %s" % (row, prettyMethodStr, debugStr))
			print("%s  %s" % (row, prettyMethodStr))

			recordStatsForLeadStarting(methodStr, oldRow)

			if row == "12345678":
				# print('It came round')
				break

		
		courseNumber += 1
	partNumber +=1

	if row == "12345678":
		print('\nIt came round. Light and fire and have some cake, my priest.\n')
		break

	if partNumber == 5:
		print('too many courses! exiting')
		break

print('++++++++++++++++++ STATS:\n')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stats)

# Ways of outputting the data:
# A method a page: bell versus pb counts
# A bell a page: method versus pb counts
# A pb a page: method versus bell rang

