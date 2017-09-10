# http://stackoverflow.com/questions/29377504/perform-a-google-search-and-return-the-number-of-results
import sys
import time

import requests
from bs4 import BeautifulSoup


def getNumber(words):

    r = requests.get(
        'http://www.google.com/search',
        params={
            'q': '"' + words + '"',
            'tbs': 'li:1'},
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find(
        'div', {
            'id': 'resultStats'}).text.split(' ')[1].replace(
        ',', '')


def main():
    cars = open('cars', 'r')
    types = open('types', 'r')
    outfile = open('results', 'w')

    t = list()

    for tt in types:
        t.append(tt.strip())
    types.close()
    for car in cars:
        car = car.strip()
        make, model = car.split(',', 2)
        results = '{0}|{1}|'.format(make, model)
        for item in t:
            time.sleep(1)
            searchString = '{0}+{1}+{2}'.format(
                make.replace(' ', '+'), model.replace(' ', '+'), item)
            print('searching for', searchString)
            results = results + getNumber(searchString) + ' '
        print(results)

        outfile.write('{0}\n'.format(results))
        outfile.flush()
        sys.stdout.flush()

if __name__ == '__main__':
    main()
