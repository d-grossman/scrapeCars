import json
import random


def main():

    testing = open('testing', 'w')
    tasking = open('allFiles', 'r')

    cars = dict()

    for task in tasking:
        task = task.strip()
        d = json.loads(task)
        if d['make'] not in cars:
            cars[d['make']] = dict()

        if d['model'] not in cars[d['make']]:
            cars[d['make']][d['model']] = list()
        cars[d['make']][d['model']].append(task)

    tasking.close()

    for make in cars.keys():
        for model in cars[make].keys():
            carray = cars[make][model]
            number = len(carray)
            tp = int(number * 0.20)
            random.shuffle(carray)
            keys = carray[:tp]
            print(len(keys), len(carray))
            for key in keys:
                testing.write('{0}\n'.format(key))

    testing.close()

if __name__ == '__main__':
    main()
