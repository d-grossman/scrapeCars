tasking = open('tasking','r')
remove = open('removeFiles.txt','r')

cars = dict()

for task in tasking:
    typ,color,make,model,url,h = task.strip().split('|')
    cars[h] = './{0}/{1}/{2}.jpg'.format(color,make,h)

for item in remove:
    if item.strip() in cars:
        print(cars[item.strip()])
