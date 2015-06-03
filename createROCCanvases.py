import copy
import ROOT

from tools.drawCanvas import drawCanvas

# "Aliases"

drawStyle = "AP"
markerStyle = 24
markerSize = 1.35
lineStyle = 1
lineWidth = 2

grid = "xy"
log = "y"
xRange = [0,0.8]
yRange = [10**-3, 1]
xSize = 800
ySize = 600

flavours = [
        {
            "key": "Bjets_vs_Lightjets",
            "filename": "Lightjets",
            "title": "(light jets)",
        },
        {
            "key": "Bjets_vs_Cjets",
            "filename": "Cjets",
            "title": "(c-jets)",
        },
        {
            "key": "Bjets_vs_PUjets",
            "filename": "PUjets",
            "title": "(PU jets)",
        },
    ]

cuts = [
        {
            "name": "Default cuts", # for legend
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetROC_TC_btagCutsOnly.root",
            "color": ROOT.kBlue,
        },
        {
            "name": "Default + MVA>0.65",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT065.root",
            "color": ROOT.kMagenta+1,
        },
        {
            "name": "Default + MVA>0.7",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT07.root",
            "color": ROOT.kGreen+1,
        },
        {
            "name": "Default + MVA>0.75",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT075.root",
            "color": ROOT.kOrange,
        },
        {
            "name": "Default + MVA>0.8",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIPSel_ptChi2BothHits_CUT08.root",
            "color": ROOT.kRed,
            },

    ]

discriminants = [
        {
            "key": "TCHE_DiscrEff",
            "filename": "TCHE",
            "title": "TCHE performances",
        },
        {
            "key": "TCHP_DiscrEff",
            "filename": "TCHP",
            "title": "TCHP performances",
        },
    ]

# General configuration
runCfg = {
        "outFile": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/bTag-trackSel-optimisation/btagCutsOnly_MVA065_MVA07_MVA075_MVA08.root",
        "printDir": "./btagCutsOnly_MVA065_MVA07_MVA075_MVA08_plots", # optional
        "formats": ["png"], # optional
        "batch": True, # optional
        }

# Will hold the canvases
canvasCfg = []

for discr in discriminants:

    for flav in flavours:

        myGraphs = []
        for cut in cuts:
            graphCfg = {   
                    "file": cut["file"],
                    "key": flav["key"] + "/" + discr["key"],
                    "name": cut["name"],
                    "color": cut["color"],
                    "style": drawStyle,
                    "markerStyle": markerStyle, # Only used if "P" in "style" (default 20)
                    "markerSize": markerSize, # (default 1)
                    "lineStyle": lineStyle, # Only used if "L" in "style" (default 1)
                    "lineWidth": lineWidth, # (default 1)
                }
            myGraphs.append(graphCfg)

        myCanvas = {
                "name": discr["filename"] + "_" + flav["filename"], # Name of the canvas for the output ROOT/png/... files
                "xSize": xSize,
                "ySize": ySize,
                "title": discr["title"] + " " + flav["title"],
                "legPos": "br", # t/b, l/r
                "xRange": xRange, # optional
                "yRange": yRange, # optional
                "grid": grid, # optional
                "log": log, # optional
                "xTitle": "B-jet efficiency", # optional
                "yTitle": "Background efficiency", # optional
                "graphs": myGraphs,
            }
        canvasCfg.append(myCanvas)

# We're all set!

if __name__ == "__main__":
    drawCanvas(runCfg, canvasCfg, mode = "TGraph")

