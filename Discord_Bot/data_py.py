import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from matplotlib import pyplot as mp
import csv
import os
plt.style.use('ggplot')


tech = list()
val = list()
with open('techData.csv') as csvfile:
    read = csv.reader(csvfile, delimiter = ',')
    for row in read:
        if(row[0] == "machine learning"):
            tech.append('ML')
        elif(row[0] == "amazon web service"):
            tech.append('AWS')
        else:
            tech.append(row[0])
        val.append(int(row[1]))

index = np.arange(len(tech))
plt.bar(index, val, align = 'center', alpha = 1)
plt.xlabel('Technology', fontsize=12)
plt.ylabel('Tech Demand', fontsize=12)
plt.xticks(index, tech, fontsize=5, rotation=90)
plt.title('Tech Used in Data Science')
mp.savefig('foo.png', dpi=720)

