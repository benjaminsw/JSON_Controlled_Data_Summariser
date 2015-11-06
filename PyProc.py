import json
import os
import sys

def main():
    #check if file exists and wheter or not it is a json file
    try:
        with open(sys.argv[1]) as jsonfile:
            jdata = json.load(jsonfile)
    except IOError:
        print 'There was an error opening the file!'
        return
    except ValueError:
        print 'The file was not in json format!'
        return
    print(jdata)
    #createmetadata(fname=fname, ext=ext)

if __name__ == '__main__':
    main()


