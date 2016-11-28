import md5

def main():
    hashes = set()
    items = 0

    images = open('dataset','r')

    for image in images.xreadlines():
        image = image.strip()
        m = md5.new(image)
        digest = m.hexdigest()
        if digest in hashes:
            print 'collision {}'.format(digest)
        hashes.add(digest)
        items = items + 1
    images.close()

    print 'processed {0} items'.format(items)
if __name__ == '__main__':
    main()
