import jcamp
import matplotlib.pyplot as plt
import sys
import numpy
import numpy as np
numpy.set_printoptions(threshold=sys.maxsize)
import os 
import jcamp
import pandas as pd
#example kinetic file
file = open('kinetic2.ir',"r")

def kineticsparser(name):
    file = open(name,"r")
    count = 0
    
    new = ''
    for line in file:
       
       count += 1
       if count == 6:
           lastx = line
           
       elif count == 7:
           firstx = line
       elif count == 9 :
           interval = int(line)
           
       elif count > 13:
           k = float(line)
           
           ok = (int(lastx)-2)+((count-13)*interval) # ascending x axis
           tr = (int(lastx)-2)-((count-13)*interval)
           #descending x axis
           L =  ((str(tr)) + ' ' + (str(k)) + '\n')
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
count = 0 
for filename in os.listdir('C:/ftirdb/ftirdb/data/kinetics/JDX files'):
    count += 1 
    new = jcamp.JCAMP_reader('C:/ftirdb/ftirdb/data/kinetics/JDX files/' + str(filename))
    x_array =(new['x'])[0:701]   
    y_array.append((new['y'])[0:701])
    plt.xlim(max(x_array), 900,2)
    if count < 100:
        plt.plot(new['x'], new['y'], label='filename', linewidth=0.2, color = 'red')
    elif count < 200:
        plt.plot(new['x'], new['y'], label='filename', linewidth=0.2, color = 'blue')
    elif count < 300:
        plt.plot(new['x'], new['y'], label='filename', linewidth=0.2, color = 'pink')
    elif count < 350:
        plt.plot(new['x'], new['y'], label='filename', linewidth=0.2, color = 'green')
    
    else:
        plt.plot(new['x'], new['y'], label='filename', linewidth=0.2, color = 'brown')


for i in y_array:
    print(len(i))
import csv
 
my_df = pd.DataFrame(y_array)
my_df.to_csv('my_csv.csv',index=False, header=False)
with open("newfile.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(y_array)

with open('x.csv', 'w+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(x_array)
plt.show()
