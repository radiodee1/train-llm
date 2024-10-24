#!/usr/bin/env python3

import argparse
from dotenv import  dotenv_values 
import os
import yaml
import json
from openai import OpenAI
import time
import requests

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
    OPENAI_MODEL_FINETUNE=str(vals['OPENAI_MODEL_FINETUNE'])
except:
    OPENAI_MODEL_FINETUNE="gpt-4o-mini-2024-07-18"

try:
    OPENAI_URL=str(vals['OPENAI_URL'])
except:
    OPENAI_URL="https://api.openai.com/v1/chat/completions"

try:
    OPENAI_URL_DELETE=str(vals['OPENAI_URL_DELETE'])
except:
    OPENAI_URL_DELETE="https://api.openai.com/v1/models/"


class Kernel:

    def __init__(self):
        self.verbose = False
        self.file = True
        self.file_num = 0
        self.epochs = 0
        self.limit = -1 
        self.completion = False
   
    def list_ckpt(self, ckpt):
        ckpt = str(ckpt)
        result = requests.get(
                'https://api.openai.com/v1/fine_tuning/jobs/' + ckpt + '/checkpoints',
                headers={ 'Authorization': 'Bearer '+ OPENAI_API_KEY }
            )
        print(result.text)

    def delete_ckpt(self, ckpt):
        ckpt = str(ckpt)
        
        result = requests.delete(
                OPENAI_URL_DELETE + ckpt, 
                headers={ 'Authorization': 'Bearer ' + OPENAI_API_KEY }
            )
        print(result.text)
        pass 


    def delete_model(self, index):
        index = int(index)
        jobname = self.model_id(index)
        result = requests.delete(
                OPENAI_URL_DELETE + jobname, 
                headers={ 'Authorization': 'Bearer ' + OPENAI_API_KEY }
            )
        print(result.text)
        pass 

    def cancel_job(self, index):
        index = int(index)
        jobname = self.job_id(index)
        client = OpenAI( organization = OPENAI_ORGANIZATION )
        client.fine_tuning.jobs.cancel(jobname)

    def model_id(self, index):
        index = int(index)
        r = open ( '../txt/llm.jobs.txt', 'r' )
        m =  r.read()
        r.close()
        m = m.replace('\'', '"')
        m = m.replace('None', '"None"')
        m = m.replace('False', '"False"')
        i = json.loads(m)
        i = i["data"][index]["fine_tuned_model"]
        
        print(i)
        return i

    def job_id(self, index):
        index = int(index)
        r = open ( '../txt/llm.jobs.txt', 'r' )
        m =  r.read()
        r.close()
        m = m.replace('\'', '"')
        m = m.replace('None', '"None"')
        m = m.replace('False', '"False"')
        i = json.loads(m)
        i = i["data"][index]["id"]
        
        print(i)
        return i

    def file_id(self, index):
        index = int(index)
        r = open ( '../txt/llm.list.txt', 'r' )
        m =  r.read()
        r.close()
        m = m.replace('\'', '"')
        m = m.replace('None', '"None"')
        m = m.replace('False', '"False"')
        i = json.loads(m)
        i = i["data"][index]["id"]
        
        print(i)
        return i

    def list_jobs(self):
        client = OpenAI( organization = OPENAI_ORGANIZATION )
        response = client.fine_tuning.jobs.list()
        print(response.to_dict())
        self.save_file(0, '---\nlist jobs')
        self.save_file(0, str(response.to_dict()), OPENAI_MODEL_FINETUNE.strip())
        self.save_file(0, str(response.to_dict()), 'jobs', 'w')

    def list_files(self):
        client = OpenAI( organization = OPENAI_ORGANIZATION )
        response = client.files.list()
        print(response.to_dict())
        self.save_file(0, '---\nlist files')
        self.save_file(0, str(response.to_dict()))
        self.save_file(0, str(response.to_dict()), 'list', 'w')

    def submit(self, filename):
        if self.completion:
            filename += '.completion'
        filename = '../jsonl/llm.' + filename + '.jsonl'
        if not os.path.isfile( filename ):
            print('something is not in the right place.')
            return
        client = OpenAI( organization = OPENAI_ORGANIZATION )

        response = client.files.create(
          file=open(filename, "rb"),
          purpose="fine-tune",
        )

        print(response.to_dict())
        self.save_file(0, '---\nsubmit ' + filename)
        self.save_file(0, str(response.to_dict()))

    def start_job(self, index):
        file_id = self.file_id(int(index))
        client = OpenAI( organization = OPENAI_ORGANIZATION )
        response = client.fine_tuning.jobs.create(
            training_file= file_id,
            model=OPENAI_MODEL_FINETUNE,
            hyperparameters={
                'n_epochs': self.epochs
            }
        )
        print(response.to_dict())
 

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
                        #multi = []
                        if not self.completion:
                            multi = []
                            multi.append({'role': 'system', 'content' : 'You are a helpful assistant.'})
                        else:
                            multi = {}
                        for m in range(len(i)):
                            if m % 2 == 0:
                                r = 'user'
                                pc = 'prompt'
                            else:
                                r = 'assistant'
                                pc = 'completion'

                            if not self.completion:
                                multi.append({'role': r, 'content': i[m]})
                            else:
                                multi[pc] = i[m]
                        if not self.completion:
                            ii = { 'messages' : multi }
                        else:
                            ii = multi
                        y.append(ii)

            if not self.completion:
                name = '.jsonl'
            else:
                name = '.completion.jsonl'
            f = open( '../jsonl/llm.'+ outfile.strip() + name , 'a')
            num = 0 
            for i in y:
                f.write(json.dumps(i) + '\n')
                if num > self.limit and self.limit != -1:
                    break
                num += 1 
            f.close()

    def p(self, *text):
        if self.verbose:
            print(*text)

    def save_file(self,  time_in , heading="", filename=OPENAI_MODEL.strip(), mode='a'):
        if self.file:
            if not os.path.isdir('../txt'):
                print("must be in 'src/' dir with 'train.py' and 'txt/' dir above.")
                return

            f = open( '../txt/llm.'+ filename.strip() +'.txt', mode)
            if heading.strip() != "":
                t = time.localtime()
                
                current_time = time.strftime("%x  %H:%M:%S", t)
                if mode != 'w':
                    f.write(str(current_time) + '\n')
                f.write(str(heading) + '\n')
                f.close()
                return

            f.write(str(self.file_num) + '\n')
            if time_in != 0:
                f.write("---\n")
                f.write(str(time_in) + "\n")
            f.write("+++\n")

            f.close()
            self.file_num += 1
        pass 

    def questions_only(self, infile, outfile='questions'):
        
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
                    for m in range(len(i)):
                        if m % 2 == 0:
                            #r = 'user'
                            y.append(i[m])
        f = open( '../jsonl/llm.'+ outfile.strip() +'.txt', 'a')

        num = 0 
        for i in y:
            f.write(str(i) + '\n')
            if num > self.limit and self.limit != -1:
                break 
            num += 1 
        f.close()

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
    parser.add_argument('--list_jobs', action="store_true", help="List all started jobs on OpenAI.")
    parser.add_argument('--id', default=None, help="Return id of file from list at index.")
    parser.add_argument('--job', default=None, help="Return id of file from list of jobs at index.")
    parser.add_argument('--start_job', default=None, help="Start fine-tune job.")
    parser.add_argument('--cancel_job', default=None, help="Cancel start_job.")
    parser.add_argument('--delete_model', default=None, help="Delete model.")
    parser.add_argument('--list_ckpt', default=None, help="list checkpoint on screen.")
    parser.add_argument('--delete_ckpt', default=None, help="Delete model or checkpoint.")
    parser.add_argument('--epochs', type=int, default=3, help="Specify number of epochs for fine-tune.")
    parser.add_argument('--questions', type=str, help="Make 'questions-only' file.")
    parser.add_argument('--limit', type=int, default=40, help="Limit lenght of 'questions' or 'jsonl' output.")
    parser.add_argument('--completion', action="store_true", help="Use prompt-completion format with jsonl.")

    args = parser.parse_args()
    if args.id == None and args.job == None:
        print(args)

    k.save_file(0, str(args))

    k.file = args.file 
    k.verbose = args.verbose
    k.epochs = args.epochs
    k.limit = args.limit
    k.completion = args.completion

    if args.jsonl != None and args.jsonl.strip() != "":
        k.save_jsonl(args.jsonl)
        exit() 

    if args.submit != None and args.submit.strip() != "":
        k.file = True 
        k.submit(args.submit)
        exit()

    if args.list_files:
        k.file = True
        k.list_files()
        exit()

    if args.list_jobs:
        k.file = True
        k.list_jobs()
        exit()

    if args.id != None:
        k.file_id(args.id)
        exit()

    if args.job != None:
        k.job_id(args.job)
        exit()

    if args.start_job != None:
        k.start_job(args.start_job)
        exit()

    if args.cancel_job != None:
        k.cancel_job(args.cancel_job)
        exit()

    if args.delete_model != None:
        k.delete_model(args.delete_model)
        exit()
    
    if args.list_ckpt != None:
        k.list_ckpt(args.list_ckpt)
        exit()

    if args.delete_ckpt != None:
        k.delete_ckpt(args.delete_ckpt)
        exit()

    if args.questions != None:
        k.questions_only(args.questions)
        exit()
