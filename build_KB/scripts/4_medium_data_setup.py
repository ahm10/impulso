
'''
Objective: Collect MEDIUMdata and ingest in grakn schema.
Run from the root
$ python ./build_KB/scripts/4_medium_datasetup.py
$ python ROOT_DIR/MEDIUM_DIR/SCRIPTS_DIR/filename.py

'''


### GET PATHS FROM UNIVERSAL CONFIG

import configparser


config = configparser.ConfigParser()
config.read('config.ini')
ROOT_BASE_DIR_PATH = config['ROOT_PATH']['basedir']
MEDIUM_BASE_DIR_PATH = ROOT_BASE_DIR_PATH + config['MEDIUM_PATHS']['basedir']
MEDIUM_DATASTORE_PATH = MEDIUM_BASE_DIR_PATH + config['MEDIUM_PATHS']['datastoredir']
SCRAPPED_PATH = MEDIUM_DATASTORE_PATH + config['MEDIUM_PATHS']['scrapped']
PARSED_PATH = MEDIUM_DATASTORE_PATH + config['MEDIUM_PATHS']['parsed'] # for title etc
STRUCTURED_PATH = MEDIUM_DATASTORE_PATH + config['MEDIUM_PATHS']['structured'] # for content


# from grakn.client import GraknClient
import grakn_utils
import csv
import pandas as pd
import json
import os


files = os.listdir(PARSED_PATH)

print(PARSED_PATH)

print(files)

for file in files: 
    
    df = pd.read_csv(PARSED_PATH + file)

    print(df.columns)



