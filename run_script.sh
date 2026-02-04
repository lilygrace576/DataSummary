#!/bin/bash
# run_script.sh

DATE=$1
echo "Running for $DATE"
apptainer exec --bind /home/lilyg/TrinityDemonstrator:/mnt /home/lilyg/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif /mnt/DataAnalysis/DataSummary/FolderDataSum $DATE y
