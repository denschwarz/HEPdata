import ROOT
from Hist1D import Hist1D
from Hist2D import Hist2D
from submission import submission
from math import sqrt

infileName = "input/HEPdataInput_TOP-21-012.root"

def getObjFromFile(fname, hname):
    gDir = ROOT.gDirectory.GetName()
    f = ROOT.TFile(fname)
    assert not f.IsZombie()
    f.cd()
    htmp = f.Get(hname)
    if not htmp:  return htmp
    ROOT.gDirectory.cd('PyROOT:/')
    res = htmp.Clone()
    f.Close()
    ROOT.gDirectory.cd(gDir+':/')
    return res

def readMatrix(matname):
    mat = getObjFromFile(infileName, matname)
    Nbins_x = mat.GetXaxis().GetNbins()
    Nbins_y = mat.GetYaxis().GetNbins()
    binthresholds_x = []
    binthresholds_y = []
    values = []
    # get values
    for i in range(Nbins_x):
        bin_x = i+1
        for j in range(Nbins_y):
            bin_y = j+1
            values.append( mat.GetBinContent(bin_x, bin_y) )
    # get binning
    for i in range(Nbins_x):
        bin_x = i+1
        binthresholds_x.append(mat.GetXaxis().GetBinLowEdge(bin_x))
    binthresholds_x.append(mat.GetXaxis().GetBinUpEdge(Nbins_x))
    for j in range(Nbins_y):
        bin_y = j+1
        binthresholds_y.append(mat.GetXaxis().GetBinLowEdge(bin_y))
    binthresholds_y.append(mat.GetYaxis().GetBinUpEdge(Nbins_y))
    return values, binthresholds_x, binthresholds_y

def readHistogram(hname):
    hist = getObjFromFile(infileName, hname)
    Nbins = hist.GetSize()-2
    values = []
    binthresholds = []
    for i in range(Nbins):
        bin = i+1
        values.append(hist.GetBinContent(bin))
        binthresholds.append(hist.GetXaxis().GetBinLowEdge(bin))
    binthresholds.append(hist.GetXaxis().GetBinUpEdge(Nbins))
    return values, binthresholds

def getErrorsFromMatrix(matname):
    mat = getObjFromFile(infileName, matname)
    Nbins = mat.GetXaxis().GetNbins()
    errors = []
    for i in range(Nbins):
        bin = i+1
        errors.append(sqrt(mat.GetBinContent(bin, bin)))
    return errors


for name in ["Unfold_XS_HIST", "Unfold_norm_HIST"]:
    print(name)
    distname = "xsec_diff_mjet"
    if "_norm_" in name:
        distname = "xsec_diff_norm_mjet"
    measurement = Hist1D(distname)
    values, thresholds = readHistogram(name)
    print(values, thresholds)
    measurement.addAxis("$m_\mathrm{jet}$", "GeV", thresholds)
    title, unit = "$\\frac{d\sigma}{dm_\mathrm{jet}}$", "$\\frac{\mathrm{fb}}{\mathrm{GeV}}$"
    if "_norm_" in name:
        title, unit = "$\\frac{1}{\sigma} \\frac{d\sigma}{dm_\mathrm{jet}}$", "$\\frac{1}{\mathrm{GeV}}$"
    measurement.addDistribution(title, unit, values)
    for uncert in ["stat", "exp", "model"]:
        covname = "Cov_XS_"
        if "_norm_" in name:
            covname = "Cov_norm_"
        errors = getErrorsFromMatrix(covname+uncert)
        measurement.addUncert(title, uncert, errors)
    measurement.makeFile()

fullnames = {
    "jer": "Jet energy resolution",
    "jms": "Jet mass scale",
    "jmsflavor": "Jet mass scale b flavour",
    "jec": "Jet energy scale",
    "pile-up": "Pileup",
    "MCstat": "MC stat",
    "cor": "XCone jet correction",
    "mass": "Choice of $m_\mathrm{t}$",
    "hdamp": "$h_\mathrm{damp}$",
    "CR": "Colour reconnection",
    "UEtune": "UE tune",
    "scale": "$\mu_\mathrm{F}$, $\mu_\mathrm{R}$ scales",
    "ISR": "ISR",
    "FSR": "FSR",
}

u_exp = Hist1D("uncertainties_exp")
u_norm_exp = Hist1D("uncertainties_norm_exp")
expSources = ["jer", "jms", "jmsflavor", "jec", "pile-up", "MCstat", "cor"]
first = True
for source in expSources:
    values, thresholds = readHistogram("DELTA_"+source)
    values_norm, thresholds_norm = readHistogram("DELTA_NORM_"+source)
    if first:
        first = False
        u_exp.addAxis("$m_\mathrm{jet}$", "GeV", thresholds)
        u_exp.addDistribution(fullnames[source], "'%'", values)
        u_norm_exp.addAxis("$m_\mathrm{jet}$", "GeV", thresholds_norm)
        u_norm_exp.addDistribution(fullnames[source], "'%'", values_norm)
    else:
        u_exp.addDistribution(fullnames[source], "'%'", values)
        u_norm_exp.addDistribution(fullnames[source], "'%'", values_norm)

u_exp.makeFile()
u_norm_exp.makeFile()


u_model = Hist1D("uncertainties_model")
u_norm_model = Hist1D("uncertainties_norm_model")
modelSources = ["mass", "hdamp", "CR", "UEtune", "scale", "ISR", "FSR"]
first = True
for source in modelSources:
    values, thresholds = readHistogram("DELTA_"+source)
    values_norm, thresholds_norm = readHistogram("DELTA_NORM_"+source)
    if first:
        first = False
        u_model.addAxis("$m_\mathrm{jet}$", "GeV", thresholds)
        u_model.addDistribution(fullnames[source], "'%'", values)
        u_norm_model.addAxis("$m_\mathrm{jet}$", "GeV", thresholds_norm)
        u_norm_model.addDistribution(fullnames[source], "'%'", values_norm)
    else:
        u_model.addDistribution(fullnames[source], "'%'", values)
        u_norm_model.addDistribution(fullnames[source], "'%'", values_norm)

u_model.makeFile()
u_norm_model.makeFile()

names2D = {
    "Cor_norm_tot"   : ("correlations_xsec_diff_norm_mjet", "Normalized correlations"),
    "Cor_XS_tot"     : ("correlations_xsec_diff_mjet", "Correlations"),
    "Cov_norm_exp"   : ("covariance_exp_xsec_diff_norm_mjet", "Normalized exp covariance"),
    "Cov_XS_exp"     : ("covariance_exp_xsec_diff_mjet", "Exp covariance"),
    "Cov_norm_model" : ("covariance_model_xsec_diff_norm_mjet", "Normalized model covariance"),
    "Cov_XS_model"   : ("covariance_model_xsec_diff_mjet", "Model covariance"),
    "Cov_norm_stat"  : ("covariance_stat_xsec_diff_norm_mjet", "Normalized stat covariance"),
    "Cov_XS_stat"    : ("covariance_stat_xsec_diff_mjet", "Stat covariance"),
}

for name in ["Cov_XS_exp", "Cov_norm_exp", "Cov_XS_model", "Cov_norm_model", "Cov_XS_stat", "Cov_norm_stat", "Cor_XS_tot", "Cor_norm_tot"]:
    (filename, distname) = names2D[name]
    values, thresholds_x, thresholds_y = readMatrix(name)
    hist2D = Hist2D(filename)
    hist2D.addAxisX("$m_\mathrm{jet}$", "GeV", thresholds_x)
    hist2D.addAxisY("$m_\mathrm{jet}$", "GeV", thresholds_y)
    hist2D.addDistribution(distname, None, values)
    hist2D.makeFile()


keywords = ["Cross Section", "Proton-Proton Scattering", "Top", "Jet Mass", "Mass"]
sub = submission("input/abstract.txt")
sub.addEntry("Unfold_combination_data.pdf", "xsec_diff_mjet", "The particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section in the fiducial region as a function of the XCone-jet mass.", "differential cross section", keywords, "Contents of Figure 11a")
sub.addEntry("Unfold_combination_Correlations_data.pdf", "correlations_xsec_diff_mjet", "Correlations between bins in the particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "correlations", keywords, "Contents of Figure 12a")
sub.addEntry(None, "covariance_stat_xsec_diff_mjet", "The covariance matrix containing the statistical uncertainties of the particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "covariance stat", keywords, "Covariances of statistical uncertainties of Figure 11a")
sub.addEntry(None, "covariance_exp_xsec_diff_mjet", "The covariance matrix containing the experimental uncertainties of the particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "covariance exp", keywords, "Covariances of experimental uncertainties of Figure 11a")
sub.addEntry(None, "covariance_model_xsec_diff_mjet", "The covariance matrix containing the model uncertainties of the particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "covariance model", keywords, "Covariances of model uncertainties of Figure 11a")

sub.addEntry("Unfold_combination_norm_data.pdf", "xsec_diff_norm_mjet", "The normalized particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section in the fiducial region as a function of the XCone-jet mass.", "normalized differential cross section", keywords, "Contents of Figure 11b")
sub.addEntry("Unfold_combination_CorrelationsNorm_data.pdf", "correlations_xsec_diff_norm_mjet", "Correlations between bins in the normalized particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "normalized correlations", keywords, "Contents of Figure 12b")
sub.addEntry(None, "covariance_stat_xsec_diff_norm_mjet", "The covariance matrix containing the statistical uncertainties of the normalized particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "normalized covariance stat", keywords, "Covariances of statistical uncertainties of Figure 11b")
sub.addEntry(None, "covariance_exp_xsec_diff_norm_mjet", "The covariance matrix containing the experimental uncertainties of the normalized particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "normalized covariance exp", keywords, "Covariances of experimental uncertainties of Figure 11b")
sub.addEntry(None, "covariance_model_xsec_diff_norm_mjet", "The covariance matrix containing the model uncertainties of the normalized particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section as a function of the XCone-jet mass.", "normalized covariance model", keywords, "Covariances of model uncertainties of Figure 11b")

sub.addEntry("SYS_exp.pdf", "uncertainties_exp", "Relative experimental uncertainties of the particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section in the fiducial region as a function of the XCone-jet mass.", "relative uncertainties exp", keywords, "Contents of Figure 9a")
sub.addEntry("SYS_model.pdf", "uncertainties_model", "Relative model uncertainties of the particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section in the fiducial region as a function of the XCone-jet mass.", "relative uncertainties model", keywords, "Contents of Figure 9b")

sub.addEntry("SYS_exp_norm.pdf", "uncertainties_norm_exp", "Relative experimental uncertainties of the normalized particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section in the fiducial region as a function of the XCone-jet mass.", "relative normalized uncertainties exp", keywords, "Contents of Figure 10a")
sub.addEntry("SYS_model_norm.pdf","uncertainties_norm_model", "Relative model uncertainties of the normalized particle-level $\mathrm{t}\overline{\mathrm{t}}$ differential cross section in the fiducial region as a function of the XCone-jet mass.", "relative normalized uncertainties model", keywords, "Contents of Figure 10b")
sub.makeFile()
