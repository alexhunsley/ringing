from lark import Lark

l = Lark('''pnlist: pnstring ("." pnstring)* ("." ENDCODE)?

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
         ''', start='pnlist')

# print( l.parse("1458[-10]").pretty() )
# print( l.parse("~12").pretty() )
# print( l.parse("1234").pretty() )

print( l.parse("12.34.x.78[-22].&").pretty() )
