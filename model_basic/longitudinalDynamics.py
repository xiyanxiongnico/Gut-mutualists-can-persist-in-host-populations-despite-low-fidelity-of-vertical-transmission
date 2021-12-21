#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 13:14:33 2021

@author: xiyanxiong
"""

def microbiota_longitudinalData(n = 150, N_init = 0.5, 
                    M_init = 0.5, Em_init = 0.5, Ex_init = 0.5, 
                    S = 0.1, s_e = 0.1, gamma = 0.1, 
                    lamda = 0.1, beta = 0.1,):
    '''
    Returns a dataframe of the proportions of different microbiota types after n generations.
        Arguments:
            Model variables:
                N(M-), M(M+), Em, Ex (float):  
            
            n(init): the number of generations
            
            Model parameters: 
                S(float): fitness advantage of microbiota containing mutualist M
                s_e(float): disadvantage of M in the environment 
                gamma(float): rate of shedding of commensal or mutualist to the environment 
                lamda(float): rate of losing the commensal during vertical transmission 
                bata(float): rate of acquiring the mutualist or commensal from the environment 
                
        Returns:
            df(DataFrame): Microbiota proportions over n generations
    
    '''

    # a function that generate microbiota for n+1 th generation given data of nth generation
    def microb_generator(N,M,Em,Ex):
        
        # the mean fitness of p in nth generation 
        mean_f_p = N + (1+S)*M
        # the mean fitness of E in nth generation 
        mean_f_E = Ex + (1 - s_e)*Em + gamma*M
    
        # number of mutualists in the n+1 th generation
        Em_next = ((1 - s_e)*Em + gamma* M)/mean_f_E
        # proportion of other bacteria in the environment 
        Ex_next = Ex/mean_f_E
        
        # proportion of microbiota type 2 in the n+1 th generation 
        N_next = (N*(1 - beta*Em) + M* (1+S)*lamda)/mean_f_p
        # proportion of microbiota type 4 in the n+1 th generation
        M_next = ((1 + S)*(1 - lamda)*M + N* beta* Em)/mean_f_p
        
        
        # return a dictionary of next generation microbiota 
        next_gen = {'Generation': i, 'N': N_next,'M': M_next, 
                    'Em':Em_next,'Ex':Ex_next}
    
        return next_gen
    
    
    # load pandas dictionary
    import pandas as pd 
  
    # create a list with generation 0 data
    gen_0 = [{'Generation': 0, 'N': N_init,
              'M': M_init, 'Em':Em_init,'Ex':Ex_init}] 
  
    # Create a DataFrame with 
    df = pd.DataFrame(gen_0)
    
    # assign initial values for the first iteration (generation 0)
    N = N_init
    M = M_init
    Em = Em_init
    Ex = Ex_init
    
    for i in range(1, n+1): 
        
        # get data for i+1 generation
        next_gen = microb_generator(N,M,Em,Ex)
        #print("generation ", i) 
        
        # turn i+1 generation data into a list and append it to the dataframe 
        df_next = pd.DataFrame([next_gen])   
        df = df.append(df_next, ignore_index=True)
        
        # use the new data as input for the next iteration         
        N = next_gen.get('N')
        M = next_gen.get('M')
        Em = next_gen.get('Em')
        Ex = next_gen.get('Ex')
    
    
    return df
    
    
    

    