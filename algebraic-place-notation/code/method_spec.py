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

    # todo: cache against the stage
    def pn(self, stage):
        # if self._pn != None:
        #     return self._pn

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
        
        return self._pn

    def pn_for_stage(self, stage):
        parts = self.config_dict['base'].split("|")

        if len(parts) == 1:
            print("SFSF pn_for_stage, returning ", parts[0])
            return parts[0]

        print("SFSF pn_for_stage, returning ", parts[stage % 2])

        # even/odd order
        return parts[stage % 2]
