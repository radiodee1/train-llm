#!/usr/bin/env python3

import argparse
from dotenv import  dotenv_values 
import os
import yaml
import json
from openai import OpenAI


vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

try:
    OPENAI_API_KEY=str(vals['OPENAI_API_KEY'])
except:
    OPENAI_API_KEY='abc'

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

try:
    OPENAI_ORGANIZATION=str(vals['OPENAI_ORGANIZATION'])
except:
    OPENAI_ORGANIZATION=""

try:
    OPENAI_PROJECT_ID=str(vals['OPENAI_PROJECT_ID'])
except:
    OPENAI_PROJECT_ID=""

try:
    OPENAI_MODEL=str(vals['OPENAI_MODEL'])
except:
    OPENAI_MODEL="gpt-3.5-turbo"

try:
    OPENAI_URL=str(vals['OPENAI_URL'])
except:
    OPENAI_URL="https://api.openai.com/v1/chat/completions"

class Kernel:

    def __init__(self):
        self.verbose = False
        self.file = True
        self.file_num = 0

    def list_files(self):
        client = OpenAI( organization = OPENAI_ORGANIZATION )
        response = client.files.list()
        print(response)
        self.save_file(0, '---\nlist')
        self.save_file(0, str(response))

    def submit(self, filename):
        filename = '../jsonl/llm.' + filename + '.jsonl'
        if not os.path.isfile( filename ):
            print('something is not in the right place.')
            return
        client = OpenAI( organization = OPENAI_ORGANIZATION )

        response = client.files.create(
          file=open(filename, "rb"),
          purpose="fine-tune"
        )
        print(response)
        self.save_file(0, '---\nsubmit ' + filename)
        self.save_file(0, str(response))

    def save_jsonl(self, infile, outfile='train'):
         if True:
            if not os.path.isdir('../jsonl'):
                print("must be in 'src/' dir with 'train.py' and 'jsonl/' dir above.")
                return
            if not os.path.isdir('../../chatterbot-corpus'):
                print("did you clone chatterbot-corpus??")
                return
            corpus_name = '../../chatterbot-corpus/chatterbot_corpus/data/english/' + infile + '.yml'
            if not os.path.isfile(corpus_name):
                print(infile, corpus_name)
                print('something is not in the right place.')
                return
            c = open( corpus_name, 'r' )
            #x = json.dumps(yaml.safe_load(c))
            x = yaml.safe_load(c)
            c.close()
            y = []

            for j in x:
                if j == "conversations":
                    for i in x[j]:
                        multi = []
                        multi.append({'role': 'system', 'content' : 'You are a helpful assistant.'})
                        for m in range(len(i)):
                            if m % 2 == 0:
                                r = 'user'
                            else:
                                r = 'assistant'
                            multi.append({'role': r, 'content': i[m]})
                        ii = { 'messages' : multi }
                        y.append(ii)

            f = open( '../jsonl/llm.'+ outfile.strip() +'.jsonl', 'a')
            for i in y:
                f.write(json.dumps(i) + '\n')
            f.close()

    def p(self, *text):
        if self.verbose:
            print(*text)

    def save_file(self,  time, heading=""):
        if self.file:
            if not os.path.isdir('../txt'):
                print("must be in 'src/' dir with 'train.py' and 'txt/' dir above.")
                return

            f = open( '../txt/llm.'+ OPENAI_MODEL.strip() +'.txt', 'a')
            if heading.strip() != "":
                f.write(str(heading) + '\n')
                f.close()
                return

            f.write(str(self.file_num) + '\n')
            if time != 0:
                f.write("---\n")
                f.write(str(time) + "\n")
            f.write("+++\n")

            f.close()
            self.file_num += 1
        pass 
 
if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Train LLM - train llm with simple corpus", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--local', action="store_true", help="Not implemented")
    parser.add_argument('--file', action="store_true", help="Save ouput to file.")
    parser.add_argument('--verbose', action="store_true", help="Print ouput to the screen.")
    parser.add_argument('--jsonl', type=str, help="Add specified corpus file to jsonl file.")
    parser.add_argument('--submit', type=str, help="Submit specified file to OpenAI.")
    parser.add_argument('--list_files', action="store_true", help="List all uploaded files on OpenAI.")

    args = parser.parse_args()
    print(args)

    k.save_file(0, str(args))

    k.file = args.file 
    k.verbose = args.verbose

    if args.jsonl != None and args.jsonl.strip() != "":
        k.save_jsonl(args.jsonl)
        exit() 

    if args.submit != None and args.submit.strip() != "":
        k.submit(args.submit)
        exit()

    if args.list_files:
        k.list_files()
        exit()
