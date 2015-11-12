line1 = ['Fiat', 'Black', 'Punto', '33872', '1745']
line1 = ['foo', ' ', '\r\n\t', '', None]
bool1 = [(not s or s.isspace()) for s in line1]
line1 = [i if not j else None for i, j in zip(line1, bool1) ]
#print set(line1)
#######################
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
infile = "D:/Dropbox/StirUni/ITNPBD2/assignment/data/carsm.txt"
import re
def readTXTdata(infile, delimiter='\t'):

     with open(infile, 'r') as f:
         line1 = f.readline().split(delimiter)
         line1 = [None if re.match( r'\n', x) else x.strip() for x in line1]
         line2 = f.readline().split(delimiter)
         line2 = [None if re.match( r'\n', x) else x.strip() for x in line2]
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
             #line = line.strip().split(delimiter)
             line = line.split(delimiter)
             line = [None if re.match(r'\n', x) else x.strip() for x in line]
             line = [toint(s) for s in line ]
             rowdata.append(line)
     coldata = map(list, zip(*rowdata))
     return  {'header':header, 'data':coldata, 'hasheader':hasheader}



readTXTdata(infile, delimiter='\t')