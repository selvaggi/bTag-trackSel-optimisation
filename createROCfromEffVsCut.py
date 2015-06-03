from tools.trackCounting import createROCfromEffVsCutCurves

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetHistos_TC_btagCutsOnly.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetROC_TC_btagCutsOnly.root"

inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT08.root"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT08.root"

sigCat = "Bjets"
bkgCats = ["Cjets", "Lightjets", "PUjets"]
discriminants = ["Jet_Ip_DiscrEff", "TCHE_DiscrEff", "TCHP_DiscrEff"]

if __name__ == "__main__":
    createROCfromEffVsCutCurves(inFile, outFile, sigCat, bkgCats, discriminants)
