#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 10:36:50 2021

@author: nicholexiong
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
from longitudinalDynamics import microbiota_longitudinalData


#%% equilibria against various degree of leakiness in vertical transmission (lambda) 

# make an empty dataframe 
df_lambda = pd.DataFrame()

# make a list of lambda values
lamda = np.arange(0, 0.405, 0.005).tolist()

for lambda_value in lamda:
    # compute corresponding equillibria values i
    df = microbiota_longitudinalData(lamda = lambda_value,gamma=0.15)
    equilibrium_lambda = df.tail(n=1)
    df_lambda = df_lambda.append(equilibrium_lambda, ignore_index=True)

# add beta values as a new column in df_beta for plotting 
df_lambda['lamda'] = lamda






#%% plot the effect of lambda - the rate of losing commensal or mutualist

# Set the size of the figure, single column figure 3 inches
plt.figure(figsize=(3.5,3))

# use a nice color palette
#palette = sns.color_palette("colorblind")
palette = sns.color_palette("Set2")
sns.set_palette(palette)

# a list of colomns for y-axes
#y_s = ['M_y','N_y','M_x','N_x','E_m','E_x']
y_s = ['M_y','M_x','N_y','N_x','E_m','E_x']

# extract threshold value 
threshold = df_lambda.iloc[0]['threshold']

# go through p2 p4 as y-axes to make plot 
for p in y_s:
    # Plot a timeseries plot using the seaborn library
    ax = sns.lineplot(y = p, x = lamda, data = df_lambda, # Select the x and y values and the dataframe
                  linewidth=1.3, # Define the width of the line
                 )

# set a different line style and color for each variable

ax.lines[1].set_linestyle("--")
ax.lines[3].set_linestyle("--")
ax.lines[4].set_linestyle("-.")
ax.lines[5].set_linestyle("-.")

ax.lines[0].set_color("seagreen")
ax.lines[1].set_color("seagreen")
ax.lines[2].set_color("firebrick")
ax.lines[3].set_color("firebrick")
ax.lines[4].set_color("mediumaquamarine")
ax.lines[5].set_color("orchid")



# add vertical line of threshold values
plt.axvline(x=threshold,color='dimgray',linestyle = ':')

# x, y labels
plt.xlabel('The leakiness of vertical transmission ($\lambda$)', fontsize=8) # Add the x axis label    
plt.ylabel('Proportion at equilibria', fontsize=8) # Add the y axis label


# x,y ticks and grid
plt.tick_params(axis='both', labelsize=8) # Change the parameters for the x and y axis
#plt.grid(True) # Display the grid lines
#plt.grid(axis='both',color='black', linestyle='-', lw=0.5, alpha=0.15) # Change the grid parameters

ax.text(0.2,1.05, "$Threshold$", size=8, color= 'black')

# legend properties
lgd = plt.legend(labels=['$M_y$','$M_x$','$N_y$','$N_x$','$E_m$','$E_o$'], loc="right",frameon = 0.5, 
                 framealpha=0.8, # Create a legend and define its location
           edgecolor='white', facecolor='white', ncol=1, # Edgecolor, facecolor and the number of columns
           title='', fontsize=8) # the title and the font size
lgd.get_title().set_fontsize('8') # Change the font size of the title
  
# Display lines for the left and bottom axes    
sns.despine(left=False, bottom=False)


# save the figure
plt.savefig('effect_of_lambda_2hosts.pdf')



