#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 10:08:08 2020

@author: xiyanxiong
"""

# load pandas dictionary
import pandas as pd 

# load numpy dictionary 
import numpy as np

# plot the data using the seaborn library
import seaborn as sns

# Use the matplotlib library to edit the plot
import matplotlib.pyplot as plt

#  import get_equilibrium from file 
from FunctionSimpleModel_getEquilibria import get_equilibrium


#%% equilibria against various degree of leakiness in vertical transmission (lambda) 

# make an empty dataframe 
df_lambda = pd.DataFrame()

# make a list of lambda values
lamda = np.arange(0, 0.41, 0.005).tolist()

for lambda_value in lamda:
    # compute corresponding equillibria values i
    equilibrium_lambda = get_equilibrium(lamda = lambda_value,gamma = 0.15)
    df_lambda = df_lambda.append(equilibrium_lambda, ignore_index=True)

# add beta values as a new column in df_beta for plotting 
df_lambda['lamda'] = lamda






#%% plot the effect of lambda - the rate of losing commensal or mutualist
# leaky vertical transmission

# Set the size of the figure
plt.figure(figsize=(3.5,3))

# use a nice color palette
#palette = sns.color_palette("colorblind")
palette = sns.color_palette("Set2")
sns.set_palette(palette)

# a list of colomns for y-axes
y_s = ['P2','P4','Em','Ex']

# extract threshold value 
threshold_upper = df_lambda.iloc[0]['threshold_upper']
threshold_lower = df_lambda.iloc[0]['threshold_lower']

# go through p2 p4 as y-axes to make plot 
for p in y_s:
    # Plot a timeseries plot using the seaborn library
    ax = sns.lineplot(y = p, x = lamda, data = df_lambda, # Select the x and y values and the dataframe
                  linewidth=1.5, # Define the width of the line
                 )

# set a different line style for Em and Ex
ax.lines[2].set_linestyle("-.")
ax.lines[3].set_linestyle("-.")

# add vertical line of threshold values
plt.axvline(x=threshold_upper,color='dimgray',linestyle = ':')
plt.axvline(x=threshold_lower,color='dimgray',linestyle = ':')

# add labels to plot 
ax.text(0.07,1.05, "$T_1$", size=8, color='black')
ax.text(0.22,1.05, "$T_2$", size=8, color= 'black')


# x, y labels
plt.xlabel('The leakiness of vertical transmission ($\lambda$)', fontsize=8) # Add the x axis label    
plt.ylabel('Proportion at equilibria', fontsize=8) # Add the y axis label


# x,y ticks and grid
plt.tick_params(axis='both', labelsize=8) # Change the parameters for the x and y axis
#plt.grid(True) # Display the grid lines
#plt.grid(axis='both',color='black', linestyle='-', lw=0.5, alpha=0.15) # Change the grid parameters


# legend properties
lgd = plt.legend(labels=["M-","M+","Em","Ex"], loc="right",frameon = 0.5, framealpha=0.8, # Create a legend and define its location
           edgecolor='white', facecolor='white', ncol=1, # Edgecolor, facecolor and the number of columns
           title='', fontsize=8) # the title and the font size
lgd.get_title().set_fontsize('8') # Change the font size of the title
  
# Display lines for the left and bottom axes    
sns.despine(left=False, bottom=False)


# save the figure
plt.savefig('effect_of_lambda.pdf')



