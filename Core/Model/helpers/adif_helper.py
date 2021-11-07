# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 17:47:20 2021

@author: Jagudo
"""

import pandas as pd
from geopy.geocoders import Nominatim

class SimpleState():
    
    def __init__(self):
        
        self.eor = 'EOR'
        self.label = ''
        self.data_len = ''
        self.value = ''
        
        self.labels = ['CALL', 
                       'QSO_DATE', 
                       'TIME_ON', 
                       'BAND', 
                       'CONTEST_ID', 
                       'MODE',
                       'RST_SENT',
                       'RST_RCVD'
                       'EOR']
        
        self.state = 'PARSING'
        self.states = ['keyword', 'len', 'value']
        self.map = {}
        
    def feed (self, datum):
        
        c = str(datum).upper()
        
        if c == '<':
            self.state = self.states[0]
            if self.value != '' and self.label != '':
                self.map[self.label] = self.value.strip()
            self.label = ''
            self.value =''
            self.data_len = ''
        elif c == ':':
            self.state = self.states[1]
        elif c == '>':
            self.state = self.states[2]
            if self.label == self.eor:
               self.state = self.eor
            
        elif self.state == self.states[0]:
            self.label = self.label + c 
        elif self.state == self.states[1]:
            self.data_len = self.label + c
        elif self.state == self.states[2]:
            self.value = self.value + c
            
    def get_map(self):
        return self.map

# PRIVATE FUNCTIONS
def _parse_body_line(l):        
    parser = SimpleState()
    
    # parse line
    while parser.state != SimpleState().eor:
        for c in l:
            parser.feed(c)
    
    # return
    return parser.get_map()    
                

# PUBLIC FUNCTIONS

def get_header (file = 'C:\\temp\\adif.adi'):
    #define variables
    header = ''
    
    # define stop
    eof = '<EOH>'
    
    # Open file
    f = open(file,'r')
    
    # parse file
    while True:
        l = f.readline()
        if not l or eof in l.upper():
            break
        else:
            header = header + l
    # return
    return header

def get_body (file = 'C:\\temp\\leones.adi', as_pandas = True, geolocate = True):
    #define variables
    header = ''
    
    # define stop
    eof = '<EOH>'
    
    # Open file
    f = open(file,'r')
    
    # parse header file
    while True:
        l = f.readline()
        if not l or eof in l.upper():
            break
        else:
            header = header + l
    
    # parse empty lines
    while True:
        l = f.readline()
        if l == '' or l == '\n':
            continue
        break
    
    # parse body
    body = {}
    while True:
        if not l:
            break
        else:
            reg = _parse_body_line(l)
            body[reg.get('CALL','')] = reg
            l = f.readline()
            
    # Converto to pandas
    if as_pandas:
        columns = list(body[list(body.keys())[0]].keys())
        df = pd.DataFrame.from_dict(body, 'index', str, columns)
        body = df
    
    # Geolocate
    if geolocate and as_pandas:
        # Helper 
        def _eval_results(x):
            try:
                return (x.latitude, x.longitude)
            except:
                return None

        # Geolocator
        geolocator = Nominatim(timeout=10, user_agent = "myGeolocator")
        
        # Lambda geolocator in whole list
        body['COORD']=body.QTH.apply(geolocator.geocode, timeout=1000000).apply(lambda x: _eval_results(x))
        
    return body
    
if __name__ == '__main__':
    data = get_body()