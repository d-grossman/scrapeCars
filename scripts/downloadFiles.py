import requests
from itertools import islice
import itertools
import random
from PIL import Image
from io import open as iopen
from io import StringIO as StringIO
from io import BytesIO as BytesIO
import json
import socket
import os
import sys
import os.path
from pathlib import Path
from multiprocessing import Pool

def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

def workFunc(task):       

    try:
        socket.setdefaulttimeout(10)
        i = requests.get(task['url'])
    except:
        error = '{0}\n'.format(json.dumps(task))
        return((False,task))

    if i.status_code == requests.codes.ok:
        filename = '{0}'.format(task['filename'])
        f = iopen(filename, 'wb')
        f.write(i.content)
        f.close()
        return((True,task))

def readTasking(fname):
    taskList = list()
    tasking = open(fname, 'r')
    for task in tasking:
        task = task.strip()
        task = json.loads(task) 
        myf = Path(task['filename'])
        if not myf.is_file():
            taskList.append( task)
    tasking.close()
    return taskList


def main():
    p = Pool()

    # file detailing what to download
    # each line should be of format:
    # fileType,color,make,odel,url,namehash
    fname = sys.argv[1]

    taskList = readTasking(fname)

    print('processed {0} lines to download'.format(len(taskList)))
  
    print('tasking loaded')

    good = open(fname+'.good','w')
    bad = open(fname+'.bad','w')
 
    atOnce = 1000   
    # do the downloads in batches
    for batch in grouper(atOnce,taskList):

        retval = p.map(workFunc,taskList)

        for r,t in retval:
            if r:
                good.write(json.dumps(t))
            else:
                bad.write(json.dumps(t))

    good.close()
    bad.close()    

if __name__ == '__main__':
    main()
