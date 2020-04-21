# -*- coding: utf-8 -*-
#
# Have confirmed that the output of this script, without the 'adjacent colours different' condition,
# matches k-ary bracelet series, e.g. for 4 letters: https://oeis.org/search?q=4%2C10%2C20%2C55%2C136%2C430%2C1300&language=english&go=Search
#
# divisor function: \sigma_x(n)=\sum_{d\mid n} d^x

import sys
import math
from math import gcd

# n divides d, as a generator
def divisorGenerator(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(int(n / i))
    for divisor in reversed(large_divisors):
        yield divisor

print(list(divisorGenerator(100)))


symbols = "ABC"

slen = len(symbols)

wordLen = -1
results = []

def reverseStr(s):
	return s[::-1]

# from https://stackoverflow.com/a/18114286/348476
def phi(n):
    amount = 0        
    for k in range(1, n + 1):
        if gcd(n, k) == 1:
            amount += 1
    return amount

# k = symbols/place notation count
# n = string length/lead length
#
# This is my implementation of the equation I found and stated at https://math.stackexchange.com/q/3633212/21468:
#
#   T(n, k) = \frac{k^{\lfloor (n+1)/2 \rfloor} + k^{\lceil (n+1)/2 \rceil}} {4} + \frac{ \sum_{d|n} \phi (d) \cdot k^{n/d} } {2n}
#
# NOTE: this equation allows adjacent colour repeats!
def calcDistinctMethodsAllowAdjacentRepeats(n, k):
	topRHS = 0
	for dThatDividesN in divisorGenerator(n):
		d = dThatDividesN
		# print("got a divisor:", dThatDividesN)

		topRHS += phi(d) * pow(k, n / d)

	rhs = topRHS / (2 * n)

	lhs = pow(k, math.floor((n + 1) / 2)) + pow(k, math.ceil((n + 1) / 2))
	lhs /= 4

	result = lhs + rhs
	# print("RESULT(n: %d, k: %d): %d" % (n, k, result))
	return result



# add word result if it's not a mirror or rotation (or both) of an existing result
def addResult(res, allowAdjacentLetters = False):
	lenny = len(res)

	if not allowAdjacentLetters:
		# drop any results with repeated adjacent letters
		#  -- also check the first and last letters!
		if res[0] == res[-1]:
			return

		for i in range(0, len(res) - 1):
			if res[i] == res[i+1]:
				return

	revRes = reverseStr(res)
	
	for rotAmount in range(0, lenny):
		rotated = res[rotAmount:] + res[:rotAmount]
		rotatedRev = revRes[rotAmount:] + revRes[:rotAmount]
	
		if rotated in results or rotatedRev in results:
			return

	results.append(res)

def addLetter(str, level, allowAdjacentLetters = True):
	if level == wordLen:
		addResult(str, allowAdjacentLetters)
		return

	for c in symbols:
		addLetter(str + c, level + 1, allowAdjacentLetters)


def calcBruteForceStrings(allowAdjacentLetters):
	addLetter("", 0, allowAdjacentLetters)

for wLen in range(1, 10):
	wordLen = wLen
	results = []

	calcBruteForceStrings(allowAdjacentLetters = True)

	# print(results)
	print("wLen = %d, brute force answer: %d" % (wLen, len(results)))
	print("   ... sum answer:", calcDistinctMethodsAllowAdjacentRepeats(n=wLen, k=len(symbols)))




