from lark import Lark

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


# l = Lark('''pnlist: ALL_SWAP
# 	              | pnstring? (("." pnstring | ALL_SWAP pnstring?))* 

l = Lark('''pnlist: pnstring ("." pnstring)*

 			pnstring: ALL_SWAP
  				    | pn*
                    | REVERSE_PN pn*

            pn: HEXDIGIT
	          | "[" SIGNED_INT "]"
              
	        REVERSE_PN: "~"
	        ALL_SWAP: "x" | "X"
			ENDCODE: "&"

	        %import common.HEXDIGIT
	        %import common.SIGNED_INT
         ''', start='pnlist', ambiguity='explicit')

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
	canonicalPnStr = canonicalisePnStr(pnStr)
	print(l.parse(canonicalPnStr).pretty())


print(canonicalisePnStr("12x"))
print(canonicalisePnStr("x12"))
print(canonicalisePnStr("12x23.43"))
print(canonicalisePnStr("34x.12x"))

r = parse("x12.x")
# r = parse("x12.x[99]")

# print(r)
# print()
# print(r.pretty())

# print( l.parse("x").pretty() )
