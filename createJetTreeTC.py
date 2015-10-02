import os
import numpy as np
from tools.trackCounting import createJetTreeTC

#storeDirectory = "/storage/data/cms/store/user/brfranco/bTag/QCD_Phys14/QCD_Pt-30to50_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/crab_QCD_Pt-30to50_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/150306_172100/0000/"
storeDirectory = "/storage/data/cms/store/user/brfranco/bTag/trackOpti/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50nsRecodebug_MCRUN2_74_V9A-v1_2015-06-19/150619_133609/0000"
rootFileNames = [ "JetTree_mc_{}.root".format(i) for i in range(1, 30) ]
treeDirectory = "btagana/ttree"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetTree_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetTree_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetTree_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetTree_TC_btagCutsOnly.root"

#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/btagCutsOnly/jetTree_TC_btagCutsOnly.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/loosenedbtagCutsOnly/jetTree_TC_loosenedbtagCutsOnly.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_Log_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_bTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"
#outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTree_TC_BDT_CUTVALUE.root"
outFile = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/jetTree_testFormulaMVA.root"

# bTag current selection
trackCut = "Track_nHitPixel >= 2 && Track_nHitAll >= 8 && abs(Track_IP2D) < 0.2 && Track_pt > 1 && \
            Track_chi2 < 5 && abs(Track_dz) < 17 && Track_length < 5 && Track_dist < 0.07" # bTag current selection

# Variables used by TMVA
# Caution! Needs to be same order as when the MVA was trained! (thank you TMVA)
trackMVAVars = [
    "log(abs(Track_dz))",
    "Track_length",
    "Track_dist",
    "Track_IP2D",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll"
]

trackMVA = {
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits.weights.xml", # pas bon!
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits.weights.xml",
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits.weights.xml",
        #"name": "N_Nmin1_bTag_zIP_absSel_ptChi2BothHits",
        
        ## No selection
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_noSel_allVar.weights.xml",
        #"name": "800_track_hist_BfrombVSFake_noSel_allVar",
        
        ## bTag selection
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_bTagSel_allVar.weights.xml",
        #"name": "BDT_800_track_hist_BfrombVSFake_bTagSel_allVar",

        ## loosened bTag selection
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_bTagLoosenedSel_allVar.weights.xml",
        #"name": "BDT_800_track_hist_BfrombVSFake_bTagLoosenedSel_allVar",
        
        ## No selection, Log(dz)
        "path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_noSel_allVarLogdz.weights.xml",
        "name": "800_track_hist_BfrombVSFake_noSel_allVarLogdz",

        ## bTag selection, Log(dz)
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_BfrombVSFake_bTagSel_allVarLogdz.weights.xml",
        #"name": "800_track_hist_BfrombVSFake_bTagSel_allVarLogdz",

        ## No selection, trackFromBvsOther
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_trackFromBVStrackNonbJet_noSel_allVar.weights.xml",
        #"name": "BDT_800_track_hist_trackFromBVStrackNonbJet_noSel_allVar",
        
        ## No selection, trackFromBjetvsOther
        #"path": "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/weights/BDT_800_track_hist_trackFrombJetVStrackNonbJet_noSel_allVar.weights.xml",
        #"name": "BDT_800_track_hist_trackFrombJetVStrackNonbJet_noSel_allVar",
        
        #"cuts": [ -0.2, -0.19, -0.16, -0.14, -0.12, -0.1, -0.08, -0.06 ],
        "cuts": np.arange(-0.2, 0, 0.005),
        "vars": trackMVAVars
        }

#cutList = {
#        "no Cut": 0,
#    }

#cutList = {
#        "067": 0.67,
#        "073": 0.73,
#        "080": 0.80,
#    }
#cutList = {
#        "055": 0.55,
#        "070": 0.70,
#        "080": 0.80,
#    }

## No selection
#cutList = {
#        "-0065": -0.065,
#        "-0080": -0.08,
#        "-0100": -0.1,
#        "-0150": -0.15
#    }

## No selection, Log(dz)
#cutList = {
#        "-005": -0.05,
#        "-006": -0.06,
#        "-007": -0.07,
#        "-009": -0.09
#    }

## bTag selection
#cutList = {
#        "-020": -0.2,
#        "-016": -0.16,
#        "-010": -0.1,
#        "-0075": -0.075
#    }

## bTag loosened selection
#cutList = {
#        "-005": -0.05,
#        "-0045": -0.045,
#        "-0033": -0.033,
#        "-0026": -0.026
#}

## No selection, trackFromBvsOther
#cutList = {
#        "-038": -0.38,
#        "-037": -0.37,
#        "-035": -0.35,
#}

## No selection, trackFromBjetvsOther
#cutList = {
#        #"-0444": -0.444,
#        #"-0440": -0.44,
#        #"-0434": -0.434,
#        "-0430": -0.43,
#}

if __name__ == "__main__":
    fileList = [ os.path.join(storeDirectory, file) for file in rootFileNames ]

    createJetTreeTC(fileList, treeDirectory, outFile, trackCut=None, trackMVA=trackMVA)
