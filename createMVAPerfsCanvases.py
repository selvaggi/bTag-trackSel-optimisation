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
log = ""
xRange = [-0.3,0.]
yRange = [0, 0.7]
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

MVAs = [
        {
            "name": "No preselection",
            "color": ROOT.kOrange,
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/jetMVAperf_TC_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll.root"
        }
    ]

discriminants = [
        {
            "key": "TCHE_DiscrEff",
            "filename": "TCHE",
            "title": "TCHE",
            "wps": ["loose", "medium"]
        },
        {
            "key": "TCHP_DiscrEff",
            "filename": "TCHP",
            "title": "TCHP",
            "wps": ["loose", "medium"]
        },
    ]

# General configuration
runCfg = {
        "outFile": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/jetMVAperfCanvases_TC_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll.root",
        #"printDir": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/testFormulaMVA/MVAplots", # optional
        "formats": ["png"], # optional
        "batch": True, # optional
        }

# Will hold the canvases
canvasCfg = []

for discr in discriminants:
    for wp in discr["wps"]:
        for flav in flavours:

            myGraphs = []
            for mva in MVAs:
                graphCfg = {   
                        "file": mva["file"],
                        "key": flav["key"] + "/" + discr["key"] + "_" + wp,
                        "name": mva["name"],
                        "color": mva["color"],
                        "style": drawStyle,
                        "markerStyle": markerStyle, # Only used if "P" in "style" (default 20)
                        "markerSize": markerSize, # (default 1)
                        "lineStyle": lineStyle, # Only used if "L" in "style" (default 1)
                        "lineWidth": lineWidth, # (default 1)
                    }
                myGraphs.append(graphCfg)

            myCanvas = {
                    "name": discr["filename"] + "_" + flav["filename"] + "_" + wp, # Name of the canvas for the output ROOT/png/... files
                    "xSize": xSize,
                    "ySize": ySize,
                    "title": discr["title"] + " " + wp + " " + flav["title"],
                    "legPos": "tl", # t/b, l/r
                    "xRange": xRange, # optional
                    "yRange": yRange, # optional
                    "grid": grid, # optional
                    "log": log, # optional
                    "xTitle": "MVA cut", # optional
                    "yTitle": "B-jet efficiency", # optional
                    "graphs": myGraphs,
                }
            
            canvasCfg.append(myCanvas)

# We're all set!

if __name__ == "__main__":
    drawCanvas(runCfg, canvasCfg, mode = "TGraph")

