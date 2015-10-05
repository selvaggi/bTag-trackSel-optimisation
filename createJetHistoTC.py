import os
import numpy as np
from tools.trackCounting import createDiscrHist, create2DDiscrHist

#inputFiles = ["/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetTrees/*.root"]
#treeDirectory = "jetTree"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetHistos_TC.root"

## No selection, Log(dZ)
#inputFiles = ["/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/*.root"]
#treeDirectory = "jetTree"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC.root"
#cutList = np.arange(-0.1, -0.0099, 0.0025)

## loosened bTag selection
#inputFiles = ["/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/*.root"]
#treeDirectory = "jetTree"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC.root"
#cutList = np.arange(-0.2, 0.0201, 0.005)

## bTag selection, Log(dZ)
inputFiles = ["/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_bTagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/*.root"]
treeDirectory = "jetTree"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_bTagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC.root"
cutList = np.arange(-0.3, 0.0801, 0.005)

## No bTag selection, trackFromBvsOther 
#inputFiles = ["/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"]
#treeDirectory = "jetTree"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#cutList = np.arange(-0.3, -0.045, 0.005)

## No bTag selection, trackFromBjetvsOther 
#inputFiles = ["/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"]
#treeDirectory = "jetTree"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#cutList = np.arange(-0.3, -0.045, 0.005)

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
    "bins": 40,
    "range": [0,40],
    })
histList.append({
    "var": "Jet_nseltracks",
    "name": "Jet_nseltracks",
    "title": "Jet number of selected tracks",
    "bins": 20,
    "range": [0,20],
    })
histList.append({
    "var": "Jet_Ip",
    "name": "Jet_Ip",
    "title": "Jet first track IP sig.",
    "bins": 500,
    "range": [-50,50],
    })
histList.append({
    "var": "TCHE",
    "name": "TCHE",
    "title": "Jet TCHE",
    "bins": 500,
    "range": [-50,50],
    })
histList.append({
    "var": "TCHP",
    "name": "TCHP",
    "title": "Jet TCHP",
    "bins": 500,
    "range": [-50,50],
    })
# These will also included, and will be used to draw an "efficiency vs. cut value" curve
#histList.append({
#    "var": "Jet_Ip",
#    "name": "Jet_Ip_DiscrEff",
#    "title": "Jet first track IP sig.",
#    "bins": 1000,
#    "range": [-1000,1000],
#    "discreff": True, # Do the efficiency curve
#    "effgraph": True, # Save a graph for each cut value separately (more disk usage, but easier browsing)
#    })
histList.append({
    "var": "TCHE",
    "name": "TCHE_DiscrEff",
    "title": "Jet TCHE",
    "bins": 1000,
    "range": [-50,100],
    "discreff": True,
    "effgraph": True,
    })
histList.append({
    "var": "TCHP",
    "name": "TCHP_DiscrEff",
    "title": "Jet TCHP",
    "bins": 1000,
    "range": [-50,100],
    "discreff": True,
    "effgraph": True,
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

create2DDiscrHist(inputFiles, treeDirectory, outFile, histList, jetCutList, cutList)
