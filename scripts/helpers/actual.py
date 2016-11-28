import json
tasking = open('tasking','r')
downloaded = open('downloaded','r')
actual = open('actual','w')

cars = dict()

for task in tasking:
    typ,color,make,model,url,h = task.strip().split('|')
    cars[h] = (typ,color,make,model,url,h)
tasking.close()

for item in downloaded:
    item = item.strip()
    dot,color,car,filename = item.split('/')
    h,ext = filename.split('.')
    
    outDict = dict()
    if h in cars:
        c = cars[h]
        outDict['color'] = c[1]
        outDict['make'] = c[2]
        outDict['model'] = c[3]
        outDict['url'] = c[4] 
        outDict['hash'] = h
        outDict['filename'] = '{0}/{1}/{2}.jpg'.format(c[1],c[2].replace(' ','_'),h)
        json.dump(outDict,actual)
        actual.write('\n')
    
     
downloaded.close()
actual.close()        
