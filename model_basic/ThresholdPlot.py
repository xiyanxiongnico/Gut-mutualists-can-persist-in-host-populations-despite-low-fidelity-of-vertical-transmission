#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:55:08 2021

@author: nicholexiong
"""


import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

#%% generate the s data frame 

# generate the lambda threshold values as a function: lamda = f(beta)
s_list = np.arange(0,2.01,0.01)
c = 0.1
beta = 0.1
gamma = 0.15


# make an empty data frame
df_threshold_s = pd.DataFrame()


# generate a list of threshold and beta values for each iteration
for s in s_list:
    T2 = (beta*gamma)/(c*(s+1))+s/(s+1)
    T1 = T2*(1-c/gamma)
    out = [{'T1': T1, 'T2': T2, 's': s}] 
    df_threshold_s = df_threshold_s.append(out,ignore_index=True)


#%% generate the beta data frame 

# generate the lambda threshold values as a function: lamda = f(beta)
beta_list = np.arange(0,1.01,0.01)
s = 0.1
c = 0.1
gamma = 0.15

# make an empty data frame
df_threshold_beta = pd.DataFrame()

# generate a list of threshold and beta values for each iteration
for beta in beta_list:
    T2 = (beta*gamma)/(c*(s+1))+s/(s+1)
    T1 = T2*(1-c/gamma)
    out = [{'T1': T1, 'T2': T2, 'Beta': beta}] 
    df_threshold_beta = df_threshold_beta.append(out,ignore_index=True)
    

    
#%% plot threshold against s 

# make subplots and set the size 
fig, ax = plt.subplots(1, 2, sharey=True, figsize = (7,3))


# use a nice color palette
sns.set_palette("Set2")

# a list of colomns for y-axes
y_s = ['T2','T1']


# go through p1 p2 p3 p4 as y-axes to make plot 
for p in y_s:
    # Plot a timeseries plot using the seaborn library
    p2 = sns.lineplot(y = p, x='s', data = df_threshold_s, # Select the x and y values and the dataframe
                  linewidth=2, # Define the width of the line
                  ax=ax[1]
                 )
    

for p in y_s:
    # Plot a timeseries plot using the seaborn library
    p1 = sns.lineplot(y = p, x='Beta', data = df_threshold_beta, # Select the x and y values and the dataframe
                  linewidth=2, # Define the width of the line
                  ax=ax[0]
                 )

p1.lines[0].set_linestyle("-.")
p2.lines[0].set_linestyle("-.")


# x, y labels
p1.set_ylabel("Leakiness, "+r'$\lambda$', fontsize=9)
p2.set_xlabel('Selective advantage to host, s', fontsize=9)
p1.set_xlabel('Mutualist acquisition, '+r'$\beta$', fontsize=9)

# scale axis 
p1.set_xlim([0, 1])
p1.set_ylim([0, 1])
p2.set_xlim([0, 2])
p2.set_ylim([0, 1])


# Change the parameters for the x and y axis
p1.tick_params(axis='both', labelsize=8)
p2.tick_params(axis='both', labelsize=8)

# add grid lines 
p1.grid(axis='both',color='black', linestyle='-', lw=0.5, alpha=0.2)
p2.grid(axis='both',color='black', linestyle='-', lw=0.5, alpha=0.2)



# legend properties
labels=["Upper threshold T2","Lower threshold T1"]

lgd = plt.legend(labels=labels, loc="top",
                 frameon = 0.5, framealpha=0.8, # Create a legend and define its location
                 #borderaxespad=-2,    # Small spacing around legend box
           edgecolor='white', facecolor='white', ncol=1, # Edgecolor, facecolor and the number of columns
           title='', fontsize=8) # the title and the font size
lgd.get_title().set_fontsize('8') # Change the font size of the title



# add labels to plot 
p1.text(0,0.9, "Extinction of the mutualist", size=8, color="firebrick")
p1.text(0.4,0.5, "Presence of the mutualist", size=8, color= "seagreen")
p2.text(0.1,0.7, "Extinction of the mutualist", size=8, color="firebrick")
p2.text(0.4,0.3, "Presence of the mutualist", size=8, color= "seagreen")

# subplot titles
p1.set_title('A',loc='left')
p2.set_title('B',loc='left')



# save the figure
plt.savefig('threshold.pdf')
    