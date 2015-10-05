import os
import sys
import numpy as np
from tools.trackCounting import createJetTreeTC

storeDirectory = "/storage/data/cms/store/user/brfranco/bTag/trackOpti/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50nsRecodebug_MCRUN2_74_V9A-v1_2015-06-19/150619_133609/0000"
firstFile = int(sys.argv[1])
lastFile = int(sys.argv[2])
rootFileNames = [ "JetTree_mc_{}.root".format(i) for i in range(firstFile, lastFile) ]
treeDirectory = "btagana/ttree"

#outDir = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetTrees/"
#outDir = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/"
#outDir = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbtagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/"
#outDir = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_btagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/"

# bTag current selection
#trackCut = "Track_nHitPixel >= 2 && Track_nHitAll >= 8 && abs(Track_IP2D) < 0.2 && Track_pt > 1 && \
#            Track_chi2 < 5 && abs(Track_dz) < 17 && Track_length < 5 && abs(Track_dist) < 0.07"

# bTag loosened selection
trackCut = "abs(Track_IP2D) < 0.2 && Track_chi2 < 5 && abs(Track_dz) < 17 && Track_length < 5 && abs(Track_dist) < 0.07"

# Variables used by TMVA
# Caution! Needs to be same order as when the MVA was trained! (thank you TMVA)
trackMVAVars = [
    "Track_dz",
    "Track_length",
    "Track_dist",
    "Track_IP2D",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll"
]

trackMVA = {
        ## No selection
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_noSel_allVar.weights.xml",
        #"name": "800_track_hist_BfrombVSFake_noSel_allVar",
        
        ## No selection, Log(dz)
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_noSel_allVarLogdz.weights.xml",
        #"name": "800_track_hist_BfrombVSFake_noSel_allVarLogdz",
        #"cuts": np.arange(-0.1, -0.0099, 0.0025),

        ## loosened bTag selection
        "path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_bTagLoosenedSel_allVar.weights.xml",
        "name": "BDT_800_track_hist_BfrombVSFake_bTagLoosenedSel_allVar",
        "cuts": np.arange(-0.2, 0.0201, 0.005),
        
        ## bTag selection
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_bTagSel_allVar.weights.xml",
        #"name": "BDT_800_track_hist_BfrombVSFake_bTagSel_allVar",

        ## bTag selection, Log(dz)
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_bTagSel_allVarLogdz.weights.xml",
        #"name": "800_track_hist_BfrombVSFake_bTagSel_allVarLogdz",
        #"cuts": np.arange(-0.3, 0.0801, 0.005),

        ## No selection, trackFromBvsOther
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_trackFromBVStrackNonbJet_noSel_allVar.weights.xml",
        #"name": "BDT_800_track_hist_trackFromBVStrackNonbJet_noSel_allVar",
        #"cuts": np.arange(-0.3, -0.045, 0.005),
        
        ## No selection, trackFromBjetvsOther
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_trackFrombJetVStrackNonbJet_noSel_allVar.weights.xml",
        #"name": "BDT_800_track_hist_trackFrombJetVStrackNonbJet_noSel_allVar",
        #"cuts": np.arange(-0.3, -0.045, 0.005),
        
        "vars": trackMVAVars
        }

if __name__ == "__main__":
    inFileList = []
    for file in rootFileNames:
        inFileList.append(os.path.join(storeDirectory, file))
    #outFile = os.path.join(outDir, rootFileNames[0])
    outFile = rootFileNames[0]
    if len(sys.argv) >= 4:
        outFile = sys.argv[3]

    createJetTreeTC(inFileList, treeDirectory, outFile, trackCut=trackCut, trackMVA=trackMVA)
