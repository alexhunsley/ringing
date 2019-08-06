from lark import Lark

l = Lark('''pn: pn pn    
			  | REVERSE_PN pn
	          | HEXDIGIT
	          | "[" NUMBER "]"
	        REVERSE_PN: "~"
	        
	        %import common.HEXDIGIT
	        %import common.NUMBER
         ''', start='pn')

print( l.parse("1458[10]") )
print( l.parse("~12") )
