# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 22:24:36 2022

@author: adamkritz
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

allepisodes = pd.read_csv(r'C:\Users\trash\Desktop\CCstuff\allepisodes100.csv', index = False)

ae_max = pd.DataFrame()    
for i in list(allepisodes.columns):  
    ae_max[i] = np.array(allepisodes[i].nlargest(n=5))
unstacked = ae_max.unstack().to_frame()
plt.figure(figsize=(12,4)) 
sns.barplot(x=unstacked.index.get_level_values(0), y=unstacked[0])
plt.title('Average of Top 5 Scores for Each Model', fontsize = 14)
plt.xlabel('Step Count', fontsize = 12)
plt.ylabel('Average Score', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Max Plot.png')
plt.show()

# Plot 2

ae_min = pd.DataFrame()    
for i in list(allepisodes.columns):  
    ae_min[i] = np.array(allepisodes[i].nsmallest(n=5))
unstacked = ae_min.unstack().to_frame()
plt.figure(figsize=(12,4)) 
sns.barplot(x=unstacked.index.get_level_values(0), y=unstacked[0])
plt.title('Average of Lowest 5 Scores for Each Model', fontsize = 14)
plt.xlabel('Step Count', fontsize = 12)
plt.ylabel('Average Score', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Min Plot.png')
plt.show()

# Plot 3

unstacked = allepisodes.unstack().to_frame()
plt.figure(figsize=(12,4)) 
sns.barplot(x=unstacked.index.get_level_values(0), y = unstacked[0])
plt.title('Average Score for Each Model', fontsize = 14)
plt.xlabel('Step Count', fontsize = 12)
plt.ylabel('Average Score', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Mean Plot.png')
plt.show()

# Plot 4

plt.figure(figsize=(12,4)) 
sns.barplot(x=list(allepisodes.columns), y=allepisodes.std())
plt.title('Standard Deviation of Score for Each Model', fontsize = 14)
plt.xlabel('Step Count', fontsize = 12)
plt.ylabel('Score Standard Deviation', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/STD Plot.png')
plt.show()

# Plot 5

plt.figure(figsize=(12,4)) 
sns.barplot(x=list(allepisodes.columns), y=allepisodes.max() - allepisodes.min())
plt.title('Range of Score for Each Model', fontsize = 14)
plt.xlabel('Step Count', fontsize = 12)
plt.ylabel('Score Range', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Range Plot.png')
plt.show()

# Plot 6

var = [0]  
cols = list(allepisodes.columns)
cols.insert(0, '0k')
j = 0
for i in list(allepisodes.columns): 
    try:
        var.append(allepisodes[i].median())
    except:
        None
    j = i
fig, ax = plt.subplots(figsize=(13,4)) 
sns.barplot(x=cols, y=var, ax = ax)
sns.lineplot(x=cols, y=var, ax = ax, lw =8)
plt.title('Median Score for Each Model', fontsize = 14)
plt.xlabel('Step Count', fontsize = 12)
plt.ylabel('Median Score', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Median Plot.png')
plt.show()

# Plot 7

var = [0]  
cols = list(allepisodes.columns)
cols.insert(0, '0k')
j = 0
for i in list(allepisodes.columns): 
    try:
        var.append(allepisodes[i].mean() - allepisodes[j].mean())
    except:
        var.append(allepisodes[i].mean())
    j = i
fig, ax = plt.subplots(figsize=(13,4)) 
sns.lineplot(x=cols, y=0, color = 'red', ax =ax)
sns.lineplot(x=cols, y=var, lw = 6, ax =ax)
plt.title('Change in Average Score from Previous Step', fontsize = 14)
plt.xlabel('Step Count', fontsize = 12)
plt.ylabel('Change in Score', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Change Plot.png')
plt.show()

# Plot 8

ae_comb = pd.DataFrame() 
ae_comb['0k-200k'] = np.array(allepisodes['40k']+allepisodes['80k']+
                      allepisodes['120k']+allepisodes['160k']+
                      allepisodes['200k']) 
ae_comb['200k-400k'] = np.array(allepisodes['240k']+allepisodes['280k']+
                      allepisodes['320k']+allepisodes['360k']+
                      allepisodes['400k']) 
ae_comb['400k-600k'] = np.array(allepisodes['440k']+allepisodes['480k']+
                      allepisodes['520k']+allepisodes['560k']+
                      allepisodes['600k']) 
ae_comb['600k-800k'] = np.array(allepisodes['640k']+allepisodes['680k']+
                      allepisodes['720k']+allepisodes['760k']+
                      allepisodes['800k']) 
ae_comb['800k-1000k'] = np.array(allepisodes['840k']+allepisodes['880k']+
                      allepisodes['920k']+allepisodes['960k']+
                      allepisodes['1000k']) 
unstacked = ae_comb.unstack().to_frame()
plt.figure(figsize=(8,4)) 
sns.barplot(x=unstacked.index.get_level_values(0), y = unstacked[0])
plt.title('Average Score in Sum of 200k Steps', fontsize = 13)
plt.xlabel('Average Score', fontsize = 11)
plt.ylabel('Score Range', fontsize = 11)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Combined Plot.png')
plt.show()

# Bonus Plot

data = [80, 20]
colors = ['yellow', 'black']
plt.pie(data, colors = colors, startangle = 30)
circle = plt.Circle((-.1, -.3),0.04 , fc='black',ec="black")
plt.gca().add_patch(circle)
rect1 = plt.Rectangle((.05, .3),0.35, 0.09, angle = 30, fc='black',ec="black")
plt.gca().add_patch(rect1)
rect2 = plt.Rectangle((.64, .28),0.3, 0.08, angle = 30, fc='red',ec="red")
plt.gca().add_patch(rect2)
rect3 = plt.Rectangle((.52, -.46),0.3, 0.08, angle = -43, fc='red',ec="red")
plt.gca().add_patch(rect3)
plt.gca().add_patch(rect2)
rect4 = plt.Rectangle((-.65, .85),0.55, 0.18, angle = -140, fc='red',ec="red")
plt.gca().add_patch(rect4)
rect5 = plt.Rectangle((-.8, .88),0.55, 0.18, angle = -110, fc='red',ec="red")
plt.gca().add_patch(rect5)
plt.title('Ms. PACMAN Pie Chart', fontsize = 12)
plt.savefig(r'C:/Users/trash/Desktop/machine learning class github/ms.pacman.ai/web_app/src/plots/Ms. PACMAN Pie Chart Plot.png')
plt.show()

