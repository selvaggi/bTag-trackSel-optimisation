from tools.MVA_facilities import train_MVA
#from createTrackTrees import TrackVars

#HitPix >= 2 and HitAll>=8 and IP2D<0.2 and Pt>1 and Chi2 < 5 and ZIP < 17 and Length <50 and Dist < 0.07

TrackVars = [

    "Track_dz",
    "Track_length",
    "Track_dist",
    "Track_dxy",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll"

]

trackSel =  "bTag"   #"no" , "bTag", "bTagLoosened", "dist"

train_MVA("./bkgTrackTree_"+trackSel+"TrackSel.root", "./sigTrackTree_"+trackSel+"TrackSel.root", TrackVars, "MLP", trackSel+"Sel_N_Nmin1")



