import urllib
import string
import os
import sys
import LaunchOnCondor

FarmDirectory = "condor"
JobName = "jetTree"
LaunchOnCondor.SendCluster_Create(FarmDirectory, JobName)

path = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/bTag-trackSel-optimisation"
#outDir = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/"
outDir = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_loosenedbTagCuts_dZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/"
#outDir = "/home/fynu/swertz/CMS_tasks/BTagTrackSel/myTrees/rejFakeTracks_manyMVA/BDT_bTagCuts_LogdZ_length_dist_IP2D_pt_chi2_nHitPix_nHitAll/jetTrees/"

start_file = 1
end_file = 1
files_per_job = 3
max_files= 235
i = 1

while end_file <= max_files:
    end_file += files_per_job
    print "{}-{}".format(start_file, end_file)
    LaunchOnCondor.SendCluster_Push(["BASH", os.path.join(path, "condor.sh"), start_file, end_file, "JetTree_mc_{}.root".format(i), outDir])
    start_file = end_file
    i += 1

LaunchOnCondor.SendCluster_Submit()
