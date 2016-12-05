import os


def main():
    carfile = open('cars', 'r')
    colorfile = open('colors', 'r')

    colors = set()
    makes = set()

    for color in colorfile:
        colors.add(color.strip())
    colorfile.close()

    for car in carfile:
        car = car.strip()
        data = car.split(',')
        makes.add(data[0].replace(' ', '_'))

    carfile.close()

    for color in colors:
        for make in makes:
            newdir = os.path.join(color, make)
            if not os.path.exists(newdir):
                os.makedirs(newdir)

if __name__ == '__main__':
    main()
