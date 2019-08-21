import jcamp
import matplotlib.pyplot as plt
import sys
import numpy
import numpy as np
numpy.set_printoptions(threshold=sys.maxsize)
import os 
import jcamp
import pandas as pd
from pandas import DataFrame
#example kinetic file
file = open('examplekinetic.ir',"r")
def ConvertToFloat(inputNumber):

    return "{0:.20f}".format(inputNumber).rstrip("0")
allspectra = ['']
def kineticsparser(name):
    file = open(name,"r")
    count = 0
    
    new = ''
    also = ''
    for line in file:
       
       count += 1
       if count == 6:
           lastx = line
           
       elif count == 7:
           firstx = line
       elif count == 9 :
           interval = int(line)
           
       elif count > 13:
           
           #k = np.float32(line)
           k = float(line)
           ok = (int(lastx)-2)+((count-13)*interval) # ascending x axis
           tr = (int(lastx)-2)-((count-13)*interval)
           #descending x axis
           L =  ((str(tr)) + ' ' + (str(k)) + '\n')
           new += L
           also = also + str(k) + ',' 
    
    alljcamp = '##TITLE=Methyl Ethyl Ketone\n##JCAMP-DX=4.24\n##DATA TYPE=INFRARED SPECTRUM\n##XUNITS=cm-1\n##YUNITS=Absorbance\n##FIRSTX=' + str(firstx)+'##LASTX=' + str(lastx) +'##XYDATA=(X++(Y..Y))\n' + new
    filename = name.split('.')
    filename = filename[0] + 'jcamp' + '.jdx'
    f = open(filename, 'w+')
    f.write(alljcamp)
    return(also)

print(allspectra)   

#iterate over entire directory to convert every file to FTIRDB

for filename in os.listdir('C:/ftirdb/ftirdb/data/kinetics'):
    if filename.endswith(".ir"):
    
        filename = 'C:/ftirdb/ftirdb/data/kinetics/' + str(filename)
        values = kineticsparser(filename)
        allspectra.append(values.split(","))
print(len(allspectra))
print(allspectra[1])
hiii = list(range(900,2304, 2))
plt.plot(hiii, allspectra[1], label='filename', linewidth=0.2, color = 'red')
plt.show()
#iterate over entire jdx directory to collect all x,y coardinates - practice plotting all
y_array = []
count = 0
count5 = 0
fig = plt.figure(1)
for filename in os.listdir('C:/ftirdb/ftirdb/data/kinetics/JDX files'):
    count += 1 
    new = jcamp.JCAMP_reader('C:/ftirdb/ftirdb/data/kinetics/JDX files/' + str(filename))
    x_array =(new['x'][0:702])
    #print(len(new['x']))
    y_array.append((new['y']))
    
    #print(len(new['y']))
    hiii = list(range(900,2304, 2))
    plt.xlim(max(x_array), 900,2)
    
    if (count < 100):
            
            #if new['y'][350] > 20:
                
            plt.plot(hiii, allspectra[count], label='filename', linewidth=0.2, color = 'red')
           
            
    elif count < 200:
            plt.plot(hiii, allspectra[count], label='filename', linewidth=0.2, color = 'blue')
            pass
    elif count < 300:
            plt.plot(hiii, allspectra[count], label='filename', linewidth=0.2, color = 'pink')
            pass
    else:
            plt.plot(hiii, allspectra[count], label='filename', linewidth=0.2, color = 'green')
            pass
   



import csv
 
my_df = pd.DataFrame(allspectra)
please = DataFrame.from_records(allspectra)
please.to_csv('my_csv.csv',index=False, header=False)
with open("newfile.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(allspectra)

with open('x.csv', 'w+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(x_array)

fig.savefig('fun.png')


