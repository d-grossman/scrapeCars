import os

def main():
    outFile = open('tasking.continue','w')
    taskFile = open('tasking','r')
    hashFile = open('done','r')

    hashSet = set()

    for hash in hashFile:
        hashSet.add(hash.strip())
    hashFile.close()

    for task in taskFile:
        task = task.strip()
        fileType, color, make, model, url, nameHash = task.split('|')
        if nameHash not in hashSet:
            outFile.write('{0}\n'.format(task))
    taskFile.close()
    outFile.close()
    

     

if __name__ == '__main__':
    main()
