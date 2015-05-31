from tools.trackCounting import createROCfromEffVsCutCurves

inFile = "../myTrees/jetHistos_TC_btagCuts_MLP_Nplus5_noSel.root"
outFile = "../myTrees/jetROC_TC_btagCuts_MLP_Nplus5_noSel.root"
sigCat = "Bjets"
bkgCats = ["Cjets", "Lightjets", "PUjets"]
discriminants = ["Jet_Ip_DiscrEff", "TCHE_DiscrEff", "TCHP_DiscrEff"]

if __name__ == "__main__":
    createROCfromEffVsCutCurves(inFile, outFile, sigCat, bkgCats, discriminants)
