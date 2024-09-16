#!/bin/bash 

NAME=0

if [ $# -eq '1' ]; then

    NAME=$1

fi

cd src 
./train.py --list_jobs 
./train.py --delete_ckpt $NAME

