from ROOT import TFile, gROOT, TH1D, kRed, TLegend
from tools.drawCanvas import *
import os

gROOT.SetBatch()

absolutePath = "/home/fynu/bfrancois/MyCMSSWcode/bTag/bTag_track_optimisation/"
patternDirectory = absolutePath + "SIGTrackTree_track_hist_BfrombVSFake_SELTrackSel.root"  #"SIGTrackTree_track_hist_trackFromBVStrackNonbJet_SELTrackSel.root" #"/SIGTrackTree_SELTrackSel.root"
trackSelection = "noBIS"   #"bTag_zIP_abs"
sample1 = "sig"
sample2 = "bkg"  # will be in red
treeName = "trackTree"
doPTreweight = False

#File1 = patternDirectory.replace("SIG",sample1).replace("SEL",trackSelection)
#File2 = patternDirectory.replace("SIG",sample2).replace("SEL",trackSelection)

File1 = "sigTrackTree_bTag_zIP_absTrackSel.root"
File2 = "bkgTrackTree_bTag_zIP_absTrackSel.root"

yAxisLabel = "Arbitrary Scale"
leftText = "QCD Pt 50-80 recodebug, Asympt25ns, #sqrt{s}=13 TeV"
rightText = ""
format = "png"
outputDirectory = "./BfrombVSFake_"+trackSelection+"TrackSel/" #"./trackFromBVStrackNonbJet_"+trackSelection+"TrackSel/"  #"./BfrombVSFake_"+trackSelection+"TrackSel/"
outFile = outputDirectory+"/compare_"+sample1+"_"+sample2+"_trackVariables"+trackSelection+"TrackSel.root"

if not os.path.exists(outputDirectory) :
    os.system("mkdir "+outputDirectory)

VarsNoSel = {

    "Track_dxy":{"name":"Track_dxy","title":"Track_dxy","bin":2000,"xmin":-0.5,"xmax":0.5},
    "Track_dz":{"name":"Track_dz","title":"Track_dz","bin":2000,"xmin":-50,"xmax":50},
    #"Track_zIP":{"name":"Track_zIP","title":"Track_zIP","bin":1000,"xmin":-30,"xmax":30},
    "Track_length":{"name":"Track_length","title":"Track_length","bin":1000,"xmin":-1,"xmax":6},
    "Track_dist":{"name":"Track_dist","title":"Track_dist","bin":1000,"xmin":-0.3,"xmax":0.01},
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

VarsbTagSel = {

    "Track_dxy":{"name":"Track_dxy","title":"Track_dxy","bin":200,"xmin":-0.5,"xmax":0.5},
    "Track_dz":{"name":"Track_dz","title":"Track_dz","bin":200,"xmin":-50,"xmax":50},
    #"Track_zIP":{"name":"Track_zIP","title":"Track_zIP","bin":100,"xmin":-30,"xmax":30},
    "Track_length":{"name":"Track_length","title":"Track_length","bin":100,"xmin":-1,"xmax":6},
    "Track_dist":{"name":"Track_dist","title":"Track_dist","bin":100,"xmin":-0.06,"xmax":0.01},
    "Track_IP2D":{"name":"Track_IP2D","title":"Track_IP2D","bin":200,"xmin":-0.5,"xmax":0.5},
    "Track_IP2Dsig":{"name":"Track_IP2Dsig","title":"Track_IP2Dsig","bin":200,"xmin":-100,"xmax":100},
    "Track_IP2Derr":{"name":"Track_IP2Derr","title":"Track_IP2Derr","bin":200,"xmin":0,"xmax":0.4},
    "Track_IP":{"name":"Track_IP","title":"Track_IP","bin":200,"xmin":-10,"xmax":10},
    "Track_IPerr":{"name":"Track_IPerr","title":"Track_IPerr","bin":200,"xmin":0,"xmax":0.2},
    "Track_IPsig":{"name":"Track_IPsig","title":"Track_IPsig","bin":200,"xmin":-200,"xmax":200},
    "Track_pt":{"name":"Track_pt","title":"Track_pt","bin":100,"xmin":0,"xmax":10},
    "Track_eta":{"name":"Track_eta","title":"Track_eta","bin":20,"xmin":-3,"xmax":3},
    "Track_chi2":{"name":"Track_chi2","title":"Track_chi2","bin":100,"xmin":0,"xmax":5.1},
    "Track_nHitPixel":{"name":"Track_nHitPixel","title":"Track_nHitPixel","bin":10,"xmin":0,"xmax":10},
    "Track_nHitAll":{"name":"Track_nHitAll","title":"Track_nHitAll","bin":35,"xmin":0,"xmax":35},
    "Track_category":{"name":"Track_category","title":"Track_category","bin":12,"xmin":-2,"xmax":10},
    "Track_PV":{"name":"Track_PV","title":"Track_PV","bin":16,"xmin":-1,"xmax":15}
    
}

Vars = VarsbTagSel
if trackSelection == "no":
    Vars = VarsNoSel

dict_histo1 = {var:TH1D(var+"1",var+"1",Vars[var]["bin"],Vars[var]["xmin"],Vars[var]["xmax"]) for var in Vars}
dict_histo2 = {var:TH1D(var+"2",var+"2",Vars[var]["bin"],Vars[var]["xmin"],Vars[var]["xmax"]) for var in Vars}


rootFile1 = TFile(File1,"read")
tree1 = rootFile1.Get(treeName)
rootFile2 = TFile(File2,"read")
tree2 = rootFile2.Get(treeName)

outRootFile = TFile(outFile,"recreate")

for entry in xrange(tree1.GetEntries()) :
    tree1.GetEntry(entry)
    for var in Vars.keys() :
        dict_histo1[var].Fill(getattr(tree1,Vars[var]["name"]))

for entry in xrange(tree2.GetEntries()) :
    tree2.GetEntry(entry)
    for var in Vars.keys() :
        dict_histo2[var].Fill(getattr(tree2,Vars[var]["name"]))


myBTGStyle()

for var in Vars.keys() : 
    dict_histo1[var].SetLineWidth(2)
    dict_histo2[var].SetLineWidth(2)
    dict_histo2[var].SetLineColor(ROOT.kRed)
    try : 
        dict_histo1[var].Scale(1./float(dict_histo1[var].Integral()))
        dict_histo2[var].Scale(1./float(dict_histo2[var].Integral()))
    except ZeroDivisionError :
        print "Can not renormalize because of integral = 0." 
        print dict_histo1[var].Integral()
        print dict_histo2[var].Integral()
    leg = TLegend(0.61,0.64,0.86,0.89)
    leg.AddEntry(dict_histo1[var],"B hadron tracks")
    leg.AddEntry(dict_histo2[var],"Fake + PU tracks")
    leg.SetFillColor(0)
    leg.SetLineColor(0)


    drawDoublehisto(dict_histo1[var],dict_histo2[var],var,var,yAxisLabel,leg,leftText,rightText,format,outputDirectory,0)
    drawDoublehisto(dict_histo1[var],dict_histo2[var],var,var,yAxisLabel,leg,leftText,rightText,format,outputDirectory,1)

