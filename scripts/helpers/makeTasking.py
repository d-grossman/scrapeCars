import md5

def main():
    items = 0

    images = open('dataset', 'r')
    tasking = open('tasking', 'w')

    for image in images.xreadlines():
        image = image.strip()
        m = md5.new(image)
        digest = m.hexdigest()
        task = '{0}|{1}\n'.format(image, digest)
        tasking.write(task)
        items = items + 1
    images.close()
    tasking.close()

    print 'processed {0} items'.format(items)
if __name__ == '__main__':
    main()
