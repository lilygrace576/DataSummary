#!/bin/bash
# run_script.sh

echo "Opening container to compile code"
value=$1
apptainer exec --bind /home/lilyg/TrinityDemonstrator:/mnt /home/lilyg/TrinityDemonstrator/DataAnalysis/containers/rootandexact.sif make $value
