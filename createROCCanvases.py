import copy
import ROOT

from tools.drawCanvas import drawCanvas

# "Aliases"

drawStyle = "L"
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
#            "name": "Default cuts", # for legend
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetROC_TC_btagCutsOnly.root",
#            "color": ROOT.kBlue,
#        },
#        {
#            "name": "Default + MVA>0.67",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUT067.root",
#            "color": ROOT.kMagenta+1,
#        },
#        {
#            "name": "Default + MVA>0.73",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUT073.root",
#            "color": ROOT.kGreen+1,
#        },
#        {
#            "name": "Default + MVA>0.8",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_ptChi2BothHits_CUT080.root",
#            "color": ROOT.kOrange,
#        },
#
#    ]

#cuts = [
#        {
#            "name": "Default cuts", # for legend
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/btagCutsOnly/jetROC_TC_btagCutsOnly.root",
#            "color": ROOT.kBlue,
#        },
#        {
#            "name": "Default + MVA>0.55",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUT055.root",
#            "color": ROOT.kMagenta+1,
#        },
#        {
#            "name": "Default + MVA>0.7",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUT070.root",
#            "color": ROOT.kGreen+1,
#        },
#        {
#            "name": "Default + MVA>0.8",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits/jetROC_TC_btagCuts_MLP_N_Nmin1_bTag_zIP_absSel_lengthDistptChi2BothHits_CUT080.root",
#            "color": ROOT.kOrange,
#        },
#
#    ]

## No Selection
#cuts = [
#        {
#            "name": "Default cuts", # for legend
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/btagCutsOnly/jetROC_TC_btagCutsOnly.root",
#            "color": ROOT.kBlue,
#        },
#        {
#            "name": "MVA>-0.065",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0065.root",
#            "color": ROOT.kMagenta+1,
#        },
#        {
#            "name": "MVA>-0.080",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0080.root",
#            "color": ROOT.kGreen+1,
#        },
#        {
#            "name": "MVA>-0.100",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0100.root",
#            "color": ROOT.kOrange,
#        },
#        {
#            "name": "MVA>-0.150",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0150.root",
#            "color": ROOT.kRed,
#        }
#    ]


## bTag Selection
#cuts = [
#        {
#            "name": "Default cuts", # for legend
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/btagCutsOnly/jetROC_TC_btagCutsOnly.root",
#            "color": ROOT.kBlue,
#        },
#        {
#            "name": "Default cuts + MVA>-0.20",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_bTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-020.root",
#            "color": ROOT.kMagenta+1,
#        },
#        {
#            "name": "Default cuts + MVA>-0.16",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_bTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-016.root",
#            "color": ROOT.kGreen+1,
#        },
#        {
#            "name": "Default cuts + MVA>-0.10",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_bTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-010.root",
#            "color": ROOT.kOrange,
#        },
#        {
#            "name": "Default cuts + MVA>-0.075",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_bTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0075.root",
#            "color": ROOT.kRed,
#        }
#    ]

## loosened bTag Selection
cuts = [
        {
            "name": "Default cuts", # for legend
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/btagCutsOnly/jetROC_TC_btagCutsOnly.root",
            "color": ROOT.kBlue,
        },
        {
            "name": "Loosened cuts", # for legend
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/loosenedbtagCutsOnly/jetROC_TC_loosenedbtagCutsOnly.root",
            "color": ROOT.kRed,
        },
        {
            "name": "Loosened cuts + MVA>-0.05",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-005.root",
            "color": ROOT.kMagenta+1,
        },
        {
            "name": "Loosened cuts + MVA>-0.045",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0045.root",
            "color": ROOT.kGreen+1,
        },
        {
            "name": "Loosened cuts + MVA>-0.033",
            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0033.root",
            "color": ROOT.kOrange,
        },
        #{
        #    "name": "Loosened cuts + MVA>-0.026",
        #    "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0026.root",
        #    "color": ROOT.kRed,
        #}
    ]

## loosened bTag Selection
#cuts = [
#        {
#            "name": "Default cuts", # for legend
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/btagCutsOnly/jetROC_TC_btagCutsOnly.root",
#            "color": ROOT.kBlue,
#        },
#        {
#            "name": "Loosened cuts", # for legend
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/loosenedbtagCutsOnly/jetROC_TC_loosenedbtagCutsOnly.root",
#            "color": ROOT.kRed,
#        },
#        {
#            "name": "MVA>-0.444",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0444.root",
#            "color": ROOT.kMagenta+1,
#        },
#        {
#            "name": "MVA>-0.440",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0440.root",
#            "color": ROOT.kGreen+1,
#        },
#        {
#            "name": "MVA>-0.434",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0434.root",
#            "color": ROOT.kOrange,
#        },
#        {
#            "name": "MVA>-0.430",
#            "file": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/BDT_trackFromBjetvsOther_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetROC_TC_BDT_CUT-0430.root",
#            "color": ROOT.kRed,
#        },
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
        "outFile": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/comp_btagCutsOnly_BDTloosenedbTagCuts/btagCutsOnly_BDTbTagCuts_-005_-0045_-0033_-0026.root",
        "printDir": "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks/comp_btagCutsOnly_BDTloosenedbTagCuts/plots", # optional
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

