import ROOT
from drawCanvas import *
import copy
from array import array
import math


def isSelectedTrack(HitPix=2, HitAll=8, IP2D=0.2, Pt=1, Chi2=5, dz=17, Length=5, Dist=0.07):  #default values are the value requested for selectedTrack in bTag code
    return HitPix >= 2 and HitAll >= 8 and abs(IP2D) < 0.2 and Pt > 1 and Chi2 < 5 and abs(dz) < 17 and Length < 5 and abs(Dist) < 0.07  # bTag current selection
    #return HitPix >= 0 and HitAll >= 0 and abs(IP2D) < 0.2 and Pt > 0 and Chi2 < 5 and abs(dz) < 17 and Length < 5 and abs(Dist) < 0.07  # Looser selection
    #return HitPix >= 1 and HitAll >= 6 and abs(IP2D) < 0.3 and Pt>0.5 and Chi2 < 7 and abs(zIP) < 20 and Length <6 and Dist < 0.1 # Looser selection
    #return Dist < 0.07    # Selection applied only on the "Jet vs track" variable
    #return True # no selection 

def isSignalJet(jetGenPT, jetFlavour):
    return jetGenPT>8 and abs(jetFlavour)==5
    
def isBkgJet(jetGenPT, jetFlavour):
    return jetGenPT<8 

def createTreeSigBkg_trackHist(rootFiles, treeDirectory, trackVariablesToStore, outRootFileName_sig, outRootFileName_bkg) :
    # Create two trees, one with signal and one with background tracks

    tree = ROOT.TChain(treeDirectory)
    for file in rootFiles:
        tree.Add(file)

    sigTree = ROOT.TTree("trackTree", "sigTrackTree")
    bkgTree = ROOT.TTree("trackTree", "bkgTrackTree")

    dict_variableName_Leaves = {variable: array('d', [0]) for variable in trackVariablesToStore }
    for variable in trackVariablesToStore: 
        sigTree.Branch(variable, dict_variableName_Leaves[variable], variable + "/D")
        bkgTree.Branch(variable, dict_variableName_Leaves[variable], variable + "/D")

    nEntries = tree.GetEntries()
    print "Will loop over ", nEntries, " events."
    
    trackHistList = []
    trackPVList = []
    for entry in xrange(nEntries):
        tree.GetEntry(entry)
        for jetInd in xrange(tree.nJet):
            for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):

                trackHist = tree.Track_history[track]
                stringTrackHist = str(trackHist)
                trackHistList.append(trackHist)
                trackPVList.append(tree.Track_PV[track])

                # For example : signal tracks are the one coming from BWeakDecay, inside a b-jet; background tracks are fakes from any other jet. 
                if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]) :
                    # See the way track history is stored in BTagAnalyzer 
                    # https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/blob/7_4_X/plugins/BTagAnalyzer.cc#L2061
                    if (stringTrackHist[len(stringTrackHist)-1] == str(1)) : 
                            for variable in dict_variableName_Leaves.keys() :
                                dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                            sigTree.Fill()
                else : 
                    if trackHist >= 10000000 and trackHist < 100000000 : 
                            for variable in dict_variableName_Leaves.keys() :
                                dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                            bkgTree.Fill()
   
    outFile_sig = ROOT.TFile(outRootFileName_sig, "recreate")
    sigTree.Write()
    outFile_sig.Close()
    print outRootFileName_sig, "written."

    outFile_bkg = ROOT.TFile(outRootFileName_bkg, "recreate")
    bkgTree.Write()
    outFile_bkg.Close()
    print outRootFileName_bkg, "written."
