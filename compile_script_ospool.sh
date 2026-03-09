#!/bin/bash
# run_script.sh

LocalPath="/home/projects/GATech_Otte" 
OSDF_path="/ospool/uw-shared/projects/GATech_Otte"

echo "Opening container to compile code"
value=$1
##
apptainer exec --bind $LocalPath/TrinityDemonstrator:/mnt $OSDF_path/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif make $value