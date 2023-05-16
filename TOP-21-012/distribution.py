class distribution:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        self.values = []
        self.uncerts = []

    def addValues(self, values):
        self.values = values

    def addUncert(self, name, errors):
        self.uncerts.append( (name, errors) )
