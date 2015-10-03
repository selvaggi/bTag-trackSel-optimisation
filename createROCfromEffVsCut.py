import numpy as np
from tools.trackCounting import createROCfromEffVsCutCurves, createMVAPerfsFromROCCurves

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/btagCutsOnly/jetHistos_TC_btagCutsOnly.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/btagCutsOnly/jetROC_TC_btagCutsOnly.root"

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/loosenedbtagCutsOnly/jetHistos_TC_loosenedbtagCutsOnly.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/loosenedbtagCutsOnly/jetROC_TC_loosenedbtagCutsOnly.root"

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUTVALUE.root"

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUTVALUE.root"

## No Selection
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUTVALUE.root"

## bTag selection
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_bTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_bTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUTVALUE.root"

## loosened bTag selection
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUTVALUE.root"

## No bTag selection, trackFromBvsOther 
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUTVALUE.root"

## No bTag selection, trackFromBjetvsOther 
#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetHistos_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUTVALUE.root"

inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/jetHisto_testFormulaMVA.root"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/jetROC_TC_testFormulaMVA.root"

sigCat = "Bjets"
bkgCats = ["Cjets", "Lightjets", "PUjets"]
discriminants = ["Jet_Ip_DiscrEff", "TCHE_DiscrEff", "TCHP_DiscrEff"]

#cutList = ["0"]
#cutList = ["067", "073", "080"]
#cutList = ["055", "070", "080"]
#cutList = ["-0065", "-0080", "-0100", "-0150"] # No selection
#cutList = ["-020", "-016", "-010", "-0075"] # bTag selection
#cutList = ["-005", "-0045", "-0033", "-0026"] # loosened bTag selection
#cutList = ["-038", "-037", "-035"] # No selection, trackFromBvsOther 
#cutList = ["-0444", "-0440", "-0434", "-0430"] # No selection, trackFromBvsOther

createROCfromEffVsCutCurves(inFile, outFile, sigCat, bkgCats, discriminants)

#if __name__ == "__main__":
#    for cut in cutList:
#        thisInFile = inFile.replace("VALUE", cut)
#        thisOutFile = outFile.replace("VALUE", cut)
#        createROCfromEffVsCutCurves(thisInFile, thisOutFile, sigCat, bkgCats, discriminants)

inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/jetROC_TC_testFormulaMVA.root"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/testFormulaMVA/jetMVAPerfs_testFormulaMVA.root"

workingPoints = { "loose": 0.1, "medium": 0.01 }
mvaCuts = np.arange(-0.2, 0, 0.005)

createMVAPerfsFromROCCurves(inFile, outFile, sigCat, bkgCats, discriminants, workingPoints, mvaCuts)
