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
    

    
#%% plot the effect of lambda - the rate of losing commensal or mutualist
# plot threshold against s 

fig, axs = plt.subplots(ncols=3, sharey=False, figsize = (6,2))

plt.subplots_adjust(left=0.07, bottom=0.18, right=0.98, top=0.9, wspace=0.35)

# use a nice color palette
sns.set_palette("Set2")


# a list of colomns for y-axes
y_s = ['P2','P4','Em','Ex']

# extract threshold value 
threshold_upper = df_lambda.iloc[0]['threshold_upper']
threshold_lower = df_lambda.iloc[0]['threshold_lower']

# go through p2 p4 as y-axes to make plot 
for p in y_s:
    # Plot a timeseries plot using the seaborn library
    sns.lineplot(ax=axs[0], y = p, x = lamda, data = df_lambda, # Select the x and y values and the dataframe
                  linewidth=1.5, # Define the width of the line
                 )

# set a different line style for Em and Ex
axs[0].lines[2].set_linestyle("-.")
axs[0].lines[3].set_linestyle("-.")

# add vertical line of threshold values
axs[0].axvline(x=threshold_upper,color='dimgray',linestyle = ':')
axs[0].axvline(x=threshold_lower,color='dimgray',linestyle = ':')

# add labels to plot 
axs[0].text(0.07,1.06, "$T_1$", size=7, color='black')
axs[0].text(0.22,1.06, "$T_2$", size=7, color= 'black')


# x, y labels
axs[0].set_xlabel('The leakiness of vertical transmission ($\lambda$)', fontsize=8) # Add the x axis label    
axs[0].set_ylabel('Proportion at equilibria', fontsize=8) # Add the y axis label


# Display lines for the left and bottom axes    
#sns.despine(left=False, bottom=False)



# a list of colomns for y-axes
y_s = ['T2','T1']


# go through p1 p2 p3 p4 as y-axes to make plot 
for p in y_s:
    # Plot a timeseries plot using the seaborn library
    sns.lineplot(ax=axs[2], y = p, x='s', data = df_threshold_s, # Select the x and y values and the dataframe
                  linewidth=1, # Define the width of the line
                 )
    

for p in y_s:
    # Plot a timeseries plot using the seaborn library
    sns.lineplot(ax=axs[1], y = p, x='Beta', data = df_threshold_beta, # Select the x and y values and the dataframe
                  linewidth=1, # Define the width of the line
                 )

axs[0].lines[0].set_color("firebrick")
axs[0].lines[1].set_color("seagreen")
axs[0].lines[2].set_color('mediumaquamarine')
axs[1].lines[0].set_linestyle(":")
axs[2].lines[0].set_linestyle(":")
axs[1].lines[0].set_color("black")
axs[1].lines[1].set_color("black")
axs[2].lines[0].set_color("black")
axs[2].lines[1].set_color("black")


# x, y labels
axs[1].set_ylabel("Leakiness, "+r'$\lambda$', fontsize=8)
axs[2].set_ylabel("Leakiness, "+r'$\lambda$', fontsize=8)
axs[2].set_xlabel('Selective advantage to host, s', fontsize=8)
axs[1].set_xlabel('Mutualist acquisition, '+r'$\beta$', fontsize=8)

# scale axis 
axs[1].set_xlim([0, 1])
axs[1].set_ylim([0, 1])
axs[2].set_xlim([0, 2])
axs[2].set_ylim([0, 1])


# Change the parameters for the x and y axis
axs[1].tick_params(axis='both', labelsize=6)
axs[2].tick_params(axis='both', labelsize=6)
axs[0].tick_params(axis='both', labelsize=6) 



# add labels to plot 
axs[1].text(0.05,0.3, "Extinction of the mutualist", size=6, color="firebrick",rotation=55)
axs[1].text(0.2,0.2, "Presence of the mutualist", size=6, color= "seagreen",rotation=30)
axs[2].text(0.1,0.7, "Extinction of the mutualist", size=6, color="firebrick")
axs[2].text(0.4,0.3, "Presence of the mutualist", size=6, color="seagreen")

# subplot titles
axs[0].set_title('A',loc='left',fontsize=8)
axs[1].set_title('B',loc='left',fontsize=8)
axs[2].set_title('C',loc='left',fontsize=8)

# legend properties
lgd = axs[0].legend(labels=["M-","M+","Em","Eo"], loc="right",frameon = 0.5, framealpha=0.8, # Create a legend and define its location
           edgecolor='white', facecolor='white', ncol=1, # Edgecolor, facecolor and the number of columns
           title='', fontsize=6) # the title and the font size
lgd.get_title().set_fontsize('8') # Change the font size of the title
  


# legend properties
labels=["Upper threshold T2","Lower threshold T1"]

lgd = axs[2].legend(labels=labels, loc="best",
                 frameon = 0.5, framealpha=0.8, # Create a legend and define its location
                 #borderaxespad=-2,    # Small spacing around legend box
           edgecolor='white', facecolor='white', ncol=1, # Edgecolor, facecolor and the number of columns
           title='', fontsize=6) # the title and the font size
lgd.get_title().set_fontsize('6') # Change the font size of the title



# save the figure
plt.savefig('lambda_threshold.pdf')
    