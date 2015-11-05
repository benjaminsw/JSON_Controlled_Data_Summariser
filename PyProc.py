import os
import sys


def createMetadata(fname, ext):
    #will update soon





def main():
    #check if file exists
    try:
        with open(sys.argv[1]) as file:
            pass
    except IOError:
        print('There was an error opening the file!')
        return
    acceptedFormat = ('.csv', '.txt', '.json')
    # Split the extension from the path and normalise it to lowercase.
    inoutFile = os.path.splitext(sys.argv[1].lower())
    ext = inoutFile[-1]
    fname = sys.argv[1]
    createMetadata(fname=fname, ext=ext)

if __name__ == '__main__':
    main()


