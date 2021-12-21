#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 14:59:55 2020

@author: xiyanxiong
"""

# explore recursive programming 

def get_equilibrium(n = 2000, p2_init = 0.5, 
                    p4_init = 0.5, Em_init = 0.5, Ex_init = 0.5, 
                    S = 0.1, s_e = 0.1, gamma = 0.1, 
                    lamda = 0.1, beta = 0.1, epsilon = 0.00001):
    '''
    Returns the estimated equilibrium of different microbiota types after n generations.
        Arguments:
            Model variables:
                p2(M-), p4(M+), Em, Ex (float):  
            
            n(init): the number of generations
            
            Model parameters: 
                S(float): fitness advantage of microbiota containing mutualist M
                s_e(float): disadvantage of M in the environment 
                gamma(float): rate of shedding of commensal or mutualist to the environment 
                lamda(float): rate of losing the commensal during vertical transmission 
                bata(float): rate of acquiring the mutualist or commensal from the environment 
                epsilon(fload): error between two iterations
                
        Returns:
            eql(list): a list of variable values at equilibrium
    
    '''

    # a function that generate microbiota for n+1 th generation given data of nth generation
    def microb_generator(p2,p4,Em,Ex):
        
        # the mean fitness of p in nth generation 
        mean_f_p = p2 + (1+S)*p4
        # the mean fitness of E in nth generation 
        mean_f_E = Ex + (1 - s_e)*Em + gamma*p4
    
        # number of mutualists in the n+1 th generation
        Em_next = ((1 - s_e)*Em + gamma* p4)/mean_f_E
        # proportion of other bacteria in the environment 
        Ex_next = Ex/mean_f_E
        
        # proportion of microbiota type 2 in the n+1 th generation 
        p2_next = (p2*(1 - beta*Em) + p4* (1+S)*lamda)/mean_f_p
        # proportion of microbiota type 4 in the n+1 th generation
        p4_next = ((1 + S)*(1 - lamda)*p4 + p2* beta* Em)/mean_f_p
        
        
        # return a dictionary of next generation microbiota 
        next_gen = {'Generation': i, 'P2': p2_next,'P4': p4_next, 
                    'Em':Em_next,'Ex':Ex_next}
    
        return next_gen
    
    
    # load pandas dictionary
    import pandas as pd 
  
    # create a list with generation 0 data
    gen_0 = [{'Generation': 0, 'P2': p2_init,
              'P4': p4_init, 'Em':Em_init,'Ex':Ex_init}] 
  
    # Create a DataFrame 
    df = pd.DataFrame(gen_0)
    
    # assign initial values for the first iteration (generation 0)
    p2 = p2_init
    p4 = p4_init
    Em = Em_init
    Ex = Ex_init
    
    for i in range(1, n+1): 
        
        # get data for i+1 generation
        next_gen = microb_generator(p2,p4,Em,Ex)
        #print("generation ", i) 
        
        # turn i+1 generation data into a list and append it to the dataframe 
        df_next = pd.DataFrame([next_gen])   
        df = df.append(df_next, ignore_index=True)
                
        # error is the sum of the difference between two iterations 
        error = (abs(next_gen.get('P2')-p2)+abs(next_gen.get('P4')-p4)+
                 abs(next_gen.get('Em')-Em)+abs(next_gen.get('Ex')-Ex))
        
        # stop the loop if the error is small enough 
        if error < epsilon :
            break
        
        # use the new data as input for the next iteration         
        p2 = next_gen.get('P2')
        p4 = next_gen.get('P4')
        Em = next_gen.get('Em')
        Ex = next_gen.get('Ex')
        

    
    # data of the last generation as equilibrium  
    equilibrium = df.tail(1)
    #find the lower threshold of stability
    threshold_left = (beta*(gamma**2)-S*(s_e**2)+gamma*S*s_e-beta*gamma*s_e)/(gamma*S*s_e+gamma*s_e)
    #find the upper threshold of stability 
    threshold_right = (beta*gamma+S*s_e)/(S*s_e+s_e)
    # appen the threshold to the equilibrium 
    equilibrium['threshold_upper']=threshold_right
    equilibrium['threshold_lower']=threshold_left
    
    return equilibrium


    
    
    