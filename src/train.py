#!/usr/bin/env python3

import argparse
from dotenv import  dotenv_values 
import os
import time
import json
#

vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

try:
    OPENAI_API_KEY=str(vals['OPENAI_API_KEY'])
except:
    OPENAI_API_KEY='abc'

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
            #f.write(identifiers['user'] + " : "+ str(self.memory_user[-1]) + "\n")
            #f.write(identifiers['ai'] + " : " + str(self.memory_ai[-1]) + "\n")
            #f.write(str(prompt) + "\n")
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


    args = parser.parse_args()
    print(args)

    k.save_file(0, str(args))

    k.file = args.file 
    k.verbose = args.verbose
