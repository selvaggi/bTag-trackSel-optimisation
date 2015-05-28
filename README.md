# bTag-trackSel-optimisation

##Files explanation

    tools.py : tools to create rootFile and make the plot from the crab output (decided to keep this possibility because easier to reweight according to Jet pt). This is the file to edit in order to change the selection of the jets/tracks.
    
    createTrackTrees.py : create the two trees with signal tracks and background tracks.
    
    plotComparedDistriFromTwoFiles.py : out of these trees, plot compared distributions. 
    
    compareTracksVariables_fromCrab.py : plot compared distributions out of the crab output.
    
    MVA_facilities.py : function to train MVA (evaluate MVA --> to be fixed, merge MVA out in tree --> to be fixed).
    
    trainMVA.py : call the MVA_facilities.py
    
    drawCanvas.py : old stuff I did to ease the plotting
    

