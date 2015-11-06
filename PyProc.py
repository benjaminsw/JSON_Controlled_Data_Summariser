
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
        print 'Please supply "CSV", "TSV" or "JSON" file'
        return
    createmetadata(fname=fname, ext=ext)

if __name__ == '__main__':
    main()


