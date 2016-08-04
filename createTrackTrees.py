from tools.crabOutAnalyzer import *
import os

storeDirectory = "/storage/data/cms/store/user/ajmerten/bTag/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M1_13TeV-powheg-pythia8_2016-07-26_1469538272670/160726_130513/0000/"

rootFileNames = ["JetTree_mc_1*.root"]
treeDirectory = "btagana/ttree"
doPTreweight = True
trackSelection = "bTag_zIP_abs"    #"bTagLoosened", "no", "dist", "bTag"
trackSelection ="nosel"
outFileSig = "sigTrackTree_"+trackSelection+"_TTbar.root"
outFileBkg = "bkgTrackTree_"+trackSelection+"_TTbar.root"

TrackVars = {

    "Track_dxy":{"name":"Track_dxy","title":"Track_dxy","bin":2000,"xmin":-0.5,"xmax":0.5},
    "Track_dz":{"name":"Track_dz","title":"Track_dz","bin":2000,"xmin":-50,"xmax":50},
#    "Track_zIP":{"name":"Track_zIP","title":"Track_zIP","bin":1000,"xmin":-30,"xmax":30},
    "Track_length":{"name":"Track_length","title":"Track_length","bin":1000,"xmin":0,"xmax":60},
    "Track_dist":{"name":"Track_dist","title":"Track_dist","bin":2000,"xmin":-4,"xmax":1},
    "Track_IP2D":{"name":"Track_IP2D","title":"Track_IP2D","bin":2000,"xmin":-0.5,"xmax":0.5},
    "Track_IP2Dsig":{"name":"Track_IP2Dsig","title":"Track_IP2Dsig","bin":200,"xmin":-100,"xmax":100},
    "Track_IP2Derr":{"name":"Track_IP2Derr","title":"Track_IP2Derr","bin":200,"xmin":0,"xmax":0.4},
    "Track_IP":{"name":"Track_IP","title":"Track_IP","bin":2000,"xmin":-10,"xmax":10},
    "Track_IPerr":{"name":"Track_IPerr","title":"Track_IPerr","bin":2000,"xmin":0,"xmax":0.2},
    "Track_IPsig":{"name":"Track_IPsig","title":"Track_IPsig","bin":2000,"xmin":-200,"xmax":200},
    "Track_pt":{"name":"Track_pt","title":"Track_pt","bin":100,"xmin":0,"xmax":10},
    "Track_eta":{"name":"Track_eta","title":"Track_eta","bin":20,"xmin":-3,"xmax":3},
    "Track_chi2":{"name":"Track_chi2","title":"Track_chi2","bin":100,"xmin":0,"xmax":6},
    "Track_nHitPixel":{"name":"Track_nHitPixel","title":"Track_nHitPixel","bin":10,"xmin":0,"xmax":10},
    "Track_nHitAll":{"name":"Track_nHitAll","title":"Track_nHitAll","bin":35,"xmin":0,"xmax":35},
    "Track_category":{"name":"Track_category","title":"Track_category","bin":12,"xmin":-2,"xmax":10},
    "Track_PV":{"name":"Track_PV","title":"Track_PV","bin":16,"xmin":-1,"xmax":15}
    
}

if __name__ == "__main__" :
    fileList = [ os.path.join(storeDirectory, file) for file in rootFileNames ]
  #  createTreeSigBkg(fileList, treeDirectory, TrackVars.keys(), outFileSig, outFileBkg)
    createTreeSigBkg_trackHist(fileList, treeDirectory, TrackVars.keys(), outFileSig, outFileBkg)
