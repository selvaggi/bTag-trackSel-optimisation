import ROOT

from tools.drawCanvas import drawCanvas

# General configuration
runCfg = {
        "outFile": "jetPlots.root",
        "printDir": "./jetPlots", # optional
        "formats": ["png"], # optional
        "batch": True, # optional
        }

# Will hold the canvases
canvasCfg = []

# The graphs we want to include in the first canvas
###### TCHE ##########################
myTH1s = [
        {   
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetHistos_TC_btagCutsOnly.root", # file where the graph is stored
            "key": "Bjets/TCHE_DiscrEff", # name/path/... of the graph inside the file
            "name": "bTag cuts", # name to be used in the legend
            "color": ROOT.kBlue,
            "lineStyle": 1, # (default 1)
            "lineWidth": 3, # (default 1)
        },
        {   
            "file": "../myTrees/jetHistos_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Lightjets/TCHE", # name/path/... of the graph inside the file
            "name": "Lightjets", # name to be used in the legend
            "color": ROOT.kBlue,
            "lineStyle": 1, # (default 1)
            "lineWidth": 3, # (default 1)
        },
    ]

# The first canvas
myCanvas = {
        "name": "TCHE_discr", # Name of the canvas for the output ROOT/png/... files
        "xSize": 800,
        "ySize": 600,
        "title": "TCHE discriminant", # optional
        "norm": True, # optional
        "grid": "xy", # optional
        "xTitle": "TCHE", # optional
        "yTitle": "Arbitrary scale", # optional
        "legPos": "bl", # t/b, l/r
        "hists": myTH1s,
    }
canvasCfg.append(myCanvas)

# We're all set!

if __name__ == "__main__":
    drawCanvas(runCfg, canvasCfg, mode = "TH1")

