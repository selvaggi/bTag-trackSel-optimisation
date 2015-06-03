import ROOT

from tools.drawCanvas import drawTGraphs

# General configuration
runCfg = {
        "outFile": "testROCCanvas.root",
        "printDir": "./plots", # optional
        "formats": ["png"], # optional
        "batch": True, # optional
        }

# Will hold the canvases
canvasCfg = []

# The graphs we want to include in the first canvas
###### TCHE ##########################
myGraphs = [
        {   
            "file": "../myTrees/jetROC_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets_vs_Lightjets/TCHE_DiscrEff", # name/path/... of the graph inside the file
            "name": "Light jets", # name to be used in the legend
            "color": ROOT.kBlue,
            "style": "AL",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" in "style" (default 1)
            "lineWidth": 3, # (default 1)
        },
        {   
            "file": "../myTrees/jetROC_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets_vs_Cjets/TCHE_DiscrEff", # name/path/... of the graph inside the file
            "name": "C-jets", # name to be used in the legend
            "color": ROOT.kGreen,
            "style": "AL",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" in "style" (default 1)
            "lineWidth": 3, # (default 1)
        },
        {   
            "file": "../myTrees/jetROC_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets_vs_PUjets/TCHE_DiscrEff", # name/path/... of the graph inside the file
            "name": "PU-jets", # name to be used in the legend
            "color": ROOT.kMagenta,
            "style": "AL",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" or "C" in "style" (default 1)
            "lineWidth": 3, # (default 1)
        },
    ]

# The first canvas
myCanvas = {
        "name": "TCHE", # Name of the canvas for the output ROOT/png/... files
        "xSize": 800,
        "ySize": 600,
        "title": "TCHE performances", # optional
        "xRange": [0,1], # optional
        "yRange": [10**-2,1], # optional
        "grid": "xy", # optional
        "log": "y", # optional
        "xTitle": "B-jet efficiency", # optional
        "yTitle": "Background efficiency", # optional
        "graphs": myGraphs,
    }
canvasCfg.append(myCanvas)

###### TCHP ##########################

myGraphs = [
        {   
            "file": "../myTrees/jetROC_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets_vs_Lightjets/TCHP_DiscrEff", # name/path/... of the graph inside the file
            "name": "Light jets", # name to be used in the legend
            "color": ROOT.kBlue,
            "style": "AL",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" in "style" (default 1)
            "lineWidth": 3, # (default 1)
        },
        {   
            "file": "../myTrees/jetROC_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets_vs_Cjets/TCHP_DiscrEff", # name/path/... of the graph inside the file
            "name": "C-jets", # name to be used in the legend
            "color": ROOT.kGreen,
            "style": "AL",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" in "style" (default 1)
            "lineWidth": 3, # (default 1)
        },
        {   
            "file": "../myTrees/jetROC_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets_vs_PUjets/TCHP_DiscrEff", # name/path/... of the graph inside the file
            "name": "PU-jets", # name to be used in the legend
            "color": ROOT.kMagenta,
            "style": "AL",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" or "C" in "style" (default 1)
            "lineWidth": 3, # (default 1)
        },
    ]
myCanvas = {
        "name": "TCHP", # Name of the canvas for the output ROOT/png/... files
        "xSize": 800,
        "ySize": 600,
        "title": "TCHP performances", # optional
        "xRange": [0,1], # optional
        "yRange": [10**-2,1], # optional
        "grid": "xy", # optional
        "log": "y", # optional
        "xTitle": "B-jet efficiency", # optional
        "yTitle": "Background efficiency", # optional
        "graphs": myGraphs,
        }
canvasCfg.append(myCanvas)

# We're all set!

if __name__ == "__main__":
    drawTGraphs(runCfg, canvasCfg)

