import copy
import ROOT

from tools.drawCanvas import drawCanvas

# "Aliases"

drawStyle = "LX"
markerStyle = 24
markerSize = 1.35
lineStyle = 1
lineWidth = 2

grid = "xy"
log = "y"
xRange = [0,0.85]
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

#cuts = [
#        {
#            "name": "MVA>#cutvalue",
#            "wps": [ 
#                { "idx": 8, "val": -0.08, "col": ROOT.kMagenta+1 },
#                { "idx": 12, "val": -0.07, "col": ROOT.kGreen+1 },
#                { "idx": 20, "val": -0.05, "col": ROOT.kOrange },
#                { "idx": 28, "val": -0.03, "col": ROOT.kRed },
#            ],
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC.root",
#        },
#        {
#            "name": "Default cuts",
#            "wps": [ 
#                { "idx": 0, "col": ROOT.kBlue }
#            ],
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetROC_TC.root",
#        }
#    ]

cuts = [
        {
            "name": "Loosened cuts + MVA>#cutvalue",
            "wps": [ 
                { "idx": 14, "val": -0.2, "col": ROOT.kMagenta+1 },
                { "idx": 18, "val": -0.11, "col": ROOT.kGreen+1 },
                { "idx": 30, "val": -0.05, "col": ROOT.kOrange },
                { "idx": 40, "val": 0.0, "col": ROOT.kRed },
            ],
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC.root",
        },
        {
            "name": "Default cuts",
            "wps": [ 
                { "idx": 0, "col": ROOT.kBlue }
            ],
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetROC_TC.root",
        }
    ]

#cuts = [
#        {
#            "name": "Default cuts + MVA>#cutvalue",
#            "wps": [ 
#                { "idx": 0, "val": -0.3, "col": ROOT.kMagenta+1 },
#                { "idx": 20, "val": -0.2, "col": ROOT.kGreen+1 },
#                { "idx": 40, "val": -0.1, "col": ROOT.kOrange },
#                { "idx": 70, "val": 0.05, "col": ROOT.kRed },
#            ],
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_bTagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC.root",
#        },
#        {
#            "name": "Default cuts",
#            "wps": [ 
#                { "idx": 0, "col": ROOT.kBlue }
#            ],
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/btagCutsOnly/jetROC_TC.root",
#        }
#    ]

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
        "outFile": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/comp_default_vs_BDTloosenedCuts.root",
        #"printDir": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/plots", # optional
        "formats": ["png"], # optional
        "batch": True, # optional
        }

# Will hold the canvases
canvasCfg = []

for discr in discriminants:

    for flav in flavours:

        myGraphs = []
        for cut in cuts:
            for wp in cut["wps"]:
                graphCfg = {   
                        "file": cut["file"],
                        "key": flav["key"] + "/" + discr["key"],
                        # Following two options only when the Graph is retrieved from a list of graphs in the file
                        "isFromTList": True,
                        "idx": wp["idx"],
                        "color": wp["col"],
                        "style": drawStyle,
                        "markerStyle": markerStyle, # Only used if "P" in "style" (default 20)
                        "markerSize": markerSize, # (default 1)
                        "lineStyle": lineStyle, # Only used if "L" in "style" (default 1)
                        "lineWidth": lineWidth, # (default 1)
                    }
                try:
                    graphCfg["name"] = cut["name"].replace("#cutvalue", str(wp["val"]))
                except KeyError:
                    graphCfg["name"] = cut["name"]
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

