import os
from tools.trackCounting import createDiscrHist

rootFileNames = ["../myTrees/jetTree_TC_btagCuts_MLP_Nplus5_noSel.root"]
treeDirectory = "jetTree"
outFile = "../myTrees/jetHistos_TC_btagCuts_MLP_Nplus5_noSel.root"

histList = []
histList.append({
    "var": "Jet_pt", # name of the variable in the TTree
    "name": "Jet_pt", # name of the histogram
    "title": "Jet Pt",
    "bins": 100,
    "range": [20,100],
    })
histList.append({
    "var": "Jet_ntracks",
    "name": "Jet_ntracks",
    "title": "Jet number of tracks",
    "bins": 35,
    "range": [0,35],
    })
histList.append({
    "var": "Jet_nseltracks",
    "name": "Jet_nseltracks",
    "title": "Jet number of selected tracks",
    "bins": 15,
    "range": [0,15],
    })
histList.append({
    "var": "Jet_Ip",
    "name": "Jet_Ip",
    "title": "Jet first track IP sig.",
    "bins": 100,
    "range": [-100,100],
    })
histList.append({
    "var": "TCHE",
    "name": "TCHE",
    "title": "Jet TCHE",
    "bins": 100,
    "range": [-100,100],
    })
histList.append({
    "var": "TCHP",
    "name": "TCHP",
    "title": "Jet TCHP",
    "bins": 100,
    "range": [-100,100],
    })
# These will also included, and will be used to draw an "efficiency vs. cut value" curve
histList.append({
    "var": "Jet_Ip",
    "name": "Jet_Ip_DiscrEff",
    "title": "Jet first track IP sig.",
    "bins": 2000,
    "range": [-5,15],
    "discreff": True
    })
histList.append({
    "var": "TCHE",
    "name": "TCHE_DiscrEff",
    "title": "Jet TCHE",
    "bins": 2000,
    "range": [-5,15],
    "discreff": True
    })
histList.append({
    "var": "TCHP",
    "name": "TCHP_DiscrEff",
    "title": "Jet TCHP",
    "bins": 2000,
    "range": [-5,15],
    "discreff": True
    })

jetCutList = []
jetCutList.append({
    "name": "Bjets", # Directory in the rootfile where the histograms for the jet in this category will be stored
    "cuts": "abs(Jet_flavour) == 5 && Jet_genpt >= 8"
    })
jetCutList.append({
    "name": "Cjets",
    "cuts": "abs(Jet_flavour) == 4 && Jet_genpt >= 8"
    })
jetCutList.append({
    "name": "Lightjets",
    "cuts": "(abs(Jet_flavour) < 4 || Jet_flavour == 21) && Jet_genpt >= 8"
    })
jetCutList.append({
    "name": "PUjets",
    "cuts": "Jet_genpt < 8"
    })

if __name__ == "__main__":
    createDiscrHist(rootFileNames, treeDirectory, outFile, histList, jetCutList)
