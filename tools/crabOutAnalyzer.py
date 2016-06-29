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

def plotFromCrabOut(rootFiles, treeDirectory, TrackVars, JetVars,  doPTreweight, outRootFileName):
    
    yAxisLabel = "Arbitrary Scale"
    leftText = "Phys14 QCD30-50 MuEnriched #sqrt{s}=13 TeV"
    rightText = ""
    format="png"
    imageDirectory = "./images/"

    ROOT.gROOT.SetBatch()
    # ouvre le rootfile, selectionne signal jet --> signal tracks, bkg jet --> bkg track, plot les variables dans TrackVars 
    tree = ROOT.TChain(treeDirectory)
    for file in rootFiles:
        tree.Add(file)
    
    nEntries = tree.GetEntries()
    nSigJet = 0
    nBkgJet = 0
    
    dict_histo_track_signal = { var: ROOT.TH1D(var+"1", var+"1", TrackVars[var]["bin"], TrackVars[var]["xmin"], TrackVars[var]["xmax"]) for var in TrackVars }
    dict_histo_track_bkg = { var: ROOT.TH1D(var+"2", var+"2", TrackVars[var]["bin"], TrackVars[var]["xmin"], TrackVars[var]["xmax"]) for var in TrackVars }
    dict_histo_jet_signal = { var: ROOT.TH1D(var+"1", var+"1", JetVars[var]["bin"], JetVars[var]["xmin"], JetVars[var]["xmax"]) for var in JetVars }
    dict_histo_jet_bkg = { var: ROOT.TH1D(var+"2", var+"2", JetVars[var]["bin"], JetVars[var]["xmin"], JetVars[var]["xmax"]) for var in JetVars }

    print "Will loop over ", nEntries, " events."
    
    for entry in xrange(nEntries):
        tree.GetEntry(entry)
        
        for jetInd in xrange(tree.nJet):
            
            if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):    
                nSigJet+=1
                
                for var in JetVars :
                    dict_histo_jet_signal[var].Fill(getattr(tree, JetVars[var]["name"])[jetInd])
                
                for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
                    if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                        for var in TrackVars :
                            dict_histo_track_signal[var].Fill(getattr(tree, TrackVars[var]["name"])[track])
            
            if isBkgJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]): 
                nBkgJet+=1
                
                for var in JetVars :
                    dict_histo_jet_bkg[var].Fill(getattr(tree, JetVars[var]["name"])[jetInd])
                
                for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
                    if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]): 
                        for var in TrackVars.keys() :
                            dict_histo_track_bkg[var].Fill(getattr(tree, TrackVars[var]["name"])[track])
    
    print "NsigJet : ", nSigJet, " N bkg jet : ", nBkgJet
    
    if doPTreweight : 
        
        print "Start pt reweighting so that pt spectrum in bkg matches the one of the signal."
        
        jetPt_ptRew2 = ROOT.TH1D("jetPt_ptRew2", "jetPt_ptRew2", JetVars["Jet_pt"]["bin"], JetVars["Jet_pt"]["xmin"], JetVars["Jet_pt"]["xmax"])
        dict_histo_track_ptRew_bkg = { var: ROOT.TH1D(var+"2_ptRew", var+"2_ptRew", TrackVars[var]["bin"], TrackVars[var]["xmin"], TrackVars[var]["xmax"]) for var in TrackVars }
        ratio = copy.deepcopy(dict_histo_jet_signal["Jet_pt"])
        dict_histo_jet_bkg["Jet_pt"].Scale( 1./dict_histo_jet_bkg["Jet_pt"].Integral() )    
        ratio.Scale( 1./ratio.Integral() )
        ratio.Divide( dict_histo_jet_bkg["Jet_pt"] )
        
        for entry in xrange(nEntries):
            tree.GetEntry(entry)
            for jetInd in xrange(tree.nJet):
                if isBkgJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):
                    ptWeight = ratio.GetBinContent(ratio.FindBin(tree.Jet_pt[jetInd])) 
                    jetPt_ptRew2.Fill(tree.Jet_pt[jetInd], ptWeight)
                    for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
                        if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]): 
                            for var in TrackVars.keys() :
                                dict_histo_track_ptRew_bkg[var].Fill(getattr(tree, TrackVars[var]["name"])[track], ptWeight)

    outRootFile = ROOT.TFile(outRootFileName, "recreate")
    myGstyle()

    for var in TrackVars.keys() :
            dict_histo_track_bkg[var].SetLineColor(ROOT.kRed)
            dict_histo_track_bkg[var].SetLineWidth(2)
            dict_histo_track_signal[var].SetLineWidth(2)

            try :
                    dict_histo_track_signal[var].Scale(1./float(dict_histo_track_signal[var].Integral()))
                    dict_histo_track_bkg[var].Scale(1./float(dict_histo_track_bkg[var].Integral()))
            except ZeroDivisionError :
                    print "Can not renormalize because of intergal = 0."
                    print dict_histo_track_signal[var].Integral()
                    print dict_histo_track_bkg[var].Integral()
            leg = ROOT.TLegend(0.61, 0.67, 0.76, 0.82)
            leg.AddEntry(dict_histo_track_signal[var], "b-jet Tracks")
            leg.AddEntry(dict_histo_track_bkg[var], "PU Tracks")
            leg.SetFillColor(0)
            leg.SetLineColor(0)


            drawDoublehisto(dict_histo_track_signal[var], dict_histo_track_bkg[var], var, var, yAxisLabel, leg, leftText, rightText, format, imageDirectory, 0)
            drawDoublehisto(dict_histo_track_signal[var], dict_histo_track_bkg[var], var, var, yAxisLabel, leg, leftText, rightText, format, imageDirectory, 1)

    for var in JetVars.keys() :
            dict_histo_jet_bkg[var].SetLineColor(ROOT.kRed)
            dict_histo_jet_bkg[var].SetLineWidth(2)
            dict_histo_jet_signal[var].SetLineWidth(2)

            try :
                    dict_histo_jet_signal[var].Scale(1./float(dict_histo_jet_signal[var].Integral()))
                    dict_histo_jet_bkg[var].Scale(1./float(dict_histo_jet_bkg[var].Integral()))
            except ZeroDivisionError :
                    print "Can not renormalize because of intergal = 0."
                    print dict_histo_jet_signal[var].Integral()
                    print dict_histo_jet_bkg[var].Integral()
            leg = ROOT.TLegend(0.61, 0.67, 0.76, 0.82)
            leg.AddEntry(dict_histo_jet_signal[var], "b-jet Tracks")
            leg.AddEntry(dict_histo_jet_bkg[var], "PU Tracks")
            leg.SetFillColor(0)
            leg.SetLineColor(0)


            drawDoublehisto(dict_histo_jet_signal[var], dict_histo_jet_bkg[var], var, var, yAxisLabel, leg, leftText, rightText, format, imageDirectory, 0)
            drawDoublehisto(dict_histo_jet_signal[var], dict_histo_jet_bkg[var], var, var, yAxisLabel, leg, leftText, rightText, format, imageDirectory, 1)

    if doPTreweight : 
        for var in TrackVars.keys() :
            dict_histo_track_ptRew_bkg[var].SetLineColor(ROOT.kRed)
            dict_histo_track_ptRew_bkg[var].SetLineWidth(2)

            try :
                dict_histo_track_ptRew_bkg[var].Scale(1./float(dict_histo_track_ptRew_bkg[var].Integral()))
            except ZeroDivisionError :
                print "Can not renormalize because of intergal = 0."
                print dict_histo_track_signal[var].Integral()
                print dict_histo_track_ptRew_bkg[var].Integral()
            leg = ROOT.TLegend(0.61, 0.67, 0.76, 0.82)
            leg.AddEntry(dict_histo_track_signal[var], "b-jet Tracks")
            leg.AddEntry(dict_histo_track_ptRew_bkg[var], "PU Tracks")
            leg.SetFillColor(0)
            leg.SetLineColor(0)


            drawDoublehisto(dict_histo_track_signal[var], dict_histo_track_ptRew_bkg[var], var+"_ptRew", var+"_ptRew", yAxisLabel, leg, leftText, rightText, format, imageDirectory, 0)
            drawDoublehisto(dict_histo_track_signal[var], dict_histo_track_ptRew_bkg[var], var+"_ptRew", var+"_ptRew", yAxisLabel, leg, leftText, rightText, format, imageDirectory, 1)

        jetPt_ptRew2.Scale(1./float(jetPt_ptRew2.Integral()))
        jetPt_ptRew2.SetLineColor(ROOT.kRed)
        jetPt_ptRew2.SetLineWidth(2)
        leg = ROOT.TLegend(0.61, 0.67, 0.76, 0.82)
        leg.AddEntry(dict_histo_track_signal[var], "b-jet Tracks")
        leg.AddEntry(dict_histo_track_ptRew_bkg[var], "PU Tracks")
        leg.SetFillColor(0)
        leg.SetLineColor(0)
        drawDoublehisto(dict_histo_jet_signal["Jet_pt"], jetPt_ptRew2, "Jet_pt_Rew", "Jet_pt_Rew", yAxisLabel, leg, leftText, rightText, format, imageDirectory, 0)
        
    outRootFile.Close()

def createTreeSigBkg(rootFiles, treeDirectory, trackVariablesToStore, outRootFileName_sig, outRootFileName_bkg) :
    # Create two trees, one with signal and one with background tracks
    # Open the rootfile, select signal jet --> signal tracks, bkg jet --> bkg track.

    # file = ROOT.TFile(rootFile, "read")
    tree = ROOT.TChain(treeDirectory)
    for file in rootFiles:
        tree.Add(file)

    sigTree = ROOT.TTree("trackTree", "sigTrackTree")
    bkgTree = ROOT.TTree("trackTree", "bkgTrackTree")

    dict_variableName_Leaves = {variable: array('d', [0]) for variable in trackVariablesToStore }
    for variable in trackVariablesToStore: 
        sigTree.Branch(variable, dict_variableName_Leaves[variable], variable + "/D")
        bkgTree.Branch(variable, dict_variableName_Leaves[variable], variable + "/D")

    nSigTrack_beforeSel = 0
    nSigTrack_afterSel = 0
    nBkgTrack_beforeSel = 0
    nBkgTrack_afterSel = 0

    nEntries = tree.GetEntries()
    print "Will loop over ", nEntries, " events."
    
    for entry in xrange(nEntries):
        tree.GetEntry(entry)
        
        for jetInd in xrange(tree.nJet):
            #jet_4v = ROOT.TLorentzVector()
            #jet_4v.SetPtEtaPhiM(tree.Jet_pt[jetInd], tree.Jet_eta[jetInd], tree.Jet_phi[jetInd], 0) # tree.Jet_mass[jetInd])
            if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):
                for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
                    nSigTrack_beforeSel += 1

                    #track_4v = ROOT.TLorentzVector()
                    #track_4v.SetPtEtaPhiE(tree.Track_pt[track], tree.Track_eta[track], tree.Track_phi[track], 0)# tree.Track_p[track])
                    #jetTrack_DR = track_4v.DeltaR(jet_4v)
                    if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                        nSigTrack_afterSel += 1
                        for variable in dict_variableName_Leaves.keys() :
                            dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                        sigTree.Fill()
            
            if isBkgJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):
                for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
                    nBkgTrack_beforeSel += 1
                    if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                        nBkgTrack_afterSel += 1
                        for variable in dict_variableName_Leaves.keys() :
                            dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                        bkgTree.Fill()
   
    print "Signal:     {} track selection efficiency.".format(nSigTrack_afterSel/float(nSigTrack_beforeSel))
    print "Background: {} track selection efficiency.".format(nBkgTrack_afterSel/float(nBkgTrack_beforeSel))

    trackEff_hist_sig = ROOT.TH1D("trackEff_hist_sig", "trackEff_hist", 100, 0, 1)
    trackEff_hist_sig.Fill(nSigTrack_afterSel/float(nSigTrack_beforeSel))
    outFile_sig = ROOT.TFile(outRootFileName_sig, "recreate")
    sigTree.Write()
    trackEff_hist_sig.Write()
    outFile_sig.Close()
    print outRootFileName_sig, "written."

    trackEff_hist_bkg = ROOT.TH1D("trackEff_hist_bkg", "trackEff_hist", 100, 0, 1)
    trackEff_hist_bkg.Fill(nBkgTrack_afterSel/float(nBkgTrack_beforeSel))
    outFile_bkg = ROOT.TFile(outRootFileName_bkg, "recreate")
    bkgTree.Write()
    trackEff_hist_bkg.Write()
    outFile_bkg.Close()
    print outRootFileName_bkg, "written."

def createTreeSigBkg_trackHist(rootFiles, treeDirectory, trackVariablesToStore, outRootFileName_sig, outRootFileName_bkg) :

    tree = ROOT.TChain(treeDirectory)
    for file in rootFiles:
        tree.Add(file)

    sigTree = ROOT.TTree("trackTree", "sigTrackTree")
    bkgTree = ROOT.TTree("trackTree", "bkgTrackTree")

    dict_variableName_Leaves = {variable: array('d', [0]) for variable in trackVariablesToStore }
    for variable in trackVariablesToStore: 
        sigTree.Branch(variable, dict_variableName_Leaves[variable], variable + "/D")
        bkgTree.Branch(variable, dict_variableName_Leaves[variable], variable + "/D")

    nTrack_beforeBcriteria = 0
    nSigTrack_beforeSel = 0
    nSigTrack_afterSel = 0
    nTrack_beforeFakeCriteria = 0
    nBkgTrack_beforeSel = 0
    nBkgTrack_afterSel = 0
    nTrackAfterSel_bJet = 0
    nBtrackAfterSel_bJet = 0
    nFakeAfterSel_nonBjet = 0
    nTrackAfterSel_nonBjet = 0
    nBtrackBeforeSel_bJet = 0
    nFakeTrack_nonBjet = 0

    nEntries = tree.GetEntries()
    print "Will loop over ", nEntries, " events."
    
    trackHistList = []
    trackPVList = []
    for entry in xrange(nEntries):
        tree.GetEntry(entry)
        for jetInd in xrange(tree.nJet):
          #if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):
          #if isBkgJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):

            #jet_4v = ROOT.TLorentzVector()
            #jet_4v.SetPtEtaPhiM(tree.Jet_pt[jetInd], tree.Jet_eta[jetInd], tree.Jet_phi[jetInd], 0) # tree.Jet_mass[jetInd])
            for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
             #if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                trackHist = tree.Track_history[track]
                stringTrackHist = str(trackHist)
                trackHistList.append(trackHist)
                trackPVList.append(tree.Track_PV[track])

                #track_4v = ROOT.TLorentzVector()
                #track_4v.SetPtEtaPhiE(tree.Track_pt[track], tree.Track_eta[track], tree.Track_phi[track], 0)# tree.Track_p[track])
                #jetTrack_DR = track_4v.DeltaR(jet_4v)
                if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]) :
                    nSigTrack_beforeSel += 1
                    if (stringTrackHist[len(stringTrackHist)-1] == str(1)) :
                    #if trackHist == 1 :
                        #nBtrackBeforeSel_bJet += 1
                        #if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                            #nTrackAfterSel_bJet += 1
                            #nTrack_beforeBcriteria += 1 
                            nBtrackAfterSel_bJet += 1
                            #nSigTrack_beforeSel += 1
                            #nSigTrack_afterSel += 1
                            for variable in dict_variableName_Leaves.keys() :
                                dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                            sigTree.Fill()
                else : 
                    #nTrack_beforeFakeCriteria += 1
                    nBkgTrack_beforeSel += 1
                    if trackHist >= 10000000 and trackHist < 100000000 :
                        #nFakeTrack_nonBjet += 1
                        #if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                        #nBkgTrack_beforeSel += 1
                            #nTrackAfterSel_nonBjet += 1
                            nFakeAfterSel_nonBjet += 1
                            #nBkgTrack_afterSel += 1
                            for variable in dict_variableName_Leaves.keys() :
                                dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                            bkgTree.Fill()
   
    #print "Signal:     {} track selection efficiency.".format(nSigTrack_afterSel/float(nSigTrack_beforeSel))
    #print "Percentage of B track in b jet (gen pt >8) : {} ".format(nBtrackBeforeSel_bJet/float(nSigTrack_beforeSel))
    #print "Percentage of B track kept after selection : {} ".format(nBtrackAfterSel_bJet/float(nBtrackBeforeSel_bJet))
    #print "Percentage of bkg track kept after selection : {} ".format(nBkgTrack_afterSel/float(nBkgTrack_beforeSel))
    #print "Background: {} track selection efficiency.".format(nBkgTrack_afterSel/float(nBkgTrack_beforeSel))
    #print "Percentage of fake track in !(b jet && gen pt >8) after sel : {} ".format(nFakeAfterSel_nonBjet/float(nTrackAfterSel_nonBjet))
    #print "Percentage of fake track in !(b jet && gen pt >8) : {} ".format(nFakeTrack_nonBjet/float(nBkgTrack_beforeSel))
    #print "Percentage of fake track in !(b jet && gen pt >8) kept after selection : {} ".format(nFakeAfterSel_nonBjet/float(nFakeTrack_nonBjet))

    trackEff_hist_sig = ROOT.TH1D("trackEff_hist_sig", "trackEff_hist", 100, 0, 1)
    #trackEff_hist_sig.Fill(nSigTrack_afterSel/float(nSigTrack_beforeSel))
    outFile_sig = ROOT.TFile(outRootFileName_sig, "recreate")
    sigTree.Write()
    trackEff_hist_sig.Write()
    outFile_sig.Close()
    print outRootFileName_sig, "written."

    trackEff_hist_bkg = ROOT.TH1D("trackEff_hist_bkg", "trackEff_hist", 100, 0, 1)
    #trackEff_hist_bkg.Fill(nBkgTrack_afterSel/float(nBkgTrack_beforeSel))
    outFile_bkg = ROOT.TFile(outRootFileName_bkg, "recreate")
    bkgTree.Write()
    trackEff_hist_bkg.Write()
    outFile_bkg.Close()
    print "% of BWeakDecay ", trackHistList.count(1)/float(len(trackHistList))
    print "% of Fake ", trackHistList.count(10000000)/float(len(trackHistList))
    print "% of PU ", trackHistList.count(1000000000)/float(len(trackHistList))
    print outRootFileName_bkg, "written."
    #print "% of Nothing ", trackHistList.count(0)/float(len(trackHistList))
    #print "Mean ", len(trackHistList)/float(sum(trackHistList))
    #print "Track PV 0 " , trackPVList.count(0)/float(len(trackPVList))
