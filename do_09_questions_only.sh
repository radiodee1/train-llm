#!/bin/bash

cd src 
echo $PWD 

if [ -f '../jsonl/llm.questions.txt' ]; then
    echo 'train file exists'
    exit 
fi 

touch ../jsonl/subject-questions.txt


while read x; do
    Y='../../chatterbot-corpus/chatterbot_corpus/data/english/'${x}'.yml'
    if [ -f $Y ]; then 
        echo $y 
    else 
        echo 'subject file not found'
        echo $Y
        exit
    fi

done < '../jsonl/subject-questions.txt'

while read x; do 
    echo $x
    ./train.py --questions $x
done < '../jsonl/subject-questions.txt'

echo '+++++++++++++++++'
cat ../jsonl/llm.questions.txt
