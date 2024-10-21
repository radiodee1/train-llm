#!/bin/bash

cd src 
echo $PWD 

if [ -f '../jsonl/llm.train.completion.jsonl' ]; then
    echo 'train file exists'
    exit 
fi 

touch ../jsonl/subject.txt


while read x; do
    Y='../../chatterbot-corpus/chatterbot_corpus/data/english/'${x}'.yml'
    if [ -f $Y ]; then 
        echo $y 
    else 
        echo 'subject file not found'
        echo $Y
        exit
    fi

done < '../jsonl/subject.txt'

while read x; do 
    echo $x
    ./train.py --jsonl  $x --completion
done < '../jsonl/subject.txt'

echo '+++++++++++++++++'

head -n 20 ../jsonl/llm.train.completion.jsonl > ../jsonl/llm.train.completion.jsonl.temp

cat ../jsonl/llm.train.completion.jsonl.temp

rm ../jsonl/llm.train.completion.jsonl
mv ../jsonl/llm.train.completion.jsonl.temp ../jsonl/llm.train.completion.jsonl 
