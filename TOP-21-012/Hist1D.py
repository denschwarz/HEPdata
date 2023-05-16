import ROOT
from distribution import distribution

class Hist1D:
    def __init__(self, name):
        self.__name = name
        self.__bins = []
        self.__distributions = []
        self.__Nbins = None
        self.__axisName = None
        self.__axisUnit = None


    def addAxis(self, name, unit, thresholds):
        if self.__Nbins is None:
            self.__Nbins = len(thresholds)-1
        else:
            if self.__Nbins != len(thresholds)-1:
                raise Exception("addAxis: number of thresholds does not fit number of bins")
        for i in range(len(thresholds)):
            if i == len(thresholds)-1:
                break
            self.__bins.append( (thresholds[i], thresholds[i+1]) )
        self.__axisName = name
        self.__axisUnit = unit

    def addDistribution(self, name, unit, values):
        if self.__Nbins != len(values):
            raise Exception("addDistribution: number of thresholds does not fit number of bins")
        dist = distribution(name, unit)
        dist.addValues(values)
        self.__distributions.append(dist)

    def addUncert(self, distname, uncertname, values):
        if self.__Nbins != len(values):
            raise Exception("addUncert: number of thresholds does not fit number of bins")
        found = False
        for dist in self.__distributions:
            if distname in dist.name:
                found = True
        if not found:
            raise Exception("addUncert: cannot add uncertainty, distribution %s does not exist"%(distname))
        for dist in self.__distributions:
            dist.addUncert(uncertname, values)

    def makeFile(self):
        with open("output/"+self.__name+".yaml", "w") as f:
            f.write('dependent_variables:\n')
            for dist in self.__distributions:
                f.write('- header:\n')
                f.write('    name: '+dist.name+'\n')
                f.write('    units: '+dist.unit+'\n')
                f.write('  values:\n')
                for i in range(self.__Nbins):
                    if len(dist.uncerts) > 0:
                        f.write('  - errors:\n')
                        for (uncertName, errors) in dist.uncerts:
                            f.write("    - label: "+uncertName+"\n")
                            f.write("      symerror: "+str(errors[i])+"\n")
                        f.write('    value: '+str(dist.values[i])+'\n')
                    else:
                        f.write('  - value: '+str(dist.values[i])+'\n')
            f.write('independent_variables:\n')
            f.write('- header:\n')
            f.write('    name: '+self.__axisName+'\n')
            f.write('    units: '+self.__axisUnit+'\n')
            f.write('  values:\n')
            for (low, high) in self.__bins:
                f.write('  - high: '+str(high)+'\n')
                f.write('    low: '+str(low)+'\n')
