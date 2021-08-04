# -*- coding: utf-8 -*-
import itertools
import sys

# digits = 6
# for i in range(0, pow(2, digits)):
# 	print("{0:b}".format(i).zfill(digits))

# sys.exit(1)

def permutedPartitions(n, I=1):
	return [*itertools.chain.from_iterable(set(itertools.permutations(p)) for p in partitions(n))]

def partitions(n, I=1):
    yield (n,)
    for i in range(I, n//2 + 1):
        for p in partitions(n-i, i):
            yield (i,) + p

# print(list(partitions(5)))

stage = 5
# number of pairs of bells allowed to swap in a row
swaps = 2

# maxSwaps = stage//2


def calcPNPossible(swaps):

	movesToPartition = stage + 1 - swaps
	partsInPartition = swaps + 1

	# perms = permutedPartitions(stage - 2)
	perms = permutedPartitions(movesToPartition)

	perms = [x for x in perms if len(x) == partsInPartition]


	### perms.sort(reverse=True)

	print(perms)

	# output diagram showing each swap
	#   like: __.. for 34 on 4 bells

	for p in perms:
		pos = -1

		for incr in p:
			pos += incr + 1
			print("............"[:incr - 1], end='')
			# pos += 1
			if pos < stage:
				print('><', end='')

		print("")

	return len(perms)

for stage in range(0, 9):
	# print("================================")
	totPerms = 0
	for i in range(0, stage//2 + 1):
		totPerms += calcPNPossible(i)

	print(totPerms)


# sequence is (if you start at stage = 0)
# 1, 1, 2, 3, 5,  8,  13, 21, 34


#       1, 2, 4,  7,  12, 20, 33, 54, 88


# fibofac is MULTIPLICATION!

# ff(1)    = 1

# so ff(2) = P(2) * P(1) 
#		   = f(2+1) * f(1+1)
#          = f(3) * f(2)
# 		   = 2 * 1
#          = 2

# so ff(3) = P(3) * P(2) * P(1) 
#		   = f(3+1) * f(2+1) * f(1+1)
#          = f(4) * f(3) * f(2)
# 		   = 3 * 2 * 1
#          = 6


# ff(4) = 6 * f(5) = 6 * 5 = 30
# ff(5) = 30 * f(6) = 30 * 8 = 240
# ff(6) = 240 * f(7) = 240 * 13 = 3120
# ff(7) = 3120 * f(8) = 3120 * 21 = 65520
# ff(8) = 65520 * f(9) = 65520 * 34 = 2,227,680

# ff seq: 1, 2, 6, 30, 240, 3120, 65520

# Squared: C_p = 1, 4, 36, 900, 57600, 9734400, 4292870400

# X fibofac:
# X ff(n) = f(n) + ff(n-1), with f(0) = 0

# print(perms)
# print(len(perms))
# print([x for x in perms if len(x) == 4])

