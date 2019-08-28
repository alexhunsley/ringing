from lark import Lark
from lark import Transformer
from lark.lexer import Token

def rotateRight(l, n):
	n = n % len(l)
	return l[-n:] + l[:-n]

def rotateLeft(l, n):
	n = n % len(l)
	return l[n:] + l[:n]

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
              | TENOR_PN
	          | "[" SIGNED_INT "]"
	          | UNDERSCORE
			  | UNDERSCORE PLACE_PATTERN_CHAR+ UNDERSCORE
			  
	        TENOR_PN: "n"

			PLACE_PATTERN_CHAR: ","
							  | "|"
							  
			allswap: ALL_SWAP
	
			UNDERSCORE: "_"
			
			DBLQUOTE: /"/

	        REVERSE_PN: "~"
	        ALL_SWAP: "x" | "X"
			ENDCODE: "&"

			%import common.HEXDIGIT
	        %import common.SIGNED_INT
         ''', start='pnlist', parser='lalr')


# print( l.parse("1458[-10]").pretty() )
# print( l.parse("~12").pretty() )
# print( l.parse("1234").pretty() )
#
# print( l.parse("12.34.x.78[-22]").pretty() )
# print( l.parse("12x34").pretty() )
#
# r = l.parse("x12x34.56")
#
# ensure each item in the PN is separated by '.', including 'X' items.
# e.g. 12x34 -> 12.x.34
def canonicalise_pn_str(str):
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


def reverse_pn_item_for_negative_places(stage, item):
	print("REV ITEM: ", item)

	if item[0] in ['~', '_']:
		return item

	p = int(item)

	if p < 0:
		return stage + 1 + p

	return p


# pn is a list like ['1', '4', '_', '7', 12].
# we replace the '_' with all places between 4 and 7.
def insert_ranged_places(pnList):
	result = []

	print("insert_ranged_places: ", pnList)

	idx = 0

	for placeIdx in range(0, len(pnList)):
		print('placeIdx, idx = ', placeIdx, idx)

		if idx == len(pnList):
			break

		if isinstance(pnList[idx], int):
			result.append(pnList[idx])
		else:
			pattern = '|'

			# is a string for ranged: either '_' or '_pattern_'
			if pnList[idx] == '_':
				# is simple range
				pass
			else:
				# is patterned range
				pattern = pnList[idx][1:-1]
				pass

			startPlace = int(pnList[idx - 1])
			endPlace = int(pnList[idx + 1])

			print("make range, start, end = ", startPlace, endPlace)
			placesAsListOfInts = range(startPlace, endPlace + 1)

			placesAsListOfIntsFilt = []
			ix = 0
			pattLen = len(pattern)
			for p in placesAsListOfInts:
				if pattern[ix % pattLen] == '|':
					placesAsListOfIntsFilt.append(p)
				ix += 1

			placesAsListOfStrs = list(map(lambda x: str(x), placesAsListOfIntsFilt))

			# chop off start item to avoid repeat
			result = result[:-1]

			result += placesAsListOfStrs

			# got to skip the '_' and the end item
			idx += 1

		idx += 1


	return result

# pnItem can either be a direct Token,
# or a list of tokens
def pnItemToValue(pnItem):
	if isinstance(pnItem, Token):
		return pnItem.value

	list_of_values = list(map(lambda x: x.value, pnItem))

	return ''.join(list_of_values)

class MyTransformer(Transformer):
	def __init__(self, stage):
		self.stage = stage

	# def pnstring(self, items):
	# 	print("found items: ", items)
	# 	return list(items)
	def pn(self, items):
		print("processing pn, got ", items)
		# todo this is where we make _||.._ into just _
		if len(items) > 0  and items[0] != '_':
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

		# todo only call value if it's not a list; if a list, process the _pattern_ thing into e.g. _||.._
		# pnList = list(map(lambda x: x.value, items))
		pnList = list(map(pnItemToValue, items))

		print("made pnlist to ", pnList)

		pnList = list(map(lambda x: str(self.stage) if x == 'n' else x, pnList))
		#
		# print("made pnlist2 to ", pnList)

		# deal with any negative items that were expressed as e.g. [-x]
		pnList = [reverse_pn_item_for_negative_places(self.stage, p) for p in pnList]

		# pnList = list(map(reversePNItemForNegativePlaces, pnList))

		# deal with place range, e.g. 4_7 means 4567
		# note the list contains strings, not ints, at this point
		pnList = insert_ranged_places(pnList)

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

	def odd_even_pn(self, items):
		return list(items)

	def underscore(self, items):
		return ['_']

def process_gpn_string(gpnStr, stage):
	parsed = parse(gpnStr)

	print()
	print("==================")
	print("For %s I PARSED:\n\n%s" % (gpnStr, parsed.pretty()))
	print()

	transformed = MyTransformer(stage=stage).transform(parsed)

	print("Transformed == ", transformed)

	return transformed
