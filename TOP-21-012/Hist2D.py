import ROOT
from distribution2D import distribution2D

class Hist2D:
    def __init__(self, name):
        self.__name = name
        self.__binsX = []
        self.__binsY = []
        self.__distributions = []
        self.__NbinsX = None
        self.__NbinsY = None
        self.__axisNameX = None
        self.__axisUnitX = None
        self.__axisNameY = None
        self.__axisUnitY = None

    def addAxisX(self, name, unit, thresholds):
        if self.__NbinsX is None:
            self.__NbinsX = len(thresholds)-1
        else:
            if self.__NbinsX != len(thresholds)-1:
                raise Exception("addAxis: number of thresholds does not fit number of bins")
        for i in range(len(thresholds)):
            if i == len(thresholds)-1:
                break
            self.__binsX.append( (thresholds[i], thresholds[i+1]) )
        self.__axisNameX = name
        self.__axisUnitX = unit

    def addAxisY(self, name, unit, thresholds):
        if self.__NbinsY is None:
            self.__NbinsY = len(thresholds)-1
        else:
            if self.__NbinsY != len(thresholds)-1:
                raise Exception("addAxis: number of thresholds does not fit number of bins")
        for i in range(len(thresholds)):
            if i == len(thresholds)-1:
                break
            self.__binsY.append( (thresholds[i], thresholds[i+1]) )
        self.__axisNameY = name
        self.__axisUnitY = unit

    def addDistribution(self, name, unit, values):
        if self.__NbinsX*self.__NbinsY != len(values):
            raise Exception("addDistribution: number of thresholds does not fit number of bins")
        dist = distribution2D(name, unit)
        dist.addValues(values)
        self.__distributions.append(dist)


    def makeFile(self):
        with open("output/"+self.__name+".yaml", "w") as f:
            f.write('dependent_variables:\n')
            for dist in self.__distributions:
                f.write('- header:\n')
                f.write('    name: '+dist.name+'\n')
                if dist.unit is not None:
                    f.write('    units: '+dist.unit+'\n')
                f.write('  values:\n')
                for i in range(self.__NbinsX*self.__NbinsY):
                    f.write('  - value: '+str(dist.values[i])+'\n')
            f.write('independent_variables:\n')
            f.write('- header:\n')
            f.write('    name: '+self.__axisNameX+'\n')
            f.write('    units: '+self.__axisUnitX+'\n')
            f.write('  values:\n')
            for (low, high) in self.__binsX:
                for i in range(self.__NbinsY):
                    f.write('  - high: '+str(high)+'\n')
                    f.write('    low: '+str(low)+'\n')
            f.write('- header:\n')
            f.write('    name: '+self.__axisNameY+'\n')
            f.write('    units: '+self.__axisUnitY+'\n')
            f.write('  values:\n')
            for i in range(self.__NbinsX):
                for (low, high) in self.__binsY:
                        f.write('  - high: '+str(high)+'\n')
                        f.write('    low: '+str(low)+'\n')
