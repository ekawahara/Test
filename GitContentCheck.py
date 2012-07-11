"""
line_check.py

Created by Evan Kawahara on 05-31-2012
Copyright (c) 2012 Tapulous, Inc.. All rights reserved.
"""

import sys
import os
import re

f = open("error.txt", "w")
f.close()
f = None


def read_checkin():
    os.chdir('ttt')
    cmd1 = 'git diff '
    cmd1 = 'svn diff HEAD^ HEAD --username buildomatic --password T4pW1thM3!!!'
    a = os.popen(cmd1)
    b = a.readlines()
    c = ''.join(b)
    print c
    d = c.split('\n')
    
    line_count = len(d)
    count = 0
    
    while(count < line_count):
        row = d[count]
        if row[0:6] =='Index:':
            index = row
        elif row[0:2] == '@@':
            linecount = row
        elif row[0:1] == '+' and row[0:3] != '+++':
            if(log_check(row)):
                cmd = 'echo \"\nThe following code inserts NSLog: \n%s\n%s\n%s\" >> error.txt' % (index, linecount, row)
                os.popen(cmd)
            if copyright_check(row):
                cmd = 'echo \"\nThe following code has a bad copyright message: \n%s\n%s\n%s\" >> error.txt' % (index, linecount, row)
                os.popen(cmd)
                
            if perfection_check(row):
                cmd = 'echo \"\nThe following code sets TAP_PERFECTION: \n%s\n%s\n%s\" >> error.txt' % (index, linecount, row)
                os.popen(cmd)
                
            if dev_server_check(row):
                cmd = 'echo \"\nThe following code enables DEV_SERVER: \n%s\n%s\n%s\" >> error.txt' % (index, linecount, row)
                os.popen(cmd)
                
            if dev_check(row):
                cmd = 'echo \"\nThe following code adds developer signing: \n%s\n%s\n%s\" >> error.txt' % (index, linecount, row)
                os.popen(cmd)
                
            if equality_check(row):
                cmd = 'echo \"\nThe following uses an inappropriate equality comparison: \n%s\n%s\n%s\" >> error.txt' % (index, linecount, row)
                os.popen(cmd)
                
            if existence_check(row):
                cmd = 'echo \"\nYou use an #ifdef here, are you sure you didn\'t mean #if ?\n%s\n%s\n%s\" >> error.txt' % (index, linecount, row)
                os.popen(cmd)
        count += 1
                
            
def log_check(s):
    #return s == 'NSLog'
    logs = re.findall('\+.*NSLog', s)
    if len(logs):
        newlogs = ''.join(logs)
        debug = re.findall('debug', newlogs)
        if len(debug):
            return False
        else:
            return True
        
        
       
def copyright_check(s):
    return False

def perfection_check(s):
    perfection = re.findall('\+.*TAP_PERFECTION=', s)
    return len(perfection)
    
def dev_server_check(s):
    dev = re.findall('\+.*USE_DEV_SERVER_ENDPOINTS=1', s)
    return len(dev)
    
def dev_check(s):
    #check for the signing being set
    dev = re.findall('\+.*iPhone Developer:', s)    
    return len(dev)    
        
def equality_check(s):
    equality = re.findall('\+.*if.*\(.*==.*@\".*\"\)', s)
    return len(equality)
    
def existence_check(s):
    existence = re.findall('\+.*#ifdef', s)
    return len(existence)

read_checkin()