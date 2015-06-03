import ROOT
import os


def drawDoublehisto(h1, h2, name, xlabel, ylabel, legend, leftText, rightText, format, directory, logY):
    if logY : 
        name = name+"_logY"
    canvas = ROOT.TCanvas(name, name) 
    if logY : 
        canvas.SetLogy(1)
    Tleft = ROOT.TLatex(0.125, 0.91, leftText) 
    Tleft.SetNDC(ROOT.kTRUE) 
    Tleft.SetTextSize(0.048) 
    font = Tleft.GetTextFont() 
    #TPaveText* Tright = new TPaveText(0.8, 0.85, 0.945, 0.90, "NDC") 
    #Tright.SetTextFont(font) 
    #Tright.AddText(rightText) 
    #Tright.SetFillColor(0) 
    maxh1 = h1.GetBinContent(h1.GetMaximumBin())
    maxh2 = h2.GetBinContent(h2.GetMaximumBin())
    if(maxh1>maxh2) : 
        h1.GetXaxis().SetTitle(xlabel) 
        h1.GetXaxis().SetTitleFont(font) 
        h1.GetYaxis().SetTitle(ylabel) 
        h1.GetYaxis().SetTitleFont(font) 
        h1.GetYaxis().SetTitleOffset(1) 
        h1.SetTitle("") 
        h1.Draw("")
        h2.Draw("same")
    else : 
        h2.GetXaxis().SetTitle(xlabel) 
        h2.GetXaxis().SetTitleFont(font) 
        h2.GetYaxis().SetTitle(ylabel) 
        h2.GetYaxis().SetTitleFont(font) 
        h2.GetYaxis().SetTitleOffset(1) 
        h2.SetTitle("") 
        h2.Draw("")
        h1.Draw("same")
    legend.SetTextFont(font) 
    legend.Draw() 
    Tleft.Draw() 
    #Tright.Draw() 
    canvas.Write() 
    printCanvas(canvas, name, format, directory) 
# lepPosMiddle[4] = {0.4, 0.4, 0.6, 0.6} 


def printCanvas(canvas, name, format, directory):
    if format != "":
        outFile = os.path.join(directory, name) + "." + format
        canvas.Print(outFile)

def drawTGraphs(runCfg, drawCfg):
    if runCfg is None or drawCfg is None:
        return

    try:
        outDir = os.path.dirname(runCfg["outFile"])
    except KeyError:
        # We simply do not write to a ROOT outputfile
        outFile = None
    else:
        if not os.path.isdir(outDir) and outDir is not "":
            print "Directory {} does not exist, creating it.".format(outDir)
            os.makedirs(outDir)
        outFile = ROOT.TFile(runCfg["outFile"], "recreate")

    try:
        if runCfg["batch"] is True:
            print "Setting batch mode."
            ROOT.gROOT.SetBatch(ROOT.kTRUE)
    except KeyError:
        pass

    for canvasCfg in drawCfg:
        print "Drawing canvas {}.".format(canvasCfg["name"])
        
        if outFile is not None:
            outFile.mkdir(canvasCfg["name"])
        
        myCnv = drawTGraphCanvas(canvasCfg)

        # We put the canvas in a ROOTfile directory
        if outFile is not None:
            outFile.cd(canvasCfg["name"])
            myCnv.Write(canvasCfg["name"])

        # Only print to a file is "printDir" is specified
        try:
            printDir = runCfg["printDir"]
        except KeyError:
            printDir = None
        else:
            if not os.path.isdir(printDir):
                print "Directory {} does not exist, creating it.".format(printDir)
                os.makedirs(printDir)

        if printDir is not None:
            try:
                printFormats = runCfg["formats"]
            except KeyError:
                print "Output format not specified, taking png by default."
                printFormats = ["png"]
            for format in printFormats:
                printCanvas(myCnv, canvasCfg["name"], format, printDir)

    if outFile is not None:
        outFile.Close()

def drawTGraphCanvas(cCfg):
    myBTGStyle() # global variables powaaaa

    # Create Canvas (title optional)
    try:
        title = cCfg["title"]
    except KeyError:
        title = ""
    myCnv = ROOT.TCanvas(cCfg["name"], cCfg["title"], cCfg["xSize"], cCfg["ySize"])
    
    # Set Grid
    try:
        if "x" in cCfg["grid"].lower():
            myCnv.SetGridx()
        if "y" in cCfg["grid"].lower():
            myCnv.SetGridy()
    except KeyError:
        pass
    
    # Set log axes
    try:
        if "x" in cCfg["log"].lower():
            myCnv.SetLogx()
        if "y" in cCfg["log"].lower():
            myCnv.SetLogy()
    except KeyError:
        pass

    myLeg = ROOT.TLegend(0.15, 0.85-0.065*len(cCfg["graphs"]), 0.35, 0.87) # To be tuned
    # We need to keep track of ALL the objects created here, otherwise they will be deleted
    # when the function end and the TCanvas will end up containing only the TGraphs (and not the legend, ...)
    cCfg["_legend"] = myLeg

    xMax = -10**10
    xMin = 10**10
    yMax = -10**10
    yMin = 10**10

    # We use a TH1, to be drawn first, to take care of the editing of the axes (titles, ranges, ...)
    myTH = ROOT.TH1D("temp", "temp", 10, -1, 1)
    cCfg["_TH1"] = myTH

    for i,gCfg in enumerate(cCfg["graphs"]):
        print "Drawing graph for {}.".format(gCfg["name"])

        # Retrieve TGraph from file
        if not os.path.isfile(gCfg["file"]):
            raise Exception("File {} not found!".format(gCfg["file"]))
        file = ROOT.TFile(gCfg["file"], "read")
        gr = file.Get(gCfg["key"])
        if not isinstance(gr, ROOT.TGraph):
            raise Exception("Could not retrieve properly TGraph {} from file {}.".format(cCfg["key"], gCfg["file"]))

        legStyle = ""
    
        # This is for easier checking:
        gCfg["style"] = gCfg["style"].lower()
        # There is no "same" option for drawing TGraphs
        # This is achieved by drawing without the "axis" option, hence:
        gCfg["style"] = gCfg["style"].replace("a", "")

        # If drawn with line, set color, style and width
        if "l" in gCfg["style"] or "c" in gCfg["style"]:
            legStyle += "l"
            gr.SetLineColor(gCfg["color"])
            try:
                gr.SetLineStyle(gCfg["lineStyle"])
            except KeyError:
                gr.SetLineStyle(1)
            try:
                gr.SetLineWidth(gCfg["lineWidth"])
            except KeyError:
                gr.SetLineWidth(1)

        # If drawn with markers, set color, style and size
        if "p" in gCfg["style"]:
            legStyle += "p"
            gr.SetMarkerColor(gCfg["color"])
            try:
                gr.SetMarkerStyle(gCfg["markerStyle"])
            except KeyError:
                gr.SetMarkerStyle(20)
            try:
                gr.SetMarkerSize(gCfg["markerSize"])
            except KeyError:
                gr.SetMarkerSize(1)

        if "e" in gCfg["style"]:
            legStyle += "e"

        # Add to the legend
        myLeg.AddEntry(gr, gCfg["name"], legStyle)

        # Retrieve x and y range
        xMaxTemp = ROOT.Double()
        xMinTemp = ROOT.Double()
        yMaxTemp = ROOT.Double()
        yMinTemp = ROOT.Double()

        gr.ComputeRange(xMinTemp, yMinTemp, xMaxTemp, yMaxTemp)

        if xMaxTemp > xMax: xMax = xMaxTemp
        if xMinTemp < xMin: xMin = xMinTemp
        if yMaxTemp > yMax: yMax = yMaxTemp
        if yMinTemp < yMin: yMin = yMinTemp

        gCfg["_graph"] = gr
        
        file.Close()

    try:
        myTH.GetXaxis().SetTitle(cCfg["xTitle"])
    except KeyError:
        pass
    try:
        myTH.GetYaxis().SetTitle(cCfg["yTitle"])
    except KeyError:
        pass
    try:
        myTH.SetTitle(cCfg["title"])
    except KeyError:
        pass

    if "xRange" not in cCfg.keys():
        cCfg["xRange"] = [ 1.1*xMin, 1.1*xMax ]
    else:
        if cCfg["xRange"][0] > cCfg["xRange"][1]:
            cCfg["xRange"].reverse()
    myTH.GetXaxis().SetRangeUser(cCfg["xRange"][0], cCfg["xRange"][1])
    if "yRange" not in cCfg.keys():
        cCfg["yRange"] = [ 1.1*yMin, 1.1*yMax ]
    else:
        if cCfg["yRange"][0] > cCfg["yRange"][1]:
            cCfg["yRange"].reverse()
    myTH.GetYaxis().SetRangeUser(cCfg["yRange"][0], cCfg["yRange"][1])

    # Time to draw!
    myTH.Draw()
    for gr in cCfg["graphs"]:
        gr["_graph"].Draw(gr["style"])
    myLeg.Draw("same")

    return myCnv

def drawRocCurve(graph, name, xlabel, ylabel, leftText, rightText, format, directory, logX):
    canvas = ROOT.TCanvas(name, name)
    canvas.SetGrid(20, 20)
    if logX : canvas.SetLogx(1)
    graph.Draw("ALP")
    graph.GetXaxis().SetTitle(xlabel)
    graph.GetYaxis().SetTitle(ylabel)
    graph.SetMarkerColor(ROOT.kBlue)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.5)
    line = ROOT.TLine(0, 0, 1, 1)
    line.Draw()
    Tleft = ROOT.TLatex(0.125, 0.91, leftText) 
    Tleft.SetNDC(ROOT.kTRUE) 
    Tleft.SetTextSize(0.048) 
    font = Tleft.GetTextFont() 
    #TPaveText* Tright = new TPaveText(0.8, 0.85, 0.945, 0.90, "NDC") 
    #Tright.SetTextFont(font) 
    #Tright.AddText(rightText) 
    #Tright.SetFillColor(0) 
    #legend.SetTextFont(font) 
    #legend.Draw() 
    Tleft.Draw() 
    #Tright.Draw() 
    canvas.Write() 
    printCanvas(canvas, name, format, directory) 
    #delete Tright 

def drawRocCurve_zoomed(graph, name, xlabel, ylabel, leftText, rightText, format, directory, logX):
    canvas = ROOT.TCanvas(name, name)
    canvas.SetGrid(20, 20)
    if logX : canvas.SetLogx(1)
    graph.SetTitle("")
    graph.Draw("ALP")
    #line = TLine(0, 0, 1, 1)
    #line.Draw()
    Tleft = ROOT.TLatex(0.125, 0.91, leftText) 
    Tleft.SetNDC(ROOT.kTRUE) 
    Tleft.SetTextSize(0.048) 
    font = Tleft.GetTextFont()
    graph.GetXaxis().SetTitle(xlabel);
    graph.GetXaxis().SetTitleFont(font);
    graph.GetYaxis().SetTitle(ylabel);
    graph.GetYaxis().SetTitleFont(font);
    graph.GetYaxis().SetTitleOffset(0.87); 
    graph.SetMarkerColor(ROOT.kBlue)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1)
    #TPaveText* Tright = new TPaveText(0.8, 0.85, 0.945, 0.90, "NDC") 
    #Tright.SetTextFont(font) 
    #Tright.AddText(rightText) 
    #Tright.SetFillColor(0) 
    #legend.SetTextFont(font) 
    #legend.Draw() 
    #Tleft.Draw()
    
    latex = ROOT.TLatex(1., 9., "")
    latex.SetTextSize(0.05)
    latex.SetTextFont(42)
    latex.SetNDC(1) #To refer the legend to the canvas not the axis.

    #latex.DrawLatex(0.1, 0.91, "CMS Phase 2, PU = 140 Delphes")
    latex.DrawLatex(0.525, 0.91, "#sqrt{s} = 14 TeV, PU = 140")

    latex2 = ROOT.TLatex(1., 9., "")
    latex2.SetTextSize(0.055)
    latex2.SetTextFont(42)
    latex2.SetNDC(1) #To refer the legend to the canvas not the axis.
    latex2.DrawLatex(0.15, 0.83, "#bf{CMS Phase II, Delphes}")

    latex3 = ROOT.TLatex(1., 9., "")
    latex3.SetTextSize(0.045)
    latex3.SetTextFont(42)
    latex3.SetNDC(1)
    latex3.DrawLatex(0.15, 0.78, "Preliminary") 
    #Tright.Draw() 
    canvas.Write() 
    printCanvas(canvas, name, format, directory) 
    #delete Tright 

def drawTriplehisto(h1, h2, h3, name, xlabel, ylabel, legend, leftText, rightText, format, directory, logY):
    canvas = ROOT.TCanvas(name, name) 
    if logY : canvas.SetLogy(1)
    Tleft = ROOT.TLatex(0.125, 0.91, leftText) 
    Tleft.SetNDC(ROOT.kTRUE) 
    Tleft.SetTextSize(0.048) 
    font = Tleft.GetTextFont() 
    #TPaveText* Tright = new TPaveText(0.8, 0.85, 0.945, 0.90, "NDC") 
    #Tright.SetTextFont(font) 
    #Tright.AddText(rightText) 
    #Tright.SetFillColor(0) 
    h1.GetXaxis().SetTitle(xlabel) 
    h1.GetXaxis().SetTitleFont(font) 
    h1.GetYaxis().SetTitle(ylabel) 
    h1.GetYaxis().SetTitleFont(font) 
    h1.GetYaxis().SetTitleOffset(0.87) 
    h1.SetTitle("") 
    h1.Draw() 
    h2.Draw("same") 
    h3.Draw("same") 
    legend.SetTextFont(font) 
    legend.Draw() 
    Tleft.Draw() 
    #Tright.Draw() 
    canvas.Write() 
    printCanvas(canvas, name, format, directory) 
# lepPosMiddle[4] = {0.4, 0.4, 0.6, 0.6} 

def myGstyle():
    gROOT.SetStyle("Plain") 
    gStyle.SetOptStat(0) 
    gStyle.SetOptTitle(0) 
    # Fonts
    gStyle.SetTextFont(132) 
    gStyle.SetTextSize(0.08) 
    gStyle.SetLabelFont(132, "x") 
    gStyle.SetLabelFont(132, "y") 
    gStyle.SetTitleOffset(1, "x") 
    gStyle.SetTitleOffset(1, "y") 
    gStyle.SetLabelFont(132, "z") 
    gStyle.SetLabelSize(0.05, "x") 
    gStyle.SetTitleSize(0.06, "x") 
    gStyle.SetLabelSize(0.05, "y") 
    gStyle.SetTitleSize(0.06, "y") 
    gStyle.SetLabelSize(0.05, "z") 
    gStyle.SetTitleSize(0.06, "z") 
    gStyle.SetHistLineWidth(2) 
    gStyle.SetHistLineColor(1) 

    gStyle.SetPadBorderMode(0) 
    gStyle.SetPadColor(0) 

    gStyle.SetPaperSize(20, 26) 
    gStyle.SetPadTopMargin(0.10)  #055) 
    gStyle.SetPadRightMargin(0.055) 
    gStyle.SetPadBottomMargin(0.15) 
    gStyle.SetPadLeftMargin(0.125) 

    gStyle.SetFrameBorderMode(0) 

    #gStyle.SetPadTickX(1) # To get tick marks on the opposite side of the frame
    #gStyle.SetPadTickY(1) 

def myGstyle():
    #ROOT.gROOT.SetStyle("Plain") 
    ROOT.gStyle.SetOptStat(0) 
    #ROOT.gStyle.SetOptTitle(0) 
    # Fonts
    ROOT.gStyle.SetTextFont(42) 
    ROOT.gStyle.SetTextSize(0.06) 
    ROOT.gStyle.SetTitleBorderSize(0)
    ROOT.gStyle.SetLabelFont(42, "x") 
    ROOT.gStyle.SetLabelFont(42, "y") 
    ROOT.gStyle.SetTitleOffset(1.1, "x") 
    ROOT.gStyle.SetTitleOffset(1.2, "y") 
    ROOT.gStyle.SetLabelFont(42, "z") 
    ROOT.gStyle.SetLabelSize(0.05, "x") 
    ROOT.gStyle.SetTitleSize(0.05, "x") 
    ROOT.gStyle.SetLabelSize(0.05, "y") 
    ROOT.gStyle.SetTitleSize(0.05, "y") 
    ROOT.gStyle.SetLabelSize(0.05, "z") 
    ROOT.gStyle.SetTitleSize(0.05, "z") 
    ROOT.gStyle.SetHistLineWidth(2) 
    ROOT.gStyle.SetHistLineColor(1) 

    ROOT.gStyle.SetPadBorderMode(0) 
    ROOT.gStyle.SetPadColor(0) 

    ROOT.gStyle.SetPaperSize(20, 26) 
    ROOT.gStyle.SetPadTopMargin(0.10)  #055) 
    ROOT.gStyle.SetPadRightMargin(0.055) 
    ROOT.gStyle.SetPadBottomMargin(0.15) 
    ROOT.gStyle.SetPadLeftMargin(0.125) 

    ROOT.gStyle.SetFrameBorderMode(0) 

    #ROOT.gStyle.SetPadTickX(1) # To get tick marks on the opposite side of the frame
    #ROOT.gStyle.SetPadTickY(1) 

def myBTGStyle():
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetPadBorderMode(0)

    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetPadColor(0)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetTitleColor(1)
    ROOT.gStyle.SetStatColor(0)

    # set the paper & margin sizes
    ROOT.gStyle.SetPaperSize(20,26)
    ROOT.gStyle.SetPadTopMargin(0.10)
    ROOT.gStyle.SetPadRightMargin(0.03)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.125)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    
    ROOT.gStyle.SetTextFont(42) #132
    ROOT.gStyle.SetTextSize(0.09)
    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetLabelSize(0.045,"xyz") #0.035
    ROOT.gStyle.SetTitleSize(0.045,"xyz")
    ROOT.gStyle.SetTitleOffset(1.15,"y")
    
    # use bold lines and markers
    ROOT.gStyle.SetMarkerStyle(8)
    ROOT.gStyle.SetHistLineWidth(2)
    ROOT.gStyle.SetLineWidth(1)
    #ROOT.gStyle.SetLineStyleString(2,"[12 12]") // postscript dashes

    # do not display any of the standard histogram decorations
    ROOT.gStyle.SetOptTitle(1)
    ROOT.gStyle.SetOptStat(0) #("m")
    ROOT.gStyle.SetOptFit(0)
    
    #ROOT.gStyle.SetPalette(1,0)
    ROOT.gStyle.cd()
    ROOT.gROOT.ForceStyle()
