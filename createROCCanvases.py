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
myGraphs = [
        {   
            "file": "../myTrees/jetROC_TC_bTagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets_vs_Lightjets/TCHE_DiscrEff", # name/path/... of the graph inside the file
            "name": "Light jets", # name to be used in the legend
            "color": ROOT.kBlue,
            "style": "ALP",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" in "style" (default 1)
            "lineWidth": 1, # (default 1)
        },
        {   
            "file": "../myTrees/jetROC_TC_bTagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Cjets_vs_Lightjets/TCHE_DiscrEff", # name/path/... of the graph inside the file
            "name": "C-jets", # name to be used in the legend
            "color": ROOT.kGreen,
            "style": "ALP",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" in "style" (default 1)
            "lineWidth": 1, # (default 1)
        },
        {   
            "file": "../myTrees/jetROC_TC_bTagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "PUjets_vs_Lightjets/TCHE_DiscrEff", # name/path/... of the graph inside the file
            "name": "PU-jets", # name to be used in the legend
            "color": ROOT.kMagenta,
            "style": "ALP",
            "markerStyle": 20, # Only used if "P" in "style" (default 20)
            "markerSize": 1.5, # (default 1)
            "lineStyle": 1, # Only used if "L" in "style" (default 1)
            "lineWidth": 1, # (default 1)
        },
    ]

# The first canvas
myCanvas = {
        "name": "TCHE", # Name of the canvas for the output ROOT/png/... files
        "xSize": 800,
        "ySize": 600,
        "title": "TCHE performances", # optional
        "grid": "xy", # optional
        "log": "y", # optional
        "xTitle": "Signal efficiency", # optional
        "yTitle": "Background efficiency", # optional
        "graphs": myGraphs,
    }
canvasCfg.append(myCanvas)

# We're all set!

if __name__ = "__main__":
    drawTGraphs(runCfg, canvasCfg)

