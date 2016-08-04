from tools.MVA_facilities import train_MVA

TrackVars_training = [

    "Track_dz",
    "Track_length",
    "Track_dist",
    "Track_dxy",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll"

]


bkgTree = "bkgTrackTree_nosel_TTbar.root"
sigTree = "sigTrackTree_nosel_TTbar.root"

train_MVA(bkgTree, sigTree, TrackVars_training, "BDT", "nosel_8Var")


