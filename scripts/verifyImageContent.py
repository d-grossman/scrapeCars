import sys
import os
import os.path
import json
import time
import numpy as np
import tensorflow as tf
from keras import backend as K
from resnet50 import ResNet50
from keras.preprocessing import image
from imagenet_utils import preprocess_input, decode_predictions

def readTasking(fname):
    af = open(fname,'r')
    data = list()
    for d in af:
        d = d.strip()
        data.append(json.loads(d))
    return data


def proc(taskFile,rootDir,atOnce=10000):
    model = ResNet50(weights='imagenet')
        
    good = list()
    bad = list()
    ugly = list()
    
    count = 0

    interesting = set()
    for x in ['car','pickup','suv','truck','crossover','van','minivan','sports_car','cab','racer','convertible','car_wheel','jeep','ambulance']:
        interesting.add(x)
    
    data = readTasking(taskFile)
    start = time.time() 
    for d in data:

        img_path = '{0}/{1}'.format(rootDir,d['filename'])
        flag = True

        try:
            img = image.load_img(img_path, target_size=(224, 224)) 
        
        except:
            ugly.append(d)
            flag = False
 
        if flag:
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            preds = model.predict(x)
            predictions = decode_predictions(preds)[0][:4]
            found = False
            for prediction in predictions:
                i,t,score = prediction
                if t in interesting:
                    good.append((d,t))
                    found = True
                    break
            if not found:
                bad.append((d,predictions[0][1]))

        if count == atOnce:
            count = 0
            im = im + 1
            z = time.time() - s
            print('processed:',im * atOnce,'Images','good',len(good),'bad',len(bad),'file',len(file),z)
            s = time.time()
        count = count + 1 

    return (good,bad,ugly)

def writeList(l,fname):
    fn = open(fname,'w')
    for item in l:
        fn.write(json.dumps(item)+'\n')
    fn.close()

def main():
    good,bad,ugly = proc(sys.argv[1],sys.argv[2])

    writeList(good,argv[1]+'.good')
    writeList(bad,argv[1]+'.bad')
    writeList(ugly,argv[1]+'.ugly')

if __name__ == '__main__':
    os.environ['THEANO_FLAGS']='mode=FAST_RUN,device=gpu,floatX=float32'
    main()
