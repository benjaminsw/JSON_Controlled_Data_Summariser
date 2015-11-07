import json
import os
import sys
import re

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

def describedata(header,data):
    summariseddata=[]
    for h in header:
        if str(type(data[header.index(h)][1])) ==  "<type 'int'>":
            summariseddata.append({'name':h,'type':'numeric', 'min':min(data[header.index(h)]),'max':max(data[header.index(h)])})
        elif str(type(data[header.index(h)][1])) ==  "<type 'str'>":
            summariseddata.append({'name':h, 'type':'string', 'uniquevalues':len(set(data[header.index(h)]))})
    return summariseddata

def readCSVdata(infile, delimiter=','):

    with open(infile, 'r') as f:
        line1 = f.readline().strip().split(delimiter)
        line2 = f.readline().strip().split(delimiter)
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
            line = line.strip().split(delimiter)
            line = [toint(s) for s in line ]
            rowdata.append(line)

    coldata = map(list, zip(*rowdata))
    return  {'header':header, 'data':coldata, 'hasheader':hasheader}

def createmetadataCSV(infile):
    return readCSVdata(infile=infile,delimiter=',')


def createmetadataTXT(infile):
    return readCSVdata(infile=infile,delimiter='\t')


def createmetadataJSON(infile):
    print infile
    #will update soon

def createmetadata(infile, ext, outfile):
    if ext == 'csv':
        data = createmetadataCSV(infile=infile)
    elif ext == 'json':
        createmetadataJSON(infile=infile)
    elif ext == 'txt':
        data = createmetadataTXT(infile=infile)
    summariseddata = describedata(header = data['header'], data = data['data'])
    print summariseddata

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
    locfile = jdata['infile']
    lstfileext = re.split(r'[.]',locfile)
    #print lstfileext
    ext = lstfileext[-1]
    outfile = jdata['metafile']

    createmetadata(infile=locfile, ext=ext, outfile=outfile)

if __name__ == '__main__':
    main()


