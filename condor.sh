#!/bin/bash

mypath=/home/fynu/swertz/CMS_tasks/BTagTrackSel/bTag-trackSel-optimisation/

module purge
module load python/python27_sl6_gcc49
module load root/6.04.00-sl6_gcc49

mkdir tools
cp $mypath/tools/Formulas.h tools/
python $mypath/createJetTreeTC.py $1 $2 $3
rm -r tools
mv $3 $4
