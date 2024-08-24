#!/bin/bash 

cd ..

echo $PWD

if [ -d chatterbot-corpus ]; then
    echo "chatterbot-corpus exists"
    exit 
fi

git clone https://github.com/gunthercox/chatterbot-corpus.git 
cd chatterbot-corpus/
echo $PWD

git checkout ae8ccd2
 
