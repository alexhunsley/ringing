# -*- coding: utf-8 -*-

import sys
import math
#
# splitCombos.py
#
# Calculations around N max combinations selected from 
# two pools of objects.
# Useful in calculating upper limits of possible bellringing methods
# when both: 
#   a) you have a treble path set
#   b) you are constraining maximum places (outside of the treble)
#        per change
#
#
# General, non-ringing example:
#
# pool A has 2 objects: ? ?
# pool B has 4 objects: ? ? ? ? 
#
#
# In general terms, if we select 2 objects from both pools collectively, the possibilities are
# (broken into three sections based number of selections on pool A) ('x' means selection):
#
#
#      pool A   pool B
#
#  1.  x x      . . . .   <--  2_C_2 * 4_C_0 = 1
#
#  2.  x .      x . . .   \
#      x .      . x . .   |
#      x .      . . x .   |
#      x .      . . . x   |<-- 2_C_1 * 4_C1 = 2 * 4 = 8
#      . x      x . . .   |
#      . x      . x . .   |
#      . x      . . x .   |
#      . x      . . . x   /
#
#  3.  . .      x x . .   \
#      . .      x . x .   |
#      . .      x . . x   |<-- 2_C_0 * 4_C_2 = 1 * 6 = 6
#      . .      . x x .   |
#      . .      . x . x   |
#      . .      . . x x   /
#
# which is 15 combinations.
#
#
# If we are look this in bellringing method terms, whereby an unselected object represents a bell
# staying in place, and an object being selected represents a pair of bells swapping, we have to
# do a reduction step where two positions becomes a single position for every swap in a pool.
#
# For example, suppose we're calculating possible combos of 2 swaps when the treble is moving between 3rd and 3ths place:
#
#    1 2 3 4 5 6 7 8
#    ? ?     ? ? ? ? 
#
# As before, we have pool A on left with 2 positions, and pool B on right with 4 positions.
#
# We break up calculation based on how many swaps are in pool A. We know there is a maximum of
# 1 swap possible there, so we have to do the reduction steps for 0 swaps and 1 swaps.
#
#    0 swap: '? ?' -> '? ?'  (0 swap, so remove 0 items)
#    1 swap: '? ?' -> '?'    (1 swap, so remove 1 items)
#
# So for the case of 0 swaps in pool A, there are 2 - 0 = 2 swaps possible in pool B.
# So now we know that, we perform the reduction step on pool B: '? ? ? ?' -> '? ?'. And to put two swaps into 2 positions,
# there is only one possibilty: '><  ><'.
#
# Drawing this as a blueline style diagram, we get:
#
#    1  2  3  4  5  6  7  8
#    |  |         ><    ><
#
# Then for the case of 1 swaps in pool A, there are 2 - 1 = 1 swaps possible in pool B.
# Therefore the reduction step for pool B is '? ? ? ?' --> '? ? ?'.
# Placing 1 possible swap into those three positions in pool B gives us 3_C_2 = 3 possibilities.
# The three possibilities are:
#
#    1  2  3  4  5  6  7  8
#    |  |         ><   |  | 
#
#    |  |        |   ><   |
#
#    |  |        |   |  ><
#
#
#  (In general, a pool size of N with M swaps size N - M.)
#

# 0, 10 then 1,9 then 2,8 to 6,6: 
# 92, 41,  67,  55, 60, 58, 59  (then it reverses back to 58 etc. due to symmetry)
#
# interesting: less possibilities for odd thing towards centre, but *more* for even thing towards centre.
#

# while writing this, I'm mentally thinking of a major method,
# with the treble currently moving in 6-8, hence we have pools
# of size 4 and 2.

poolAObjectCount = 2
poolBObjectCount = 8


# print(math.factorial(2))

# the n_C_r function:
#
#   = n! / (n-r!)r!
def calcCombos(n, r):
	# print("      =========== factorial: ", n, r)
	return math.factorial(n) // (math.factorial(n - r) * math.factorial(r))

# print(calcCombos(3, 1))



# maximum places we allow in a change.
# it's unusual to get more than 4.
def calcSplitCombosCount(poolAObjectCount, poolBObjectCount, maximumPlaces = -1):
	totalCountIncludingTreble = poolAObjectCount + poolBObjectCount + 2

	fullChange = '.' * totalCountIncludingTreble
	print(fullChange)

	totalObjects = poolAObjectCount + poolBObjectCount

	# we need to ensure pool A count <= pool B count as algorithm
	# assume this; swap them if necessary.

	if poolBObjectCount < poolAObjectCount:
		poolAObjectCount, poolBObjectCount = poolBObjectCount, poolAObjectCount

	print("")
	print(" Pool A size:", poolAObjectCount)
	print(" Pool B size:", poolBObjectCount)
	print("")


	maximumSwapsPoolsA = poolAObjectCount // 2 
	maximumSwapsPoolsB = poolBObjectCount // 2

	maximumSwapsEverywhere = maximumSwapsPoolsA + maximumSwapsPoolsB

	if maximumPlaces >= 0:
		minimumSwapsEverywhere = max(0, (totalObjects - maximumPlaces) // 2)
	else:
		minimumSwapsEverywhere = 0

	print(" maximumSwapsEverywhere = ", maximumSwapsEverywhere)
	print(" minimumSwapsEverywhere = ", minimumSwapsEverywhere, " (to prevent >", maximumPlaces, "places being made)")
	print("")
	print(" maximumSwapsPoolsA = ", maximumSwapsPoolsA)
	print(" maximumSwapsPoolsB = ", maximumSwapsPoolsB)

	print("")
	print("")

	print(" <><><><><><><> have swap ranges: ", minimumSwapsEverywhere, maximumSwapsEverywhere)

	totalPossibilities = 0



	for swaps in range(minimumSwapsEverywhere, maximumSwapsEverywhere + 1):
		print('')
		print("   generating", swaps, "swaps:")

		if swaps == 0:
			print("   Skipping 0 swaps, it does nothing, adding 1 possibility")
			totalPossibilities += 1
			continue

		shortfallOfSwapsInPoolB = swaps - maximumSwapsPoolsB

		minimumSwapsPoolA = max(0, shortfallOfSwapsInPoolB)

		print("")
		print("   shortfallOfSwapsInPoolB = %d, so minimumSwapsPoolA = %d" % (shortfallOfSwapsInPoolB, minimumSwapsPoolA))

		# for swapsInA in range(minimumSwapsPoolA, maximumSwapsPoolsA + 1):
		for swapsInA in range(minimumSwapsPoolA, min(maximumSwapsPoolsA + 1, swaps)): # second term incorrect
			print("    --> doing poolA swaps:", swapsInA)
			swapsInB = swaps - swapsInA
			print("       --> so need", swapsInB, "swaps in B")

			if swapsInB < 0:
				print('\n\n')
				sys.exit("ABORT: found < 0 swaps in B!\n\n")

			reducedPoolSizeA = poolAObjectCount - swapsInA
			reducedPoolSizeB = poolBObjectCount - swapsInB

			changeWithTreble = fullChange[0:reducedPoolSizeA] + '><' + fullChange[0:reducedPoolSizeB]
			print("    %s   " % changeWithTreble, end='')

			combosForA = calcCombos(reducedPoolSizeA, swapsInA)
			combosForB = calcCombos(reducedPoolSizeB, swapsInB)

			print("   A combos = %d_C_%d = %d; " % (reducedPoolSizeA, swapsInA, combosForA), end='')
			print("   B combos = %d_C_%d = %d" % (reducedPoolSizeB, swapsInB, combosForB))

			possibilities = combosForA * combosForB
			totalPossibilities += possibilities
			print("   ->->-> so possibilities for this pair is ", possibilities)

		# swapsWantedInB = 

		print("")
		print("   TOTAL POSSIBILITIES:", totalPossibilities)
	return totalPossibilities

stage = 7

evenResults = []
oddResults = []

maxPlaces = -1

# splitCombosCount = calcSplitCombosCount(0, 8, maxPlaces)
# splitCombosCount = calcSplitCombosCount(1, 7, maxPlaces)
# splitCombosCount = calcSplitCombosCount(2, 6, maxPlaces)
# splitCombosCount = calcSplitCombosCount(3, 5, maxPlaces)
# splitCombosCount = calcSplitCombosCount(4, 4, maxPlaces)
# splitCombosCount = calcSplitCombosCount(5, 3, maxPlaces)
# splitCombosCount = calcSplitCombosCount(6, 2, maxPlaces)
# splitCombosCount = calcSplitCombosCount(7, 1, maxPlaces)
# splitCombosCount = calcSplitCombosCount(8, 0, maxPlaces)

# splitCombosCount = calcSplitCombosCount(5, 4, maxPlaces)
# splitCombosCount = calcSplitCombosCount(4, 5, maxPlaces)

for poolASize in range(0, stage - 2 + 1):
	print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= poolASize:", poolASize)
	poolBSize = stage - 2 - poolASize

	splitCombosCount = calcSplitCombosCount(poolASize, poolBSize, maxPlaces)

	if poolASize % 2 == 0:
		evenResults.append(splitCombosCount)
	else:
		oddResults.append(splitCombosCount)

	print("ANSWER:", splitCombosCount)

print("evens:", evenResults)
print("odds:", oddResults)

all = list(zip(evenResults, oddResults))
allFlatten = lambda l: [item for sublist in l for item in sublist]

print("all:", allFlatten(all))
