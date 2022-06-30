#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 16:11:17 2022

@author: nicholexiong
"""
# library
import seaborn as sns
import matplotlib.pyplot as plt  
import pandas as pd
import numpy as np


c = 0.1 
gamma = 0.1
beta = 0.1
alpha = 0.1
delta = 0.02
#k = 0.1

k_list = np.arange(0.02, 1.05, 0.05).round(2).tolist()

# make a list of s values
s_list = np.arange(0, 2.05, 0.05).round(2).tolist()

# make column names 
col_names = []

for s in s_list:
    name = 's='+str(s)
    col_names.append(name)

# make an empty dataframe 
df_heatmap = pd.DataFrame(columns = col_names)



for k in k_list:
    
    # make a list of threshold with different s value 
    thres_s = []
    
    for s in s_list :
        threshold = np.around((beta*gamma+s*c+alpha*beta*gamma*(1-delta/k))/(s*c+c),
                             decimals=3)
        thres_s.append(threshold)
        print(thres_s)
        #print(s)
        print(k)
    # append list of thresholds to dataframe 
    df_heatmap.loc[len(df_heatmap)] = thres_s


# make row names 
row_names = []

for k in k_list:
    name = 'k='+str(k)
    row_names.append(name)


# Change the row indexes
df_heatmap.index = row_names


# Default heatmap
heapmap = sns.heatmap(df_heatmap)

#%%

#c = 0.1 
#gamma = 0.1
#beta = 0.1
alpha = 0.1
delta = 0.02
# horiz = beta*gamma/c
horiz = 0.6

# proportion of cultural practice: cult = 1-delta/k
# k>delta, 0<delta/k <1

# make a list of k values
cult_list = np.arange(0, 1.05, 0.05).round(2).tolist()

# make a list of s values
s_list = np.arange(0, 1.05, 0.05).round(2).tolist()
s_list_flip = np.flip(s_list)

# make column names 
col_names = ['s','cultural practice','Threshold']



# make an empty dataframe 
df_heatmap = pd.DataFrame(columns = col_names)



for s in s_list_flip:
    
    for cult in cult_list :
        threshold = np.around((horiz*(1+alpha)*cult+s)/(s+1),
                             decimals=3)
        row = [s,cult,threshold]
        print(row)
        df_heatmap.loc[len(df_heatmap)] = row


df_heatmap = df_heatmap.pivot('s','cultural practice','Threshold')
df_heatmap = df_heatmap.iloc[::-1]


#%%
horiz = 0.1
# make an empty dataframe 
df_heatmap2 = pd.DataFrame(columns = col_names)



for s in s_list:
    
    for cult in cult_list :
        threshold = np.around((horiz*(1+alpha)*cult+s)/(s+1),
                             decimals=3)
        row = [s,cult,threshold]
        print(row)
        df_heatmap2.loc[len(df_heatmap2)] = row


df_heatmap2 = df_heatmap2.pivot('s','cultural practice','Threshold')
df_heatmap2 = df_heatmap2.iloc[::-1]


#%%
horiz = 1.1
# make an empty dataframe 
df_heatmap3 = pd.DataFrame(columns = col_names)



for s in s_list:
    
    for cult in cult_list :
        threshold = np.around((horiz*(1+alpha)*cult+s)/(s+1),
                             decimals=3)
        row = [s,cult,threshold]
        print(row)
        df_heatmap3.loc[len(df_heatmap3)] = row


df_heatmap3 = df_heatmap3.pivot('s','cultural practice','Threshold')
df_heatmap3 = df_heatmap3.iloc[::-1]


#%%
from matplotlib.collections import LineCollection
from scipy import ndimage

#,gridspec_kw=dict(width_ratios=[4,5])
fig, axs = plt.subplots(ncols=3, sharey=True,gridspec_kw=dict(width_ratios=[5,5,6]),
                        figsize = (6,2))

plt.subplots_adjust(left=0.08, bottom=0.19, right=0.95, top=0.9, wspace=0.1)

# pass min and max value to color bar 
vmin = min(df_heatmap.values.min(), df_heatmap2.values.min(),df_heatmap3.values.min())
#vmax = max(df_heatmap.values.max(), df_heatmap2.values.max(),df_heatmap3.values.max())

smooth_scale = 1

z_0 = ndimage.zoom(df_heatmap2.to_numpy(), smooth_scale)
cntr = axs[0].contour(np.linspace(0, len(df_heatmap2.columns), len(df_heatmap2.columns) * smooth_scale),
                  np.linspace(0, len(df_heatmap2.index), len(df_heatmap2.index) * smooth_scale),
                  z_0, levels=[0.2, 0.4, 0.8, 1], colors=['g'])

# Default heatmap
sns.heatmap(df_heatmap2,cbar=False, ax=axs[0],vmin=vmin,vmax=1,xticklabels=4,yticklabels=4)
axs[0].set_title(r'$\beta\gamma/c=0.1$',fontsize=8)
axs[0].set_xlabel('Cultural practice frequency', fontsize=8)
axs[0].set_ylabel('Fitness advantage, s', fontsize=8)
axs[0].text(1, 15, '0.2',color='w',size=8)
axs[0].text(1, 6, '0.4',color='w',size=8)


z_1 = ndimage.zoom(df_heatmap.to_numpy(), smooth_scale)

cntr = axs[1].contour(np.linspace(0, len(df_heatmap.columns), len(df_heatmap.columns) * smooth_scale),
                  np.linspace(0, len(df_heatmap.index), len(df_heatmap.index) * smooth_scale),
                  z_1, levels=[0.2, 0.4, 0.8, 1], colors=['g'])
sns.heatmap(df_heatmap, cbar=False, ax=axs[1],vmin=vmin,vmax=1,xticklabels=4,yticklabels=4)
axs[1].set_title(r'$\beta\gamma/c=0.6$',fontsize=8) 
axs[1].set_xlabel('Cultural practice frequency', fontsize=8)
axs[1].set(ylabel= '')
axs[1].text(1, 16, '0.2',color='w',size=8)
axs[1].text(9, 16, '0.4',color='w',size=8)
axs[1].text(17, 3, '0.8',color='g',size=8)


z_2 = ndimage.zoom(df_heatmap3.to_numpy(), smooth_scale)

cntr = axs[2].contour(np.linspace(0, len(df_heatmap3.columns), len(df_heatmap3.columns) * smooth_scale),
                  np.linspace(0, len(df_heatmap3.index), len(df_heatmap3.index) * smooth_scale),
                  z_2, levels=[0.2, 0.4, 0.8, 1], colors=['g'])

sns.heatmap(df_heatmap3, cbar=True, ax=axs[2],vmin=vmin,vmax=1,xticklabels=4,yticklabels=4)
axs[2].set_title(r'$\beta\gamma/c=1.1$',fontsize=8)
axs[2].set_xlabel('Cultural practice frequency', fontsize=8)
axs[2].set(ylabel= '')
axs[2].text(1, 16, '0.2',color='w',size=8)
axs[2].text(5, 16, '0.4',color='w',size=8)
axs[2].text(14, 16, '0.8',color='g',size=8)
axs[2].text(18, 16, '1',color='g',size=8)
  
# Change the parameters for the x and y axis
axs[0].tick_params(axis='both', labelsize=8) 
axs[1].tick_params(axis='x', labelsize=8)
axs[2].tick_params(axis='x', labelsize=8)


#plt.show()
plt.savefig('heatmap.pdf')

