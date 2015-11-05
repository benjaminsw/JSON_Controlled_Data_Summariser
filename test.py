import os
import sys



def printPath(fpath):
    print fpath

ext = os.path.splitext(sys.argv[1])[-1].lower()
#filePath = os.path.splitext(sys.argv[1])[-1].lower()
printPath(ext)


