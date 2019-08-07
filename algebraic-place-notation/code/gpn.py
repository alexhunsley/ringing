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

# "x5.x"

# I seem to be able to remove the * from this line without ill effect:
#                     | ALL_SWAP pnlist*

l = Lark('''eitherlist: dotlist
	                  | xlist
	                  | pnstring

			   dotlist: eitherlist ("." eitherlist)*

			   xlist: ALL_SWAP? eitherlist (ALL_SWAP eitherlist)?

 			pnstring: ALL_SWAP
  				    | pn+
                    | REVERSE_PN pn*

            pn: HEXDIGIT
	          | "[" SIGNED_INT "]"
              
	        REVERSE_PN: "~"
	        ALL_SWAP: "x" | "X"
			ENDCODE: "&"

	        %import common.HEXDIGIT
	        %import common.SIGNED_INT
         ''', start='eitherlist', ambiguity='resolve')

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


print(canonicalisePnStr("12x"))
print(canonicalisePnStr("x12"))
print(canonicalisePnStr("12x23.43"))
print(canonicalisePnStr("34x.12x"))

# NOTE: we're not handling [x] items currently.
# r = parse("x12.34x56.78x.56.x.324.x.x")

# the 5 and 6 get split:
# r = parse("x1.3x56.78")

# r = parse("x1.3x5")
r = parse("3x5")

print(r)
print(r.pretty())




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



# #works:
# # r = parse("x.5x")

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

# print( l.parse("x").pretty() )
