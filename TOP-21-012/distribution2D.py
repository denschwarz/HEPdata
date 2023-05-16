class distribution2D:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        self.values = []

    def addValues(self, values):
        self.values = values
