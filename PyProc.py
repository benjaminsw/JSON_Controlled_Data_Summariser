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
    except TypeError:
        return None

def toascii(string):

    try:
        return float(string)
    except ValueError:
        return string.encode('ascii','ignore')

def describedata(header,data):

    summariseddata=[]
    for h in header:
        #http://stackoverflow.com/questions/16096754/remove-none-value-from-a-list-without-removing-the-0-value
        noneremoved =  [x for x in data[header.index(h)] if x is not None]
        if str(type(noneremoved[0])) ==  "<type 'int'>":
            #http://stackoverflow.com/questions/29422691/how-to-count-the-number-of-occurences-of-none-in-a-list
            summariseddata.append({'name':h,'type':'numeric', 'min':min(noneremoved), 'max':max(noneremoved), 'missing':len(filter(lambda x: x is None, data[header.index(h)]))})
        if str(type(noneremoved[0])) ==  "<type 'float'>":
            summariseddata.append({'name':h,'type':'numeric', 'min':min(noneremoved), 'max':max(noneremoved), 'missing':len(filter(lambda x: x is None, data[header.index(h)]))})
        elif str(type(noneremoved[0])) ==  "<type 'str'>":
            summariseddata.append({'name':h, 'type':'string', 'uniquevalues':len(set(noneremoved)), 'missing':len(filter(lambda x: x is None, data[header.index(h)]))})
    return summariseddata

def readCSVdata(infile, delimiter=','):

    with open(infile, 'r') as f:
        line1 = f.readline().strip().split(delimiter)
        #check if there are any missing value
        bool1 = [(not s or s.isspace()) for s in line1]
        #replace it with None
        line1 = [i if not j else None for i, j in zip(line1, bool1)]
        line2 = f.readline().strip().split(delimiter)
        bool2 = [(not s or s.isspace()) for s in line2]
        line2 = [i if not j else None for i, j in zip(line2, bool2)]
        boolline1 = [isint(s) for s in line1 ]
        #boolline2 = [isint(s) for s in line2 ]
        #if not(boolline1 == boolline2):
        if sum(boolline1)==0:
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
            bool = [(not s or s.isspace()) for s in line]
            line = [i if not j else None for i, j in zip(line, bool)]
            line = [toint(s) for s in line ]
            rowdata.append(line)
    coldata = map(list, zip(*rowdata))
    return  {'header':header, 'data':coldata, 'hasheader':hasheader}

def readTXTdata(infile, delimiter='\t'):

    with open(infile, 'r') as f:
        line1 = f.readline().strip().split(delimiter)
        #check if there are any missing value
        bool1 = [(not s or s.isspace()) for s in line1]
        #replace it with None
        line1 = [i if not j else None for i, j in zip(line1, bool1)]
        line2 = f.readline().strip().split(delimiter)
        bool2 = [(not s or s.isspace()) for s in line2]
        line2 = [i if not j else None for i, j in zip(line2, bool2)]
        boolline1 = [isint(s) for s in line1 ]
        #boolline2 = [isint(s) for s in line2 ]
        #if not(boolline1 == boolline2):
        if sum(boolline1)==0:
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
            bool = [(not s or s.isspace()) for s in line]
            line = [i if not j else None for i, j in zip(line, bool)]
            line = [toint(s) for s in line ]
            rowdata.append(line)
    coldata = map(list, zip(*rowdata))
    return  {'header':header, 'data':coldata, 'hasheader':hasheader}

def readJSONdata(infile):
    jdata = []
    header =[]
    rowdata = []
    with open(infile, 'r') as f:
        for line in f:
            jdata.append(json.loads(line))
    #rowdata=[]
    for j in jdata:
        tmpheader = []
        #lambda sort by keys in descending order http://stackoverflow.com/questions/20577840/python-dictionary-sorting-in-descending-order-based-on-values
        for k,v in collections.OrderedDict(sorted(j.items(), key=lambda t: t[0])).iteritems():
            tmpheader.append(toascii(k))
        if  len(tmpheader) > len(header):
            header = tmpheader
    for j in jdata:
        #http://stackoverflow.com/questions/17321138/python-one-line-list-comprehension-if-else-variants
        rowdata.append([toascii(j[k]) if k in j else None for k in header ])
    coldata = map(list, zip(*rowdata))
    return {'data':coldata, 'header':header, 'hasheader':True}

def createmetadata(infile, ext, outfile):

    if ext == 'csv':
        sep = ','
        data = readCSVdata(infile=infile,delimiter=sep)
        data['sep']=sep
        data['type']='tabular'
    elif ext == 'json':
        sep = ':'
        data = readJSONdata(infile=infile)
        data['sep']=sep
        data['type']='json'
    elif ext == 'txt':
        sep = '\t'
        data = readTXTdata(infile=infile,delimiter=sep)
        data['sep']=sep
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


