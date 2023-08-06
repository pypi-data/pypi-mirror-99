import sys
from einsteinify import einsteinify

def main():
    if len(sys.argv) < 2:
        raise Exception("You must specify the path as argument of the program")

    PATH = sys.argv[1]
    einsteinify(PATH)

if __name__ == '__main__':
    main()