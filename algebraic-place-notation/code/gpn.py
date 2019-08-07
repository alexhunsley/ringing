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
                  | pnstring pnstring

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
r = l.parse("x12x")

print(r)
print()
print(r.pretty())

# print( l.parse("x").pretty() )
