import ROOT
from array import array
import numpy as np
import os
import sys
import warnings

# This is needed because using TTreeFormula::EvalInstance() produces a Python warning,
# while everything runs absolutely fine.
# See https://root.cern.ch/phpBB3/viewtopic.php?f=14&t=14213
warnings.filterwarnings(action='ignore', category=RuntimeWarning, message='creating converter.*')

# Needed to use many TTreeFormulae on a TChain
# See https://sft.its.cern.ch/jira/browse/ROOT-7677
ROOT.gInterpreter.ProcessLine("#include \"tools/Formulas.h\"")

class trackCutSelector:
    """ Using the BTagAnalyzer tree and track number, check whether track passes cuts or not. """

    def __init__(self, tree, formulaManager, cuts):
        self.cuts = cuts
        self.formulaManager = formulaManager
        self.formula = ROOT.TTreeFormula("Cut_formula", cuts, tree)
        self.formulaManager.Add(self.formula)
        tree.SetNotify(self.formulaManager)

    def evaluate(self, tree, trackN):
        # Important otherwise the vector is not loaded correctly
        self.formula.GetNdata()
        return self.formula.EvalInstance(trackN)

class trackMVASelector:
    """ Using the BTagAnalyzer tree and track number, check whether track is selected by MVA or not. """
    
    def __init__(self, tree, formulaManager, path, name, cuts, trackVars):
        self.name = name
        self.path = path
        self.formulaManager = formulaManager
        self.cuts = cuts
        self.reader = ROOT.TMVA.Reader()
        
        # We cannot use a dict to hold the variables since TMVA cares about the order of the variables
        self.trackVars = [ (name, array("f", [0])) for name in trackVars ]
        for var in self.trackVars:
            self.reader.AddVariable(var[0], var[1])
        
        self.trackVarFormulas = { name: ROOT.TTreeFormula(name, name, tree) for name in trackVars }
        for formula in self.trackVarFormulas.values():
            self.formulaManager.Add(formula)
        tree.SetNotify(formulaManager)
        
        self.reader.BookMVA(self.name, self.path)

    def sync(self, tree, trackN):
        for var in self.trackVars:
            self.trackVarFormulas[var[0]].GetNdata()
            var[1][0] = self.trackVarFormulas[var[0]].EvalInstance(trackN)

    def getValue(self, tree, trackN):
        self.sync(tree, trackN)
        return self.reader.EvaluateMVA(self.name)

    def evaluate(self, tree, trackN):
        results = []
        mvaValue = self.getValue(tree, trackN) 
        return [ mvaValue > cut for cut in self.cuts ]



def createJetTreeTC(rootFiles, treeDirectory, outFileName, trackCut=None, trackMVA=None):
    """ Create TTree containing info about the jets.
    The tracks in the jets are selected either using cuts, or a MVA, or both.
    Only jets with at least one track are kept.
    For each jet, the number of selected tracks, and the jet IPsig, TCHE, and TCHP values are stored as vectors (one entry per cut on the MVA)."""

    tree = ROOT.TChain(treeDirectory)
    for file in rootFiles:
        tree.Add(file)

    outFile = ROOT.TFile(outFileName, "recreate")
    outTree = ROOT.TTree("jetTree", "jetTree")

    # The variables that are simply copied from the input tree
    copiedVariablesFloatToStore = ["Jet_genpt", "Jet_pt", "Jet_eta", "Jet_phi"]
    copiedVariablesIntToStore = ["Jet_ntracks", "Jet_flavour"]
    
    copiedVariablesFloat = { name: array("d", [0]) for name in copiedVariablesFloatToStore }
    for name, var in copiedVariablesFloat.items():
        outTree.Branch(name, var, name + "/D")
    copiedVariablesInt = { name: array("i", [0]) for name in copiedVariablesIntToStore }
    for name, var in copiedVariablesInt.items():
        outTree.Branch(name, var, name + "/I")

    copiedVariables = dict( copiedVariablesFloat, **copiedVariablesInt )
    
    # The variables that we compute here and store in the output tree
    nCuts = 1
    outVariablesIntToStore = ["Jet_nseltracks"]
    outVariablesFloatToStore = ["Jet_Ip", "TCHE", "TCHP"]
    outVariables = dict( { name: ROOT.std.vector(float)() for name in outVariablesFloatToStore }, **{ name: ROOT.std.vector(int)() for name in outVariablesIntToStore } )
    
    for name, var in outVariables.items():
        outTree.Branch(name, var)

    print ""

    formulaManager = ROOT.Formulas()
    
    # Create a trackCutSelector to select tracks using cuts
    myTrackCutSel = None
    if trackCut is not None:
        print "Will use base rectangular cuts: {}".format(trackCut)
        myTrackCutSel = trackCutSelector(tree, formulaManager, trackCut)

    # Create a trackMVASelector to select tracks using the MVA output
    myTrackMVASel = None
    if trackMVA is not None:
        if not os.path.isfile(trackMVA["path"]):
            raise Exception("Error: file {} does not exist.".format(trackMVA["path"]))
        print "Will use MVA-based track selector {} on cut values {}.\n".format(trackMVA["name"], trackMVA["cuts"])
        myTrackMVASel = trackMVASelector(tree, formulaManager, trackMVA["path"], trackMVA["name"], trackMVA["cuts"], trackMVA["vars"])
        nCuts = len(trackMVA["cuts"])

    print ""
    
    nEntries = tree.GetEntries()
    print "Will loop over ", nEntries, " events."

    nSelTracksB     = [0]*nCuts
    nTotTracksB     = 0
    nSelTracksLight = [0]*nCuts
    nTotTracksLight = 0
    nSelTracksC     = [0]*nCuts
    nTotTracksC     = 0
    nSelTracksPU    = [0]*nCuts
    nTotTracksPU    = 0

    # Looping over events
    for entry in xrange(nEntries):
        if (entry+1) % 1000 == 0:
            print "Event {}.".format(entry+1)
        tree.GetEntry(entry)
            
        # Looping over jets
        for jetInd in xrange(tree.nJet):
            selTracks = [ [] for i in xrange(nCuts) ]

            # Looping over tracks
            for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
                if tree.Jet_genpt[jetInd] >= 8:
                    if abs(tree.Jet_flavour[jetInd]) == 5:
                        nTotTracksB += 1
                    if abs(tree.Jet_flavour[jetInd]) == 4:
                        nTotTracksC += 1
                    if abs(tree.Jet_flavour[jetInd]) < 4 or tree.Jet_flavour[jetInd] == 21:
                        nTotTracksLight += 1
                else:
                    nTotTracksPU += 1
                
                keepTrack = [ True for i in xrange(nCuts) ]

                if myTrackCutSel is not None:
                    cutResult = myTrackCutSel.evaluate(tree, track)
                    keepTrack = [ x and cutResult for x in keepTrack ]
                if not any(keepTrack): continue

                if myTrackMVASel is not None:
                    keepTrack = [ x and y for (x,y) in zip(keepTrack, myTrackMVASel.evaluate(tree, track)) ]
                if not any(keepTrack): continue

                for i in xrange(nCuts):
                    if keepTrack[i]:
                        if tree.Jet_genpt[jetInd] >= 8:
                            if abs(tree.Jet_flavour[jetInd]) == 5:
                                nSelTracksB[i] += 1
                            if abs(tree.Jet_flavour[jetInd]) == 4:
                                nSelTracksC[i] += 1
                            if abs(tree.Jet_flavour[jetInd]) < 4 or tree.Jet_flavour[jetInd] == 21:
                                nSelTracksLight[i] += 1
                        else:
                            nSelTracksPU[i] += 1
                
                        # For selected tracks, store pair (track number, IPsig)
                        selTracks[i].append( (track, tree.Track_IPsig[track]) )

            selectedJet = False
            for i in xrange(nCuts):
                if len(selTracks[i]):
                    selectedJet = True

                    outVariables["Jet_nseltracks"].push_back(len(selTracks[i]))

                    # Sort tracks according to decreasing IP significance
                    sorted(selTracks[i], reverse = True, key = lambda track: track[1])

                    # TCHE = IPsig of 2nd track, TCHP = IPsig of 3rd track (default to -10**10)
                    outVariables["Jet_Ip"].push_back(selTracks[i][0][1])
                    outVariables["TCHE"].push_back(-10**10)
                    outVariables["TCHP"].push_back(-10**10)
                    if len(selTracks[i]) > 1:
                        outVariables["TCHE"][i] = selTracks[i][1][1]
                    if len(selTracks[i]) > 2:
                        outVariables["TCHP"][i] = selTracks[i][2][1]
            
            if selectedJet:
                # Get value of the variables we simply copy
                for name, var in copiedVariables.items():
                    var[0] = tree.__getattr__(name)[jetInd]

                outTree.Fill()

            for var in outVariables.values():
                var.clear()

    print ""

    for i in xrange(nCuts):
        if trackMVA is not None:
            print "MVA cut value {}:".format(trackMVA["cuts"][i])
        else:
            print "Non-MVA cuts:"
        print "B track efficiency:  {}/{} = {}%.".format(nSelTracksB[i], nTotTracksB, float(100*nSelTracksB[i])/nTotTracksB)
        print "C track efficiency:  {}/{} = {}%.".format(nSelTracksC[i], nTotTracksC, float(100*nSelTracksC[i])/nTotTracksC)
        print "Light track efficiency:  {}/{} = {}%.".format(nSelTracksLight[i], nTotTracksB, float(100*nSelTracksLight[i])/nTotTracksLight)
        print "PU track efficiency: {}/{} = {}%.\n".format(nSelTracksPU[i], nTotTracksPU, float(100*nSelTracksPU[i])/nTotTracksPU)

    outFile.cd()
    outTree.Write()
    outFile.Close()


def createDiscrHist(inputFileList, treeDirectory, outputFileName, histList, jetCategList):
    """ Using the tree output by createJetTreeTC, create histograms of the variables defined in histList.
    A separate histogram is created on the set of jets defined by each cut in jetCategList.
    The histograms are then saved in outputFileName, in different folders. """

    tree = ROOT.TChain(treeDirectory)
    for file in inputFileList:
        tree.Add(file)

    outFile = ROOT.TFile(outputFileName, "recreate")

    # Define the jet category selection formulae
    for cat in jetCategList:
        cat["formula"] = ROOT.TTreeFormula(cat["name"], cat["cuts"], tree)
        tree.SetNotify(cat["formula"])
        outFile.mkdir(cat["name"])
        cat["total"] = 0 # keep track of the total number of entries for each jet category

    # For each histogram of histList, and for each cut of jetCutList, define a TH1
    for histDict in histList:
        histDict["categDict"] = { cat["name"]: ROOT.TH1D(cat["name"] + "_" + histDict["name"], histDict["title"], histDict["bins"], histDict["range"][0], histDict["range"][1]) for cat in jetCategList }

    # Loop on the jets and fill histograms
    for entry in xrange(tree.GetEntries()):
        tree.GetEntry(entry)
        for cat in jetCategList:
            if cat["formula"].EvalInstance():
                cat["total"] += 1
                for histDict in histList:
                    value = tree.__getattr__(histDict["var"])
                    # We don't want to include the under/overflow:
                    if value >= histDict["range"][0] and value < histDict["range"][1]:
                        histDict["categDict"][ cat["name"] ].Fill(value)

    for cat in jetCategList:
        print "Total number of entries for category {}: {}.".format(cat["name"], cat["total"]) 

    # Write histograms to output file
    for cat in jetCategList:
        outFile.cd(cat["name"])
        for histDict in histList:
            histDict["categDict"][ cat["name"] ].Write(histDict["name"])

    # For those who asked it, create TGraph of eff. vs. cut value:
    for cat in jetCategList:
        outFile.cd(cat["name"])

        for histDict in histList:
            if "discreff" in histDict.keys():
                if histDict["discreff"] is True:
                    myGraph = drawEffVsCutCurve(myTH1 = histDict["categDict"][ cut["name"] ], total = cat["total"])
                    myGraph.Write(histDict["name"] + "_graph")

    outFile.Close()


def create2DDiscrHist(inputFile, treeDirectory, outputFileName, histList, jetCategList, mvaCutList):
    """ Using the tree output by createJetTreeTC, create histograms of the variables defined in histList.
    A separate histogram is created on the set of jets defined by each cut in jetCategList.
    The y-direction of the histogram corresponds to different cut values on the MVA.
    The histograms are then saved in outputFileName, in different folders. """

    tree = ROOT.TChain(treeDirectory)
    if not os.path.isfile(inputFile):
        raise Exception("File {} is not valid.".format(inputFile))
    tree.Add(inputFile)

    outFile = ROOT.TFile(outputFileName, "recreate")

    # Define the jet category selection formulae
    for cat in jetCategList:
        cat["formula"] = ROOT.TTreeFormula(cat["name"], cat["cuts"], tree)
        tree.SetNotify(cat["formula"])
        outFile.mkdir(cat["name"])
        cat["total"] = 0 # keep track of the total number of entries for each jet category

    nCuts = len(mvaCutList)

    # For each histogram of histList, and for each cut of jetCutList, define a TH2
    # The y-axis of the TH2 corresponds to the different cut values on the MVA
    for histDict in histList:
        histDict["categDict"] = { cat["name"]: ROOT.TH2D(cat["name"] + "_" + histDict["name"], histDict["title"], histDict["bins"], histDict["range"][0], histDict["range"][1], nCuts, 0, nCuts) for cat in jetCategList }

    # Loop on the jets and fill histograms
    for entry in xrange(tree.GetEntries()):
        tree.GetEntry(entry)
        for cat in jetCategList:
            if cat["formula"].EvalInstance():
                cat["total"] += 1
                for histDict in histList:
                    value = tree.__getattr__(histDict["var"])
                    try:
                        if len(value) > 1:
                            for mvaCut in xrange( len(value) ):
                                # We don't want to include the under/overflow:
                                #if value[mvaCut] >= histDict["range"][0] and value[mvaCut] < histDict["range"][1]:
                                histDict["categDict"][ cat["name"] ].Fill(value[mvaCut], mvaCut)
                    except TypeError:
                        for mvaCut in xrange(nCuts):
                            # We don't want to include the under/overflow:
                            #if value >= histDict["range"][0] and value < histDict["range"][1]:
                            histDict["categDict"][ cat["name"] ].Fill(value, mvaCut)

    for cat in jetCategList:
        print "Total number of entries for category {}: {}.".format(cat["name"], cat["total"]) 

    # Write histograms to output file
    for cat in jetCategList:
        outFile.cd(cat["name"])
        for histDict in histList:
            histDict["categDict"][ cat["name"] ].Write(histDict["name"])

    # For those who asked it, create TGraphAsymmErrors of eff. vs. cut value for each cut on the MVA:
    for cat in jetCategList:
        outFile.cd(cat["name"])

        for histDict in histList:
            if "discreff" in histDict.keys():
                if histDict["discreff"] is True:
                    
                    myList = ROOT.TList()
                    
                    for i in range(nCuts):
                        myEffGraph = createEfficiency( histDict["categDict"][ cat["name"] ].ProjectionX(histDict["name"]+"_projX"+str(i), i+1, i+1) ).CreateGraph()
                        # For those who asked it, store each graph separately (for easier viewing in a TBrowser)
                        if "effgraph" in histDict.keys():
                            if histDict["effgraph"] is True:
                                myEffGraph.Write( histDict["name"] + "_graph_" + str(i) )
                        myList.Add(myEffGraph)
                    
                    myList.Write(histDict["name"] + "_graphs", ROOT.TObject.kSingleKey)
    
    outFile.Close()


def drawEffVsCutCurve(myTH1, total = 0):
    """ Create and return eff. vs. cut TGraph, from a one-dimensional histogram.
    The efficiencies are computed relative to the histogram's integral,
    or relative to 'total' if it is given. """

    discrV = [ myTH1.GetBinLowEdge(1) ]
    integral = myTH1.Integral()
    effV = [ integral ]

    for i in xrange(2, myTH1.GetNbinsX()):
        discrV.append(myTH1.GetBinLowEdge(i))
        integral -= myTH1.GetBinContent(i-1)
        effV.append(integral)

    # We may want the max. efficiency to be correctly normalised,
    # if the TH1 passed as argument doesn't cover the whole range.
    if total is not 0:
        if total < integral:
            print "Warning in createEffVsCutCurve: total number specified to be *smaller* than the histograms's integral. Something might be wrong."
        integral = total
    effV = [ x/integral for x in effV ]
    
    return ROOT.TGraph(len(discrV), np.array(discrV), np.array(effV))

def createEfficiency(myTH1):
    """ Create TEfficiency object based on the discriminant in myTH1:
    Efficiency in bin i is #entries(bins >= i)/#total entries. 
    Under- and overflow are taken into account. """

    total = myTH1.Integral(0, myTH1.GetXaxis().GetNbins()+1)

    totTH1 = ROOT.TH1D( myTH1.Clone("total") )
    passTH1 = ROOT.TH1D( myTH1.Clone("passed") )
    for i in range(totTH1.GetXaxis().GetNbins()+2):
        totTH1.SetBinContent(i, total)
        passTH1.SetBinContent(i, myTH1.Integral(i, totTH1.GetXaxis().GetNbins()+1))

    myEff = ROOT.TEfficiency(passTH1, totTH1)
    myEff.SetStatisticOption(ROOT.TEfficiency.kFCP)

    return myEff


def createROCfromEffVsCutCurves(inFile, outFile, sigCat, bkgCats, discriminants, writeGraphs=False):
    """ Draw ROC curves from TGraphs (stored in inFile) of efficiency vs. discriminant cut value,
    created by the function createDiscrHist().
    Store the curves in outFile. """

    inputFile = ROOT.TFile(inFile, "read")

    sigGraphList = { discri: inputFile.Get(sigCat + "/" + discri + "_graphs") for discri in discriminants }
    bkgGraphListDict = {}
    for bkg in bkgCats:
        bkgGraphListDict[bkg] = { discri: inputFile.Get(bkg + "/" + discri + "_graphs") for discri in discriminants }

    outputFile = ROOT.TFile(outFile, "recreate")

    for bkg, bkgGraphList in bkgGraphListDict.items():
        outputFile.mkdir(sigCat + "_vs_" + bkg)
        outputFile.cd(sigCat + "_vs_" + bkg)

        for discri in discriminants:
            myList = ROOT.TList()
            
            for i in range(bkgGraphList[discri].GetEntries()):
                bkgGraph = bkgGraphList[discri].At(i)
                sigGraph = sigGraphList[discri].At(i)
                myROC = drawROCfromEffVsCutCurves(sigGraph, bkgGraph)
                myList.Add(myROC)
                if writeGraphs:
                    myROC.Write(discri + "_{}".format(i))
            
            myList.Write(discri, ROOT.TObject.kSingleKey)

    inputFile.Close()
    outputFile.Close()


def drawROCfromEffVsCutCurves(sigGraph, bkgGraph):
    """ Return ROC curve drawn from the "efficiency vs. discriminant" cut curves of signal and background. 
    For now, assume the range and binning of the discriminants is the same for both signal and background.
    This might have to be refined. """

    nPoints = sigGraph.GetN() 

    if nPoints != bkgGraph.GetN():
        print "Background and signal curves must have the same number of entries!"
        print "Entries signal:     {}".format(nPoints) 
        print "Entries background: {}".format(bkgGraph.GetN())
        sys.exit(1)

    sigEff = []
    sigEffErrXLow = []
    sigEffErrXUp = []
    bkgEff = []
    bkgEffErrYLow = []
    bkgEffErrYUp = []

    for i in range(nPoints):
        sigValX = ROOT.Double()
        sigValY = ROOT.Double()
        bkgValX = ROOT.Double()
        bkgValY = ROOT.Double()

        sigGraph.GetPoint(i, sigValX, sigValY)
        bkgGraph.GetPoint(i, bkgValX, bkgValY)

        sigEff.append(sigValY)
        sigEffErrXLow.append(sigGraph.GetErrorXlow(i))
        sigEffErrXUp.append(sigGraph.GetErrorXhigh(i))

        bkgEff.append(bkgValY)
        bkgEffErrYLow.append(bkgGraph.GetErrorYlow(i))
        bkgEffErrYUp.append(bkgGraph.GetErrorYhigh(i))

    return ROOT.TGraphAsymmErrors(nPoints, np.array(sigEff), np.array(bkgEff), np.array(sigEffErrXLow), np.array(sigEffErrXUp), np.array(bkgEffErrYLow), np.array(bkgEffErrYUp))


def createMVAPerfsFromROCCurves(inFile, outFile, sigCat, bkgCats, discriminants, workingPoints, mvaCuts):
    """ Create a set of graphs of "cut on MVA" vs. "Tagger signal efficiency" for a given tagger background rejection (workingPoints) """
    
    inputFile = ROOT.TFile(inFile, "read")

    outputFile = ROOT.TFile(outFile, "recreate")

    for bkg in bkgCats:
        outputFile.mkdir(sigCat + "_vs_" + bkg)
        outputFile.cd(sigCat + "_vs_" + bkg)
        
        for discri in discriminants:
            for wp, wpRej in workingPoints.items():
                ROCList = inputFile.Get(sigCat + "_vs_" + bkg + "/" + discri)
                perfCurve = drawPerfCurveFromROCList(ROCList, wpRej, mvaCuts)
                perfCurve.Write(discri + "_" + wp)

    outputFile.Close()
    inputFile.Close()


def drawPerfCurveFromROCList(ROCList, wpRej, cuts):
    """ Draw a graph of "cut on MVA" vs. "Tagger signal efficiency" for a given tagger background rejection (wpRej) """

    nROC = ROCList.GetEntries()
    if nROC != len(cuts):
        raise Exception("Error: number of cuts does not correspond to number of ROCs!")

    effList = []
    effListErrUp = []
    effListErrLow = []

    for i in range(nROC):
        thisROC = ROCList.At(i)
        nPoints = thisROC.GetN()
       
        foundPoint = False

        for j in range(nPoints):
            
            sigEff = ROOT.Double()
            bkgEff = ROOT.Double()
            thisROC.GetPoint(j, sigEff, bkgEff)
            
            if bkgEff <= wpRej:
                effList.append(sigEff)
                effListErrLow.append(thisROC.GetErrorXlow(j))
                effListErrUp.append(thisROC.GetErrorXhigh(j))
                foundPoint = True
                break

        if not foundPoint:
            effList.append(0)
            effListErrLow.append(0)
            effListErrUp.append(0)

    return ROOT.TGraphAsymmErrors(nROC, np.array(cuts), np.array(effList), np.zeros(len(cuts)), np.zeros(len(cuts)), np.array(effListErrLow), np.array(effListErrUp))

