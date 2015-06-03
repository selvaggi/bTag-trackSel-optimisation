import ROOT

from tools.drawCanvas import drawCanvas

# General configuration
runCfg = {
        "outFile": "testPlotHistos.root",
        "printDir": "./plots", # optional
        "formats": ["png"], # optional
        "batch": True, # optional
        }

# Will hold the canvases
canvasCfg = []

# The graphs we want to include in the first canvas
###### TCHE ##########################
myTH1s = [
        {   
            "file": "../myTrees/jetHistos_TC_btagCuts_MLP_Nplus5_noSel.root", # file where the graph is stored
            "key": "Bjets/TCHE", # name/path/... of the graph inside the file
            "name": "B-jets", # name to be used in the legend
            "color": ROOT.kRed,
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
        "xRange": [0,1], # optional
        "norm": True, # optional
        "grid": "xy", # optional
        "xTitle": "TCHE", # optional
        "yTitle": "Arbitrary scale", # optional
        "hists": myTH1s,
    }
canvasCfg.append(myCanvas)

# We're all set!

if __name__ == "__main__":
    drawCanvas(runCfg, canvasCfg, mode = "TH1")

