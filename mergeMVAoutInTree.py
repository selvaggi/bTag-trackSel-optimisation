from tools.MVA_facilities import MVA_out_in_tree

trackSel = "track_hist_BfrombVSFake_no"
filesToMerge = [ ["sigTrackTree_"+trackSel+"TrackSel.root"], ["bkgTrackTree_"+trackSel+"TrackSel.root"] ]  # allow to have several files for the bkg or signal to be merged 
treeName = "trackTree"
discriVars = [

    "Track_dz",
    "Track_length",
    "Track_dist",
    "Track_IP2D",
    "Track_pt",
    "Track_chi2",
    "Track_nHitPixel",
    "Track_nHitAll"

]

MVAname = "BDT_800_"+trackSel+"Sel_allVar"
xmlFile = "./weights/"+MVAname+".weights.xml"

for files in filesToMerge : 
    MVA_out_in_tree(files, treeName, discriVars, xmlFile, MVAname, files[0].replace(".root",MVAname+".root"))


