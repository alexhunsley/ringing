from lark import Lark
from lark import Transformer
import sys
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


l = Lark('''pnlist: separator
				  | separator? pnstring (separator pnstring)* separator?

			?separator: ("." | allswap)+

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
         ''', start='pnlist', ambiguity='resolve')

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
			print("-- trans:pn, got item: ", item)
			return item
		return items

	def pnlist(self, items):
		print("-- trans:pnlist, got items: ", items)
		# return list(map(lambda x: x.value, items))
		return items

	def pnstring(self, items):
		print("-- trans:pnstring, got items: ", items)
		return list(map(lambda x: x.value, items))

	def allswap(self, items):
		print("-- trans:ALL_SWAP, got items: ", items)
		return ['x']

	def separator(self, items):
		return []

# the 5 and 6 get split:
# r = parse("x1.3x56.78x")
r = parse("1[29]x5.6")

print(r)
print(r.pretty())

transformed = MyTransformer().transform(r)
print(transformed)


# rr = processPN("1[29]x5.6")

def parsedDataToPNList(parsedData):
	transformed = MyTransformer().transform(parsedData)
	
	# return transformed
	transformedRemoveEmptyItems = [x for x in transformed if x != []]
	return transformedRemoveEmptyItems

print(parsedDataToPNList(r))

# print("==============")

# r = parse("2x")
# print(r)
# print(r.pretty())

# print("==============")

# r = parse("x3x")
# print(r)
# print(r.pretty())

# print("==============")




# r = parse("x.1")
# print(r)
# print(r.pretty())

# print("==============")

# r = parse("2.x")
# print(r)
# print(r.pretty())

# print("==============")

# r = parse("x.3.x")
# print(r)
# print(r.pretty())

# print("==============")



# # works:
# r = parse("x.5x")
# print(r)
# print(r.pretty())


# r = parse("x5.x")

# # r = parse("x1.2.3x5.x")
# print(r)
# print(r.pretty())


# r = parse("x.5x")

# # r = parse("x1.2.3x5.x")
# print(r)
# print(r.pretty())


# r = parse("x.12.56.x5x.78x")

# # r = parse("x1.2.3x5.x")
# print(r)
# print(r.pretty())


# r = parse("1.2.3.4.5.6.7.8.9")

# # r = parse("x1.2.3x5.x")
# print(r)
# print(r.pretty())

# r = parse("x12.x[99]")

# print(r)
# print()
# print(r.pretty())

# print( l.parse("5").pretty() )

# print( l.parse("x").pretty() )

# r = l.parse(".x.")
# print(r)
# print()
# print(r.pretty())

# r = l.parse("x.x")
# print(r)
# print()
# print(r.pretty())

# print( l.parse(".x").pretty() )

# print( l.parse("x.").pretty() )

# print( l.parse("x.5").pretty() )

# print( l.parse("5.x").pretty() )

# print( l.parse("[1]").pretty() )
# print( l.parse(".[2]").pretty() )
# print( l.parse("[3].").pretty() )


# r = parse("x12.34x56.~78x.56.x.324.x[1].x")

# print(r)
# print(r.pretty())

