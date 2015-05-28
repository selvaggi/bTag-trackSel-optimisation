import ROOT
from drawCanvas import *
import copy
from array import array

def isSelectedTrack(HitPix=2, HitAll=8, IP2D=0.2, Pt=1, Chi2=5, ZIP=17, Length=50, Dist=0.07):  #default values are the value requested for selectedTrack in bTag code
	return HitPix >= 2 and HitAll>=8 and IP2D<0.2 and Pt>1 and Chi2 < 5 and ZIP < 17 and Length <50 and Dist < 0.07  # bTag current selection
	#return HitPix >= 1 and HitAll>=6 and IP2D<0.3 and Pt>0.5 and Chi2 < 7 and ZIP < 20 and Length <60 and Dist < 0.1
	#return True  

def isSelectedTrack_forTree(ZIP=17, Dist=0.07):  #default values are the value requested for selectedTrack in bTag code
	#return HitPix >= 2 and HitAll>=8 and IP2D<0.2 and Pt>1 and Chi2 < 5 and ZIP < 17 and Length <50 and Dist < 0.07
	#return HitPix >= 1 and HitAll>=6 and IP2D<0.3 and Pt>0.5 and Chi2 < 7 and ZIP < 20 and Length <60 and Dist < 0.1
	return  ZIP < 17 and Dist < 0.07 
    #return True

def isSignalJet(jetGenPT, jetFlavour):
	return jetGenPT>8 and abs(jetFlavour)==5
	
def isBkgJet(jetGenPT, jetFlavour):
	return jetGenPT<8 

def plotFromCrabOut(rootFile, treeDirectory, TrackVars, JetVars,  doPTreweight, outRootFileName):
    
    yAxisLabel = "Arbitrary Scale"
    leftText = "Phys14 QCD30-50 MuEnriched #sqrt{s}=13 TeV"
    rightText = ""
    format=""
    imageDirectory = "./images/"

    ROOT.gROOT.SetBatch()
    # ouvre le rootfile, selectionne signal jet --> signal tracks, bkg jet --> bkg track, plot les variables dans TrackVars 
    file = ROOT.TFile(rootFile, "read")
    tree = file.Get(treeDirectory)
    nEntries = tree.GetEntries()
    nSigJet = 0
    nBkgJet = 0
    dict_histo_track_signal = {var:ROOT.TH1D(var+"1",var+"1",TrackVars[var]["bin"],TrackVars[var]["xmin"],TrackVars[var]["xmax"]) for var in TrackVars}
    dict_histo_track_bkg = {var:ROOT.TH1D(var+"2",var+"2",TrackVars[var]["bin"],TrackVars[var]["xmin"],TrackVars[var]["xmax"]) for var in TrackVars}
    dict_histo_jet_signal = {var:ROOT.TH1D(var+"1",var+"1",JetVars[var]["bin"],JetVars[var]["xmin"],JetVars[var]["xmax"]) for var in JetVars}
    dict_histo_jet_bkg = {var:ROOT.TH1D(var+"2",var+"2",JetVars[var]["bin"],JetVars[var]["xmin"],JetVars[var]["xmax"]) for var in JetVars}

    print "Will loop over ", nEntries, " events."
    for entry in  xrange(nEntries):
        tree.GetEntry(entry)
        for jetInd in xrange(len(tree.Jet_pt)):
            if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):	
                nSigJet+=1
                for var in JetVars :
                    dict_histo_jet_signal[var].Fill(getattr(tree,JetVars[var]["name"])[jetInd])
                for track in xrange(tree.Jet_nFirstTrack[jetInd],tree.Jet_nLastTrack[jetInd]):
                    if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track],tree.Track_IP2D[track],tree.Track_pt[track],tree.Track_chi2[track],tree.Track_zIP[track],tree.Track_length[track],tree.Track_dist[track]):
                        for var in TrackVars :
                            dict_histo_track_signal[var].Fill(getattr(tree,TrackVars[var]["name"])[track])
            if isBkgJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]): 
                nBkgJet+=1
                for var in JetVars :
                    dict_histo_jet_bkg[var].Fill(getattr(tree,JetVars[var]["name"])[jetInd])
                    for track in xrange(tree.Jet_nFirstTrack[jetInd],tree.Jet_nLastTrack[jetInd]):
                        if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track],tree.Track_IP2D[track],tree.Track_pt[track],tree.Track_chi2[track],tree.Track_zIP[track],tree.Track_length[track],tree.Track_dist[track]): 
                            for var in TrackVars.keys() :
                                dict_histo_track_bkg[var].Fill(getattr(tree,TrackVars[var]["name"])[track])
    print "NsigJet : ", nSigJet, " N bkg jet : ", nBkgJet
    if doPTreweight : 
        print "Start pt reweighting to match pt spectrum in both signal and bkg jets."
        jetPt_ptRew2 = ROOT.TH1D("jetPt_ptRew2","jetPt_ptRew2",JetVars["Jet_pt"]["bin"],JetVars["Jet_pt"]["xmin"],JetVars["Jet_pt"]["xmax"])
        dict_histo_track_ptRew_bkg = {var:ROOT.TH1D(var+"2_ptRew",var+"2_ptRew",TrackVars[var]["bin"],TrackVars[var]["xmin"],TrackVars[var]["xmax"]) for var in TrackVars}
        ratio = copy.copy(dict_histo_jet_signal["Jet_pt"])
        dict_histo_jet_bkg["Jet_pt"].Scale(1./float(dict_histo_jet_bkg["Jet_pt"].Integral()))	
        ratio.Scale(1./float(ratio.Integral()))
        ratio.Divide(dict_histo_jet_bkg["Jet_pt"])
        for entry in xrange(nEntries):
            tree.GetEntry(entry)
            for jetInd in xrange(len(tree.Jet_pt)):
                if isBkgJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):
                    ptWeight = ratio.GetBinContent(ratio.FindBin(tree.Jet_pt[jetInd])) 
                    jetPt_ptRew2.Fill(tree.Jet_pt[jetInd],ptWeight)
                    for track in xrange(tree.Jet_nFirstTrack[jetInd],tree.Jet_nLastTrack[jetInd]):
                        if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track],tree.Track_IP2D[track],tree.Track_pt[track],tree.Track_chi2[track],tree.Track_zIP[track],tree.Track_length[track],tree.Track_dist[track]): 
                            for var in TrackVars.keys() :
                                dict_histo_track_ptRew_bkg[var].Fill(getattr(tree,TrackVars[var]["name"])[track],ptWeight)

    outRootFile = ROOT.TFile(outRootFileName,"recreate")
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
            leg = ROOT.TLegend(0.61,0.67,0.76,0.82)
            leg.AddEntry(dict_histo_track_signal[var],"'Signal' Tracks")
            leg.AddEntry(dict_histo_track_bkg[var],"'Bkg' Tracks")
            leg.SetFillColor(0)
            leg.SetLineColor(0)


            drawDoublehisto(dict_histo_track_signal[var],dict_histo_track_bkg[var],var,var,yAxisLabel,leg,leftText,rightText,format,imageDirectory,0)
            drawDoublehisto(dict_histo_track_signal[var],dict_histo_track_bkg[var],var,var,yAxisLabel,leg,leftText,rightText,format,imageDirectory,1)

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
            leg = ROOT.TLegend(0.61,0.67,0.76,0.82)
            leg.AddEntry(dict_histo_jet_signal[var],"'Signal' Tracks")
            leg.AddEntry(dict_histo_jet_bkg[var],"'Bkg' Tracks")
            leg.SetFillColor(0)
            leg.SetLineColor(0)


            drawDoublehisto(dict_histo_jet_signal[var],dict_histo_jet_bkg[var],var,var,yAxisLabel,leg,leftText,rightText,format,imageDirectory,0)
            drawDoublehisto(dict_histo_jet_signal[var],dict_histo_jet_bkg[var],var,var,yAxisLabel,leg,leftText,rightText,format,imageDirectory,1)

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
            leg = ROOT.TLegend(0.61,0.67,0.76,0.82)
            leg.AddEntry(dict_histo_track_signal[var],"'Signal' Tracks")
            leg.AddEntry(dict_histo_track_ptRew_bkg[var],"'Bkg' Tracks")
            leg.SetFillColor(0)
            leg.SetLineColor(0)


            drawDoublehisto(dict_histo_track_signal[var],dict_histo_track_ptRew_bkg[var],var+"_ptRew",var+"_ptRew",yAxisLabel,leg,leftText,rightText,format,imageDirectory,0)
            drawDoublehisto(dict_histo_track_signal[var],dict_histo_track_ptRew_bkg[var],var+"_ptRew",var+"_ptRew",yAxisLabel,leg,leftText,rightText,format,imageDirectory,1)

        jetPt_ptRew2.Scale(1./float(jetPt_ptRew2.Integral()))
        jetPt_ptRew2.SetLineColor(ROOT.kRed)
        jetPt_ptRew2.SetLineWidth(2)
        leg = ROOT.TLegend(0.61,0.67,0.76,0.82)
        leg.AddEntry(dict_histo_track_signal[var],"'Signal' Tracks")
        leg.AddEntry(dict_histo_track_ptRew_bkg[var],"'Bkg' Tracks")
        leg.SetFillColor(0)
        leg.SetLineColor(0)
        drawDoublehisto(dict_histo_jet_signal["Jet_pt"],jetPt_ptRew2,"Jet_pt_Rew","Jet_pt_Rew",yAxisLabel,leg,leftText,rightText,format,imageDirectory,0)
		
    outRootFile.Close()

def createTreeSigBkg(rootFile, treeDirectory, trackVariablesToStore, outRootFileName_sig, outRootFileName_bkg) :
    # ouvre le rootfile, selectionne signal jet --> signal tracks, bkg jet --> bkg track , train MVA, donne une fonction
    #file = ROOT.TFile(rootFile, "read")

    tree = ROOT.TChain(treeDirectory)
    tree.Add(rootFile)

    sigTree = ROOT.TTree("trackTree","sigTrackTree")
    bkgTree = ROOT.TTree("trackTree","bkgTrackTree")

    listArrayVariables = []
    dict_variableName_listArrayLeaves = {variable : [array('d',[0]), variable+"/D" ] for variable in trackVariablesToStore }
    for variable in dict_variableName_listArrayLeaves.keys() :
        sigTree.Branch(variable, dict_variableName_listArrayLeaves[variable][0], dict_variableName_listArrayLeaves[variable][1])
        bkgTree.Branch(variable, dict_variableName_listArrayLeaves[variable][0], dict_variableName_listArrayLeaves[variable][1])

    nSigTrack_beforeSel = 0
    nSigTrack_afterSel = 0
    nBkgTrack_beforeSel = 0
    nBkgTrack_afterSel = 0

    nEntries = tree.GetEntries()
    print "Will loop over ", nEntries, " events."
    for entry in xrange(nEntries):
        tree.GetEntry(entry)
        for jetInd in xrange(len(tree.Jet_pt)):
            if isSignalJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):
                for track in xrange(tree.Jet_nFirstTrack[jetInd],tree.Jet_nLastTrack[jetInd]):
                    nSigTrack_beforeSel += 1
                    if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track],tree.Track_IP2D[track],tree.Track_pt[track],tree.Track_chi2[track],tree.Track_zIP[track],tree.Track_length[track],tree.Track_dist[track]):
                    #if isSelectedTrack_forTree(tree.Track_zIP[track],tree.Track_dist[track]):
                        nSigTrack_afterSel += 1
                        for variable in dict_variableName_listArrayLeaves.keys() :
                            dict_variableName_listArrayLeaves[variable][0][0] = getattr(tree, variable)[track]
                        sigTree.Fill()
            if isBkgJet(tree.Jet_genpt[jetInd], tree.Jet_flavour[jetInd]):
                for track in xrange(tree.Jet_nFirstTrack[jetInd],tree.Jet_nLastTrack[jetInd]):
                    nBkgTrack_beforeSel += 1
                    #if isSelectedTrack(tree.Track_nHitPixel[track], tree.Track_nHitAll[track],tree.Track_IP2D[track],tree.Track_pt[track],tree.Track_chi2[track],tree.Track_zIP[track],tree.Track_length[track],tree.Track_dist[track]):
                    #if isSelectedTrack_forTree(tree.Track_zIP[track],tree.Track_dist[track]):
                    if True :
                        nBkgTrack_afterSel += 1
                        for variable in dict_variableName_listArrayLeaves.keys() :
                            dict_variableName_listArrayLeaves[variable][0][0] = getattr(tree, variable)[track]
                        bkgTree.Fill()
    trackEff_hist_sig = ROOT.TH1D("trackEff_hist_sig","trackEff_hist",100,0,1)
    trackEff_hist_sig.Fill(nSigTrack_afterSel/float(nSigTrack_beforeSel))
    outFile_sig = ROOT.TFile(outRootFileName_sig,"recreate")
    sigTree.Write()
    trackEff_hist_sig.Write()
    outFile_sig.Close()
    print outRootFileName_sig, "written."

    trackEff_hist_bkg = ROOT.TH1D("trackEff_hist_bkg","trackEff_hist",100,0,1)
    trackEff_hist_bkg.Fill(nBkgTrack_afterSel/float(nBkgTrack_beforeSel))
    outFile_bkg = ROOT.TFile(outRootFileName_bkg,"recreate")
    bkgTree.Write()
    trackEff_hist_bkg.Write()
    outFile_bkg.Close()
    print outRootFileName_bkg, "written."

