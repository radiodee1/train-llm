#!/bin/bash 

INDEX=0

if [ $# -eq '1' ]; then

    INDEX=$1

fi

cd src 
./train.py --list_jobs 
./train.py --delete_model $INDEX

echo "Run this script with the INDEX of the model to delete"
echo "as the first parameter. Otherwise zero will be used."
