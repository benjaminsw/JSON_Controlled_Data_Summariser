import os
import sys

def isint(value):
  try:
    int(value)
    return True
  except:
    return False

def toint(string):
    try:
        return int(string)
    except ValueError:
        return string

def createmetadataCSV(fname):

    data=readCSVdata(fname)
    summariseddata = describedata(header = data['header'], data = data['data'])
    print {'filename':str(os.getcwd()+'\\'+fname),
           'format':{'type':'tabular', 'sep':','},
           'header':data['hasheader']}

def describedata(header,data):
    summariseddata=[]
    for h in header:
        if str(type(data[header.index(h)][1])) ==  "<type 'int'>":
            summariseddata.append({'name':h,'type':'numeric', 'min':min(data[header.index(h)]),'max':max(data[header.index(h)])})
        elif str(type(data[header.index(h)][1])) ==  "<type 'str'>":
            summariseddata.append({'name':h, 'type':'string', 'uniquevalues':len(set(data[header.index(h)]))})
    return summariseddata

def readCSVdata(fname):

    with open(fname, 'r') as f:
        line1 = f.readline().strip().split(',')
        line2 = f.readline().strip().split(',')
        boolline1 = [isint(s) for s in line1 ]
        boolline2 = [isint(s) for s in line2 ]
        if not(boolline1 == boolline2):
            header = line1
            hasheader = True
            line2 = [toint(s) for s in line2 ]
            rowdata=[line2]
        else:
            header = ['Var'+str(i) for i in range(1,len(line1)+1)]
            hasheader = False
            line1 = [toint(s) for s in line1 ]
            line2 = [toint(s) for s in line2 ]
            rowdata = [line1,line2]
        for line in f.readlines():
            line = line.strip().split(',')
            line = [toint(s) for s in line ]
            rowdata.append(line)

    coldata = map(list, zip(*rowdata))
    return  {'header':header, 'data':coldata, 'hasheader':hasheader}

'''
        #l,name = line.strip().split(',')
        #lines.append((l,name))
'''



def createmetadataJSON(fname):
    print fname
    #will update soon


def createmetadata(fname, ext):
    if ext == '.csv':
        createmetadataCSV(fname=fname)
    elif ext == '.json':
        createmetadataJSON(fname=fname)

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




