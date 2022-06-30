#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 13:21:51 2021
This script plot the longitudinal dynamics of microbiota type over n generations 
@author: xiyanxiong
"""

     
# plot the data using the seaborn library
import seaborn as sns

# Use the matplotlib library to edit the plot
import matplotlib.pyplot as plt

# import data
from longitudinalDynamics import microbiota_longitudinalData

# get dataframe for the plots by running the imported function
df1 = microbiota_longitudinalData(lamda = 0.1)
df2 = microbiota_longitudinalData(lamda = 0.3)

# make subplots and set the size 
fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize = (8,4))

# plot title
n = len(df1)-1
mytitle='Microbiota over '+ str(n) +' generations'

# add title and location of the title 
fig.suptitle(mytitle, fontsize=13, x=0.5, y=0.95)


# use a nice color palette
sns.set_palette("Set2")

# a list of colomns for y-axes
y_s = ['N','M','Em','Ex']


# go through p1 p2 p3 p4 as y-axes to make subplot1 
for p in y_s:
    # Plot a timeseries plot using the seaborn library
    p1 = sns.lineplot(y = p, x='Generation', data = df1, # Select the x and y values and the dataframe
                  linewidth=2, # Define the width of the line
                  ax=ax[0]
                 )

# add horizontal line to check equilibria values
# plt.axhline(y=0.55,color='dimgray',linestyle = ':')
# plt.axhline(y=0.45,color='dimgray',linestyle = ':')


# go through p1 p2 p3 p4 as y-axes to make subplot2
for p in y_s:
    # Plot a timeseries plot using the seaborn library
    p2 = sns.lineplot(y = p, x='Generation', data = df2, # Select the x and y values and the dataframe
                  linewidth=2, # Define the width of the line
                  ax=ax[1]
                 )
    


# set a different line style for Em and Ex
p1.lines[2].set_linestyle("-.")
p1.lines[3].set_linestyle("-.")
p2.lines[2].set_linestyle("-.")
p2.lines[3].set_linestyle("-.")

p1.lines[0].set_color("firebrick")
p1.lines[1].set_color("seagreen")
p1.lines[2].set_color('mediumaquamarine')
p2.lines[0].set_color("firebrick")
p2.lines[1].set_color("seagreen")
p2.lines[2].set_color('mediumaquamarine')

# x, y labels
p1.set_ylabel('Proportion', fontsize=13)
p1.set_xlabel('Generation', fontsize=13)
p2.set_xlabel('Generation', fontsize=13)

# scale axis 
p1.set_xlim([0, n])
p1.set_ylim([0, 1])

# Change the parameters for the x and y axis
p1.tick_params(axis='both', labelsize=13)
p2.tick_params(axis='both', labelsize=13)

# add grid lines 
p1.grid(axis='both',color='black', linestyle='-', lw=0.5, alpha=0.2)
p2.grid(axis='both',color='black', linestyle='-', lw=0.5, alpha=0.2)


# legend properties
# Create the legend
lgd = fig.legend(labels=['$N$','$M$','$E_m$','$E_o$'],   # The labels for each line
           loc="right",   # Position of legend
           frameon = 0.5, framealpha=0.8,
           borderaxespad=-0.5,    # Small spacing around legend box
           title="Type", # Title for the legend,
           edgecolor='white', facecolor='white', ncol=1,
           fontsize=12
           )
lgd.get_title().set_fontsize('12') # Change the font size of the title

# Display lines for the left and bottom axes (instead of a box around the plot)
sns.despine(left=False, bottom=False)



# save the figure
plt.savefig('microbiota_evolution.pdf')
    
 