import sys
import re
import json
import collections

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

def toascii(string):

    try:
        return float(string)
    except ValueError:
        return string.encode('ascii','ignore')

def describedata(header,data):

    summariseddata=[]
    for h in header:
        if str(type(data[header.index(h)][1])) ==  "<type 'int'>":
            summariseddata.append({'name':h,'type':'numeric', 'min':min(data[header.index(h)]),'max':max(data[header.index(h)])})
        if str(type(data[header.index(h)][1])) ==  "<type 'float'>":
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

def readJSONdata(infile):

    jdata = []
    with open(infile, 'r') as f:
        for line in f:
            jdata.append(json.loads(line))

    rowdata=[]
    for j in jdata:
        val=[]
        header = []
        #lambda sort by keys in descending order http://stackoverflow.com/questions/20577840/python-dictionary-sorting-in-descending-order-based-on-values
        for k, v in collections.OrderedDict(sorted(j.items(), key=lambda t: t[0])).iteritems():
            val.append(toascii(v))
            header.append(k)
        rowdata.append(val)
    coldata = map(list, zip(*rowdata))
    return {'data':coldata, 'header':header, 'hasheader':True}


def createmetadata(infile, ext, outfile):

    if ext == 'csv':
        data = readCSVdata(infile=infile,delimiter=',')
        data['sep']=','
        data['type']='tabular'
    elif ext == 'json':
        data = readJSONdata(infile=infile)
        data['sep']=':'
        data['type']='json'
    elif ext == 'txt':
        data = readCSVdata(infile=infile,delimiter='\t')
        data['sep']='\t'
        data['type']='tabular'
    summariseddata = describedata(header = data['header'], data = data['data'])
    metadata = {'filename':infile,
                'format':{'type':data['type'],'sep':data['sep']},
                'headerrow':int(data['hasheader']),
                'numentries':len(data['data'][1]),
                'numfields':len(data['header']),
                'fields':summariseddata}
    writetoJSON(metadata=metadata, outfile=outfile)

def writetoJSON(metadata, outfile):

    with open(outfile, 'w') as fp:
        json.dump(metadata, fp)

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
    ext = lstfileext[-1]
    outfile = jdata['metafile']
    createmetadata(infile=locfile, ext=ext, outfile=outfile)
    print 'The program has been successfully executed'
    print 'Benjamin Wiriyapong SID:2426366'

if __name__ == '__main__':
    main()


