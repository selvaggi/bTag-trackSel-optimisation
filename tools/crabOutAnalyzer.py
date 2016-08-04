import ROOT
from drawCanvas import *
import copy
from array import array
import math


def isSelectedTrack(HitPix=2, HitAll=8, IP2D=0.2, Pt=1, Chi2=5, dz=17, Length=5, Dist=0.07):  #default values are the value requested for selectedTrack in bTag code
    return HitPix >= 2 and HitAll >= 8 and abs(IP2D) < 0.2 and Pt > 1 and Chi2 < 5 and abs(dz) < 17 and Length < 5 and abs(Dist) < 0.07  # bTag current selection
    #return HitPix >= 2 and HitAll >= 8 and abs(IP2D) < 0.2 and Pt > 1 and Chi2 < 5 and abs(dz) < 17# bTag current selection
    
    #return HitPix >= 0 and HitAll >= 0 and abs(IP2D) < 0.2 and Pt > 0 and Chi2 < 5 and abs(dz) < 17 and Length < 5 and abs(Dist) < 0.07  # Looser selection
    #return HitPix >= 1 and HitAll >= 6 and abs(IP2D) < 0.2 and Pt > 0.5 and Chi2 < 5 and abs(dz) < 10 and Length < 5 and Dist < 0.07 # Looser selection
    #return Dist < 0.07    # Selection applied only on the "Jet vs track" variable
    #return True # no selection 

def isSignalJet(jetGenPT, jetFlavour):
    return jetGenPT>8 and abs(jetFlavour)==5
     
def isBkgJet(jetGenPT, jetFlavour):
    return jetGenPT<8 

def isNonBJet(jetGenPT, jetFlavour):
    return jetGenPT>8 and abs(jetFlavour)!=5

def isLightJet(jetGenPT, jetFlavour):
    return jetGenPT>8 and abs(jetFlavour)!=5 and abs(jetFlavour)!=4

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
    nPuTrack_beforeSel = 0
    nBkgTrack_afterSel = 0
    nTrackAfterSel_bJet = 0
    nBtrackAfterSel_bJet = 0
    nFakeAfterSel_nonBjet = 0
    nTrackAfterSel_nonBjet = 0
    nBtrackBeforeSel_bJet = 0
    nFakeTrack_nonBjet = 0
    nFakeTrack_beforeSel = 0
    nCtrackBeforeSel_bJet = 0
    nBkgTrack_beforeSel = 0
    nBtrackBeforeSel_NonBJet = 0
    nPuTrack_beforeSel_NonBJet = 0
    nBkgTrack_beforeSel_NonBJet = 0
    nFakeTrack_beforeSel_NonBJet = 0
    nCtrackBeforeSel_NonBJet = 0
   
    nBjets = 0
    nLjets = 0
   
    nFakesPerJet = 0
    
    nEntries = tree.GetEntries()
    print "Will loop over ", nEntries, " events."
    
    hCSV_nFakes_sig = ROOT.TH2D("hCSV_nFakes_Sig", "hCSV_nFakes_Sig", 5, 0, 5, 15, 0, 1.5)
    hCSV_nFakes_bkg = ROOT.TH2D("hCSV_nFakes_Bkg", "hCSV_nFakes_Bkg", 5, 0, 5, 15, 0, 1.5)
     
    trackHistList = []
    trackPVList = []
    for entry in xrange(nEntries):
        tree.GetEntry(entry)
        for jetInd in xrange(tree.nJet):
        
	    if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]) :
	        nBjets += 1
	 	  
	    if isLightJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]) :
	        nLjets += 1
	   
	    nFakesPerLightJet = 0
	    nFakesPerBJet = 0
	    nSelected = 0
	    
	    for track in xrange(tree.Jet_nFirstTrack[jetInd], tree.Jet_nLastTrack[jetInd]):
                  trackHist = tree.Track_history[track]
                  stringTrackHist = str(trackHist)
                  trackHistList.append(trackHist)
                  trackPVList.append(tree.Track_PV[track])
                
		#if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_IP2D[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                #if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track], tree.Track_dxy[track], tree.Track_pt[track], tree.Track_chi2[track], tree.Track_dz[track], tree.Track_length[track], tree.Track_dist[track]):
                  nSelected += 1
		   
	          if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]) :
                    nSigTrack_beforeSel += 1
                     
		    # is coming from C weak decay, not B and  is signal
		    if (stringTrackHist[len(stringTrackHist)-2] == str(1) and stringTrackHist[len(stringTrackHist)-10] == str(1) and stringTrackHist[len(stringTrackHist)-1] == str(0) ) :
		            nCtrackBeforeSel_bJet += 1
		   
		    # is coming from B weak decay and is signal
		    if (stringTrackHist[len(stringTrackHist)-1] == str(1) and stringTrackHist[len(stringTrackHist)-10] == str(1)) :
                            nBtrackBeforeSel_bJet += 1
                            for variable in dict_variableName_Leaves.keys() :
                                dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                            sigTree.Fill()
                    
		    # is fake or pu
	            elif trackHist < 1e9 :
		       for variable in dict_variableName_Leaves.keys() :
                           dict_variableName_Leaves[variable][0] = getattr(tree, variable)[track]
                       bkgTree.Fill()
                       nFakesPerBJet += 1
	   
		       # is fake 
	               if (len(stringTrackHist)>=8 and stringTrackHist[len(stringTrackHist)-8] == str(1)) :
		         nFakeTrack_beforeSel += 1
                     
		       # is pu
		       else: 
                          nPuTrack_beforeSel += 1
                
		   
	          elif isLightJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]) :
		     nBkgTrack_beforeSel_NonBJet += 1
                 
		     # is coming from C weak decay, not B and  is signal
		     if (stringTrackHist[len(stringTrackHist)-2] == str(1) and stringTrackHist[len(stringTrackHist)-10] == str(1) and stringTrackHist[len(stringTrackHist)-1] == str(0) ) :
		         nCtrackBeforeSel_NonBJet += 1
		 
		     # is coming from B weak decay and is signal
		     if (stringTrackHist[len(stringTrackHist)-1] == str(1) and stringTrackHist[len(stringTrackHist)-10] == str(1)) :
                         nBtrackBeforeSel_NonBJet +=1
	                 
		     # is non-signal and non-fake (i.e is pile-up)  
		     elif trackHist < 1e9 :
		        # is fake 
			nFakesPerLightJet += 1
			if (len(stringTrackHist)>=8 and stringTrackHist[len(stringTrackHist)-8] == str(1)) :
		           nFakeTrack_beforeSel_NonBJet += 1
	              # is pu
	             else: 
                           nPuTrack_beforeSel_NonBJet += 1
           
	    if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]) and  nSelected > 0 :
	        #hCSV_nFakes_sig.Fill(nFakesPerBJet/float(nSelected),tree.Jet_CombIVF[jetInd])
	        hCSV_nFakes_sig.Fill(nFakesPerBJet,tree.Jet_CombIVF[jetInd])
	       	
	    elif isLightJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd])  and  nSelected > 0 :
	        hCSV_nFakes_bkg.Fill(nFakesPerLightJet,tree.Jet_CombIVF[jetInd])
		   
   
    print "Average number of B track per b jet (gen pt >8) : {} ".format(round(nBtrackBeforeSel_bJet/float(nBjets),3))
    print "Average number of C tracks per b jet (gen pt >8) : {} ".format(round(nCtrackBeforeSel_bJet/float(nBjets),3))
    print "Average number of Pu track per b jet (gen pt >8) : {} ".format(round(nPuTrack_beforeSel/float(nBjets),3))
    print "Average number of fake track per b jet (gen pt >8) : {} ".format(round(nFakeTrack_beforeSel/float(nBjets),3))
    print "Average number of tracks per b jet (gen pt >8) : {} ".format(round(nSigTrack_beforeSel/float(nBjets),3))
     
    print "Percentage of B track in b jet (gen pt >8) : {} ".format(round(100*nBtrackBeforeSel_bJet/float(nSigTrack_beforeSel),3))
    print "Percentage of Pu track in (b jet && gen pt >8) : {} ".format(round(100*nPuTrack_beforeSel/float(nSigTrack_beforeSel),3))
    print "Percentage of Fake track in (b jet && gen pt >8) : {} ".format(round(100*nFakeTrack_beforeSel/float(nSigTrack_beforeSel),3))
   
    
    print "Average number of B track per light jet (gen pt >8) : {} ".format(round(nBtrackBeforeSel_NonBJet/float(nLjets),3))
    print "Average number of Pu track per light jet (gen pt >8) : {} ".format(round(nPuTrack_beforeSel_NonBJet/float(nLjets),3))
    print "Average number of fake track per light jet (gen pt >8) : {} ".format(round(nFakeTrack_beforeSel_NonBJet/float(nLjets),3))
    print "Average number of tracks per light jet (gen pt >8) : {} ".format(round(nBkgTrack_beforeSel_NonBJet/float(nLjets),3))
   
    print "Percentage of B track in light jet (gen pt >8) : {} ".format(round(100*nBtrackBeforeSel_NonBJet/float(nBkgTrack_beforeSel_NonBJet),3))
    print "Percentage of Pu track in light jet (gen pt >8) : {} ".format(round(100*nPuTrack_beforeSel_NonBJet/float(nBkgTrack_beforeSel_NonBJet),3))
    print "Percentage of Fake track in light jet (gen pt >8): {} ".format(round(100*nFakeTrack_beforeSel_NonBJet/float(nBkgTrack_beforeSel_NonBJet),3))
   
    
     
    ## produce latex table
    
    #print "B decay & " , format(round(nBtrackBeforeSel_bJet/float(nBjets),2)) , "(" , format(round(100*nBtrackBeforeSel_bJet/float(nSigTrack_beforeSel),2))
    
    
    
    trackEff_hist_sig = ROOT.TH1D("trackEff_hist_sig", "trackEff_hist", 100, 0, 1)
    #trackEff_hist_sig.Fill(nSigTrack_afterSel/float(nSigTrack_beforeSel))
    outFile_sig = ROOT.TFile(outRootFileName_sig, "recreate")
    sigTree.Write()
    trackEff_hist_sig.Write()
    hCSV_nFakes_sig.Write()
    outFile_sig.Close()
    print outRootFileName_sig, "written."

    trackEff_hist_bkg = ROOT.TH1D("trackEff_hist_bkg", "trackEff_hist", 100, 0, 1)
    #trackEff_hist_bkg.Fill(nBkgTrack_afterSel/float(nBkgTrack_beforeSel))
    outFile_bkg = ROOT.TFile(outRootFileName_bkg, "recreate")
    bkgTree.Write()
    trackEff_hist_bkg.Write()
    hCSV_nFakes_bkg.Write()
    outFile_bkg.Close()
    print "% of BWeakDecay ", trackHistList.count(1e9+1)/float(len(trackHistList))
    print "% of CWeakDecay ", trackHistList.count(1e9+10)/float(len(trackHistList))
    print "% of BCWeakDecay ", trackHistList.count(1e9+11)/float(len(trackHistList))
    
    print "% of Signal ", trackHistList.count(1e9)/float(len(trackHistList))
    print "% of Fake ", trackHistList.count(10000000)/float(len(trackHistList))

    print outRootFileName_bkg, "written."
    #print "% of Nothing ", trackHistList.count(0)/float(len(trackHistList))
    #print "Mean ", len(trackHistList)/float(sum(trackHistList))
    #print "Track PV 0 " , trackPVList.count(0)/float(len(trackPVList))
