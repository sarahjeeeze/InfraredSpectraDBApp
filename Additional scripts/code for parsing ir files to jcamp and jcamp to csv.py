import jcamp
import matplotlib.pyplot as plt
import sys
import numpy
import numpy as np
numpy.set_printoptions(threshold=sys.maxsize)
import os 
import jcamp
#example kinetic file
file = open('kinetic2.ir',"r")

def kineticsparser(name):
    file = open(name,"r")
    count = 0
    
    new = ''
    for line in file:
       
       count += 1
       if count == 7:
           lastx = line
       elif count == 6:
           firstx = line
       elif count == 9 :
           interval = int(line)
           
       elif count > 13:
           k = line
           
           
           ok = (int(lastx)-2)+((count-13)*interval) # ascending x axis
           tr = (int(firstx)+2)-((count-13)*interval) #descending x axis
           L =  ((str(tr)) + ' ' + (str(k)))
           new += L
    alljcamp = '##TITLE=Methyl Ethyl Ketone\n##JCAMP-DX=4.24\n##DATA TYPE=INFRARED SPECTRUM\n##XUNITS=cm-1\n##YUNITS=Absorbance\n##FIRSTX=' + str(firstx)+'##LASTX=' + str(lastx) +'##XYDATA=(X++(Y..Y))\n' + new
    filename = name.split('.')
    filename = filename[0] + 'jcamp' + '.jdx'
    f = open(filename, 'w+')
    f.write(alljcamp)

    

#iterate over entire directory to convert every file to FTIRDB

for filename in os.listdir('C:/ftirdb/ftirdb/data/kinetics'):
    if filename.endswith(".ir"):
    
        filename = 'C:/ftirdb/ftirdb/data/kinetics/' + str(filename)
        kineticsparser(filename)

#iterate over entiry jdx directory to collect all x,y coardinates - practice plotting all
y_array = []
for filename in os.listdir('C:/ftirdb/ftirdb/data/kinetics/JDX files'):
    new = jcamp.JCAMP_reader('C:/ftirdb/ftirdb/data/kinetics/JDX files/' + str(filename))
    x_array =(new['x'])[0:701]   
    y_array.append((new['y'])[0:701])
    plt.plot(new['x'], new['y'], label='filename', linewidth=0.2)
import csv
 
print(len(y_array))

y_array = np.array(y_array).T.tolist()

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(y_array)

with open('x.csv', 'w+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(x_array)

