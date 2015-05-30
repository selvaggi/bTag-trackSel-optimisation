import os
from trackCounting import gt, geq, lt, leq, eq, neq
from trackCounting import produceTaggedJetTree

storeDirectory = "/storage/data/cms/store/user/brfranco/bTag/QCD_Phys14/QCD_Pt-30to50_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/crab_QCD_Pt-30to50_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/150306_172100/0000/"
rootFileNames = ["JetTree_phys14_1.root"]
treeDirectory = "btagana/ttree"
outFile = "../myTrees/jetTree_TC_btagCuts_MLP_Nplus5_noSel.root"

trackCut = [ # bTag current selection
    ( "Track_nHitPixel", geq, 2 ),
    ( "Track_nHitAll", geq, 8 ),
    ( "Track_IP2D", lt, 0.2 ),
    ( "Track_pt", gt, 1 ),
    ( "Track_chi2", lt, 5 ),
    ( "Track_zIP", lt, 17 ),
    ( "Track_length", lt, 50 ),
    ( "Track_dist", lt, 0.07 )
]
#return HitPix >= 1 and HitAll>=6 and IP2D<0.3 and Pt>0.5 and Chi2 < 7 and ZIP < 20 and Length <60 and Dist < 0.1

# Variables used by TMVA
# Caution! Needs to be same order as when the MVA was trained! (thank you TMVA)
trackMVAVars = [
    "Track_zIP",
    "Track_length",
    "Track_dist",
    "Track_IP2D",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll",
]

trackMVA = {
        "path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/MLP_Nplus5_noSel.weights.xml",
        "name": "Nplus5_noSel",
        "cut": 0.6,
        "vars": trackMVAVars
        }

if __name__ == "__main__":
    fileList = [ os.path.join(storeDirectory, file) for file in rootFileNames ]
    produceTaggedJetTree(fileList, treeDirectory, outFile, trackCut=trackCut, trackMVA=trackMVA)
