import json


def main():
    testing = open('testing', 'r')
    tasking = open('allFiles', 'r')
    training = open('training', 'w')

    testSet = set()

    for test in testing:
        test = test.strip()
        d = json.loads(test)
        testSet.add(d['hash'])
    testing.close()

    for task in tasking:
        task2 = task.strip()
        d = json.loads(task2)
        if d['hash'] not in testSet:
            training.write(task)

    training.close()
    tasking.close()

if __name__ == '__main__':
    main()
