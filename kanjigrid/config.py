import json

class Config:

    def __init__(self, fn, defaults={}):
        self.fn = fn
        self.config = {}
        self.defaults = defaults


    def __getitem__(self,key):
        return self.config[key]


    def __setitem__(self,key,value):
        self.config[key] = value


    def reset(self):
        self.config.update(self.defaults)


    def save(self):
        with open(self.fn,'w') as f:
            f.write(json.dumps(self.config))


    def load(self):
        self.config = self.defaults.copy()

        try:
            with open(self.fn,'r') as f:
                self.config.update(json.load(f))
        except Exception as e:
            pass
