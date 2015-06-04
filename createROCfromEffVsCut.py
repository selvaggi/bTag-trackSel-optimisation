from tools.trackCounting import createROCfromEffVsCutCurves

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetHistos_TC_btagCutsOnly.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetROC_TC_btagCutsOnly.root"

#inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUTVALUE.root"

inFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUTVALUE.root"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUTVALUE.root"

sigCat = "Bjets"
bkgCats = ["Cjets", "Lightjets", "PUjets"]
discriminants = ["Jet_Ip_DiscrEff", "TCHE_DiscrEff", "TCHP_DiscrEff"]

#cutList = ["0"]
#cutList = ["067", "073", "080"]
cutList = ["055", "070", "080"]

if __name__ == "__main__":
    for cut in cutList:
        thisInFile = inFile.replace("VALUE", cut)
        thisOutFile = outFile.replace("VALUE", cut)
        createROCfromEffVsCutCurves(thisInFile, thisOutFile, sigCat, bkgCats, discriminants)
