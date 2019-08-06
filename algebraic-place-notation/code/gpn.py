from lark import Lark

l = Lark('''pnlist: pn* 
                  | REVERSE_PN pn*

            pn: HEXDIGIT
	          | "[" SIGNED_INT "]"

	        REVERSE_PN: "~"
	        
	        %import common.HEXDIGIT
	        %import common.SIGNED_INT
         ''', start='pnlist')

print( l.parse("1458[-10]").pretty() )
print( l.parse("~12").pretty() )
print( l.parse("1234").pretty() )
