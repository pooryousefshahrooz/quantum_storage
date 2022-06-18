#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


"""implement our OR model. When we want to code an optimization model,
we put a placeholder for that model (like a blank canvas), 
then add its elements (decision variables and constraints) to it."""
import csv
from network import Network
from workload import Work_load
# from docplex.mp.progress import *
# from docplex.mp.progress import SolutionRecorder
import os

import pandas as pd
from docplex.mp.progress import *
from docplex.mp.progress import SolutionRecorder
import networkx as nx
import time


# In[ ]:


def CPLEX_resource_cinsumption_minimization(network,work_load,life_time,iteration):
    
    import docplex.mp.model as cpx
    opt_model = cpx.Model(name="Storage problem model"+str(iteration))
    w_vars = {}
    u_vars = {}
    #opt_model = Model(name="Storage problem model")
#     for t in work_load.T:
#         for k in work_load.each_t_requests[t]:
#             for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
#     x_vars  = {(t,k,p): opt_model.integer_var(lb=0, ub= 100,
#                               name="x_{0}_{1}_{2}".format(t,k,p))  for t in work_load.T 
#                for k in work_load.each_t_requests[t] 
#                for p in network.each_request_virtual_paths[k]}
    
#     s_vars  = {(t,k,p): opt_model.integer_var(lb=0, ub= 100,
#                               name="s_{0}_{1}_{2}".format(t,k,p))  for t in work_load.T 
#                for k in work_load.each_t_requests[t] 
#                for p in network.each_request_real_paths[k]}
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
                    opt_model.add_constraint(u_vars[t,j,p_s] == u_vars[t-1,j,p_s]-
                    opt_model.sum(w_vars[t-1,k,p] *network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                    for k in work_load.each_t_requests[t] if k!=j for p in network.each_request_virtual_paths_include_subpath[k][p_s])
                    +opt_model.sum(w_vars[t-1,j,p_s])
                                         , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))
    else:
        #inventory evolution constraint
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p_s in network.each_request_real_paths[j]:
                    opt_model.add_constraint(u_vars[t,j,p_s] == -
                    opt_model.sum(w_vars[t-1,k,p] *network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
                    for k in work_load.each_t_requests[t] if k!=j for p in network.each_request_virtual_paths_include_subpath[k][p_s] 
                    )
                    + opt_model.sum(w_vars[t-1,j,p_s])
                                         , ctname="inventory_evolution_{0}_{1}".format(t,j,p_s))

    # serving from inventory constraint
    for t in work_load.T[1:]:
        for j in network.storage_pairs:
            
            for p_s in network.each_request_real_paths[j]:
#                 print("for time %s and storage pair %s and real sub path %s"%(t,j,p_s))
#                 for k in work_load.each_t_requests[t]:
#                     print("this is the request ",k)
#                     if k!=j:
#                         print("which was not equal to storage pair")
#                         for p in network.each_request_virtual_paths_include_subpath[k][p_s]:
#                             print("this path %s include the sub path %s"%(p,p_s))
                            
                opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]*network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t))
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
                opt_model.sum(w_vars[t,k,p]*network.get_required_purification_EPR_pairs(p,work_load.get_each_request_threshold(k,t)) for k in work_load.each_t_requests[t]
                for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k] if network.check_path_include_edge(edge,p))
                                     
                 <= network.each_edge_capacity[edge], ctname="edge_capacity_{0}_{1}".format(t,edge))
     
    # storage servers capacity constraint
    for t in work_load.T:
        for s1 in network.storage_nodes:
            opt_model.add_constraint(opt_model.sum(u_vars[t,(s1,s2),p] 
                for s2 in network.storage_nodes if network.check_storage_pair_exist(s1,s2)
                for p in network.each_request_real_paths[(s1,s2)])
        <= network.get_storage_capacity(s1), ctname="storage_capacity_constraint_{0}_{1}".format(t,s1))
    
    # constraints for serving from storage at time zero and 1 should be zero
    for t in [0,1]:
        opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]
                for k in work_load.each_t_requests[t] for p in network.each_request_virtual_paths[k] 
                )<=0, ctname="serving_from_inventory_{0}".format(t))
    
    # constraints for putting in storage at time zero  should be zero
    for t in [0]:
        opt_model.add_constraint(opt_model.sum(w_vars[t,k,p]
                for k in work_load.each_t_requests[t] for p in network.each_request_real_paths[k] 
                )<=0, ctname="storing_in_inventory_{0}".format(t))   
    

    # constraint for inventory is zero at time zero 
    for t in [0]:
        for j in network.storage_pairs:
             for p_s in network.each_request_real_paths[j]:
                    opt_model.add_constraint(u_vars[t,j,p_s] <=0, ctname="storage_capacity_constraint_{0}_{1}_{2}".format(t,j,p_s))
    
    """defining an objective, which is a linear expression"""
#     objective = opt_model.sum(1/len(work_load.T[1:])*1/len(work_load.each_t_real_requests[t])*1/work_load.each_t_each_request_demand[t][k]
#                               *(w_vars[t,k,p] * network.get_path_length(p)) for t in work_load.T[1:]
#                               for k in work_load.each_t_real_requests[t] 
#                               for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]
#                               )
    objective = opt_model.sum(1/len(work_load.T[1:])*1/len(work_load.each_t_real_requests[t])*1/work_load.each_t_each_request_demand[t][k]
                              *(w_vars[t,k,p] * network.get_path_length(p)) for t in work_load.T[1:]
                              for k in work_load.each_t_real_requests[t] 
                              for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]
                              )
#     opt_model.minimize(1/len(work_load.T[1:])*
#                     1/opt_model.sum(len(work_load.each_t_real_requests[t]) for t in work_load.T[1:])*
#                     (opt_model.sum(w_vars[t,k,p] * network.get_path_length(p)/work_load.each_t_each_request_demand[t][k] for t in work_load.T[1:]
#                               for k in work_load.each_t_real_requests[t] 
#                               for p in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]))
#                                 )
    
    # for maximization
    opt_model.minimize(objective)
    
#     opt_model.solve()
    opt_model.print_information()
    #try:
    opt_model.solve()

    #save_csv_file(w_vars,"./optimization_solution_w_values.csv")
#         save_csv_file(x_vars,"./optimization_solution_x_values.csv")
#         save_csv_file(s_vars,"./optimization_solution_s_values.csv")



#     opt_df = pd.DataFrame.from_dict(u_vars, orient="index", 
#                                 columns = ["variable_object"])
#     opt_df.index =  pd.MultiIndex.from_tuples(opt_df.index, 
#                                    names=["column_i", "column_j"])
#     opt_df.reset_index(inplace=True)

#     opt_df["solution_value"] =  opt_df["variable_object"].apply(lambda item: item.solution_value)

#     opt_df.drop(columns=["variable_object"], inplace=True)
#     opt_df.to_csv("./optimization_solution_u_values.csv")
#     for t in work_load.T[1:]:
#         for k in  work_load.each_t_requests[t]:
#             for path in network.each_request_real_paths[k]+network.each_request_virtual_paths[k]:
#                 print("for request %s path %s %s we have lenght %s "%(k,path,network.set_of_paths[path],network.get_path_length(path)))
#     import pdb
    
    print('docplex.mp.solution',opt_model.solution)
    objective_value = 0
    try:
        if opt_model.solution:
            objective_value =opt_model.solution.get_objective_value()
    except ValueError:
        print(ValueError)
        #pass
    #pdb.set_trace()
    if objective_value>0:
        #time.sleep(4)
        
        for t in work_load.T[1:]:
            for j in network.storage_pairs:
                for p in network.each_request_real_paths[j]:
                    print("for time %s storage pair %s on path %s we have %s",t,j,p,u_vars[t,j,p].solution_value)
        import pdb
        #pdb.set_trace()
        #print(ValueError)
    opt_model.clear()
    #if objective_value<2:
        #print(objective_value,network.storage_pairs,network.user_pairs)
        
    #
    return objective_value
#     except ValueError:
#         print(ValueError)


# In[ ]:





# In[ ]:


def minimizing_resource_consumption(each_network_topology_file,spike_mean,num_spikes,experiment_repeat):
    for network_topology,file_path in each_network_topology_file.items():
        results_file_path = 'results_file_feasibility_checking.csv'
        import pdb
        each_storage_each_path_number_value = {}
        # pdb.set_trace()
        distance_between_users = 3
        number_of_user_pairs =1
        number_of_time_slots = 15
        for i in range(experiment_repeat):
    #         network = Network('abilene')
            network = Network(file_path)
            network.get_user_pairs(number_of_user_pairs,distance_between_users,number_of_time_slots)
            network.set_user_pair_fidelity_threshold()
            work_load = Work_load(number_of_time_slots,"time_demands_file.csv")

            objective_values = []
            selected_storage_nodes = []
            selected_storage_pairs = []

            #nx.draw(network.g,with_labels=True)
            # plt.show()

            for number_of_storages in range(0,7):

                """with new storage pairs, we will check the solution for each number of paths(real and virtual)"""
                for num_paths in range(3,4):
                    network.reset_pair_paths()
                    work_load.reset_variables()
                    pairs = []
                    #print("network.each_t_user_pairs",network.each_t_user_pairs)
                    for t,user_pairs in network.each_t_user_pairs.items():            
                        for user_pair in user_pairs:
                            if user_pair not in pairs:
                                pairs.append(user_pair)
                    network.get_each_user_pair_real_paths(pairs)
                    import pdb
                    #pdb.set_trace()
                    path_counter_id = 0
                    print("for number of storages round  ",number_of_storages)
                    """select and add new storage pairs"""
                    network.get_new_storage_pairs(number_of_storages)
                    work_load.set_each_time_requests(network.each_t_user_pairs,network.storage_pairs)
                    work_load.set_each_time_real_requests(network.each_t_user_pairs)

                    #print("network.storage_pairs",network.storage_pairs)
                    #import pdb
                    #pdb.set_trace()
                    network.get_each_user_pair_real_paths(network.storage_pairs)
                    if number_of_storages==1:
                        number_of_storages = 2

                    """first we add the real paths between storage pairs"""

                    print("for iteration %s storage %s and path number %s"%(i,number_of_storages,num_paths))
                    for storage_pair in network.storage_pairs:
                        #print("going to get real paths between storage pair ",storage_pair)
                        paths = network.get_real_path(storage_pair,num_paths)
                        #print("got paths",paths)
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
                            #print("*** we used path_counter_id",path_counter_id)
                            path_counter_id+=1

                    across_all_time_slots_pairs = []
                    for t,user_pairs in network.each_t_user_pairs.items():
                        for user_pair in user_pairs:
                            if user_pair not in across_all_time_slots_pairs:
                                across_all_time_slots_pairs.append(user_pair)
                    all_sub_paths = []
                    for user_pair in across_all_time_slots_pairs:
                        paths = network.get_real_path(user_pair,num_paths)
                        #print("we got real paths for user pair",user_pair,paths)
                        for path in paths:
                            network.set_of_paths[path_counter_id] = path
                            network.set_each_path_length(path_counter_id,path)
                            network.each_path_path_id[tuple(path)] = path_counter_id
                            try:
                                network.each_request_real_paths[user_pair].append(path_counter_id)
                            except:
                                network.each_request_real_paths[user_pair]=[path_counter_id]
                            #print("*** we used path_counter_id",path_counter_id)
                            path_counter_id+=1
            #             print("for user pair  we got real paths and it is",user_pair)
#                         print("network.each_request_real_paths",network.each_request_real_paths)
#                         print("network.set_of_paths",network.set_of_paths)
                        import pdb
                        #pdb.set_trace()
                        for storage_pair in network.storage_pairs:
                            """add one new path to the previous paths"""

                            for real_sub_path in network.each_storage_real_paths[storage_pair]:
                                #for edge in real_sub_path:
                                    #network.g.remove_edge(edge[0],edge[1])
                                #network.g.add_edge(storage_pair[0],storage_pair[1],weight=0)
#                                 print("we are going to add a virtual path for user pair %s that includes %s"%(user_pair,real_sub_path))
                                paths = network.get_paths_to_connect_users_to_storage(user_pair,real_sub_path,num_paths)
                                this_sub_path_id = network.each_path_path_id[tuple(real_sub_path)]
                                #print(paths)

                                for path in paths:
                                    network.set_each_path_length(path_counter_id,path)
                                    """we remove the sub path that is connecting two storage pairs 
                                    from the path because we do not want to check the edge capacity for the edges of this subpath"""
#                                     print("we set length %s for path %s having sub path %s with ID %s"%(len(path),path,real_sub_path,this_sub_path_id))
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
                                    path = network.remove_storage_pair_real_path_from_path(real_sub_path,path)
                                    #print("and after removing sub path we have ",path,real_sub_path,len(path))
                                    network.set_of_paths[path_counter_id] = path
                                    try:
                                        network.each_request_virtual_paths[user_pair].append(path_counter_id)
                                    except:
                                        network.each_request_virtual_paths[user_pair]=[path_counter_id]
                                    #print("*** we used path_counter_id",path_counter_id)
                                    path_counter_id+=1


                                for pair in network.storage_pairs:
                                    network.each_request_virtual_paths[pair]=[]

                            #print("for user pair %s to storage pair %s we got real paths and it is:"%(user_pair,storage_pair))
#                         print("for user pair %s we added the virtual path to all storage pairs")
#                         print("network.each_request_virtual_paths",network.each_request_virtual_paths)
#                         print("network.set_of_paths",network.set_of_paths)
#                         import pdb
                        
                    if number_of_storages==0:
                        for t,pairs in network.each_t_user_pairs.items():
                            for pair in pairs:
                                network.each_request_virtual_paths[pair]=[]
                    for j in network.storage_pairs:
                        for sub_path_id in all_sub_paths:
                            try:
                                network.each_request_virtual_paths_include_subpath[j][sub_path_id] = []
                            except:
                                network.each_request_virtual_paths_include_subpath[j]={}
                                network.each_request_virtual_paths_include_subpath[j][sub_path_id] = []
                    for t in range(number_of_time_slots):
                        for k in work_load.each_t_requests[t]:
                            try:
                                if k in list(network.each_request_virtual_paths_include_subpath.keys()):
                                    pass
                                else:
                                    network.each_request_virtual_paths_include_subpath[k]= {}
                            except:
                                network.each_request_virtual_paths_include_subpath[k]= {}
                                
#                     for t in work_load.T[1:]:
#                         for j in network.storage_pairs:
#                             for p_s in network.each_request_real_paths[j]:
#                                 for k in work_load.each_t_requests[t]:
#                                     print(p for p in network.each_request_virtual_paths_include_subpath[k][p_s] 
#                                           if k in list(network.each_request_virtual_paths_include_subpath.keys()))
#                     print("network.each_request_real_paths",network.each_request_real_paths)
#                     print("network.each_request_virtual_paths",network.each_request_virtual_paths)
#                     print("network.set_of_paths",network.set_of_paths)
#                     print('network.each_request_real_paths',network.each_request_real_paths)
#                     print('network.each_request_virtual_paths',network.each_request_virtual_paths)
                    import pdb
                   
                    """we set the demands for each user pair"""
                    work_load.set_each_user_pair_demands(number_of_time_slots,network.each_t_user_pairs,spike_mean,num_spikes)
                                                   
                    """we set the capacity of each storage node"""

                    network.set_storage_capacity()

                    """we add new storage pairs as our user pairs and set the demand for them zero"""

                    work_load.set_storage_pairs_as_user_pairs(network.storage_pairs)

                    """we set the fidelity threshold of each new storage pair as a user request"""

                    work_load.set_threshold_fidelity_for_request_pairs(network.each_t_user_pairs,network.storage_pairs,network.each_user_request_fidelity_threshold)

                    """we set the required EPR pairs to achieve each request threshold fidelity"""
                    network.set_required_EPR_pairs_for_path_fidelity_threshold()


                    """we set at least one demand for each time to avoid divided by zero error"""

                    work_load.check_demands_per_each_time(network.each_t_user_pairs)
                    """we print all variables to check the variables and values"""

            #         print("we ahve these parameters for network")

#                     print('network.set_E',network.set_E)
#                     print('network.each_edge_capacity',network.each_edge_capacity)



            #         print('network.each_path_basic_fidelity',network.each_path_basic_fidelity)
            #         print('network.oracle_for_target_fidelity',network.oracle_for_target_fidelity)
#                     print('network.storage_pairs',network.storage_pairs)
            #         print('network.storage_nodes',network.storage_nodes)
            #         print('network.each_storage_capacity',network.each_storage_capacity)


#                     print("we now print workload parameters to check")

#                     print('work_load.T',work_load.T)
#                     print('work_load.num_requests',work_load.num_requests)
#                     #print('work_load.request_pairs',work_load.request_pairs)
#                     print('work_load.each_t_requests',work_load.each_t_requests)
#                     print('work_load.each_t_real_requests',work_load.each_t_real_requests)
                    
#                     print('work_load.each_t_each_request_demand',work_load.each_t_each_request_demand)
            #         print('work_load.each_request_threshold',work_load.each_request_threshold)
            #         print('work_load.each_user_request_fidelity_threshold',work_load.each_user_request_fidelity_threshold)

                    import pdb
                    #pdb.set_trace()
                    """solve the optimization"""
                    life_time_set = [1000,2]
                    for life_time in life_time_set:
                        try:
                            objective_value=-1
                            try:

                                objective_value = CPLEX_resource_cinsumption_minimization(network,work_load,life_time,i)
                            except ValueError:
                                print(ValueError)
                                #pass
                            objective_values.append(objective_value)

        #                     print("demand",work_load.each_t_each_request_demand)
        #                     print("user pairs",network.each_t_user_pairs)
        #                     print('network.set_of_paths',network.set_of_paths)
        #                     print('network.each_request_real_paths',network.each_request_real_paths)
        #                     print('network.each_request_virtual_paths',network.each_request_virtual_paths)
        #                     print("work_load.each_t_real_requests",work_load.each_t_real_requests)
        #                     time.sleep(4)
        #                     import pdb
        #                     
                            print("life time %s the objective value for %s storage nodes and %s paths between each pair of nodes is %s"%(life_time,number_of_storages,num_paths,objective_value))
                            #pdb.set_trace()
                            #time.sleep(5)
                            #if objective_value>=0:
                            with open(results_file_path, 'a') as newFile:                                
                                newFileWriter = csv.writer(newFile)
                                newFileWriter.writerow([network_topology,number_of_storages,num_paths,life_time,objective_value,spike_mean,num_spikes,i]) 
                                try:
                                    each_storage_each_path_number_value[number_of_storages][num_paths].append(objective_value)
                                except:
                                    try:
                                        each_storage_each_path_number_value[number_of_storages][num_paths]=[objective_value]
                                    except:
                                        each_storage_each_path_number_value[number_of_storages]= {}
                                        each_storage_each_path_number_value[number_of_storages][num_paths]=[objective_value]

                        except ValueError:
                            #pass
                            print(ValueError)
            print("until the %s th iteration we have %s"%(i,each_storage_each_path_number_value)) 
            #time.sleep(10)
        # work_load = Work_load()
        # network = Network('../data')

        # solution_value = CPLEX_resource_cinsumption_minimization(network,work_load)
        # print('done')


# In[ ]:





# In[ ]:


experiment_repeat =500
spike_mean = 200
num_spikes = 1
each_network_topology_file = {"ATT":'data/ATT_topology_file',"Abilene":'data/abilene',"SURFnet":'data/Surfnet'}
for i in range(5):
    each_network_topology_file["random_erdos_renyi_"+str(i)]= "data/random_erdos_renyi_"+str(i)+".txt"
    each_network_topology_file["random_barabasi_albert_"+str(i)]= "data/random_barabasi_albert_"+str(i)+".txt"
# each_network_topology_file = {"Testing_topology":'data/test_topology'}
minimizing_resource_consumption(each_network_topology_file,spike_mean,num_spikes,experiment_repeat)


# In[2]:


# for number_of_storages in range(0,2):
#     print(number_of_storages)


# In[ ]:


# class Network(object):
#     def __init__(self, config, data_dir='./data/'):
#         #self.topology_file = data_dir + config.topology_file
#         self.topology_file = 'data'
#         self.set_E = [(1,2),(2,3),(3,4),(4,5),(2,7),(7,8),(8,9),(9,5),(5,6),(2,10),(10,11),(11,12),(12,5)]
#         self.each_edge_capacity = {(1,2):20,(2,3):20,(3,4):20,(4,5):20,(2,7):20,(7,8):20,(8,9):20,
#                                    (9,5):20,(5,6):20,(2,10):20,(10,11):20,(11,12):20,(12,5):20}
        
#         self.max_edge_capacity = 10
#         self.set_of_paths = {0:[(1,2),(2,10),(10,11),(11,12),(12,5),(5,6)],
#                              1:[(2,3),(3,4),(4,5)],
#                             2:[(2,7),(7,8),(8,9),(9,5)],
#                              3:[(10,11),(11,12)],
#                             4:[(1,2),(2,5),(5,6)],5:[(1,2),(2,5),(5,6)],
#                             6:[(2,10),(10,12),(12,5)],
#                             7:[(1,2),(2,10),(10,12),(12,5),(5,6)]}
#         self.each_path_basic_fidelity = {0:0.7,
#                              1:0.8,
#                             2:0.75,
#                              3:0.9,
#                             4:0.7,
#                             5:0.6,
#                             6:0.8,
#                             7:0.8}
#         self.oracle_for_target_fidelity={0:{0.7:2,0.8:3,0.9:2},
#                              1:{0.7:2,0.8:3,0.9:2},
#                             2:{0.7:3,0.8:4,0.9:2},
#                              3:{0.7:3,0.8:4,0.9:2},
#                             4:{0.7:3,0.8:4,0.9:2},
#                             5:{0.7:3,0.8:4,0.9:2},
#                             6:{0.7:3,0.8:4,0.9:2},
#                             7:{0.7:2,0.8:4,0.9:2}} 
#         self.each_request_real_paths = {(1,6):[0],(2,5):[1,2],(10,12):[3]}
#         self.each_request_virtual_paths = {(1,6):[3,4,7],(2,5):[6],(10,12):[]}
#         self.storage_pairs = [(2,5),(10,12)]
#         self.storage_nodes = [2,5,10,12]
#         self.each_storage_capacity = {2:100,5:100,10:100,12:100}
        
#         #self.shortest_paths_file = self.topology_file +'_shortest_paths'
#         #self.DG = nx.DiGraph()

#         #self.load_topology()
#         #self.calculate_paths()
#     def get_required_purification_EPR_pairs(self,p,threshold):
#         if threshold>=0.9:
#             return self.oracle_for_target_fidelity[p][0.9]
#         elif 0.8<threshold<0.9:
#             return self.oracle_for_target_fidelity[p][0.8]
#         elif threshold<0.8:
#             return self.oracle_for_target_fidelity[p][0.7]
#         else:
#             return 1
        
#     def load_topology(self):
#         print('[*] Loading topology...', self.topology_file)
#         f = open(self.topology_file, 'r')
#         header = f.readline()
#         self.num_nodes = int(header[header.find(':')+2:header.find('\t')])
#         self.num_links = int(header[header.find(':', 10)+2:])
#         f.readline()
#         self.link_capacities = np.empty((self.num_links))
#         self.link_weights = np.empty((self.num_links))
#         for line in f:
#             link = line.split('\t')
#             i, s, d, w, c = link
#             print('this is our line',link,i, s, d, w, c)
#             self.link_capacities[int(i)] = float(c)
#             self.link_weights[int(i)] = int(w)
#             self.DG.add_weighted_edges_from([(int(s),int(d),int(w))])
#             self.set_E.append()
        
#         f.close()
#         #print('nodes: %d, links: %d\n'%(self.num_nodes, self.num_links))
#         nx.draw_networkx(self.DG)
#         plt.show()
#     def check_path_include_sub_path(self,sub_path,path):
#         if self.set_of_paths[sub_path] in self.set_of_paths[path]:
#             return True
#         else:
#             return False
#     def get_edges(self):
#         return self.set_E
#     def get_storage_capacity(self,storage):
#         return self.each_storage_capacity[storage]
#     def check_path_include_edge(self,edge,path):
#         #print('edge is %s and path is %s and Paths is %s'%(edge,path,self.set_of_paths))
#         if edge in self.set_of_paths[path]:
#             return True
#         elif edge not  in self.set_of_paths[path]:
#             return False
#     def check_storage_pair_exist(self,s1,s2):
#         if (s1,s2) in self.storage_pairs:
#             return True
#         else:
#             return False
#     def check_request_use_path(self,k,p):
#         if p in self.each_request_virtual_paths[k] or (p in self.each_request_virtual_paths[k]):
#             return True
#         else:
#             return False
#     #         edge_capacity
#     #         paths
#     #         virtual_paths
#     def get_path_length(self,path):
#         return len(self.set_of_paths[path])
#     def scale_network(self,each_edge_scaling):
        
#         for edge in self.set_E:
#             self.each_edge_capacity[edge] = self.each_edge_capacity[edge]*each_edge_scaling
            
        
# class Work_load(object):
#     def __init__(self):
#         self.T = [0,1,2]
#         self.num_requests = 2
#         self.request_pairs = [(1,6),(2,5),(10,12)]
#         self.each_t_requests = {0:[(1,6),(2,5),(10,12)],1:[(1,6),(2,5),(10,12)],2:[(1,6),(2,5),(10,12)]}
#         self.each_t_real_requests = {1:[(1,6)],2:[(1,6)]}
#         self.time_intervals = 2
#         self.each_t_each_request_demand = {0:{(1,6):10,(2,5):0,(10,12):0},
#                                            1:{(1,6):1,(2,5):0,(10,12):0},2:{(1,6):10,(2,5):0,(10,12):0}}
#         self.each_request_thrshold = {(1,6):{0:0.9,1:0.8,2:0.9},
#                                      (2,5):{0:0.3,1:0.3,2:0.3},
#                                      (10,12):{0:0.3,1:0.3,2:0.3}
#                                      }
#     def get_each_request_thrshold(self,k,t):
#         return self.each_request_thrshold[k][t]
#     def generate_workload_circle(self,alpha,T,request_pairs):
#         new_t_request_demands = {}
#         for t,request_demand in self.each_t_each_request_demand.items():
#             new_t_request_demands[t] = {}
#             for req,d in request_demand.items():
#                 new_t_request_demands[t][req] = d*alpha
#         for k,v in new_t_request_demands.items():
#             self.each_t_each_request_demand[k] = v
        
        


# In[ ]:



def save_csv_file(variable,file_name):
    opt_df = pd.DataFrame.from_dict(variable, orient="index", 
                                columns = ["variable_object"])
    opt_df.index =  pd.MultiIndex.from_tuples(opt_df.index, 
                                   names=["column_i", "column_j","column_k"])
    opt_df.reset_index(inplace=True)

    opt_df["solution_value"] =  opt_df["variable_object"].apply(lambda item: item.solution_value)

    opt_df.drop(columns=["variable_object"], inplace=True)
    opt_df.to_csv(file_name)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# # connect a listener to the model
# opt_model.add_progress_listener(TextProgressListener())
# opt_model.solve(clean_before_solve=True);

# for l, listener in enumerate(opt_model.iter_progress_listeners(), start=1):
#     print("listener #{0} has type '{1}', clock={2}".format(l, listener.__class__.__name__, listener.clock))
# opt_model.clear_progress_listeners()
# opt_model.add_progress_listener(TextProgressListener(clock='objective', absdiff=1, reldiff=0))
# sol_recorder = SolutionRecorder()
# opt_model.clear_progress_listeners()
# opt_model.add_progress_listener(sol_recorder)
# opt_model.solve(clean_before_solve=True);

# # utility function to display recorded solutions in a recorder.
# def display_recorded_solutions(rec):
#     print('* The recorder contains {} solutions'.format(rec.number_of_solutions))
#     for s, sol in enumerate(rec.iter_solutions(), start=1):
#         sumvals = sum(v for _, v in sol.iter_var_values())
#         print('  - solution #{0}, obj={1}, non-zero-values={2}, total={3}'.format(
#            s, sol.objective_value, sol.number_of_var_values, sumvals))

# display_recorded_solutions(sol_recorder)


# sol_recorder2 = SolutionRecorder(clock='objective')
# opt_model.clear_progress_listeners()
# opt_model.add_progress_listener(sol_recorder2)
# opt_model.solve(clean_before_solve=True)
# display_recorded_solutions(sol_recorder2)
# #large_hearts.add_progress_listener(TextProgressListener(clock='gap'))
# # maximum non-improving time is 4 seconds.
# opt_model.add_progress_listener(AutomaticAborter(max_no_improve_time=4))
# # again use clean_before_solve to ensure deterministic run of this cell.
# opt_model.solve(clean_before_solve=True, log_output=False);


# In[ ]:


# """defining our decicion variables (that are integer)
# store decision variables in Python dictionaries (or Pandas Series)
# where dictionary keys are decision variables, and values are decision variable objects.
# A decision variable is defined with three main properties: 
# its type (continuous, binary or integer), 
# its lower bound (0 by default), and 
# its upper bound (infinity by default)"""

# x_vars  = {(i,j): opt_model.integer_var(lb=l[i,j], ub= u[i,j],
#                               name="x_{0}_{1}".format(i,j))  for i in set_I for j in set_J}

# # print(x_vars)#{(1, 1): docplex.mp.Var(type=I,name='x_1_1',lb(lower bound)=2,ub(upper bound)=10), 
# ##(1, 2): docplex.mp.Var(type=I,name='x_1_2',ub=10) ...


# In[ ]:


# """set constraints. 
# Any constraint has three parts: a left-hand side (normally a linear combination of decision variables),
# a right-hand side (usually a numeric value), and
# a sense (Less than or equal, Equal, or Greater than or equal).
# To set up any constraints, we need to set each part:"""

# # <= constraints
# constraints = {j : 
# opt_model.add_constraint(
#     ct=opt_model.sum(a[i,j] * x_vars[i,j] for i in set_I) <= b[j], ctname="constraint_{0}".format(j)) for j in set_J}
# # >= constraints
# constraints = {j : opt_model.add_constraint(ct=opt_model.sum(a[i,j] * x_vars[i,j] for i in set_I) >= b[j], ctname="constraint_{0}".format(j)) for j in set_J}
# # == constraints
# constraints = {j : 
# opt_model.add_constraint( ct=opt_model.sum(a[i,j] * x_vars[i,j] for i in set_I) == b[j], ctname="constraint_{0}".format(j)) for j in set_J}


# In[ ]:





# In[ ]:


# """we call the solver to solve our optimization model."""
# # solving with local cplex
# opt_model.solve()

# # solving with cplex cloud
# # opt_model.solve(url="your_cplex_cloud_url", key="your_api_key")


# In[ ]:


# """get results and post-process them
# If the problem is solved to optimality, we can get and process results as follows:
# """
# import pandas as pd
# opt_df = pd.DataFrame.from_dict(x_vars, orient="index", 
#                                 columns = ["variable_object"])
# opt_df.index =  pd.MultiIndex.from_tuples(opt_df.index, 
#                                names=["column_i", "column_j"])
# opt_df.reset_index(inplace=True)

# opt_df["solution_value"] =  opt_df["variable_object"].apply(lambda item: item.solution_value)
    
# opt_df.drop(columns=["variable_object"], inplace=True)
# opt_df.to_csv("./optimization_solution.csv")


# In[ ]:


# # """input parameters"""
# # import random
# # n = 10
# # m = 5
# # set_I = range(1, n+1)
# # set_J = range(1, m+1)
# # # print(set_I)#range(1, 11)
# # # print(set_J)# range(1, 6)

# # c = {(i,j): random.normalvariate(0,1) for i in set_I for j in set_J}
# # a = {(i,j): random.normalvariate(0,5) for i in set_I for j in set_J}
# # l = {(i,j): random.randint(0,10) for i in set_I for j in set_J}
# # u = {(i,j): random.randint(10,20) for i in set_I for j in set_J}
# # b = {j: random.randint(0,30) for j in set_J}

# # print(c) {(1, 1): #-0.03927470599644141, (1, 2): 1.0333198122747003, (1, 3): ....


# from docplex.mp.progress import ProgressListener

# class AutomaticAborter(ProgressListener):
#     """ a simple implementation of an automatic search stopper.
#     """
#     def __init__(self, max_no_improve_time=10.):
#         super(AutomaticAborter, self).__init__(ProgressClock.All)
#         self.last_obj = None
#         self.last_obj_time = None
#         self.max_no_improve_time = max_no_improve_time
        
#     def notify_start(self):
#         super(AutomaticAborter, self).notify_start()
#         self.last_obj = None
#         self.last_obj_time = None    
        
#     def is_improving(self, new_obj, eps=1e-4):
#         last_obj = self.last_obj
#         return last_obj is None or (abs(new_obj- last_obj) >= eps)
            
#     def notify_progress(self, pdata):
#         super(AutomaticAborter, self).notify_progress(pdata)
#         if pdata.has_incumbent and self.is_improving(pdata.current_objective):
#             self.last_obj = pdata.current_objective
#             self.last_obj_time = pdata.time
#             print('----> #new objective={0}, time={1}s'.format(self.last_obj, self.last_obj_time))
#         else:
#             # a non improving move
#             last_obj_time = self.last_obj_time
#             this_time = pdata.time
#             if last_obj_time is not None:
#                 elapsed = (this_time - last_obj_time)
#                 if elapsed >= self.max_no_improve_time:
#                     print('!! aborting cplex, elapsed={0} >= max_no_improve: {1}'.format(elapsed,
#                                                                              self.max_no_improve_time))
#                     self.abort()
#                 else:
#                     print('----> non improving time={0}s'.format(elapsed))

