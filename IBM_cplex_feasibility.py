#!/usr/bin/env python
# coding: utf-8

# In[ ]:





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


def CPLEX_resource_cinsumption_minimization(network,work_load,life_time,iteration,cyclic_workload,storage_capacity,delat_value):
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
                        opt_model.sum(w_vars[(t-1)%len(work_load.T),k,p] *
                        network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                        for k in work_load.each_t_requests[t] if k!=j 
                        for p in network.each_request_virtual_paths_include_subpath[k][p_s])*delat_value
                        +opt_model.sum(w_vars[(t-1)%len(work_load.T),j,p_s])*delat_value
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))
                    else:
                        opt_model.add_constraint(u_vars[t,j,p_s] == u_vars[t-1,j,p_s]-
                        opt_model.sum(w_vars[t-1,k,p] *
                        network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                        for k in work_load.each_t_requests[t] if k!=j 
                        for p in network.each_request_virtual_paths_include_subpath[k][p_s])*delat_value
                        +opt_model.sum(w_vars[t-1,j,p_s])*delat_value
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))
    else:
        #inventory evolution constraint
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p_s in network.each_request_real_paths[j]:
                    
                    if cyclic_workload:
                        opt_model.add_constraint(u_vars[t,j,p_s] == -
                        opt_model.sum(w_vars[(t-1)%len(work_load.T),k,p] *
                        network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                        for k in work_load.each_t_requests[t] if k!=j 
                        for p in network.each_request_virtual_paths_include_subpath[k][p_s] 
                        )*delat_value
                        + opt_model.sum(w_vars[(t-1)%len(work_load.T),j,p_s])*delat_value
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))
                    else:
                        opt_model.add_constraint(u_vars[t,j,p_s] == -
                        opt_model.sum(w_vars[t-1,k,p] *
                        network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                        for k in work_load.each_t_requests[t] if k!=j 
                        for p in network.each_request_virtual_paths_include_subpath[k][p_s] 
                        )*delat_value
                        + opt_model.sum(w_vars[t-1,j,p_s])*delat_value
                                             , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))

    # serving from inventory constraint
    for t in work_load.T[1:]:
        for j in network.storage_pairs:
            
            for p_s in network.each_request_real_paths[j]:

                opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]*
                network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                for k in work_load.each_t_requests[t] if k!=j 
                for p in network.each_request_virtual_paths_include_subpath[k][p_s] 
                if k in list(network.each_request_virtual_paths_include_subpath.keys()))*delat_value<=u_vars[t,j,p_s]
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
                opt_model.sum(w_vars[t,k,p]*network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t)) for k in work_load.each_t_requests[t]
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k] if network.check_path_include_edge(edge,p))
                                     
                 <= network.each_edge_capacity[edge], ctname="edge_capacity_{0}_{1}".format(t,edge))
     
    # storage servers capacity constraint
#     storage_capacity = storage_capacity/delat_value
    for t in work_load.T:
        #for s1 in network.storage_nodes:
        for j in network.storage_pairs:
            opt_model.add_constraint(opt_model.sum(u_vars[t,j,p]
                for p in network.each_request_real_paths[j]) <= storage_capacity 
        , ctname="storage_capacity_constraint_{0}_{1}".format(t,j))
            
#     for t in work_load.T:
#         for s1 in network.storage_nodes:
#             opt_model.add_constraint(opt_model.sum(u_vars[t,(s1,s2),p] 
#                 for s2 in network.storage_nodes if network.check_storage_pair_exist(s1,s2)
#                 for p in network.each_request_real_paths[(s1,s2)])
#         <= storage_capacity, ctname="storage_capacity_constraint_{0}_{1}".format(t,s1))
    
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

    
    print('docplex.mp.solution',opt_model.solution)
    objective_value = -1
    try:
        if opt_model.solution:
            objective_value =opt_model.solution.get_objective_value()
    except ValueError:
        print(ValueError)

    each_inventory_per_time_usage = {}
    each_time_each_path_delivered_EPRs = {}
    each_time_each_path_purification_EPRs = {}
    if objective_value>0:
        
#         for t in work_load.T[1:]:
#             for k in work_load.each_t_real_requests[t]:
#                 for p in network.each_request_virtual_paths[k]:
#                     if network.get_path_length(p)==1:
                        #print("this is the path length for path %s "%(network.get_path_length(p)))
                        #print("k is ",k)
                        #print(network.storage_pairs)
        
        time.sleep(5)
        for t in work_load.T[1:]:
            for k in work_load.each_t_real_requests[t]: 
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
                    try:
                        each_time_each_path_delivered_EPRs[t][k]+=w_vars[t,k,p].solution_value
                    except:
                        try:
                            each_time_each_path_delivered_EPRs[t][k]= w_vars[t,k,p].solution_value
                        except:
                            each_time_each_path_delivered_EPRs[t]={}
                            each_time_each_path_delivered_EPRs[t][k]= w_vars[t,k,p].solution_value
        
                    try:
                        each_time_each_path_purification_EPRs[t][k]+=network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                    except:
                        try:
                            each_time_each_path_purification_EPRs[t][k]= network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                        except:
                            each_time_each_path_purification_EPRs[t]={}
                            each_time_each_path_purification_EPRs[t][k]= network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))        
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p in network.each_request_real_paths[j]:
                    try:
                        each_inventory_per_time_usage[j][t]=u_vars[t,j,p].solution_value
                    except:
                        try:
                            each_inventory_per_time_usage[j][t]=u_vars[t,j,p].solution_value
                        except:
                            each_inventory_per_time_usage[j] = {}
                            each_inventory_per_time_usage[j][t]=u_vars[t,j,p].solution_value        
        
    opt_model.clear()
   
    return objective_value,each_inventory_per_time_usage,each_time_each_path_delivered_EPRs,each_time_each_path_purification_EPRs


# In[ ]:





# In[ ]:


def feasibility(each_network_topology_file,results_file_path,inventory_utilization_results_file_path,delived_purification_EPRs_file_path,number_of_user_pairs,number_of_time_slots, spike_means,num_spikes,experiment_repeat,storage_node_selection_schemes,fidelity_threshold_ranges,cyclic_workload,storage_capacities,given_life_time_set,distance_between_users,setting_demands,edge_fidelity_ranges):
    print("each_network_topology_file %s \n ,results_file_path %s , inventory_utilization_results_file_path %s ,number_of_user_pairs %s ,number_of_time_slots %s , spike_means %s ,num_spikes %s ,experiment_repeat %s ,storage_node_selection_schemes %s ,fidelity_threshold_ranges %s ,cyclic_workload %s ,storage_capacities %s ,given_life_time_set %s ,distance_between_users %s"%(each_network_topology_file,results_file_path,inventory_utilization_results_file_path,number_of_user_pairs,number_of_time_slots, spike_means,num_spikes,experiment_repeat,storage_node_selection_schemes,fidelity_threshold_ranges,cyclic_workload,storage_capacities,given_life_time_set,distance_between_users))
    for edge_fidelity_range in edge_fidelity_ranges:
        for network_topology,file_path in each_network_topology_file.items():
            for spike_mean in each_topology_mean_value_spike[network_topology]:
                import pdb
                each_storage_each_path_number_value = {}
                network = Network(file_path,False,edge_fidelity_range,max_edge_capacity_value,fidelity_threshold_ranges)

                for i in range(experiment_repeat):
                    
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
                                for num_paths in [1]:
                                    network.reset_storage_pairs()
                                    for number_of_storages in [0,2,4,6,8,10]:
                                        #if number_of_storages ==0:
                                        #num_paths = 10-number_of_storages+1
                                        try:
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
                                            available_flag = network.get_new_storage_pairs(number_of_storages,storage_node_selection_scheme)
                                            #if available_flag:
                                            work_load.set_each_time_requests(network.each_t_user_pairs,network.storage_pairs)
                                            work_load.set_each_time_real_requests(network.each_t_user_pairs)

                                            network.get_each_user_pair_real_paths(network.storage_pairs)
                                            if number_of_storages==1:
                                                number_of_storages = 2

                                            """first we add the real paths between storage pairs"""
                                            for storage_pair in network.storage_pairs:
                                                paths = network.get_real_path(storage_pair,1,path_selection_scheme)
                                                for path in paths:
                                                    if network.get_this_path_fidelity(path)>=0.6:
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
                                                paths = network.get_real_path(user_pair,num_paths,path_selection_scheme)
                                                this_user_has_at_least_one_virtual_path_flag = False
                                                for path in paths:
                                                    if network.get_this_path_fidelity(path)>=0.6:
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
                                                        this_sub_path_flag = False
                                                        paths = network.get_paths_to_connect_users_to_storage(user_pair,real_sub_path,num_paths,path_selection_scheme)

                                                        this_sub_path_id = network.each_path_path_id[tuple(real_sub_path)]
                                                        if this_sub_path_id not in all_sub_paths:
                                                            all_sub_paths.append(this_sub_path_id)
                                                        for path in paths:
                                                            if network.get_this_path_fidelity(path)>=0.6:
                                                                this_sub_path_flag = True
                                                                this_user_has_at_least_one_virtual_path_flag = True
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

                                                                

                                                                network.set_of_paths[path_counter_id] = path
                                                                try:
                                                                    network.each_request_virtual_paths[user_pair].append(path_counter_id)
                                                                except:
                                                                    network.each_request_virtual_paths[user_pair]=[path_counter_id]

                                                                path_counter_id+=1


                                                        for pair in network.storage_pairs:
                                                            network.each_request_virtual_paths[pair]=[]
                                                        if not this_sub_path_flag:
                                                            try:
                                                                network.each_request_virtual_paths_include_subpath[user_pair][this_sub_path_id]=[]
                                                            except:
                                                                network.each_request_virtual_paths_include_subpath[user_pair]={}
                                                                network.each_request_virtual_paths_include_subpath[user_pair][this_sub_path_id]=[]

                                                if not this_user_has_at_least_one_virtual_path_flag:
                                                    network.each_request_virtual_paths[user_pair]=[]

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


#                                             for t in work_load.T:
#                                                 if number_of_storages!=0:
#                                                     for j in network.storage_pairs:
#                                                         for p_s in network.each_request_real_paths[j]:
#         #                                                     print("for time %s and storage pair %s and real sub path %s"%(t,j,p_s))
#                                                             for k in work_load.each_t_requests[t]:
#         #                                                         print("this is the request ",k)
#                                                                 if k!=j:
#         #                                                             print("which was not equal to storage pair",t,j,p_s,k)
#         #                                                             print("virtual including subpath",network.each_request_virtual_paths_include_subpath[k])
#         #                                                             print("network.each_request_virtual_paths[k]",network.each_request_virtual_paths[k])
#                                                                     for p in network.each_request_virtual_paths_include_subpath[k][p_s]:
#                                                                         if p not in network.each_request_virtual_paths[k]:
#                                                                             import pdb
#                                                                             print("ERROR storages %s time %s request %s has a path %s for subpaths but it is not in his virtual paths %s"%(number_of_storages,t,k,p,p_s))
#                                                                             #print(network.each_request_real_paths[k])
#                                                                             print("virtual paths including subpath list ",network.each_request_virtual_paths_include_subpath[k][p_s])
#                                                                             print("virtual paths",network.each_request_virtual_paths[k])
#                                                                             pdb.set_trace()

                                            import pdb


                                            """we set the capacity of each storage node"""

                                            network.set_storage_capacity()

                                            """we add new storage pairs as our user pairs and set the demand for them zero"""

                                            work_load.set_storage_pairs_as_user_pairs(network.storage_pairs)


                                            """we set the fidelity threshold of each new storage pair as a user request"""
                                            network.set_each_path_basic_fidelity()
                                            work_load.set_threshold_fidelity_for_request_pairs(network.each_t_user_pairs,network.storage_pairs,network.each_user_request_fidelity_threshold)

                                            """we set the required EPR pairs to achieve each request threshold fidelity"""
                                            #network.set_required_EPR_pairs_for_path_fidelity_threshold()
                                            flag_of_having_at_least_one_path = network.check_each_request_real_virtual_paths(work_load.T,work_load.each_t_requests)
                                            network.set_required_EPR_pairs_for_each_path_each_fidelity_threshold()
                                            if not flag_of_having_at_least_one_path:
                                                for k in work_load.each_t_requests[t]:
                                                    if k not in network.each_request_real_paths:
                                                        print("we have not set real paths for this request")
                                                        paths = network.get_real_path(k,num_paths,path_selection_scheme)
                                                        print("but these are paths ",paths)
                                                        pdb.set_trace()
                                                    if number_of_storages>0:
                                                        if  k not in network.each_request_virtual_paths:
                                                            print("we have not set virtual paths for this request",k,number_of_storages,network.storage_pairs)
                                                            available_flag = network.get_new_storage_pairs(number_of_storages,storage_node_selection_scheme)
                                                            print("available_flag",available_flag)
                                                            for storage_pair in network.storage_pairs:
                                                                print("for storage pair ",storage_pair)
                                                                for real_sub_path in network.each_storage_real_paths[storage_pair]:
                                                                    paths = network.get_paths_to_connect_users_to_storage(user_pair,real_sub_path,num_paths,path_selection_scheme)
                                                                    print("we have these %s for this storage pair %s"%(paths,storage_pair))
                                                            pdb.set_trace()
                                            """solve the optimization"""
                                            for delat_value in delat_values:
                                                for life_time in given_life_time_set:
                                                    try:
                                                        objective_value=-1

                                                        if flag_of_having_at_least_one_path:
                                                            try:
                                                                objective_value,each_inventory_per_time_usage,each_time_each_path_delivered_EPRs,each_time_each_path_purification_EPRs = CPLEX_resource_cinsumption_minimization(network,work_load,life_time,i,cyclic_workload,storage_capacity,delat_value)
                                                            except ValueError:
                                                                print(ValueError)
                                                        else:
                                                            print("oops we do not have even one path for one k at a time!!")
                                                            objective_value = -1
                                                        objective_values.append(objective_value)


                                                        print("for topology %s iteration %s from %s spike mean %s capacity %s  fidelity range %s  life time %s storage %s and path number %s objective_value %s"%
                                                        (network_topology,i,experiment_repeat, spike_mean,storage_capacity,fidelity_threshold_range,life_time, number_of_storages,num_paths, objective_value))  


                                                        with open(results_file_path, 'a') as newFile:                                
                                                            newFileWriter = csv.writer(newFile)
                                                            newFileWriter.writerow([network_topology,number_of_storages,num_paths,
                                                                                    life_time,
                                                                                    objective_value,spike_mean,num_spikes,i,
                                                                                    storage_node_selection_scheme,
                                                                                    fidelity_threshold_range,cyclic_workload,
                                                                                    distance_between_users,storage_capacity,edge_fidelity_range,delat_value]) 
                                                        for storage_pair,t_saved_EPRs in each_inventory_per_time_usage.items():
                                                            for t ,EPRs in t_saved_EPRs.items():
                                                                this_slot_demands = work_load.get_each_t_whole_demands(t,network.each_t_user_pairs[t])
                                                                with open(inventory_utilization_results_file_path, 'a') as newFile:                                
                                                                    newFileWriter = csv.writer(newFile)
                                                                    newFileWriter.writerow([network_topology,number_of_storages,
                                                                    num_paths,i,life_time,storage_pair,t,EPRs,spike_mean,
                                                                    num_spikes,storage_node_selection_scheme,this_slot_demands,
                                                                    fidelity_threshold_range,
                                                                    cyclic_workload,distance_between_users,storage_capacity,edge_fidelity_range,delat_value])
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
                                                                    k,delived_EPRs,purification_EPRs,edge_fidelity_range,delat_value])

                                                    except ValueError:
                                                        #pass
                                                        print(ValueError)
                                        except ValueError:
                                            print(ValueError)
                                            pass


# In[ ]:





# In[ ]:


# setup with 400 max edge capacity and storage capacity 200 and 60 s time interval
# works with mean in file results.. all_three_networks.csv

experiment_repeat =70 #indicates the number of times that we repeat the experiment

num_spikes = 3 # shows the number of nodes that have spike in their demand. Should be less than the number of user pairs
topology_set = sys.argv[1] # can be either real, random1, or random2
delat_values = [20]# each time interval is 1 minute or 60 seconds
setting_demands = sys.argv[2] # indicates the way we generate the demands. python_library for using tgem library. ransom for generating a random demand
number_of_user_pairs =int(sys.argv[3])
spike_means = [1] # list of mean value for spike model traffic generation
edge_fidelity_ranges = [(0.96,0.99)]
max_edge_capacity_value = 1400
path_selection_scheme = "shortest"
each_topology_mean_value_spike = {}
if setting_demands not in ["random","python_library"]:
    print("please run the script by python IBM_cplex_feasibiloty.py real/random1/random2 random/python_library")
else:
    storage_node_selection_schemes=["Degree","Random"]
    storage_node_selection_schemes=["Random","Degree"]
    cyclic_workload = "sequential"
    storage_capacities = [800,1200,1500,2000]
    storage_capacities = [50,100,200,300,400,600,800,1000,1500,2000,4000,6000]
    storage_capacities = [12000]
    fidelity_threshold_ranges = [0.75,0.8,0.85,0.9,0.92,0.94,0.96,0.98]
    fidelity_threshold_ranges = [0.8]
    distance_between_users = 2

    given_life_time_set = [1000,2]# 1000 indicates infinite time slot life time and 2 indicates one time slot life
    
    number_of_time_slots = 10
    results_file_path = 'results/results_feasibility_final_20_sec_interval_new_formulation_final.csv'
    inventory_utilization_results_file_path = 'results/inventory_feasibility_utilization_final_20_sec_interval_new_formulation.csv'
    delived_purification_EPRs_file_path = 'results/delived_purification_EPRs_file_path_final_20_sec_interval_new_formulation.csv'
    each_network_topology_file = {}
    if topology_set =="real":
        each_network_topology_file = {"SURFnet":'data/Surfnet',"Abilene":'data/abilene',"IBM":'data/IBM',"ATT":'data/ATT_topology_file'}
        each_network_topology_file = {"SURFnet":'data/Surfnet',"IBM":'data/IBM',"ATT":'data/ATT_topology_file',"Abilene":'data/abilene'}
        each_topology_mean_value_spike={"ATT":[350],"IBM":[350],"SURFnet":[350],"Abilene":[350]
                               }
    elif topology_set =="random1":
        for i in [2,4,6]:
            each_network_topology_file["random_erdos_renyi2_"+str(i)]= "data/random_erdos_renyi2_"+str(i)+".txt"
            each_topology_mean_value_spike["random_erdos_renyi2_"+str(i)] = [200]
            each_network_topology_file["random_barabasi_albert2_"+str(i)]= "data/random_barabasi_albert2_"+str(i)+".txt"
            each_topology_mean_value_spike["random_barabasi_albert2_"+str(i)] = [200]
    # each_network_topology_file = {"Testing_topology":'data/test_topology'}
        
    elif topology_set =="random2":
        for i in range(1,4):
            each_network_topology_file["random_erdos_renyi_"+str(i)]= "data/random_erdos_renyi_"+str(i)+".txt"
            each_network_topology_file["random_barabasi_albert_"+str(i)]= "data/random_barabasi_albert_"+str(i)+".txt"
        
            each_topology_mean_value_spike["random_erdos_renyi_"+str(i)] = [300]
            each_topology_mean_value_spike["random_barabasi_albert_"+str(i)] = [300]
    elif topology_set =="big":
        for i in range(2):
            each_network_topology_file["random_erdos_renyi_"+str(i)]= "data/size_"+str(400)+"_random_erdos_reni_0_0_1_"+str(i)+".txt"
    elif topology_set =="all":
        each_network_topology_file = {"SURFnet":'data/Surfnet',"IBM":'data/IBM',"ATT":'data/ATT_topology_file',"Abilene":'data/abilene'}
        each_topology_mean_value_spike={"ATT":[350],"IBM":[350],"SURFnet":[350],"Abilene":[350]}
        for i in [2]:
            each_network_topology_file["G_50_0.05_"+str(i)]= "data/random_erdos_renyi2_"+str(i)+".txt"
            each_topology_mean_value_spike["G_50_0.05_"+str(i)] = [400]
            each_network_topology_file["PA_50_2_"+str(i)]= "data/random_barabasi_albert2_"+str(i)+".txt"
            each_topology_mean_value_spike["PA_50_2_"+str(i)] = [400]
        for i in [2]:
            each_network_topology_file["G_50_0.1_"+str(i)]= "data/random_erdos_renyi_"+str(i)+".txt"
            each_network_topology_file["PA_50_3_"+str(i)]= "data/random_barabasi_albert_"+str(i)+".txt"
            each_topology_mean_value_spike["G_50_0.1_"+str(i)] = [400]
            each_topology_mean_value_spike["PA_50_3_"+str(i)] = [400]
    elif topology_set =="random_reny":
        for i in [2]:
            each_network_topology_file["G_50_0.05_"+str(i)]= "data/random_erdos_renyi2_"+str(i)+".txt"
            each_network_topology_file["PA_50_3_"+str(i)]= "data/random_erdos_renyi_"+str(i)+".txt"
            each_topology_mean_value_spike["G_50_0.05_"+str(i)] = [350,400]
            each_topology_mean_value_spike["PA_50_3_"+str(i)] = [350,400]

    elif topology_set =="random":
        for i in [2]:
            each_network_topology_file["random_barabasi_albert2_"+str(i)]= "data/random_barabasi_albert2_"+str(i)+".txt"
            each_network_topology_file["random_barabasi_albert_"+str(i)]= "data/random_barabasi_albert_"+str(i)+".txt"
            each_topology_mean_value_spike["random_barabasi_albert2_"+str(i)] = [350,400]
            each_topology_mean_value_spike["random_barabasi_albert_"+str(i)] = [350,400]

#         for i in range(1,2):
#             each_network_topology_file["random_erdos_renyi_"+str(i)]= "data/random_erdos_renyi_"+str(i)+".txt"
#             each_network_topology_file["random_barabasi_albert_"+str(i)]= "data/random_barabasi_albert_"+str(i)+".txt"
#             each_topology_mean_value_spike["random_erdos_renyi_"+str(i)] = [30]
#             each_topology_mean_value_spike["random_barabasi_albert_"+str(i)] = [30]
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

    feasibility(each_network_topology_file,results_file_path,inventory_utilization_results_file_path,delived_purification_EPRs_file_path,number_of_user_pairs,number_of_time_slots,spike_means,num_spikes,experiment_repeat,storage_node_selection_schemes,fidelity_threshold_ranges,cyclic_workload,storage_capacities,given_life_time_set,distance_between_users,setting_demands,edge_fidelity_ranges)


# In[2]:


"""We have 6 pairs of users"""
each_topology_mean_value_spike={"ATT":200,"IBM":0,"SURFnet":200,"Abilene":150
                               }


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




