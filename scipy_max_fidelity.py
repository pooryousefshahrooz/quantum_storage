#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import scipy.optimize as spo
import numpy as np


# In[ ]:



import csv
from network import Network
from workload import Work_load
# from docplex.mp.progress import *
# from docplex.mp.progress import SolutionRecorder
import os
import sys
import pandas as pd
from docplex.mp.progress import *
from docplex.mp.progress import SolutionRecorder
import networkx as nx
import time


# In[ ]:


def CPLEX_feasibility(network,work_load,life_time,iteration,cyclic_workload,storage_capacity):
    if cyclic_workload =="cyclic":
        cyclic_workload=True
    else:
        cyclic_workload= False
    import docplex.mp.model as cpx
    opt_model = cpx.Model(name="Storage problem model"+str(iteration))
    w_vars = {}
    u_vars = {}
    
    w_vars  = {(t,k,p): opt_model.continuous_var(lb=0, ub= network.max_edge_capacity,
                              name="w_{0}_{1}_{2}".format(t,k,p))  for t in work_load.T 
               for k in work_load.each_t_requests[t] 
               for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]}

    u_vars  = {(t,j,p): opt_model.continuous_var(lb=0, ub= network.max_edge_capacity,
                                  name="u_{0}_{1}_{2}".format(t,j,p))  for t in work_load.T 
                   for j in network.storage_pairs for p in network.each_request_real_paths[j]}   

    if life_time ==1000:
        #inventory evolution constraint
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p_s in network.each_request_real_paths[j]:
                    
 
                    if cyclic_workload:
                        opt_model.add_constraint(u_vars[t,j,p_s] == u_vars[(t-1)%len(work_load.T),j,p_s]-
                        opt_model.sum(w_vars[(t-1)%len(work_load.T),k,p]
                        for k in work_load.each_t_requests[t] if k!=j for p in network.each_request_virtual_paths_include_subpath[k][p_s])
                        +opt_model.sum(w_vars[(t-1)%len(work_load.T),j,p_s])
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))
                    else:
                        opt_model.add_constraint(u_vars[t,j,p_s] == u_vars[t-1,j,p_s]-
                        opt_model.sum(w_vars[t-1,k,p] 
                        for k in work_load.each_t_requests[t] if k!=j for p in network.each_request_virtual_paths_include_subpath[k][p_s])
                        +opt_model.sum(w_vars[t-1,j,p_s])
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))
    else:
        #inventory evolution constraint
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p_s in network.each_request_real_paths[j]:
                    
                    if cyclic_workload:
                        opt_model.add_constraint(u_vars[t,j,p_s] == -
                        opt_model.sum(w_vars[(t-1)%len(work_load.T),k,p] 
                        for k in work_load.each_t_requests[t] if k!=j for p in network.each_request_virtual_paths_include_subpath[k][p_s] 
                        )
                        + opt_model.sum(w_vars[(t-1)%len(work_load.T),j,p_s])
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))
                    else:
                        opt_model.add_constraint(u_vars[t,j,p_s] == -
                        opt_model.sum(w_vars[t-1,k,p] 
                        for k in work_load.each_t_requests[t] if k!=j for p in network.each_request_virtual_paths_include_subpath[k][p_s] 
                        )
                        + opt_model.sum(w_vars[t-1,j,p_s])
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))

    # serving from inventory constraint
    for t in work_load.T[1:]:
        for j in network.storage_pairs:
            
            for p_s in network.each_request_real_paths[j]:

                opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]
                for k in work_load.each_t_requests[t] if k!=j for p in network.each_request_virtual_paths_include_subpath[k][p_s] if k in list(network.each_request_virtual_paths_include_subpath.keys()))<=u_vars[t,j,p_s]
                                     , ctname="inventory_serving_{0}_{1}_{2}".format(t,j,p_s))  
 
     
    # Demand constriant
    for t in work_load.T[1:]:
        for k in  work_load.each_t_requests[t]:
            opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]
            for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]) >= 
                    work_load.each_t_each_request_demand[t][k], ctname="constraint_{0}_{1}".format(t,k))
    
    #Edge constraint
    for t in work_load.T:
        for edge in network.set_E:
            opt_model.add_constraint(
                opt_model.sum(w_vars[t,k,p] for k in work_load.each_t_requests[t]
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k] if network.check_path_include_edge(edge,p))
                                     
                 <= network.each_edge_capacity[edge], ctname="edge_capacity_{0}_{1}".format(t,edge))
     
    # storage servers capacity constraint
    for t in work_load.T:
        for s1 in network.storage_nodes:
            opt_model.add_constraint(opt_model.sum(u_vars[t,(s1,s2),p] 
                for s2 in network.storage_nodes if network.check_storage_pair_exist(s1,s2)
                for p in network.each_request_real_paths[(s1,s2)])
        <= storage_capacity, ctname="storage_capacity_constraint_{0}_{1}".format(t,s1))
    
    # constraints for serving from storage at time zero and 1 should be zero
    if not cyclic_workload:
        for t in [0,1]:
            opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]
                    for k in work_load.each_t_requests[t] for p in network.each_request_virtual_paths[k] 
                    )<=0, ctname="serving_from_inventory_{0}".format(t))
    
    # constraints for putting in storage at time zero  should be zero
    """this is becasue we start the formulation from 1 and not from zero and we have t-1 in our formulation"""
    for t in [0]:
        opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]
                for k in work_load.each_t_requests[t] for p in network.each_request_real_paths[k] 
                )<=0, ctname="storing_in_inventory_{0}".format(t))   
    

    # constraint for inventory is zero at time zero 
    if not cyclic_workload:
        for t in [0]:
            for j in network.storage_pairs:
                 for p_s in network.each_request_real_paths[j]:
                        opt_model.add_constraint(u_vars[t,j,p_s] <=0, ctname="storage_capacity_constraint_{0}_{1}_{2}".format(t,j,p_s))
    
    """defining an objective, which is a linear expression"""

    objective = opt_model.sum(1/len(work_load.T[1:])*1/len(work_load.each_t_real_requests[t])*1/work_load.each_t_each_request_demand[t][k]
                              *(w_vars[t,k,p] * network.get_path_length(p)) for t in work_load.T[1:]
                              for k in work_load.each_t_real_requests[t] 
                              for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]
                              )

    
  
    opt_model.minimize(objective)
    
    opt_model.print_information()
    
    opt_model.solve()

    
    #print('docplex.mp.solution',opt_model.solution)
    objective_value = -1
    try:
        if opt_model.solution:
            objective_value =opt_model.solution.get_objective_value()
    except ValueError:
        print(ValueError)
    each_time_each_path_delivered_EPRs = {}
    if objective_value>0:
        for t in work_load.T[1:]:
            for k in work_load.each_t_real_requests[t]: 
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                    try:
                        each_time_each_path_delivered_EPRs[t][k][p]=w_vars[t,k,p].solution_value
                    except:
                        try:
                            each_time_each_path_delivered_EPRs[t][k]= {}
                            each_time_each_path_delivered_EPRs[t][k][p]=w_vars[t,k,p].solution_value
                        except:
                            each_time_each_path_delivered_EPRs[t]={}
                            each_time_each_path_delivered_EPRs[t][k]= {}
                            each_time_each_path_delivered_EPRs[t][k][p]=w_vars[t,k,p].solution_value
    
        
       
    opt_model.clear()
   
    return objective_value,each_time_each_path_delivered_EPRs


# In[ ]:


def maximizing_avg_fidelity(network,work_load,life_time,iteration,storage_capacity,max_allowed_purifiying_EPRs):
    wn_start = []
    bnds = []
    # Constraints
    # edge constraint
    # print("each_t_k_p_w_vars_indx",each_t_k_p_w_vars_indx)
    # print("each_t_k_p_n_vars_indx",each_t_k_p_n_vars_indx)

    for t in work_load.T:
        for k in work_load.each_t_requests[t]:
            for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                wn_start.append(20)
                wn_start.append(10)
                bnds.append((0,network.max_edge_capacity))
                bnds.append((1,max_allowed_purifiying_EPRs))
        for j in network.storage_pairs:
            for p_s in network.each_request_real_paths[j]:
                wn_start.append(network.max_edge_capacity)
                bnds.append((0,storage_capacity))

    indx = 0
    each_t_k_p_n_vars_indx = {}
    each_t_k_p_w_vars_indx = {}
    each_t_k_p_u_vars_indx = {}
    for t in work_load.T:
        for k in work_load.each_t_requests[t]:
            for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                each_t_k_p_w_vars_indx[t,k,p] = indx
                indx+=1
                each_t_k_p_n_vars_indx[t,k,p] = indx
                indx+=1
        for j in network.storage_pairs:
            for p_s in network.each_request_real_paths[j]:
                each_t_k_p_u_vars_indx[t,j,p_s] = indx
                indx+=1
    



    # Constraints
    # edge constraint
    # print("each_t_k_p_w_vars_indx",each_t_k_p_w_vars_indx)
    # print("each_t_k_p_n_vars_indx",each_t_k_p_n_vars_indx)

    def edge_constraint(wn,w_indxes,n_indxes,edge,edge_capacity):
        index_tracker = 0
        edge_load = 0
        #print("for edge %s capacity %s we need to check %s %s"%(edge,edge_capacity,w_indxes,n_indxes ))
        for indx in w_indxes:
            edge_load= edge_load+wn[indx]*wn[n_indxes[index_tracker]]
            index_tracker+=1
    #     if edge_capacity-edge_load>0:
    #         print("for edge %s capacity %s we have load %s constraint %s"%(edge,edge_capacity,edge_load,edge_capacity-edge_load))
        return edge_capacity-edge_load

    def demand_constraint(wn,w_indxes,t,k,demand):
        served_EPRs = 0
        #print("for time %s request %s demand %s"%(t,k,demand))
        for indx in w_indxes:
            served_EPRs= served_EPRs+wn[indx]
    #     print("served_EPRs %s and demand is %s"%(served_EPRs,demand))
        return served_EPRs-demand
    def inventory_constraint(wn,u_t_j_p_s_indx,u_t_1_j_p_s_indx,w_vars_t_1_j_p_s_indx,w_indxes,n_indxes):
        served_from_storage = 0
        index_tracker = 0
        #print('1 w',len(w_indxes),w_indxes)
        #print('1 n',len(n_indxes),n_indxes)
        for indx in w_indxes:
            served_from_storage= served_from_storage+wn[indx]*wn[n_indxes[index_tracker]]
            index_tracker+=1
        stored_at_storage = wn[w_vars_t_1_j_p_s_indx]
        inventory_result =  wn[u_t_1_j_p_s_indx]-served_from_storage+stored_at_storage-wn[u_t_j_p_s_indx] 
        return inventory_result
    def inventory_constraint_one_time_slot(wn,u_t_j_p_s_indx,w_vars_t_1_j_p_s_indx,w_indxes,n_indxes):
        served_from_storage = 0
        index_tracker = 0

        for indx in w_indxes:
            served_from_storage= served_from_storage+wn[indx]*wn[n_indxes[index_tracker]]
            index_tracker+=1
        stored_at_storage = wn[w_vars_t_1_j_p_s_indx]
        inventory_result =  -served_from_storage+stored_at_storage-wn[u_t_j_p_s_indx] 
        return inventory_result
    def serving_from_inventory_constraint(wn,u_t_j_p_s_indx,w_indxes,n_indxes):
        served_from_storage = 0
        index_tracker = 0
        #print('2 w',len(w_indxes),w_indxes)
        #print('2 n',len(n_indxes),n_indxes)
        for indx in w_indxes:
            served_from_storage= served_from_storage+wn[indx]*wn[n_indxes[index_tracker]]
            index_tracker+=1
        inventory_usage =  wn[u_t_j_p_s_indx]-served_from_storage
        return inventory_usage

    def storage_capacity_constraint(wn,w_indxes,storage_capacity):
        served_from_storage = 0
        for indx in w_indxes:
            served_from_storage= served_from_storage+wn[indx]
        return storage_capacity-served_from_storage
    def serving_from_storage_time_zero(wn,w_indxes):
        served_from_storage = 0
        for indx in w_indxes:
            served_from_storage= served_from_storage+wn[indx]
        return served_from_storage-0
    def storage_at_time_zero_constraint(wn,u_index):
        storage_at_time_zero = wn[u_index]
        return storage_at_time_zero-0
    def placing_at_storage_at_time_zero_constraint(wn,w_indxes):
        placed_at_storage = 0
        for indx in w_indxes:
            placed_at_storage= placed_at_storage+wn[indx]
        return placed_at_storage-0
    constraints = []
    # inventory constraints
    if life_time ==1000:
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p_s in network.each_request_real_paths[j]:
                    w_indxes = []
                    n_indxes = []
                    for k in work_load.each_t_requests[t]:
                        if k!=j:
                            for p in network.each_request_virtual_paths_include_subpath[k][p_s]:
                                w_indxes.append(each_t_k_p_w_vars_indx[t-1,k,p])
                                n_indxes.append(each_t_k_p_n_vars_indx[t-1,k,p])
                    u_t_j_p_s_indx = each_t_k_p_u_vars_indx[t,j,p_s]
                    u_t_1_j_p_s_indx = each_t_k_p_u_vars_indx[t-1,j,p_s]
                    w_vars_t_1_j_p_s_indx = each_t_k_p_w_vars_indx[t-1,j,p_s]
                    constraints.append({'type': 'eq', 'fun':inventory_constraint,'args':(u_t_j_p_s_indx,u_t_1_j_p_s_indx,w_vars_t_1_j_p_s_indx,w_indxes,n_indxes,)})
    else:
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p_s in network.each_request_real_paths[j]:
                    w_indxes = []
                    n_indxes = []
                    for k in work_load.each_t_requests[t]:
                        if k!=j:
                            for p in network.each_request_virtual_paths_include_subpath[k][p_s]:
                                w_indxes.append(each_t_k_p_w_vars_indx[t-1,k,p])
                                n_indxes.append(each_t_k_p_n_vars_indx[t-1,k,p])
                    u_t_j_p_s_indx = each_t_k_p_u_vars_indx[t,j,p_s]
                    u_t_1_j_p_s_indx = each_t_k_p_u_vars_indx[t-1,j,p_s]
                    w_vars_t_1_j_p_s_indx = each_t_k_p_w_vars_indx[t-1,j,p_s]
                    constraints.append({'type': 'eq', 'fun':inventory_constraint_one_time_slot,'args':(u_t_j_p_s_indx,w_vars_t_1_j_p_s_indx,w_indxes,n_indxes,)})
    # serving from inventory constraint
    for t in work_load.T[1:]:
        for j in network.storage_pairs:
            for p_s in network.each_request_real_paths[j]:
                w_indxes=[]
                n_indxes=[]
                for k in work_load.each_t_requests[t]:
                    if k!=j:
                        for p in network.each_request_virtual_paths_include_subpath[k][p_s]:
                            if k in list(network.each_request_virtual_paths_include_subpath.keys()):
                                w_indxes.append(each_t_k_p_w_vars_indx[t,k,p])
                                n_indxes.append(each_t_k_p_n_vars_indx[t,k,p])
                #print("3 w",len(w_indxes),w_indxes)
                #print("3 n",len(n_indxes),n_indxes)
                constraints.append({'type': 'eq', 'fun':serving_from_inventory_constraint,'args':(u_t_j_p_s_indx,w_indxes,n_indxes,)})
    # edge constraint
    for t in work_load.T:
        for edge in network.set_E:
            w_indxes = []
            n_indxes = [] 
            for k in work_load.each_t_requests[t]:
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                    if network.check_path_include_edge(edge,p):
                        w_indxes.append(each_t_k_p_w_vars_indx[t,k,p])
                        n_indxes.append(each_t_k_p_n_vars_indx[t,k,p])
            constraints.append({'type': 'ineq', 'fun': edge_constraint, 'args': (w_indxes,n_indxes,edge,network.each_edge_capacity[edge],)})
    # Demand constriant
    for t in work_load.T[1:]:
        for k in  work_load.each_t_requests[t]:
            w_indxes = []
            for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                w_indxes.append(each_t_k_p_w_vars_indx[t,k,p])
            constraints.append({'type': 'ineq', 'fun':demand_constraint,'args':(w_indxes,t,k,work_load.each_t_each_request_demand[t][k],)})

    # storage servers capacity constraint
    for t in work_load.T:
        for s1 in network.storage_nodes:
            w_indxes = []
            for s2 in network.storage_nodes:
                if network.check_storage_pair_exist(s1,s2):
                    for p in network.each_request_real_paths[(s1,s2)]:
                        w_indxes.append(each_t_k_p_u_vars_indx[t,(s1,s2),p])
            constraints.append({'type': 'ineq', 'fun':storage_capacity_constraint,'args':(w_indxes,storage_capacity,)})


    # constraints for serving from storage at time zero and 1? should be zero
    for t in [0]:
        w_indxes = []
        for k in work_load.each_t_requests[t]:
            for p in network.each_request_virtual_paths[k]:
                w_indxes.append(each_t_k_p_w_vars_indx[t,k,p])
        constraints.append({'type': 'eq', 'fun':serving_from_storage_time_zero,'args':(w_indxes,)})


    # constraints for putting in storage at time zero should be zero
    """this is becasue we start the formulation from 1 and not from zero and we have t-1 in our formulation"""
    for t in [0]:
        w_indxes = []
        for k in work_load.each_t_requests[t]:
            for p in network.each_request_real_paths[k]:
                w_indxes.append(each_t_k_p_w_vars_indx[t,k,p])
        constraints.append({'type': 'eq', 'fun':placing_at_storage_at_time_zero_constraint,'args':(w_indxes,)})



    # constraint for inventory is zero at time zero 
    for t in [0]:
        for j in network.storage_pairs:
             for p_s in network.each_request_real_paths[j]:
                    u_index=each_t_k_p_u_vars_indx[t,j,p_s]
                    constraints.append({'type': 'eq', 'fun':storage_at_time_zero_constraint,'args':(u_index,)})

    def get_path_purified_fidelity(n,F_p):
        f = round(F_p,4)
        n = int(n)
        #print("purifiying %s with %s EPR pairs"%(f,n))
        if (int(n),f) in network.each_n_f_purification_result:
            #print("we used from memeory!")
            return network.each_n_f_purification_result[(int(n),f)]
        else:
            fidelity = network.recursive_purification(n,f)
            network.each_n_f_purification_result[(int(n),f)] =  round(fidelity,4)
            return fidelity
    def objective_function_test(wn):
#         for t in work_load.T[1:]:
#             for k in work_load.each_t_real_requests[t]:
#                 for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
#                     print("for t %s k %s p %s we have w=%s n=%s demand %s"%(t,k,p,wn[each_t_k_p_w_vars_indx[t,k,p]],wn[each_t_k_p_n_vars_indx[t,k,p]],work_load.each_t_each_request_demand[t][k]))
#         for t in work_load.T[1:]:
#             for j in network.storage_pairs:
#                 for p_s in network.each_request_real_paths[j]:
#                     print("for t %s j %s p_s %s we have u=%s "%(t,j,p_s,wn[each_t_k_p_u_vars_indx[t,j,p_s]]))

    #     print("bnds",bnds)
    #     for t in T[1:]:
    #         for k in each_t_real_requests[t]:
    #             for p in each_request_real_paths[k]+each_request_virtual_paths[k]:
    #                 print("for t %s k %s p %s we have start w=%s n=%s     "%(t,k,p,  wn[each_t_k_p_w_vars_indx[t,k,p]],  wn[each_t_k_p_n_vars_indx[t,k,p]]))
    #                 print("for t %s k %s p %s we have bound w=%s n=%s"%(t,k,p,bnds[each_t_k_p_w_vars_indx[t,k,p]],bnds[each_t_k_p_n_vars_indx[t,k,p]]))

    #         for j in storage_pairs:
    #             for p_s in each_request_real_paths[j]:
    #                 print("for t %s j %s p_s %s we have bound u=%s "%(t,j,p_s,bnds[each_t_k_p_u_vars_indx[t,j,p_s]]))

    #     time.sleep(4)
        w_vars = {}
        n_vars= {}
        indx = 0
        for t in work_load.T:
            for k in work_load.each_t_requests[t]:
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                    w_vars[t,k,p] = wn[each_t_k_p_w_vars_indx[t,k,p]]
                    indx+=1
                    n_vars[t,k,p] = wn[each_t_k_p_n_vars_indx[t,k,p]]
                    indx+=1
        #print("each_t_k_p_w_vars_indx",each_t_k_p_w_vars_indx)
        #print("w_vars",w_vars)
        each_t_fidelities = []
        for t in work_load.T[1:]:
            for k in work_load.each_t_real_requests[t]:
                served_EPRs = 0
                this_k_purified_fidelities = []
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                    purified_fidelity = get_path_purified_fidelity(n_vars[t,k,p],network.each_path_basic_fidelity[p])
                    #print("purified_fidelity ",purified_fidelity)
                    weighted_purified_fidelity = w_vars[t,k,p]*purified_fidelity
                    #print("weighted_purified_fidelity ",weighted_purified_fidelity)
                    this_k_purified_fidelities.append(weighted_purified_fidelity)
                    served_EPRs = served_EPRs+w_vars[t,k,p]
            #each_t_fidelities.append(sum(this_k_purified_fidelities)/each_t_each_request_demand[t][k])
            each_t_fidelities.append(sum(this_k_purified_fidelities)/served_EPRs)
        final_avg_fidelity = sum(each_t_fidelities)/len(each_t_fidelities)
    #     *(w_vars[t,k,p] * recursive_purification(n_vars[t,k,p],each_p_fidelity[p])) 
    #     for t in T[1:] for k in each_t_real_requests[t] for p in each_request_real_paths[k]+each_request_virtual_paths[k]
        return -final_avg_fidelity
    objective_value = -1
    fail_flag = False
    solver_flag = False
    try:
        result = spo.minimize(objective_function_test,wn_start,method="Nelder-Mead",options = {"disp":True,"tol":0.01},constraints = constraints, bounds = bnds)
        #print result
        if result.success:
            print("success!")
            solver_flag = True
            print("final fidelity is ",result.fun)
            objective_value = -(result.fun)
            wn = result.x
            w0 = wn[0]
            n0 = wn[1]
            w1 = wn[2]
            n1 = wn[3]
        #     print(f"w0={w0} n0={n0} w1={w1} n1={n1}")
            #print("wn is %s "%wn)
            for t in work_load.T[1:]:
                for k in work_load.each_t_real_requests[t]:
                    
                    for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                        print("for t %s k %s p %s we have w=%s n=%s demand %s"%(t,k,p,wn[each_t_k_p_w_vars_indx[t,k,p]],wn[each_t_k_p_n_vars_indx[t,k,p]],work_load.each_t_each_request_demand[t][k]))
            for t in work_load.T[1:]:
                for j in network.storage_pairs:
                    for p_s in network.each_request_real_paths[j]:
                        print("for t %s j %s p_s %s we have u=%s "%(t,j,p_s,wn[each_t_k_p_u_vars_indx[t,j,p_s]]))
        
        else:
            print("Sorry, could not find a minimum.") 
            solver_flag = False
            fail_flag = True
            objective_value = -(result.fun)
    except ValueError:
        print(ValueError)
#         objective_value = -1

    each_inventory_per_time_usage = {}
    each_time_each_path_delivered_EPRs = {}
    each_time_each_path_purification_EPRs = {}
    if objective_value>0 and not fail_flag:
        for t in work_load.T[1:]:
            for k in work_load.each_t_real_requests[t]: 
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                    try:
                        each_time_each_path_delivered_EPRs[t][k]+=wn[each_t_k_p_w_vars_indx[t,k,p]]
                    except:
                        try:
                            each_time_each_path_delivered_EPRs[t][k]= wn[each_t_k_p_w_vars_indx[t,k,p]]
                        except:
                            each_time_each_path_delivered_EPRs[t]={}
                            each_time_each_path_delivered_EPRs[t][k]= wn[each_t_k_p_w_vars_indx[t,k,p]]
        
                    try:
                        each_time_each_path_purification_EPRs[t][k]+=wn[each_t_k_p_n_vars_indx[t,k,p]]
                    except:
                        try:
                            each_time_each_path_purification_EPRs[t][k]= wn[each_t_k_p_n_vars_indx[t,k,p]]
                        except:
                            each_time_each_path_purification_EPRs[t]={}
                            each_time_each_path_purification_EPRs[t][k]= wn[each_t_k_p_n_vars_indx[t,k,p]]
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p in network.each_request_real_paths[j]:
                    try:
                        each_inventory_per_time_usage[j][t]=wn[each_t_k_p_u_vars_indx[t,j,p]]
                    except:
                        try:
                            each_inventory_per_time_usage[j][t]=wn[each_t_k_p_u_vars_indx[t,j,p]]
                        except:
                            each_inventory_per_time_usage[j] = {}
                            each_inventory_per_time_usage[j][t]=wn[each_t_k_p_u_vars_indx[t,j,p]]    
        
   
   
    return objective_value,each_inventory_per_time_usage,each_time_each_path_delivered_EPRs,each_time_each_path_purification_EPRs,solver_flag


# In[ ]:





# In[ ]:





# In[ ]:


def maximizing_fidelity(each_network_topology_file,results_file_path,inventory_utilization_results_file_path,delived_purification_EPRs_file_path,number_of_user_pairs,number_of_time_slots, spike_means,num_spikes,experiment_repeat,storage_node_selection_schemes,fidelity_threshold_ranges,cyclic_workload,storage_capacities,given_life_time_set,distance_between_users,setting_demands,max_allowed_purifiying_EPRs):
    print("each_network_topology_file %s \n ,results_file_path %s , inventory_utilization_results_file_path %s ,number_of_user_pairs %s ,number_of_time_slots %s , spike_means %s ,num_spikes %s ,experiment_repeat %s ,storage_node_selection_schemes %s ,fidelity_threshold_ranges %s ,cyclic_workload %s ,storage_capacities %s ,given_life_time_set %s ,distance_between_users %s"%(each_network_topology_file,results_file_path,inventory_utilization_results_file_path,number_of_user_pairs,number_of_time_slots, spike_means,num_spikes,experiment_repeat,storage_node_selection_schemes,fidelity_threshold_ranges,cyclic_workload,storage_capacities,given_life_time_set,distance_between_users))
    
    for network_topology,file_path in each_network_topology_file.items():
        for spike_mean in spike_means:
            import pdb
            each_storage_each_path_number_value = {}
            network = Network(file_path,True)
            
            for i in range(experiment_repeat):
                network.reset_storage_pairs()
                network.get_user_pairs(number_of_user_pairs,distance_between_users,number_of_time_slots)
                work_load = Work_load(number_of_time_slots,"time_demands_file.csv")
                """we set the demands for each user pair"""
                if setting_demands=="python_library":
                    work_load.set_each_user_pair_demands(number_of_time_slots,network.each_t_user_pairs,spike_mean,num_spikes)
                else:
                    work_load.set_each_user_pair_demands_randomly(number_of_time_slots,network.each_t_user_pairs,spike_mean,num_spikes)
                """we set at least one demand for each time to avoid divided by zero error"""
                work_load.check_demands_per_each_time(network.each_t_user_pairs)                                      
                for storage_capacity in storage_capacities:
                    for fidelity_threshold_range in fidelity_threshold_ranges:
                        network.set_user_pair_fidelity_threshold(fidelity_threshold_range)
                        for storage_node_selection_scheme in storage_node_selection_schemes:

                            objective_values = []
                            selected_storage_nodes = []
                            selected_storage_pairs = []

                            #nx.draw(network.g,with_labels=True)
                            # plt.show()
                            for num_paths in [3]:
                                
                                for life_time in given_life_time_set:
                                    current_available_fidelities=[]
                                    permited_work_load = False
                                    for number_of_storages in [0,2,3,4,5,6]:
                                        if number_of_storages ==0 or (number_of_storages>0 and permited_work_load):
                                            network.each_request_real_paths = {}
                                            network.reset_pair_paths()
                                            """with new storage pairs, we will check the solution for each number of paths(real and virtual)"""
                                            work_load.reset_variables()
                                            pairs = []
                                            for t,user_pairs in network.each_t_user_pairs.items():            
                                                for user_pair in user_pairs:
                                                    if user_pair not in pairs:
                                                        pairs.append(user_pair)
                                            network.get_each_user_pair_real_paths(pairs)

                                            path_counter_id = 0
                                            """select and add new storage pairs"""
                                            network.get_new_storage_pairs(number_of_storages,storage_node_selection_scheme)

                                            work_load.set_each_time_requests(network.each_t_user_pairs,network.storage_pairs)
                                            work_load.set_each_time_real_requests(network.each_t_user_pairs)

                                            network.get_each_user_pair_real_paths(network.storage_pairs)
                                            if number_of_storages==1:
                                                number_of_storages = 2

                                            """first we add the real paths between storage pairs"""
                                            for storage_pair in network.storage_pairs:
                                                paths = network.get_real_path(storage_pair,num_paths)
                                                for path in paths:
                                                    network.set_each_path_length(path_counter_id,path)
                                                    network.set_of_paths[path_counter_id] = path
                                                    network.each_path_path_id[tuple(path)] = path_counter_id
                                                    try:
                                                        network.each_request_real_paths[storage_pair].append(path_counter_id)
                                                    except:
                                                        network.each_request_real_paths[storage_pair]=[path_counter_id]
                                                    try:
                                                        network.each_storage_real_paths[storage_pair].append(path)
                                                    except:
                                                        network.each_storage_real_paths[storage_pair]=[path]
                                                    path_counter_id+=1

                                            across_all_time_slots_pairs = []
                                            for t,user_pairs in network.each_t_user_pairs.items():
                                                for user_pair in user_pairs:
                                                    if user_pair not in across_all_time_slots_pairs:
                                                        across_all_time_slots_pairs.append(user_pair)
                                            all_sub_paths = []
                                            for user_pair in across_all_time_slots_pairs:
                                                paths = network.get_real_path(user_pair,num_paths)
                                                for path in paths:
                                                    network.set_of_paths[path_counter_id] = path
                                                    network.set_each_path_length(path_counter_id,path)
                                                    network.each_path_path_id[tuple(path)] = path_counter_id
                                                    try:
                                                        network.each_request_real_paths[user_pair].append(path_counter_id)
                                                    except:
                                                        network.each_request_real_paths[user_pair]=[path_counter_id]
                                                    path_counter_id+=1

                                                for storage_pair in network.storage_pairs:
                                                    """add one new path to the previous paths"""

                                                    for real_sub_path in network.each_storage_real_paths[storage_pair]:

                                                        paths = network.get_paths_to_connect_users_to_storage(user_pair,real_sub_path,num_paths)

                                                        this_sub_path_id = network.each_path_path_id[tuple(real_sub_path)]

                                                        for path in paths:
                                                            path = network.remove_storage_pair_real_path_from_path(real_sub_path,path)
                                                            network.set_each_path_length(path_counter_id,path)
                                                            """we remove the sub path that is connecting two storage pairs 
                                                            from the path because we do not want to check the edge capacity for the edges of this subpath"""
                                                            try:
                                                                network.each_request_virtual_paths_include_subpath[user_pair][this_sub_path_id].append(path_counter_id)
                                                            except:
                                                                try:
                                                                    network.each_request_virtual_paths_include_subpath[user_pair][this_sub_path_id]=[path_counter_id]
                                                                except:
                                                                    network.each_request_virtual_paths_include_subpath[user_pair]={}
                                                                    network.each_request_virtual_paths_include_subpath[user_pair][this_sub_path_id]=[path_counter_id]

                                                            if this_sub_path_id not in all_sub_paths:
                                                                all_sub_paths.append(this_sub_path_id)

                                                            network.set_of_paths[path_counter_id] = path
                                                            try:
                                                                network.each_request_virtual_paths[user_pair].append(path_counter_id)
                                                            except:
                                                                network.each_request_virtual_paths[user_pair]=[path_counter_id]

                                                            path_counter_id+=1


                                                        for pair in network.storage_pairs:
                                                            network.each_request_virtual_paths[pair]=[]

                                            if number_of_storages==0:
                                                for t,pairs in network.each_t_user_pairs.items():
                                                    for pair in pairs:
                                                        network.each_request_virtual_paths[pair]=[]
                                                        for j in network.storage_pairs:
                                                            for sub_path_id in all_sub_paths:
                                                                network.each_request_virtual_paths_include_subpath[pair][sub_path_id]={}
                                            for j in network.storage_pairs:
                                                for sub_path_id in all_sub_paths:
                                                    try:
                                                        network.each_request_virtual_paths_include_subpath[j][sub_path_id] = []
                                                    except:
                                                        network.each_request_virtual_paths_include_subpath[j]={}
                                                        network.each_request_virtual_paths_include_subpath[j][sub_path_id] = []
                                            for t in range(number_of_time_slots):
                                                for k in work_load.each_t_requests[t]:
                                                    for sub_path_id in all_sub_paths:
                                                        try:
                                                            if k in list(network.each_request_virtual_paths_include_subpath.keys()):
                                                                if sub_path_id not in list(network.each_request_virtual_paths_include_subpath[k].keys()):

                                                                    try:
                                                                        network.each_request_virtual_paths_include_subpath[k][sub_path_id] = []
                                                                    except:
                                                                        network.each_request_virtual_paths_include_subpath[k]={}
                                                                        network.each_request_virtual_paths_include_subpath[k][sub_path_id] = []
                                                                else:
                                                                    action= "do nothing!"
                                                            else:
                                                                for sub_path_id in all_sub_paths:
                                                                    try:
                                                                        network.each_request_virtual_paths_include_subpath[k][sub_path_id] = []
                                                                    except:
                                                                        network.each_request_virtual_paths_include_subpath[k]={}
                                                                        network.each_request_virtual_paths_include_subpath[k][sub_path_id] = []
                                                        except:
                                                            for sub_path_id in all_sub_paths:
                                                                try:
                                                                    network.each_request_virtual_paths_include_subpath[k][sub_path_id] = []
                                                                except:
                                                                    network.each_request_virtual_paths_include_subpath[k]={}
                                                                    network.each_request_virtual_paths_include_subpath[k][sub_path_id] = []


                                            for t in work_load.T:
                                                if number_of_storages!=0:
                                                    for j in network.storage_pairs:
                                                        for p_s in network.each_request_real_paths[j]:
        #                                                     print("for time %s and storage pair %s and real sub path %s"%(t,j,p_s))
                                                            for k in work_load.each_t_requests[t]:
        #                                                         print("this is the request ",k)
                                                                if k!=j:
        #                                                             print("which was not equal to storage pair",t,j,p_s,k)
        #                                                             print("virtual including subpath",network.each_request_virtual_paths_include_subpath[k])
        #                                                             print("network.each_request_virtual_paths[k]",network.each_request_virtual_paths[k])
                                                                    for p in network.each_request_virtual_paths_include_subpath[k][p_s]:
                                                                        if p not in network.each_request_virtual_paths[k]:
                                                                            import pdb
                                                                            print("ERROR storages %s time %s request %s has a path %s for subpaths but it is not in his virtual paths %s"%(number_of_storages,t,k,p,p_s))
                                                                            #print(network.each_request_real_paths[k])
                                                                            print("virtual paths including subpath list ",network.each_request_virtual_paths_include_subpath[k][p_s])
                                                                            print("virtual paths",network.each_request_virtual_paths[k])
                                                                            pdb.set_trace()

                                            import pdb


                                            """we set the capacity of each storage node"""

                                            network.set_storage_capacity()

                                            """we add new storage pairs as our user pairs and set the demand for them zero"""

                                            work_load.set_storage_pairs_as_user_pairs(network.storage_pairs)


                                            """we set the fidelity threshold of each new storage pair as a user request"""
                                            network.set_each_path_basic_fidelity()
                                            work_load.set_threshold_fidelity_for_request_pairs(network.each_t_user_pairs,network.storage_pairs,network.each_user_request_fidelity_threshold)

                                            """we set the required EPR pairs to achieve each request threshold fidelity"""
                                            network.set_required_EPR_pairs_for_path_fidelity_threshold()


                                            """solve the optimization"""
        #                                     

                                            try:
                                                objective_value=-100
                                                try:
                                                    #objective_value,each_inventory_per_time_usage,each_time_each_path_delivered_EPRs,each_time_each_path_purification_EPRs = CPLEX_resource_cinsumption_minimization(network,work_load,life_time,i,cyclic_workload,storage_capacity)
                                                    if number_of_storages==0:
                                                        feasibility_objective_value,each_t_each_p_each_w = CPLEX_feasibility(network,work_load,life_time,i,cyclic_workload,storage_capacity)
                                                        print("feasibility: for topology %s iteration %s from %s spike mean %s capacity %s  fidelity range %s  life time %s storage %s and path number %s objective_value %s"%
                                                        (network_topology,i,experiment_repeat, spike_mean,storage_capacity,fidelity_threshold_range,life_time, number_of_storages,num_paths, feasibility_objective_value))  
                                                        if feasibility_objective_value>0:
                                                            if number_of_storages==0:
                                                                permited_work_load = True
                                                    if permited_work_load:
                                                        objective_value,each_inventory_per_time_usage,each_time_each_path_delivered_EPRs,each_time_each_path_purification_EPRs,solver_flag=maximizing_avg_fidelity(network,work_load,life_time,i,storage_capacity,max_allowed_purifiying_EPRs)
                                                        
                                                        if not solver_flag:
                                                            if number_of_storages==0:
                                                                each_t_fidelities = []
                                                                for t,k_paths_ws in each_t_each_p_each_w.items():
                                                                    for k,paths_ws in k_paths_ws.items():
                                                                        served_EPRs = 0
                                                                        this_k_purified_fidelities = []
                                                                        for p,w in paths_ws.items():
                                                                            purified_fidelity = network.each_path_basic_fidelity[p]
                                                                            #print("purified_fidelity ",purified_fidelity)
                                                                            weighted_purified_fidelity = w*purified_fidelity
                                                                            #print("weighted_purified_fidelity ",weighted_purified_fidelity)
                                                                            this_k_purified_fidelities.append(weighted_purified_fidelity)
                                                                            served_EPRs = served_EPRs+w
                                                                    #each_t_fidelities.append(sum(this_k_purified_fidelities)/each_t_each_request_demand[t][k])
                                                                    each_t_fidelities.append(sum(this_k_purified_fidelities)/served_EPRs)
                                                                objective_value = sum(each_t_fidelities)/len(each_t_fidelities)
                                                                current_available_fidelities.append(objective_value)
                                                        else:
                                                            current_available_fidelities.append(objective_value)
                                                        objective_value = max(current_available_fidelities)
                                                    else:
                                                        if number_of_storages==0:
                                                            permited_work_load = False
                                                        objective_value = -100

                                                except ValueError:
                                                    print(ValueError)
                                                    #pass

                                                
                                                print("fidelity: for topology %s iteration %s from %s spike mean %s capacity %s  fidelity range %s  life time %s storage %s and path number %s objective_value %s"%
                                                    (network_topology,i,experiment_repeat, spike_mean,storage_capacity,fidelity_threshold_range,life_time, number_of_storages,num_paths, objective_value))  
                                                if permited_work_load:
                                                    with open(results_file_path, 'a') as newFile:                                
                                                        newFileWriter = csv.writer(newFile)
                                                        newFileWriter.writerow([network_topology,number_of_storages,num_paths,
                                                                                life_time,
                                                                                objective_value,spike_mean,num_spikes,i,
                                                                                storage_node_selection_scheme,
                                                                                fidelity_threshold_range,cyclic_workload,
                                                                                distance_between_users,storage_capacity]) 
                                                    if objective_value>0 and number_of_storages>0:
                                                        for storage_pair,t_saved_EPRs in each_inventory_per_time_usage.items():
                                                            for t ,EPRs in t_saved_EPRs.items():
                                                                this_slot_demands = work_load.get_each_t_whole_demands(t,network.each_t_user_pairs[t])
                                                                with open(inventory_utilization_results_file_path, 'a') as newFile:                                
                                                                    newFileWriter = csv.writer(newFile)
                                                                    newFileWriter.writerow([network_topology,number_of_storages,
                                                                    num_paths,i,life_time,storage_pair,t,EPRs,spike_mean,
                                                                    num_spikes,storage_node_selection_scheme,this_slot_demands,
                                                                    fidelity_threshold_range,
                                                                    cyclic_workload,distance_between_users,storage_capacity])
                                                        for t,k_delived_EPRs in  each_time_each_path_delivered_EPRs.items():
                                                            this_slot_demands = work_load.get_each_t_whole_demands(t,network.each_t_user_pairs[t])
                                                            for k,delived_EPRs in k_delived_EPRs.items():
                                                                purification_EPRs = each_time_each_path_purification_EPRs[t][k]
                                                                with open(delived_purification_EPRs_file_path, 'a') as newFile:                                
                                                                    newFileWriter = csv.writer(newFile)
                                                                    newFileWriter.writerow([network_topology,number_of_storages,
                                                                    num_paths,i,t,life_time,spike_mean,
                                                                    num_spikes,storage_node_selection_scheme,this_slot_demands,
                                                                    fidelity_threshold_range,
                                                                    cyclic_workload,distance_between_users,storage_capacity,
                                                                    k,delived_EPRs,purification_EPRs])

                                            except ValueError:
                                                #pass
                                                print(ValueError)


# In[ ]:





# In[ ]:


experiment_repeat =30 #indicates the number of times that we repeat the experiment
spike_means = [400] # list of mean value for spike model traffic generation
num_spikes = 3 # shows the number of nodes that have spike in their demand. Should be less than the number of user pairs
topology_set = sys.argv[1] # can be either real, random1, or random2

setting_demands = sys.argv[2] # indicates the way we generate the demands. python_library for using tgem library. ransom for generating a random demand
max_allowed_purifiying_EPRs = int(sys.argv[3])
if setting_demands not in ["random","python_library"]:
    print("please run the script by python IBM_cplex_feasibiloty.py real/random1/random2 random/python_library")
else:
    storage_node_selection_schemes=["Degree","Random"]
    storage_node_selection_schemes=["Degree"]
    cyclic_workload = "sequential"
    storage_capacities = [400,500,200,600,100]
    storage_capacities = [200]
    fidelity_threshold_ranges = [0.65,0.7,0.75,0.8,0.85,0.9,0.95,0.98,1.0]
    fidelity_threshold_ranges = [0.8]
    distance_between_users = 2

    given_life_time_set = [1000,2]# 1000 indicates infinite time slot life time and 2 indicates one time slot life
    number_of_user_pairs =6
    number_of_time_slots = 5
    results_file_path = 'results/results_maximizing_fidelity.csv'
    inventory_utilization_results_file_path = 'results/inventory_maximizing_fidelity_utilization.csv'
    delived_purification_EPRs_file_path = 'results/delived_purification_EPRs_file_path_maximizing_fidelity.csv'
    each_network_topology_file = {}
    if topology_set =="real":
        each_network_topology_file = {"SURFnet":'data/Surfnet',"ATT":'data/ATT_topology_file',"IBM":'data/IBM',"Abilene":'data/abilene'}

    elif topology_set =="random1":
        for i in [2,4,6]:
            each_network_topology_file["random_erdos_renyi2_"+str(i)]= "data/random_erdos_renyi2_"+str(i)+".txt"
            each_network_topology_file["random_barabasi_albert2_"+str(i)]= "data/random_barabasi_albert2_"+str(i)+".txt"
    # each_network_topology_file = {"Testing_topology":'data/test_topology'}
    elif topology_set =="random2":
        for i in range(1,4):
            each_network_topology_file["random_erdos_renyi_"+str(i)]= "data/random_erdos_renyi_"+str(i)+".txt"
            each_network_topology_file["random_barabasi_albert_"+str(i)]= "data/random_barabasi_albert_"+str(i)+".txt"
    elif topology_set =="big":
        for i in range(2):
            each_network_topology_file["random_erdos_renyi_"+str(i)]= "data/size_"+str(400)+"_random_erdos_reni_0_0_1_"+str(i)+".txt"
    elif topology_set =="linear":
        for topology_size in [30,20]:
            each_network_topology_file["linear_chain_"+str(topology_size)]= "data/linear_topology_"+str(topology_size)+".txt"
        
    # import networkx as nx
    # all_diameters = []
    # for topology,file in each_network_topology_file.items():
    #     print("for topology",topology)

    #     g = nx.Graph()
    #     f = open(file, 'r')
    #     header = f.readline()
    #     for line in f:
    #         line = line.strip()
    #         link = line.split('\t')
    #         i, s, d, c = link
    #         g.add_edge(int(s),int(d),weight=1)
    #     f.close()  
    #     all_diameters.append(nx.diameter(g))

    maximizing_fidelity(each_network_topology_file,results_file_path,inventory_utilization_results_file_path,delived_purification_EPRs_file_path,number_of_user_pairs,number_of_time_slots,spike_means,num_spikes,experiment_repeat,storage_node_selection_schemes,fidelity_threshold_ranges,cyclic_workload,storage_capacities,given_life_time_set,distance_between_users,setting_demands,max_allowed_purifiying_EPRs)


# In[2]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




