from tools.MVA_facilities import train_MVA

TrackVars_training = [

#    "Track_zIP",
    "Track_length",
    "Track_dist",
#    "Track_IP2D",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll"

]

trackSel =  "bTag_zIP_abs"   #"no" , "bTag", "bTagLoosened", "dist"

absolutePath = "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation"
bkgTree = absolutePath + "/bkgTrackTree_"+trackSel+"TrackSel.root"
sigTree = absolutePath + "/sigTrackTree_"+trackSel+"TrackSel.root"


train_MVA(bkgTree, sigTree, TrackVars_training, "CUT", trackSel+"Sel_lengthDistptChi2BothHits")  



