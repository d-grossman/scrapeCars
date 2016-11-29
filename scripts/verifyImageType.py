from resnet50 import ResNet50
from keras.preprocessing import image
from imagenet_utils import preprocess_input, decode_predictions
import numpy as np
import json
import time
import sys
from multiprocessing import Pool
import functools

def readTasking(filename):

    tasking = open(filename,'r')
    data = list()
    fileProblems = list()

    for task in tasking:
        task = task.strip()
        line = json.loads(task)
        data.append(line)
    tasking.close()
    return data

def procLine2(l, r):
    img_path = '{0}/{1}'.format(r,l['filename'])
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        return (1,l['filename'])
    except:
        return (0,l['filename'])

def writeTasking(filename, tasking, bad):
    outFile = open(filename,'w')
    badFiles = set()
    for item in bad:
        if item[0] == 0:
            badFiles.add(item[1])
    for task in tasking:
        if task['filename'] not in badFiles:
            outFile.write(json.dumps(task)+'\n')

    outFile.close()
            
        
def main():
    procLine = functools.partial(procLine2, r=sys.argv[2] )
    p = Pool()
    tasking = readTasking(sys.argv[1])
    files = p.map(procLine,tasking)
    writeTasking(sys.argv[1]+'.new',tasking,files)


if __name__ == '__main__':
    main()

