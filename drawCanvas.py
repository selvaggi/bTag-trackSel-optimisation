from ROOT import TCanvas, TLegend, TLatex, TLine, gROOT, gStyle, TGraph, TMultiGraph, kTRUE
import os


def drawDoublehisto(h1, h2, name, xlabel, ylabel, legend, leftText, rightText, format, directory, logY):
    if logY : 
        name = name+"_logY"
    canvas = TCanvas(name, name) 
    if logY : 
        canvas.SetLogy(1)
    Tleft = TLatex(0.125, 0.91, leftText) 
    Tleft.SetNDC(kTRUE) 
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
    if format ! = "":
        outFile = os.path.join(directory, name) + "." + format
        canvas.Print(outFile)


def drawRocCurve(graph, name, xlabel, ylabel, leftText, rightText, format, directory, logX):
        canvas = TCanvas(name, name)
        canvas.SetGrid(20, 20)
    if logX : canvas.SetLogx(1)
        graph.Draw("ALP")
        graph.GetXaxis().SetTitle(xlabel)
        graph.GetYaxis().SetTitle(ylabel)
        graph.SetMarkerColor(kBlue)
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(0.5)
        line = TLine(0, 0, 1, 1)
        line.Draw()
        Tleft = TLatex(0.125, 0.91, leftText) 
        Tleft.SetNDC(kTRUE) 
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
        canvas = TCanvas(name, name)
        canvas.SetGrid(20, 20)
    if logX : canvas.SetLogx(1)
        graph.SetTitle("")
        graph.Draw("ALP")
        #line = TLine(0, 0, 1, 1)
        #line.Draw()
        Tleft = TLatex(0.125, 0.91, leftText) 
        Tleft.SetNDC(kTRUE) 
        Tleft.SetTextSize(0.048) 
        font = Tleft.GetTextFont()
    graph.GetXaxis().SetTitle(xlabel);
        graph.GetXaxis().SetTitleFont(font);
        graph.GetYaxis().SetTitle(ylabel);
        graph.GetYaxis().SetTitleFont(font);
        graph.GetYaxis().SetTitleOffset(0.87); 
        graph.SetMarkerColor(kBlue)
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1)
        #TPaveText* Tright = new TPaveText(0.8, 0.85, 0.945, 0.90, "NDC") 
        #Tright.SetTextFont(font) 
        #Tright.AddText(rightText) 
        #Tright.SetFillColor(0) 
        #legend.SetTextFont(font) 
        #legend.Draw() 
        #Tleft.Draw()
    
    latex = TLatex(1., 9., "")
    latex.SetTextSize(0.05)
    latex.SetTextFont(42)
    latex.SetNDC(1) #To refer the legend to the canvas not the axis.

    #latex.DrawLatex(0.1, 0.91, "CMS Phase 2, PU = 140 Delphes")
    latex.DrawLatex(0.525, 0.91, "#sqrt{s} = 14 TeV, PU = 140")

    latex2 = TLatex(1., 9., "")
    latex2.SetTextSize(0.055)
    latex2.SetTextFont(42)
    latex2.SetNDC(1) #To refer the legend to the canvas not the axis.
    latex2.DrawLatex(0.15, 0.83, "#bf{CMS Phase II, Delphes}")

    latex3 = TLatex(1., 9., "")
    latex3.SetTextSize(0.045)
    latex3.SetTextFont(42)
    latex3.SetNDC(1)
    latex3.DrawLatex(0.15, 0.78, "Preliminary") 
        #Tright.Draw() 
        canvas.Write() 
        printCanvas(canvas, name, format, directory) 
        #delete Tright 

def drawTriplehisto(h1, h2, h3, name, xlabel, ylabel, legend, leftText, rightText, format, directory, logY):
        canvas = TCanvas(name, name) 
    if logY : canvas.SetLogy(1)
        Tleft = TLatex(0.125, 0.91, leftText) 
        Tleft.SetNDC(kTRUE) 
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

def drawTGraph(graphs, name, xlabel, ylabel, legend, leftText, rightText, format, directory):
        canvas = TCanvas(name, name)
    canvas.SetGridx()
    canvas.SetGridy()
        Tleft = TLatex(0.125, 0.91, leftText) 
        Tleft.SetNDC(kTRUE) 
        Tleft.SetTextSize(0.048) 
        font = Tleft.GetTextFont() 
        #TPaveText* Tright = new TPaveText(0.8, 0.85, 0.945, 0.90, "NDC") 
        #Tright.SetTextFont(font) 
        #Tright.AddText(rightText) 
        #Tright.SetFillColor(0)
    mg = TMultiGraph()
    for graph in graphs:
        mg.Add(graph)
    mg.Draw("AP") 
    mg.GetXaxis().SetTitle(xlabel)
        mg.GetXaxis().SetTitleFont(font)
    #mg.GetYaxis().SetRangeUser(0.7, 1.3)
        mg.GetYaxis().SetTitle(ylabel)
        mg.GetYaxis().SetTitleFont(font)
        mg.GetYaxis().SetTitleOffset(0.87)
        mg.SetTitle("")
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

