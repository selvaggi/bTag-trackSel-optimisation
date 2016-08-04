import ROOT
from drawCanvas import *
from array import array
import os, sys

def train_MVA(bkgTree, sigTree, discriList, MVAmethod,label):
    
    file_proc1 = ROOT.TFile(bkgTree)    
    file_proc2 = ROOT.TFile(sigTree)   

    tree_proc1 = file_proc1.Get("trackTree")
    tree_proc2 = file_proc2.Get("trackTree")

    Nproc1 = float(tree_proc1.GetEntries())
    Nproc2 = float(tree_proc2.GetEntries())

    proc1_weight = 1/Nproc1
    proc2_weight = 1/Nproc2

    MVA_fileName = "TMVA_"+MVAmethod+"_"+label+".root"
    file_MVA = ROOT.TFile(MVA_fileName,"recreate")

    print "Will write MVA info in ", MVA_fileName 

    factory = ROOT.TMVA.Factory(MVAmethod, file_MVA)
   
    #dataloader = ROOT.TMVA.DataLoader("dataset");
   
    for discriVar in discriList :
        factory.AddVariable(discriVar)
        #dataloader.AddVariable(discriVar)

    factory.AddSignalTree(tree_proc2, proc2_weight)
    factory.AddBackgroundTree(tree_proc1, proc1_weight)
   
    # add cuts here eventually
    
    sigcut = ""
    bkgcut = ""

    factory.PrepareTrainingAndTestTree( ROOT.TCut( sigcut ), ROOT.TCut( bkgcut ),
                                      ":".join([ "nTrain_Signal=50000",     # Number of signal events used, 0 = ALL
                                               "nTrain_Background=50000", # Number of background events, 0 = ALL
                                               "nTest_Signal=50000",     # Number of signal events used, 0 = ALL
                                               "nTest_Background=50000", # Number of background events, 0 = ALL
                                               "SplitMode=Random",    # How are events chosen to be used for either training or testing
                                               "NormMode=NumEvents",  # Integral of datasets is given by number of events
                                                                      #   (could e.g. also be sum of weights or simply defined to be 1)
                                               "!V"                   # Don't print everything (i.e. not verbose) 
                                               ]))

    if MVAmethod == "BDT":
        method = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_"+label,"!H:!V:NTrees=2000:MinNodeSize=0.05:MaxDepth=6:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")
    elif MVAmethod == "MLP":
        method = factory.BookMethod(ROOT.TMVA.Types.kMLP, "N_Nmin1_"+label, "H:V:VarTransform=Norm:NCycles=3000:HiddenLayers=N:TestRate=10")
    elif MVAmethod == "CUT":
        method = factory.BookMethod(ROOT.TMVA.Types.kCuts, "MC_"+label, "!H:!V:FitMethod=MC:EffSel:SampleSize=8000000:VarProp=FSmart")
    elif MVAmethod == "ALL":
        method = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_"+label,"!H:!V:NTrees=2000:MinNodeSize=0.5:MaxDepth=6:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")
        method = factory.BookMethod(ROOT.TMVA.Types.kMLP, "N_Nmin1_"+label, "H:V:VarTransform=Norm:NCycles=3000:HiddenLayers=N:TestRate=10")
        method = factory.BookMethod(ROOT.TMVA.Types.kCuts, "MC_"+label, "!H:!V:FitMethod=MC:EffSel:SampleSize=8000000:VarProp=FSmart")
  
      
    else :
        print "MVA method must be BDT, MLP, CUT or ALL."
        sys.exit()

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    file_MVA.Close()

def MVA_out_in_tree(files, treeName, discriList, xmlFile, MVAname, outFileName):   

    chain = ROOT.TChain(treeName)
    for file in files:
        chain.Add(file)
        
    file_withBDTout = ROOT.TFile(outFileName, "recreate")
    tree_withBDTout = chain.CloneTree(0)
    print "Number of input tree entries : ", chain.GetEntries()
    
    leave_BDTout = "MVA_"+MVAname
    BDT_out = array('d',[0])
    tree_withBDTout.Branch(leave_BDTout, BDT_out, leave_BDTout+"/D")    

    reader = ROOT.TMVA.Reader()

    dict_variableName_Array = {variable : array('f', [0]) for variable in discriList}
    for var in discriList :
        reader.AddVariable(var, dict_variableName_Array[var])

    reader.BookMVA(MVAname, xmlFile)

    for entry in xrange(chain.GetEntries()):
        chain.GetEntry(entry)
        for var in discriList :
            dict_variableName_Array[var][0] = getattr(chain, var)
        BDT_out[0] = reader.EvaluateMVA(MVAname)
        tree_withBDTout.Fill()
    print "Number of output tree entries : ",tree_withBDTout.GetEntries()
    tree_withBDTout.Write()
    file_withBDTout.Close()
    print "Output file : ", outFileName, " written."

def evaluate_BDT(bkgTree, sigTree, discriList, MVAname):     # TO BE FIXED (from an old code) 

    file_proc1 = ROOT.TFile(bkgTree)    
    file_proc2 = ROOT.TFile(sigTree)    
    
    tree_proc2=file_proc2.Get("Event")
    tree_proc1=file_proc1.Get("Event")
    
    Nproc2=float(tree_proc2.GetEntries())
    Nproc1=float(tree_proc1.GetEntries())
    proc2_weight=1/Nproc2
    proc1_weight=1/Nproc1
       
    reader = ROOT.TMVA.Reader()
    
    var_discri1 = array('f',[0]) 
    reader.AddVariable(discri1,var_discri1)
    var_discri2 = array('f',[0]) 
    reader.AddVariable(discri2,var_discri2)
    
    reader.BookMVA("BDT_"+label,"weights/BDT_"+label+".weights.xml")    
    
    histo_proc1_BDT_out=ROOT.TH1F("histo_proc1_BDT_out","histo_proc1_BDT_out",100,-1,1)
    histo_proc2_BDT_out=ROOT.TH1F("histo_proc2_BDT_out","histo_proc2_BDT_out",100,-1,1)
    histo_proc2_BDT_out.SetLineColor(ROOT.kRed)
     
    for entry in xrange(tree_proc1.GetEntries()):
        tree_proc1.GetEntry(entry)
        var_discri1[0] = getattr(tree_proc1,discri1)
        var_discri2[0] = getattr(tree_proc1,discri2)
        histo_proc1_BDT_out.Fill(reader.EvaluateMVA("BDT_"+label))
        
    
    for entry in xrange(tree_proc2.GetEntries()):
        tree_proc2.GetEntry(entry)
        var_discri1[0]= getattr(tree_proc2,discri1)
        var_discri2[0]= getattr(tree_proc2,discri2)
        histo_proc2_BDT_out.Fill(reader.EvaluateMVA("BDT_"+label))
    
    legend = ROOT.TLegend(0.61,0.67,0.76,0.82)
    legend.AddEntry(histo_proc1_BDT_out,"Proc1")
    legend.AddEntry(histo_proc2_BDT_out,"Proc2") #rightarrow WWbb");
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    
    
    
    canvasName = "BDTout"
    xlabel = "BDT output"                      #"HH efficiency"
    ylabel = "Arbitrary Scale"   #"t#bar{t} efficiency"
    leftText = "First Try for a MIS (Delphes), #sqrt{s}=14 TeV, NoPU"
    rightText = "WW #rightarrow l#nul#nu"
    format="png"
    directory = "../images/BDT/"
    
    drawDoublehisto(histo_proc1_BDT_out,histo_proc2_BDT_out,canvasName,xlabel,ylabel,legend,leftText,rightText,format,directory,0)


