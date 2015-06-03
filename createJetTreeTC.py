import os
from tools.trackCounting import gt, geq, lt, leq, eq, neq
from tools.trackCounting import createJetTreeTC

storeDirectory = "/storage/data/cms/store/user/brfranco/bTag/QCD_Phys14/QCD_Pt-30to50_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/crab_QCD_Pt-30to50_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/150306_172100/0000/"
rootFileNames = ["JetTree_phys14_1.root"]
treeDirectory = "btagana/ttree"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetTree_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT075.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetTree_TC_btagCutsOnly.root"

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
# Failed try: we cannot use TTreeFormula, because what we access is not
# Track_pt but Track_pt[tracknumber]. Any better solution?
#trackCut = "Track_nHitPixel >= 2 && \
#            Track_nHitAll >= 8 && \
#            Track_IP2D < 0.2 && \
#            Track_pt > 1 && \
#            Track_chi2 < 5 && \
#            Track_zIP < 17 && \
#            Track_length < 50 && \
#            Track_dist < 0.07\
#            " # bTag current selection

# Variables used by TMVA
# Caution! Needs to be same order as when the MVA was trained! (thank you TMVA)
trackMVAVars = [
    #"Track_zIP",
    #"Track_length",
    #"Track_dist",
    #"Track_IP2D",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll",
]

trackMVA = {
        "path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits.weights.xml",
        "name": "N_Nmin1_bTag_zIPSel_ptChi2BothHits",
        "cut": 0.75,
        "vars": trackMVAVars
        }

if __name__ == "__main__":
    fileList = [ os.path.join(storeDirectory, file) for file in rootFileNames ]
    createJetTreeTC(fileList, treeDirectory, outFile, trackCut=trackCut, trackMVA=trackMVA)
