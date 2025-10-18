#!/bin/bash
# run_script.sh

DATE=$1
echo "Running for $DATE"
# apptainer exec --bind /storage/osg-otte1/shared/TrinityDemonstrator:/mnt /storage/osg-otte1/shared/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif /mnt/DataAnalysis/DataSummary/FolderDataSum $DATE y
apptainer exec --bind /storage/osg-otte1/shared/TrinityDemonstrator:/mnt /storage/osg-otte1/shared/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif /storage/osg-otte1/lsheram6/DataSummary/FolderDataSum $DATE y
