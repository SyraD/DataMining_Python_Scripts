#!/usr/bin/env python


import sys
import urllib3
import simplejson
import json
import sqlite3
import time
import datetime
from pprint import pprint
import ast 							


import sys
from Table_SMC_election2016_timeline import * #make sure the filename is correct.
from GetData_SMC_election2016 import get_data_user_timeline_all_pages
from WriteTable_SMC_election2016_timeline import write_data

####################################################################################################


class Scrape:
    def __init__(self):
        engine = sqlalchemy.create_engine("sqlite:///C:/Users/MODIFY.sqlite", echo=False)   #ABSOLUTE PATH TO DB
        Session = sessionmaker(bind=engine)
        self.session = Session()  
        Base.metadata.create_all(engine)
        
    def run(self):
        code = ast.parse(open("C:/Users/MODIFY/PyScripts/Iteration_SMC_election2016.py").read())                        
        eval(compile(code, '', 'exec'))
        

##### FOLLOWING LINE IS A CHECK TO SEE WHETHER THIS FILE IS BEING RUN BY ITSELF (TRUE) OR IMPORTED FROM ANOTHER MODULE #####
##### http://ibiblio.org/g2swap/byteofpython/read/module-name.html #####
if __name__ == "__main__":
    s = Scrape()
    s.run()