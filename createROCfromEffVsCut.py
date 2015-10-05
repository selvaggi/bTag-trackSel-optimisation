import numpy as np
from tools.trackCounting import createROCfromEffVsCutCurves, createMVAPerfsFromROCCurves

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetHistos_TC.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetROC_TC.root"

## No Selection, Log(dZ)
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC.root"

## loosened bTag selection
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC.root"

## bTag selection, Log(dZ)
inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_bTagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC.root"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_bTagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC.root"

## No bTag selection, trackFromBvsOther 
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUTVALUE.root"

## No bTag selection, trackFromBjetvsOther 
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUTVALUE.root"

sigCat = "Bjets"
bkgCats = ["Cjets", "Lightjets", "PUjets"]
discriminants = ["TCHE_DiscrEff", "TCHP_DiscrEff"]
#discriminants = ["Jet_Ip_DiscrEff", "TCHE_DiscrEff", "TCHP_DiscrEff"]

createROCfromEffVsCutCurves(inFile, outFile, sigCat, bkgCats, discriminants)

############# Already create MVA perfs

inFile = outFile 

# No Selection, Log(dZ)
#outFile ="/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetMVAperf_TC.root"
#mvaCuts = np.arange(-0.1, -0.0099, 0.0025)

## loosened bTag selection
#outFile ="/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetMVAperf_TC.root"
#mvaCuts = np.arange(-0.2, 0.0201, 0.005)

## bTag selection, Log(dZ)
outFile ="/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_bTagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetMVAperf_TC.root"
mvaCuts = np.arange(-0.3, 0.0801, 0.005)

workingPoints = { "loose": 0.1, "medium": 0.01 }

createMVAPerfsFromROCCurves(inFile, outFile, sigCat, bkgCats, discriminants, workingPoints, mvaCuts)
