import json
from pprint import pprint
data = []
with open('D:/Dropbox/StirUni/ITNPBD2/assignment/data/cars.json','r') as f:
    #for line in f.readlines():
        #data = f.readline().strip()
        #print data
    #data = f.readline()
#print(data)

    for line in f:
        data.append(json.loads(line))

print data