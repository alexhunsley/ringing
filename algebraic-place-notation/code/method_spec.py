from simpleeval import *

import util

# class TestClass():
#     def __init__(self):
#         print("init for TestClass")

# from gpn import *
# class MethodSpec(object):
class MethodSpec():
    def __init__(self, config_dict):
        self.config_dict = config_dict
        print("MethodSpec given config dict:", config_dict)
        self._pn = None
        self.simpeval = SimpleEval()

    def name(self):
        return self.config_dict['name']

    # todo: cache against the stage
    def pn(self, stage):
        # if self._pn != None:
        #     return self._pn

        parsedLeadend = None

        leadend = self.leadend_for_stage(stage)

        if leadend != None:
            parsedLeadend = util.process_gpn_string(leadend, stage)

        print("Found leadend: ", parsedLeadend)

        use_pn = self.pn_for_stage(stage)
        print("SFSF use_pn for stage: ", use_pn)
        parsed_pn = util.process_gpn_string(use_pn, stage)

        if 'length' in self.config_dict:
            lengthExpression = self.config_dict['length']

            pn_len = simple_eval(lengthExpression, names={'n': stage})
            print("SFSF pn_len=", pn_len)
            print("SFSF parsed pn: ", parsed_pn)

            parsed_pn = parsed_pn * int((pn_len / len(parsed_pn)))

            print("SFSF use_pn to=", parsed_pn)
            print("SFSF mult pn to=", pn_len)
        else:
            # now parse the pn_as_str
            self._pn = parsed_pn

        # todo - mult by length item in that case

        # print("Eval check: ", simple_eval("4+n", names={'n': 3}))
        self._pn = parsed_pn

        if parsedLeadend != None:
            self._pn[-1] = parsedLeadend[0]

        return self._pn

    def pn_for_key(self, key, stage):
        if key not in self.config_dict:
            return None

        parts = self.config_dict[key].split("|")

        if len(parts) == 1:
            print("SFSF pn_for_stage, returning ", parts[0])
            return parts[0]

        print("SFSF pn_for_stage, returning ", parts[stage % 2])

        # even/odd order
        return parts[stage % 2]

    def pn_for_stage(self, stage):
        return self.pn_for_key("base", stage)

    def leadend_for_stage(self, stage):
        return self.pn_for_key("leadend", stage)

    def gen_standard_pn(self, gpnList):
        bells = "1234567890ETABCD"

        print("gpnList = ", gpnList)
        fullResult = []
        for pnItem in gpnList:
            print("pnItem = ", pnItem)

            if pnItem[0] == 'x' or pnItem[0] == 'X':
                fullResult.append('x')
                continue

            result = ""
            for pn in pnItem:
                print("pn = ", pn)
                # convertedOnePart = list(map(lambda x: bells[int(x) - 1], pnItem))
                # convertedOnePart = list(map(lambda x: bells[int(x) - 1], pn))

                convertedOnePart = bells[pn - 1]
                result = result + convertedOnePart

            fullResult.append(result)

        fullResult = '.'.join(fullResult)
        print("MADE fullResult = ", fullResult)
        return fullResult

    def gen_link(self, stage):
        stage_names = ['Unary', 'Diddymus', 'Singles', 'Minimus', 'Doubles', 'Minor', 'Triples', 'Major', 'Caters', 'Royal', 'Cinques', 'Maximus', '13', '14', '15', '16']

        title = "Untitled"
        if 'name' in self.config_dict:
            title = self.config_dict['name']
            title = "%s %s" % (title, stage_names[stage - 1])
            url_title = title.replace(" ", "%20")

        standard_pn_list = self.gen_standard_pn(self.pn(stage))
        print("standard_pn_list = ", standard_pn_list)

        # return "HI"
        return ("http://www.boojum.org.uk/cgi-bin/line.pl?bells=%d&pn=%s&title=%s&action.x=1" \
               % (stage, standard_pn_list, url_title), standard_pn_list, title)
