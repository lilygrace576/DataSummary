#!/bin/bash
# run_script.sh
LocalPath="/data/TrinityLabComputer" 

DATE=$1
echo "Running for $DATE"
apptainer exec --bind $LocalPath/TrinityDemonstrator:/mnt $LocalPath/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif /mnt/DataAnalysis/DataSummary/FolderDataSum $DATE y
