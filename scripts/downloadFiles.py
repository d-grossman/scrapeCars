import requests
from PIL import Image
from io import open as iopen
from io import StringIO as StringIO
from io import BytesIO as BytesIO
import socket
import os
import sys


def main():
    # file detailing what to download
    # each line should be of format:
    # fileType,color,make,odel,url,namehash
    fname = sys.argv[1]
    tasking = open(fname, 'r')
    errorFile = open(fname + '.errors','w')
    doneFile = open(fname + '.done','w')

    for task in tasking:
        task = task.strip()
        fileType, color, make, model, url, nameHash = task.split('|')
        if fileType in ['jpg', 'gif', 'jpeg', 'bmp', 'png', 'tiff']:
            try:
                socket.setdefaulttimeout(10)
                i = requests.get(url)
            except:
                error = '{0}\n'.format(task)
                errorFile.write(error)

            if i.status_code == requests.codes.ok:
                filename = '{0}.{1}'.format(nameHash, 'jpg')
                outfile = os.path.join(color, make.replace(' ', '_'), filename)
                if fileType not in ['jpg', 'jpeg']:
                    try:
                        image = Image.open(BytesIO(i.content))
                        image.save(outfile, 'JPEG')
                        image.close()
                    except:
                        error = '{0}\n'.format(task)
                        errorFile.write(error)

                else:
                    f = iopen(outfile, 'wb')
                    f.write(i.content)
                    f.close()

        doneFile.write('{0}\n'.format(nameHash))

        doneFile.flush()        
        errorFile.flush()
 
    tasking.close()
    errorFile.close()


if __name__ == '__main__':
    main()
