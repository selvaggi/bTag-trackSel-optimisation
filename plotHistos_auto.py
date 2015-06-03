import copy
import ROOT

from tools.drawCanvas import drawCanvas

# "Aliases"

lineStyle = 1
lineWidth = 2

grid = "xy"
xSize = 800
ySize = 600

flavours = [
        {
            "key": "Bjets",
            "filename": "Bjets",
            "title": "(b-jets)",
        },
        {
            "key": "Lightjets",
            "filename": "Lightjets",
            "title": "(light jets)",
        },
        {
            "key": "Cjets",
            "filename": "Cjets",
            "title": "(c-jets)",
        },
        {
            "key": "PUjets",
            "filename": "PUjets",
            "title": "(PU jets)",
        },
    ]

cuts = [
        {
            "name": "bTag cuts", # for legend
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetHistos_TC_btagCutsOnly.root",
            "color": ROOT.kBlue,
        },
        {
            "name": "Cuts + MVA>0.65",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT065.root",
            "color": ROOT.kMagenta+1,
        },
        {
            "name": "Cuts + MVA>0.7",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT07.root",
            "color": ROOT.kGreen+1,
        },
        {
            "name": "Cuts + MVA>0.75",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT075.root",
            "color": ROOT.kOrange,
        },
        {
            "name": "Cuts + MVA>0.8",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetHistos_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT08.root",
            "color": ROOT.kRed,
            },

    ]

histos = [
        {
            "key": "Jet_pt",
            "filename": "Jet_pt",
            "title": "Jet Pt",
            "xTitle": "Jet Pt (GeV)",
            "log": "",
            "rebin": 4,
        },
        {
            "key": "Jet_ntracks",
            "filename": "Jet_ntracks",
            "title": "Jet total number of tracks",
            "xTitle": "Jet_ntracks",
            "log": "",
            "rebin": 2,
        },
        {
            "key": "Jet_nseltracks",
            "filename": "Jet_nseltracks",
            "title": "Jet number of selected tracks",
            "xTitle": "Jet_nseltracks",
            "log": "",
        },
        {
            "key": "Jet_Ip_DiscrEff",
            "filename": "Jet_IPsig",
            "title": "Jet_IPsig",
            "xTitle": "Jet_IPsig",
            "log": "",
            "rebin": 2,
        },
        {
            "key": "TCHE_DiscrEff",
            "filename": "TCHE",
            "title": "TCHE discriminant",
            "xTitle": "TCHE",
            "log": "",
            "rebin": 2,
        },
        {
            "key": "TCHP_DiscrEff",
            "filename": "TCHP",
            "title": "TCHP discriminant",
            "xTitle": "TCHP",
            "log": "",
            "rebin": 2,
        },
    ]

# General configuration
runCfg = {
        "outFile": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/bTag-trackSel-optimisation/jetPlots.root",
        "printDir": "./jetPlots", # optional
        "formats": ["png"], # optional
        "batch": True, # optional
        }

# Will hold the canvases
canvasCfg = []

for histo in histos:

    for flav in flavours:

        myHists = []
        for cut in cuts:
            histCfg = {   
                    "file": cut["file"],
                    "key": flav["key"] + "/" + histo["key"],
                    "name": cut["name"],
                    "color": cut["color"],
                    "lineStyle": lineStyle, # Only used if "L" in "style" (default 1)
                    "lineWidth": lineWidth, # (default 1)
                }
            try:
                histCfg["rebin"] = histo["rebin"] # optional
                histCfg["xRange"] = histo["xRange"] # optional
            except KeyError:
                pass
            myHists.append(histCfg)

        myCanvas = {
                "name": histo["filename"] + "_" + flav["filename"], # Name of the canvas for the output ROOT/png/... files
                "xSize": xSize,
                "ySize": ySize,
                "title": histo["title"] + " " + flav["title"],
                "legPos": "tr", # t/b, l/r
                "grid": grid, # optional
                "log": histo["log"], # optional
                "xTitle": histo["xTitle"],
                "yTitle": "Arbitrary scale", # optional
                "norm": True,
                "hists": myHists,
            }
        canvasCfg.append(myCanvas)

# We're all set!

if __name__ == "__main__":
    drawCanvas(runCfg, canvasCfg, mode = "TH1")

