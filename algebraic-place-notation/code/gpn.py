from lark import Lark
from lark import Transformer
import sys
import timeit

#
# To avoid re-parsing the basic spec info for each stage generated,
# there is a spec parsing stage that reads the spec including PN but doesn't
# do any PN parsing yet.  We then generate (and cache) PN derived for different
# stages as and when it is required, given desired stage.
#
# Using a custom parser for the spec config is OTT. Should use a Configuration file parser or similar.
#

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
l = Lark('''odd_even_pn: pnlist
	                   | pnlist "|" pnlist

			pnlist: _separator
				  | _separator? pnstring (_separator pnstring)* _separator?

			_separator: ("." | allswap)+

 			pnstring: pn+
                    | REVERSE_PN pn+

            pn: HEXDIGIT | TENOR_PN
	          | "[" SIGNED_INT "]"

	        TENOR_PN: "n"

			allswap: ALL_SWAP

			DBLQUOTE: /"/

	        REVERSE_PN: "~"
	        ALL_SWAP: "x" | "X"
			ENDCODE: "&"

			%import common.HEXDIGIT
	        %import common.SIGNED_INT
         ''', start='odd_even_pn', parser='lalr')




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

# Convert any negative place item to a positive place
# given the stage.
# e.g. '-2' on stage 8 would become 7, and '-8' would be 1.
# Doesn't change or do anything regarding '~'.
def reversePNItemForNegativePlaces(stage, item):
	if item == '~':
		return item

	p = int(item)

	if p < 0:
		return stage + 1 + p

	return p


class MyTransformer(Transformer):
	def __init__(self, stage):
		self.stage = stage

	# def pnstring(self, items):
	# 	print("found items: ", items)
	# 	return list(items)
	def pn(self, items):
		print("processing pn, got ", items)
		if len(items) > 0:
			item = items[0]
			# print("-- trans:pn, got item: ", item)

			# if item == 'n':
			# 	item = "[%d]" % self.stage

			return item

		return items

	def pnlist(self, items):
		# print("-- trans:pnlist, got items: ", items)
		# return list(map(lambda x: x.value, items))
		return items

	def pnstring(self, items):
		print("now got: ", items)

		# pnList = list(map(lambda x: self.stage if x == 'n' else x, items))

		# print("-- trans:pnstring, got items: ", items)
		pnList = list(map(lambda x: x.value, items))

		print("made pnlist to ", pnList)

		pnList = list(map(lambda x: str(self.stage) if x == 'n' else x, items))

		print("made pnlist2 to ", pnList)

		# deal with any negative items that were expressed as e.g. [-x]
		pnList = [reversePNItemForNegativePlaces(self.stage, p) for p in pnList]

		# pnList = list(map(reversePNItemForNegativePlaces, pnList))

		# reverse entire list positions if prepending with '~' (means 'mirror')
		if pnList[0] == '~':
			pnList = pnList[1:]
			pnList = list(map(lambda x: self.stage + 1 - int(x), pnList))
		else:
			pnList = list(map(lambda x: int(x), pnList))

		pnList.sort()
		return pnList

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

	transformed = MyTransformer(stage=8).transform(parsed)

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
	processGPNString("x.[-1][-2]")
	processGPNString("4[-1].x")

#running 1000 trials with timeit:
#    1.1s lalr
#    14.8s earley

# timeit.timeit(parseStuff, number=1000)

# parseStuff()
t = processGPNString("5x")
print()
print(t.pretty())

t = processGPNString("1n.3[-2]|x")
print()
print(t.pretty())

#--------------------------------------------

spec = Lark('''file: "{" defline* "}"
                   | _pn

			   defline: _propname "=" _value
			   		  | _pnpropname "=" pnvalue 

  		  // property names for stuff that's not place-notation
			   _propname: name
			   	       | stage
			   	       | length
			   	       | id

			   name: "name"
			   stage: "stage"
			   length: "length"
			   id: "id"

  		  // property names for stuff that's is place-notation
			   _pnpropname: notation
			   			  | base

			   notation: "notation"
			   base: "base"

			   _value: strvalue | numvalue

			   // escaped pn
			   pnvalue: "\\"" _pn "\\""

			   // unescaped pn
			   _pn: /~?[xXn.\-\[\]|0-9A-Z]+/

			   strvalue: "\\"" STRVALUE "\\""

// find something better for this
			   STRVALUE: /[*()\[\].,\- ?!:;0-9a-zA-Z]+/

			   numvalue: INT

			   %import common.WS
			   %ignore WS

			   %import common.INT
            ''', start='file', parser='lalr')


class SpecTransformer(Transformer):
	def __init__(self):
		self.stringProps = {}
		self.intProps = {}
		self.pnProps = {}

	# def pnpropname(self, items):
	# 	return items[0]

	# def pnstring(self, items):
	# 	print("found items: ", items)
	# 	return list(items)
	# def pnvalue(self, items):
	# 	print("processing pn, got ", items)
	# 	if len(items) > 0:
	# 		item = items[0]
	# 		# print("-- trans:pn, got item: ", item)

	# 		# if item == 'n':
	# 		# 	item = "[%d]" % self.stage

	# 		return item

	# 	return items

	def strvalue(self, items):
		return items[0].value

	def numvalue(self, items):
		return int(items[0].value)

	def defline(self, items):
		print("DEFLINE: items = ", items)
		if isinstance(items[1], str):
			print("found a string called %s, val = %s" % (items[0], items[1]))
			# remove the quotation marks at either end while we're at it
#			print("Before removal: ", items[1])
#			print("after removal: ", items[1][1:-1])
			# self.stringProps[items[0]] = items[1][1:-1]
		else:
			print("found a number called %s, val = %s " % (items[0], items[1]))
			self.intProps[items[0]] = items[1]

		# if items[0] == "stage":
		# elif items[0] == "notation":
		# 	print("found notation, val = ", items[1])
		# elif items[0] == "base":
		# 	print("found base, val = ", items[1])

		return items

	def notation(self, items):
		return "notation"

	def base(self, items):
		return "base"

	def name(self, items):
		return "name"

	def pnvalue(self, items):
		return items[0].value

	def stage(self, items):
		# print("called stage, items =-", items)
		return "stage"

	def length(self, items):
		# print("called stage, items =-", items)
		return "length"

	def id(self, items):
		# print("called stage, items =-", items)
		return "id"

	def file(self, items):
		# print("called stage, items =-", items)
		return items

	# def strvalue(self, items):
	# 	if isinstance(items[0], str):
	# 		print("Got a string: ", items)
	# 		return items[0].value

	# 	print("Got a number: ", items)
	# 	return items[0].value

# test1 = '''{ 
# 	notation="~23x[5]."
# 	base="x.14."
#  	name=   "alex. hi! ? ( ) [asdsa]"
# 	stage  =62 
# }'''

test1 = '''{ 
	id="plainhunt"
    base="n.1|x.1n"
    length="2*n"
}'''



parsedSpec = spec.parse(test1) 
print(parsedSpec)
print(parsedSpec.pretty())

specTx = SpecTransformer()
specTransformed = specTx.transform(parsedSpec)

print("spec transformed = ", specTransformed)

print("spec TX dicts: strings = %s, ints = %s" % (specTx.stringProps, specTx.intProps))
# # test direct use of PN
# test2 = "x.14.x.14.x.14.x.14"

# rr=spec.parse(test2) 
# print(rr)
# print(rr.pretty())



# print(test2)


