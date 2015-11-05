import os
import sys

def createMetadataCSV(fname):
    #will update soon

def createMetadataJSON(fname):
    #will update soon


def createMetadata(fname, ext):
    if ext == '.csv':
        createMetadataCSV(fname=fname)
    elif ext == '.json':
        createMetadataJSON(fname=fname)

def main():
    #check if file exists
    try:
        with open(sys.argv[1]) as file:
            pass
    except IOError:
        print 'There was an error opening the file!'
        return
    acceptedFormat = ('.csv', '.txt', '.json')
    # Split the extension from the path and normalise it to lowercase.
    inputFile = os.path.splitext(sys.argv[1].lower())
    ext = inputFile[-1]
    fname = sys.argv[1]
    if ext not in acceptedFormat:
        print 'Please input "CSV", "TSV" or "JSON"'
        return
    createMetadata(fname=fname, ext=ext)

if __name__ == '__main__':
    main()


