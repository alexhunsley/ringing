from lark import Lark
from lark import Transformer
import sys
import timeit

#
# examples of acceptable PN:
#
# x can have . around it:
#     x.1
#     x.1.x
#     1.x
#
# x doesn't need . between it and non-x:
#     x12
#     x12x
#     12x
#
# random:
#     1.2.3.4
#     12
#     12.34
#     12.90E
#     x12x34.14
#     145.56x78x12
#     1.x.2.x.3.x
#
#

# We prepend separator with _, which means it is always removed, but children remain in-place.
# this avoids need to later remove empty items from the transformed list.
# Anther (not as good) strategy is to throw the Discard exception in the transformer, which
# would remove that node 
l = Lark('''pnlist: _separator
				  | _separator? pnstring (_separator pnstring)* _separator?

			_separator: ("." | allswap)+

 			pnstring: pn+
                    | REVERSE_PN pn+

            pn: HEXDIGIT
	          | "[" SIGNED_INT "]"

			allswap: ALL_SWAP

	        REVERSE_PN: "~"
	        ALL_SWAP: "x" | "X"
			ENDCODE: "&"

	        %import common.HEXDIGIT
	        %import common.SIGNED_INT
         ''', start='pnlist', parser='lalr')

# print( l.parse("1458[-10]").pretty() )
# print( l.parse("~12").pretty() )
# print( l.parse("1234").pretty() )

# print( l.parse("12.34.x.78[-22]").pretty() )
# print( l.parse("12x34").pretty() )

# r = l.parse("x12x34.56")

# ensure each item in the PN is separated by '.', including 'X' items.
# e.g. 12x34 -> 12.x.34
def canonicalisePnStr(str):
	newStr = ""

	lastChar = ''

	passingABracketCode = False

	for c in str:
		if c != '.' and lastChar != '.':
			if (not c.isdigit()) and lastChar.isdigit():
				newStr = newStr + '.'
			elif (c.isdigit()) and not lastChar.isdigit():
				newStr = newStr + '.'

		newStr = newStr + c

		lastChar = c	

	return newStr

def parse(pnStr):
	return l.parse(pnStr) 

	# canonicalPnStr = canonicalisePnStr(pnStr)
	# return l.parse(canonicalPnStr) 


# print(canonicalisePnStr("12x"))
# print(canonicalisePnStr("x12"))
# print(canonicalisePnStr("12x23.43"))
# print(canonicalisePnStr("34x.12x"))



class MyTransformer(Transformer):
	# def pnstring(self, items):
	# 	print("found items: ", items)
	# 	return list(items)
	def pn(self, items):
		if len(items) > 0:
			item = items[0]
			# print("-- trans:pn, got item: ", item)
			return item
		return items

	def pnlist(self, items):
		# print("-- trans:pnlist, got items: ", items)
		# return list(map(lambda x: x.value, items))
		return items

	def pnstring(self, items):
		# print("-- trans:pnstring, got items: ", items)
		return list(map(lambda x: x.value, items))

	def allswap(self, items):
		# print("-- trans:ALL_SWAP, got items: ", items)
		return ['x']

	def separator(self, items):
		return []



def processGPNString(gpnStr):
	parsed = parse(gpnStr)

	# print()
	# print("==================")
	# print("For %s I PARSED:\n\n%s" % (gpnStr, parsed.pretty()))
	# print()

	transformed = MyTransformer().transform(parsed)

	print(transformed)

	return transformed


def parseStuff():
	processGPNString("1[29]x5.6")
	processGPNString("x")
	processGPNString("xxxxx")
	processGPNString("xx....x.x..xxx.")
	processGPNString(".")
	processGPNString("......")
	processGPNString(".x")
	processGPNString("x.")
	processGPNString("2x")
	processGPNString("x2")
	processGPNString("x.2")
	processGPNString("2.x")

#1000 trials with timeit:
#    1.1s lalr
#    14.8s earley

# timeit.timeit(parseStuff, number=1000)

parseStuff()
