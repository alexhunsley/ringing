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

# # outputs 1, 2, 3, 6
# print(list(divisorGenerator(6)))




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

# removal of rotations
	# revRes = reverseStr(res)
	
	# for rotAmount in range(0, lenny):
	# 	rotated = res[rotAmount:] + res[:rotAmount]
	# 	rotatedRev = revRes[rotAmount:] + revRes[:rotAmount]
	
	# 	if rotated in results or rotatedRev in results:
	# 		return

	results.append(res)

def addLetter(str, level, allowAdjacentLetters = True):
	if level == wordLen:
		addResult(str, allowAdjacentLetters)
		return

	for c in symbols:
		addLetter(str + c, level + 1, allowAdjacentLetters)


def calcBruteForceStrings(allowAdjacentLetters):
	addLetter("", 0, allowAdjacentLetters)


def isRepeatedString(str):
	haveRepeat = False
	infoStr = ""

	strlen = len(str)
	
	# remove last number, for n itself
	# this list includes 1!
	divisors = list(divisorGenerator(strlen))[:-1]

	for div in divisors:
		part = str[0:div]
		repeats = int(strlen / div)
		multStr = part * repeats
#		print("Checking against part = %s, mult = %s" % (part, multStr))
		if str == multStr:
			haveRepeat = True
			infoStr += "%s x '%s', " % (repeats, part)

	if len(infoStr) > 0:
		# remove final ", "
		infoStr = infoStr[:-2]
	return (haveRepeat, infoStr)


def prime_factors(n):
    '''PRIME FACTORS: generates a list of prime factors for the number given
    RETURNS: number(being factored), list(prime factors), count(how many loops to find factors, for optimization)
    '''
    num = n                         #number at the end
    count = 0                       #optimization (to count iterations)
    index = 0                       #index (to test)
    t = [2, 3, 5, 7]                #list (to test)
    f = []                          #prime factors list
    while t[index] ** 2 <= n:
        count += 1                  #increment (how many loops to find factors)
        if len(t) == (index + 1):
            t.append(t[-2] + 6)     #extend test list (as much as needed) [2, 3, 5, 7, 11, 13...]
        if n % t[index]:            #if 0 does else (otherwise increments, or try next t[index])
            index += 1              #increment index
        else:
            n = n // t[index]       #drop max number we are testing... (this should drastically shorten the loops)
            f.append(t[index])      #append factor to list
    if n > 1:
        f.append(n)                 #add last factor...
    return num, f, f'count optimization: {count}'

# sys.exit(1)

# print("isRep: ", isRepeatedString("012345"))
# print("isRep: ", isRepeatedString("010010"))
# print("isRep: ", isRepeatedString("111111"))
# print("isRep: ", isRepeatedString("101010"))

# count repetetive strings
wordLen = 8
results = []

symbols = "ABCD"
slen = len(symbols)

calcBruteForceStrings(allowAdjacentLetters = True)

print(results)

totalRepeatingPNs = 0

for res in results:
	(isRepeat, repeatInfo) = isRepeatedString(res)

	if isRepeat:
		totalRepeatingPNs += 1
	print("%s %s" % (res, repeatInfo))

print("\n========== Total repeating PNs:", totalRepeatingPNs)


### math check

(_, primeFactors, _) = prime_factors(wordLen)

# # remove last item, which is the number itself
# primeFactors = primeFactors[:-1]

# so if wordLen itself is prime, remove it from the primeFactors list here! <---------------------------------------

uniquePrimeFactors = list(set(primeFactors))
# uniquePrimeFactors = [1] + uniquePrimeFactors

# print("new list with 1 added: ", uniquePrimeFactors)

print("num prime factors: ", len(uniquePrimeFactors))
print("unique PFs: ", uniquePrimeFactors)

totalWays = 0

for pf in uniquePrimeFactors:
	# none of these ways overlap since we're only considering unique prime factors!
	numWays = int(pow(slen, wordLen / pf))
	print("for pf %d, found numways %d" % (pf, numWays))

	# discount the combos with all same char, which all factors have a repeat at
	totalWays += numWays - slen

# for AA, BB, CC etc where all symbols are the same
totalWays += slen

#for the first and last combo (e.g. 0000, 1111)
# totalWays += 1

print("========== TOTAL WAYS: ", totalWays)




# for wLen in range(1, 10):
# 	wordLen = wLen
# 	results = []

# 	calcBruteForceStrings(allowAdjacentLetters = True)

# 	# print(results)
# 	print("wLen = %d, brute force answer: %d" % (wLen, len(results)))
# 	print("   ... sum answer:", calcDistinctMethodsAllowAdjacentRepeats(n=wLen, k=len(symbols)))




