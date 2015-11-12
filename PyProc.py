import sys
import re
import json
import collections

def isint(value):
    '''
    :param value: a string
    this function receives a string and check if it consists of number
    :return: - True if string can be casted to int,
             - False otherwise
    '''
    try:
        int(value)
        return True
    except:
        return False

def toint(string):
    '''
    :param string: a string
    this function receives a string and tries to cast it to int
    :return: - int of the string if successful.
             - if it is a string, return string.
             - if receives non-type, return None
    '''
    try:
        return int(string)
    except ValueError:
        return string
    except TypeError:
        return None

def toascii(string):
    '''
    :param string: a string which is of a unicode type
    this function receives a unicode string and tries to determine if it is a number
    if not return a string of unicode type
    :return: - a float if string is a number.
             - the same string of ascii type, otherwise.
    '''
    try:
        return float(string)
    except ValueError:
        return string.encode('ascii','ignore')

def describedata(header,data):
    '''
    :param header: a list which represents a header retrieved from infile data in readCSVdata, readTXTdata or readJSONdata
    :param data: a list os lists which represents the body of data which is represent as vectors of same data type
    this function construct basic statistical summary of data in 'data'
    if string, tells data type, count possible values and also count missing values
    if int or float, tell data type, find min and max and the number of missing values
    :return:a dictionary that summarises data. each key is a field from header and values are summarisation of that key
    '''
    summariseddata=[]
    for h in header:
        #remove 'None' and put it back to 'noneremoved'
        #http://stackoverflow.com/questions/16096754/remove-none-value-from-a-list-without-removing-the-0-value
        noneremoved =  [x for x in data[header.index(h)] if x is not None]
        if str(type(noneremoved[0])) ==  "<type 'int'>":
            #the number of missing values is represented by counting the number of 'None' occuring in each list in 'data'
            #http://stackoverflow.com/questions/29422691/how-to-count-the-number-of-occurences-of-none-in-a-list
            summariseddata.append({'name':h,'type':'numeric', 'min':min(noneremoved), 'max':max(noneremoved), 'missing':len(filter(lambda x: x is None, data[header.index(h)]))})
        if str(type(noneremoved[0])) ==  "<type 'float'>":
            summariseddata.append({'name':h,'type':'numeric', 'min':min(noneremoved), 'max':max(noneremoved), 'missing':len(filter(lambda x: x is None, data[header.index(h)]))})
        elif str(type(noneremoved[0])) ==  "<type 'str'>":
            summariseddata.append({'name':h, 'type':'string', 'uniquevalues':len(set(noneremoved)), 'missing':len(filter(lambda x: x is None, data[header.index(h)]))})
    return summariseddata

def readCSVdata(infile, delimiter=','):
    '''
    :param infile: a string which is a path to a CSV file specified in JSON
    :param delimiter: a string which is a separator that uses to separate a token. default is a comma
    this function read in CSV file as specify in 'infile' and dissect it to
    - header: if it can be detected. if not, it generates 'Var1', 'Var2' etc. in accordance with the number of fields in the file
    - body/data: which purely represents data in the file. if missing propagate 'None' and also tries to detect tpe whether or not it can cast to an integer
    - hasheader: is a boolean value. true if file has a header. false, otherwise.
    :return: a dictionary consisting of header of the file, body of the file which is data and boolean if the file has a header in the first row.
    '''

    with open(infile, 'r') as f:
        #1)read in a line as a list. 2)split up data by commas in each line 3)strip out non string charectors.
        line1 = f.readline().strip().split(delimiter)
        #create a list of boolean. true if the value of that index of list is not missing. false, otherwise. missing values definitions: white space, empty string, new line character, tab character
        bool1 = [(not s or s.isspace()) for s in line1]
        #compare the list that keeps values againt boolean list that indicate position of missing values
        #if data is missing, propragate 'None' back to the list.
        line1 = [i if not j else None for i, j in zip(line1, bool1)]
        line2 = f.readline().strip().split(delimiter)
        bool2 = [(not s or s.isspace()) for s in line2]
        line2 = [i if not j else None for i, j in zip(line2, bool2)]
        #check if any element can convert to int. if it can assume that there is no header.
        boolline1 = [isint(s) for s in line1 ]
        #unused code------
        #boolline2 = [isint(s) for s in line2 ]
        #if not(boolline1 == boolline2):
        #unused code-------
        #check if there is a header
        if sum(boolline1)==0: #there is a header
            header = line1
            hasheader = True
            line2 = [toint(s) for s in line2 ]
            rowdata=[line2]
        else: #no header
            header = ['Var'+str(i) for i in range(1,len(line1)+1)]
            hasheader = False
            line1 = [toint(s) for s in line1 ]
            line2 = [toint(s) for s in line2 ]
            rowdata = [line1,line2]
        #read the rest of the file and attempt to cast to int if possible
        for line in f.readlines():
            line = line.strip().split(delimiter)
            bool = [(not s or s.isspace()) for s in line]
            line = [i if not j else None for i, j in zip(line, bool)]
            line = [toint(s) for s in line ]
            #append to a list of the entire dataset. this is a row dataset
            rowdata.append(line)
    #transpost from row dataset to column dataset inorder to keep the same data type in the same list
    coldata = map(list, zip(*rowdata))
    #concatinate header, data and and boolean hasheader to a dictionary and return
    return  {'header':header, 'data':coldata, 'hasheader':hasheader}

def readTXTdata(infile, delimiter='\t'):
    '''
    :param infile: a string which is a path to a TXT file specified in JSON
    :param delimiter: a string which is a separator that uses to separate a token. default is a tab
    this function read in TXT file as specify in 'infile' and dissect it to
    - header: if it can be detected. if not, it generates 'Var1', 'Var2' etc. in accordance with the number of fields in the file
    - body/data: which purely represents data in the file. if missing propagate 'None' and also tries to detect tpe whether or not it can cast to an integer
    - hasheader: is a boolean value. true if file has a header. false, otherwise.
    :return: a dictionary consisting of header of the file, body of the file which is data and boolean if the file has a header in the first row.
    '''
    #open file to read data
    with open(infile, 'r') as f:
        #1)read in a line as a list. 2)split up data by tabs in each line.
        line1 = f.readline().split(delimiter)
        #strip out non string charectors and if the last element contains only new line character, assume that data is missing or any other empty string, so propagate 'None'
        line1 = [None if re.match( r'\n|^$', x) else x.strip() for x in line1]
        line2 = f.readline().split(delimiter)
        line2 = [None if re.match( r'\n|^$', x) else x.strip() for x in line2]
        #check if it can cast to int
        boolline1 = [isint(s) for s in line1 ]
        #unused code--------
        #boolline2 = [isint(s) for s in line2 ]
        #if not(boolline1 == boolline2):
        #unused code--------
        if sum(boolline1)==0: #there is a header
            header = line1
            hasheader = True
            line2 = [toint(s) for s in line2 ]
            rowdata=[line2]
        else: #no header
            header = ['Var'+str(i) for i in range(1,len(line1)+1)]
            hasheader = False
            line1 = [toint(s) for s in line1 ]
            line2 = [toint(s) for s in line2 ]
            rowdata = [line1,line2]
        #read in the reast of the file
        for line in f.readlines():
            line = line.split(delimiter)
            line = [None if re.match(r'\n|^$', x) else x.strip() for x in line]
            line = [toint(s) for s in line ]
            rowdata.append(line)
    #change data stucture from raw data to column data
    coldata = map(list, zip(*rowdata))
    return  {'header':header, 'data':coldata, 'hasheader':hasheader}


def readJSONdata(infile):
    '''
    :param infile: a string which is a path to a JSON file specified in JSON argument
    this function read in JSON file as specify in 'infile' and dissect it to
    - header: by retrieve from key in json file
    - body/data: which purely represents data in the file. if missing propagate 'None' and also tries to detect tpe whether or not it can cast to an integer
    :return: a dictionary consisting of header of the file, body of the file which is data.
    '''
    jdata = []
    header =[]
    rowdata = []
    #open file and read each object and keep it in 'jdata' variable as a list of dictionary
    with open(infile, 'r') as f:
        for line in f:
            jdata.append(json.loads(line))
    #iterate through each object to find object which contain most key
    for j in jdata:
        tmpheader = []
        #lambda sort by keys in descending order http://stackoverflow.com/questions/20577840/python-dictionary-sorting-in-descending-order-based-on-values
        for k,v in collections.OrderedDict(sorted(j.items(), key=lambda t: t[0])).iteritems():
            tmpheader.append(toascii(k))
        if  len(tmpheader) > len(header):
            header = tmpheader
    #propaget data in to each column acordingly and also change from unicode to ascii
    for j in jdata:
        #http://stackoverflow.com/questions/17321138/python-one-line-list-comprehension-if-else-variants
        rowdata.append([toascii(j[k]) if k in j else None for k in header ])
    #transpost from row data to column data representation
    coldata = map(list, zip(*rowdata))
    return {'data':coldata, 'header':header, 'hasheader':True}

def createmetadata(infile, ext, outfile):
    '''
    :param infile: a string which is a path to a file
    :param ext: a string which is file extension
    :param outfile: a string which is a path and file name to write
    classify file to call a appropriate function to read data in appropriately
    :return: None
    '''
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
    #get an overview of data
    summariseddata = describedata(header = data['header'], data = data['data'])
    #create metadata in dictionary format, then send it to write
    metadata = {'filename':infile,
                'format':{'type':data['type'],'sep':data['sep']},
                'headerrow':int(data['hasheader']),
                'numentries':len(data['data'][1]),
                'numfields':len(data['header']),
                'fields':summariseddata}
    writetoJSON(metadata=metadata, outfile=outfile)

def writetoJSON(metadata, outfile):
    '''
    :param metadata: a dictionary of metadata to write
    :param outfile: a string of path and file name to write
    write a metadata dictionary to a file
    :return: None
    '''
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
    #get file extension
    ext = lstfileext[-1]
    outfile = jdata['metafile']
    createmetadata(infile=locfile, ext=ext, outfile=outfile)
    print 'The program has been successfully executed'
    print 'Benjamin Wiriyapong SID:2426366'

if __name__ == '__main__':
    main()


