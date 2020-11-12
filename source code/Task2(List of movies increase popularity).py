import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.pyplot import figure
figure(num=None, figsize=(90, 50), dpi=40, facecolor='w', edgecolor='k')
with open('Data_collection.json') as f:
 data = json.load(f)
tuple1 = []
tuple2 = []
for value in data['data']:
    #print(value['Title'], value['Positon'])
    tuple1.append(value['Popularity'])
    tuple2.append(value['Title'])
print(tuple(tuple1),tuple(tuple2))

tuple1
y_pos = np.arange(len(tuple1))
popularity_bar = tuple2

plt.bar(y_pos, popularity_bar, align='center', alpha=0.5)

plt.xticks(y_pos, tuple1)
plt.ylabel('Popularity of Movies')
plt.xlabel('List of Popularity')
plt.title('Populairy BAR CHAT')

plt.show()
