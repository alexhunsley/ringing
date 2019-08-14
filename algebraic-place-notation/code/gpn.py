from lark import Lark
from lark import Transformer

import simpleeval
import util

import sys
import timeit
import method_spec
#
# To avoid re-parsing the basic spec info for each stage generated,
# there is a spec parsing stage that reads the spec including PN but doesn't
# do any PN parsing yet.  We then generate (and cache) PN derived for different
# stages as and when it is required, given desired stage.
#
# Using a custom parser for the spec config is OTT. Should use a Configuration file parser or similar.
#

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

# To specify a range of places from a to b inclusive, we can write:
#
# a_b.  So e.g. 4_[-3].


# def parse_stuff():
# 	util.process_gpn_string("1[29]x5.6")
# 	util.process_gpn_string("x")
# 	util.process_gpn_string("xxxxx")
# 	util.process_gpn_string("xx....x.x..xxx.")
# 	util.process_gpn_string(".")
# 	util.process_gpn_string("......")
# 	util.process_gpn_string(".x")
# 	util.process_gpn_string("x.")
# 	util.process_gpn_string("2x")
# 	util.process_gpn_string("x2")
# 	util.process_gpn_string("x.[-1][-2]")
# 	util.process_gpn_string("4[-1].x")

#running 1000 trials with timeit:
#    1.1s lalr
#    14.8s earley

# timeit.timeit(parseStuff, number=1000)

# parseStuff()
# t = util.process_gpn_string("5x")
# print()
# print(t.pretty())
#


# t = util.process_gpn_string("1n.3[-2]|x")
# print()
# print(t.pretty())

#--------------------------------------------

spec = Lark('''file: "{" defline* "}"
                   | _pn

			   defline: _propname "=" _value
			   		  | _pnpropname "=" pnvalue 

  		  // property names for stuff that's not place-notation
			   _propname: name
			   	       | stage
			   	       | length
			   	       | id

			   name: "name"
			   stage: "stage"
			   length: "length"
			   id: "id"

  		  // property names for stuff that's is place-notation
			   _pnpropname: notation
			   			  | base
			   			  | leadend

			   notation: "notation"
			   base: "base"
			   leadend: "leadend"

			   _value: strvalue | numvalue

			   // escaped pn
			   pnvalue: "\\"" _pn "\\""

			   // unescaped pn
			   _pn: /~?[xXn._\-\[\]|0-9A-Z]+/

			   strvalue: "\\"" STRVALUE "\\""

// find something better for this
			   STRVALUE: /[*()\[\].,\- ?!:;0-9a-zA-Z]+/

			   numvalue: INT

			   %import common.WS
			   %ignore WS

			   %import common.INT
            ''', start='file', parser='lalr')



# print("res = ", util.insert_ranged_places(['1', '_', '3', '4', '5', '_', '9']))
# sys.exit(1)


class SpecTransformer(Transformer):
	def __init__(self):
		self.stringProps = {}
		self.intProps = {}
		self.pnProps = {}

	# def pnpropname(self, items):
	# 	return items[0]

	# def pnstring(self, items):
	# 	print("found items: ", items)
	# 	return list(items)
	# def pnvalue(self, items):
	# 	print("processing pn, got ", items)
	# 	if len(items) > 0:
	# 		item = items[0]
	# 		# print("-- trans:pn, got item: ", item)

	# 		# if item == 'n':
	# 		# 	item = "[%d]" % self.stage

	# 		return item

	# 	return items

	def strvalue(self, items):
		return items[0].value

	def numvalue(self, items):
		return int(items[0].value)

	def defline(self, items):
		print("DEFLINE: items = ", items)
		if isinstance(items[1], str):
			print("found a string called %s, val = %s" % (items[0], items[1]))
			# remove the quotation marks at either end while we're at it
#			print("Before removal: ", items[1])
#			print("after removal: ", items[1][1:-1])
			# self.stringProps[items[0]] = items[1][1:-1]
		else:
			print("found a number called %s, val = %s " % (items[0], items[1]))
			self.intProps[items[0]] = items[1]

		# if items[0] == "stage":
		# elif items[0] == "notation":
		# 	print("found notation, val = ", items[1])
		# elif items[0] == "base":
		# 	print("found base, val = ", items[1])

		return items

	def notation(self, items):
		return "notation"

	def base(self, items):
		return "base"

	def name(self, items):
		return "name"

	def pnvalue(self, items):
		return items[0].value

	def stage(self, items):
		# print("called stage, items =-", items)
		return "stage"

	def length(self, items):
		# print("called stage, items =-", items)
		return "length"

	def leadend(self, items):
		# print("called stage, items =-", items)
		return "leadend"

	def id(self, items):
		# print("called stage, items =-", items)
		return "id"

	def file(self, items):
		# print("called stage, items =-", items)
		return items

	# def strvalue(self, items):
	# 	if isinstance(items[0], str):
	# 		print("Got a string: ", items)
	# 		return items[0].value

	# 	print("Got a number: ", items)
	# 	return items[0].value

# test1 = '''{
# 	name="Evil Erin"
# 	id="plainhunt"
#     base="3.1.34.x.34.1n|3.1.34n.n.34n.1"
# }'''

# test1 = '''{
# 	name="Evil Erin with Places"
# 	id="evilerinplaces"
#     base="3.1.3_[-3].x.3_[-3].1n|3.1.3_[-2]n.n.3_[-2]n.1"
# }'''

test1 = '''{
	name="Almost Double Little Bob TR to 6"
	id="almostdoublelittlebobtrto6"
    base="x.1n.x.1n.x.56.x.1n.x.1n.x.12"
}'''


# print(method_spec.TestClass())

parsedSpec = spec.parse(test1) 
print(parsedSpec)
print(parsedSpec.pretty())

specTx = SpecTransformer()
specTransformed = specTx.transform(parsedSpec)

specDict = dict(specTransformed)

ms = method_spec.MethodSpec(specDict)

print("spec transformed = ", specTransformed)
print("spec dict = ", specDict)

print("spec TX dicts: strings = %s, ints = %s" % (specTx.stringProps, specTx.intProps))

for s in range(6, 10, 2):
	print("--------------- made PN from methodSpec: ", ms.pn(s))
	print("link: ", ms.gen_link(s))

# # test direct use of PN
# test2 = "x.14.x.14.x.14.x.14"

# rr=spec.parse(test2) 
# print(rr)
# print(rr.pretty())



# print(test2)


