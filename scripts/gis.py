import json
from hashlib import md5
from urllib.request import Request
from urllib.request import urlopen

from bs4 import BeautifulSoup


# read the make and model from a file
# file is in format of:
# make,model
def readCars(carFile):
    cars = dict()
    mm = open(carFile, 'r')
    allmm = mm.readlines()
    mm.close()
    for item in allmm:
        me, ml = item.split(',', 1)
        make = me.strip()
        model = ml.strip()

        if make not in cars:
            cars[make] = set()

        cars[make].add(model)
    return cars


# read the acceptable colors from a file
# file is in the format of:
# color
def readColors(colorFile):
    colors = list()
    c = open(colorFile, 'r')
    allc = c.readlines()
    c.close()
    for i in allc:
        colors.append(i.strip())
    return colors


# download a file with a given user-agent string
def get_soup(url, header):
    # return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,
    # headers=header)), 'html.parser')
    return BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')


# format item metadata
def makeLine(color, make, model, img, Type):
    d = dict()
    d['make'] = make
    d['model'] = model
    d['color'] = color
    text = '' + color + make + model + img
    m = md5()
    m.update(text.encode('utf-8'))
    d['hash'] = m.hexdigest()
    d['filename'] = '{0}/{1}/{2}.{3}'.format(color, make, d['hash'], Type)
    d['url'] = img
    return d


# for a specific make model and color of car attempt to get num images
def getCAR(color, makeIn, modelIn, num, outFile, outError):
    make = makeIn.replace(' ', '+')
    model = modelIn.replace(' ', '+')
    query = '{0}+{1}+{2}'.format(color, make, model)
    # url = 'https://www.google.co.in/search?q=' + query + '&source=lnms&tbm=isch'
    url = 'https://www.google.co.in/search?q=' + query + '&tbs=sur:fc&tbm=isch'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
    try:
        soup = get_soup(url, header)
        ActualImages = []
        for a in soup.find_all('div', {'class': 'rg_meta'}):
            link, Type = json.loads(a.text)['ou'], json.loads(a.text)['ity']
            ActualImages.append((link, Type))

        for i, (img, Type) in enumerate(ActualImages[:num]):
            if Type is not None:
                # write out where to get the image from
                data = makeLine(color, makeIn, modelIn, img, Type)
                outFile.write(json.dumps(data) + '\n')

    except:
        # spout some error messages when things go poorly
        data = makeLine(color, makeIn, modelIn, img, 'FAIL')
        outError.write(json.puts(data) + '\n')


def main(imagesPerMakeModel=100):
    cars = readCars('cars')
    colors = readColors('colors')

    outFile = open('dataset', 'w')
    outError = open('errorset', 'w')

    for color in colors:
        for make in cars.keys():
            for model in cars[make]:
                # time.sleep(2)
                getCAR(color, make, model, imagesPerMakeModel, outFile, outError)
                outFile.flush()
                outError.flush()

    outFile.close()
    outError.close()


if __name__ == '__main__':
    main()
