#!/bin/bash
# run_script.sh

LocalPath="/home/projects/GATech_Otte" 
OSDF_path="/ospool/uw-shared/projects/GATech_Otte"

DATE=$1
echo "Running for $DATE"
apptainer exec --bind $LocalPath/TrinityDemonstrator:/mnt $OSDF_path/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif /mnt/DataAnalysis/DataSummary/FolderDataSum $DATE y
## add second mount for shared?
# apptainer exec --bind $LocalPath/TrinityDemonstrator:/mnt --bind $OSDF_path/TrinityDemonstrator:/osdf_mnt $OSDF_path/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif /mnt/DataAnalysis/DataSummary/FolderDataSum $DATE y