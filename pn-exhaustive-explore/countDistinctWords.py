# -*- coding: utf-8 -*-

import sys
import math

symbols = "ABCD"

slen = len(symbols)

wordLen = 3
results = []

def reverseStr(s):
	return s[::-1]

# add word result if it's not a mirror or rotation (or both) of an existing result
def addResult(res):
	lenny = len(res)

	revRes = reverseStr(res)
	
	for rotAmount in range(0, lenny):
		rotated = res[rotAmount:] + res[:rotAmount]
		rotatedRev = revRes[rotAmount:] + revRes[:rotAmount]
	
		if rotated in results or rotatedRev in results:
			return

	results.append(res)

def addLetter(str, level):
	if level == wordLen:
		addResult(str)
		return

	for c in symbols:
		addLetter(str + c, level + 1)


for wLen in range(1, 10):
	wordLen = wLen
	results = []

	addLetter("", 0)
	# print(results)
	print(len(results))
