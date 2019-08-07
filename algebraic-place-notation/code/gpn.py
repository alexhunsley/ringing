from lark import Lark



# l = Lark('''pnlist: ALL_SWAP
# 	              | pnstring? (("." pnstring | ALL_SWAP pnstring?))* 

l = Lark('''pnlist: pnstring? (("." pnstring | ALL_SWAP pnstring?))* 

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
print( l.parse("x12x34x").pretty() )
# print( l.parse("x").pretty() )
