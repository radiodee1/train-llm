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


if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Train LLM - train llm with simple corpus", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--local', action="store_true", help="Not implemented")
 
    args = parser.parse_args()
    print(args)
