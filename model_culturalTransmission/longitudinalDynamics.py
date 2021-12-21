#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 09:25:53 2021

This is a function that returns the longitudinal dynamics of the model with two hosts
over time.

@author: nicholexiong
"""

# c*lambda+c*lambda*s-c*s
def microbiota_longitudinalData(n = 2000, M_y_init = 0.25, N_y_init = 0.25,
                    M_x_init = 0.25, N_x_init = 0.25, Em_init = 0.5, Ex_init = 0.5, 
                    s = 0.1, c = 0.1, gamma = 0.1, 
                    lamda = 0.1, beta = 0.1, alpha = 0.1, alphaV = 0, k = 0.1, delta = 0.02, 
                    epsilon = 0.00001):
    '''
    Returns a dataframe of the proportions of different microbiota types after n generations.
        Arguments:
            Model variables:
                M_x, N_x, M_y, N_y (float): The proportion of M+ 
                and M- type microbiota in two hosts (X and Y).
                
                Em, Ex(float): The proportion of Mutualist and other bacteria in the environment.
            
            n(init): the number of generations
            
            Model parameters: 
                s(float): fitness advantage of microbiota containing mutualist M
                c(float): disadvantage of M in the environment 
                gamma(float): rate of shedding of commensal or mutualist to the environment 
                lamda(float): rate of losing the commensal during vertical transmission 
                bata(float): rate of acquiring the mutualist or commensal from the environment
                epsilon(float): error between two iterations
                
        Returns:
            df(DataFrame): Microbiota proportions over n generations
    
    '''

    # a function that generate microbiota for n+1 th generation given data of nth generation
    def microb_generator(M_y, N_y, M_x, N_x, Em, Ex):
        
        
        # the mean fitness of p in nth generation 
        mean_f_p = (1+s)*(M_y+M_x)+N_y+N_x
        # the mean fitness of E in nth generation 
        mean_f_E = Ex + (1 - c)*Em + gamma*(M_y+M_x)
        
        # proportion of microbiota M+ in host1 in the n+1 th generation 
        M_y_next = ((1+s)*(1-lamda)*M_y + beta*(1+alpha)*N_y*Em + M_y*(k*M_x-delta))/mean_f_p
        # proportion of microbiota M- in host1 in the n+1 th generation 
        N_y_next = ((1-beta*(1+alpha)*Em)*N_y+lamda*(1+s)*M_y + N_y*(k*N_x-delta))/mean_f_p
        # proportion of microbiota M+ in host2 in the n+1 th generation
        M_x_next = ((1+s)*(1-lamda*(1+alphaV))*M_x+beta*N_x*Em + M_y*(delta-k*M_x))/mean_f_p
        # proportion of microbiota type 4 in the n+1 th generation
        N_x_next = ((1-beta*Em)*N_x+lamda*(1+alphaV)*(1+s)*M_x + N_y*(delta-k*N_x))/mean_f_p
    
        # number of mutualists in the n+1 th generation
        Em_next = ((1 - c)*Em + gamma* (M_y+M_x))/mean_f_E
        # proportion of other bacteria in the environment 
        Ex_next = Ex/mean_f_E
        
        
        
        # return a dictionary of next generation microbiota 
        next_gen = {'Generation': i, 'M_y': M_y_next,'N_y': N_y_next, 
                    'M_x':M_x_next,'N_x':N_x_next, 
                    'E_m':Em_next,'E_x':Ex_next}
    
        return next_gen
    
    
    # load pandas dictionary
    import pandas as pd 
  
    # create a list with generation 0 data
    gen_0 = [{'Generation': 0, 'M_y': M_y_init, 'N_y':N_y_init, 'M_x':M_x_init,
              'N_x': N_x_init, 'E_m':Em_init,'E_x':Ex_init}] 
  
    # Create a DataFrame with 
    df = pd.DataFrame(gen_0)
    
    # assign initial values for the first iteration (generation 0)
    M_y = M_y_init
    N_y = N_y_init
    M_x = M_x_init
    N_x = N_x_init
    Em = Em_init
    Ex = Ex_init
    
    for i in range(1, n+1): 
        
        # get data for i+1 generation
        next_gen = microb_generator(M_y,N_y,M_x,N_x,Em,Ex)
        #print("generation ", i) 
        
        # turn i+1 generation data into a list and append it to the dataframe 
        df_next = pd.DataFrame([next_gen])   
        df = df.append(df_next, ignore_index=True)
        
        # error is the sum of the difference between two iterations 
        error = (abs(next_gen.get('M_y')-M_y)+abs(next_gen.get('N_y')-N_y)+
                 abs(next_gen.get('M_x')-M_x)+abs(next_gen.get('N_x')-N_x)+
                 abs(next_gen.get('E_m')-Em)+abs(next_gen.get('E_x')-Ex))
        
        # stop the loop if the error is small enough 
        if error < epsilon :
            break        
        
        # use the new data as input for the next iteration         
        M_y = next_gen.get('M_y')
        N_y = next_gen.get('N_y')
        M_x = next_gen.get('M_x')
        N_x = next_gen.get('N_x')
        Em = next_gen.get('E_m')
        Ex = next_gen.get('E_x')
    
    #find the upper threshold of stability 
    threshold = (beta*gamma+s*c+alpha*beta*gamma*(1-delta/k))/(s*c+c)
    # appen the threshold to the equilibrium 
    df['threshold']=threshold
    
    return df
    
    
    

    