from lark import Lark
from lark import Transformer


# We prepend separator with _, which means it is always removed, but children remain in-place.
# this avoids need to later remove empty items from the transformed list.
# Anther (not as good) strategy is to throw the Discard exception in the transformer, which
# would remove that node 
l = Lark('''pnlist: _separator
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
		pnList = [reverse_pn_item_for_negative_places(self.stage, p) for p in pnList]

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

	def odd_even_pn(self, items):
		return list(items)

def process_gpn_string(gpnStr, stage):
	parsed = parse(gpnStr)

	print()
	print("==================")
	print("For %s I PARSED:\n\n%s" % (gpnStr, parsed.pretty()))
	print()

	transformed = MyTransformer(stage=stage).transform(parsed)

	print("Transformed == ", transformed)

	return transformed
