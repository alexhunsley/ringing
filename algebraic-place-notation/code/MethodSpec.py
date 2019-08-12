class MethodSpec():
    def __init__(self, config_dict):
        self.config_dict = config_dict
        self._pn = None

    def pn(self):
        if self._pn != None:
            return self._pn

        if 'base' in self.config_dict:
            if 'length' not in self.config_dict:
                self._pn = self.config_dict['base']

        # todo - mult by length item in that case

        return self.config_dict['base']
