#!/usr/bin/env python
# coding: utf-8

# In[1]:


from plotting_functions import *
import csv
import math
from math import log
from tmgen.models import uniform_tm,spike_tm,modulated_gravity_tm,random_gravity_tm,gravity_tm,exp_tm


# In[43]:


def get_available_topologies(results_file_path,given_spike_mean,given_threshold_range,given_num_of_paths,given_life_time):
    all_selected_topologies = []
    all_available_storage_capacities = []
    with open(results_file_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in (reader):
            topology = line[0]
            num_paths = int(line[2])
            life_time =int(line[3])
            spike_mean = int(line[5])
            threshold_range = float(line[9])
            storage_capacity = int(line[12])
            if given_spike_mean == int(line[5]):
                if "erdos" in topology and "erdos_renyi2" not in topology:
                    topology = "G(n,p=0.1)"
                elif "barabasi_albert_" in topology and "barabasi_albert2_" not in topology:
                    topology= "G(n,m=3)"
                elif "erdos_renyi2" in topology:
                    topology = "G(n,p=0.05)"
                elif "barabasi_albert2" in topology:
                    topology= "G(n,m=2)"
                else:
                    topology = topology
                if int(life_time)==given_life_time and given_spike_mean ==spike_mean and threshold_range ==given_threshold_range and given_num_of_paths == num_paths:
                    if topology not in all_selected_topologies:
                        all_selected_topologies.append(topology)
                    if storage_capacity not in all_available_storage_capacities:
                        all_available_storage_capacities.append(storage_capacity)
    return all_selected_topologies,all_available_storage_capacities
    
def get_each_storage_capacity_storage_numbers_swaps(results_file_path,given_topology,given_spike_mean,given_threshold_range,given_num_of_paths,given_life_time,given_capacity):
    each_storage_numbers_swappings = {}
    each_topology_plot_name = {}
    with open(results_file_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in (reader):
            topology = line[0]
            threshold_range = float(line[9])
            spike_mean = int(line[5])
            storage_capacity = int(line[12])
            if "erdos" in topology and "erdos_renyi2" not in topology:
                topology = "G(n,p=0.1)"
                plot_name = "CDF_swappings_G_n_p_0.1_"+str(threshold_range)+"_"+str(storage_capacity)+".pdf"
            elif "barabasi_albert_" in topology and "barabasi_albert2_" not in topology:
                topology= "G(n,m=3)"
                plot_name = "CDF_swappings_G_n_m_3_"+str(threshold_range)+"_"+str(storage_capacity)+".pdf"
            elif "erdos_renyi2" in topology:
                topology = "G(n,p=0.05)"
                plot_name = "CDF_swappings_G_n_p_0.05_"+str(threshold_range)+"_"+str(storage_capacity)+".pdf"
            elif "barabasi_albert2" in topology:
                topology= "G(n,m=2)"
                plot_name = "CDF_swappings_G_n_m_2_"+str(threshold_range)+"_"+str(storage_capacity)+".pdf"
            else:
                topology = topology
                plot_name = "CDF_swappings_"+str(topology)+"_"+str(threshold_range)+"_"+str(storage_capacity)+".pdf"
            each_topology_plot_name[topology]= plot_name
            storage_numbers = int(line[1])
            num_paths = int(line[2])
            life_time =int(line[3])
            
            objective_function_value =float(line[4])
            storage_selection_scheme = line[8]
            #print(line)
            if objective_function_value >0 and given_capacity ==storage_capacity and topology ==given_topology and int(life_time)==given_life_time and given_spike_mean ==spike_mean and threshold_range ==given_threshold_range and given_num_of_paths == num_paths:
                storage_numbers_key = str(storage_numbers)
                
                try:
                    each_storage_numbers_swappings[storage_selection_scheme][storage_numbers_key].append(objective_function_value)
                except:
                    try:
                        each_storage_numbers_swappings[storage_selection_scheme][storage_numbers_key]= [objective_function_value]
                    except:
                        each_storage_numbers_swappings[storage_selection_scheme] = {}
                        each_storage_numbers_swappings[storage_selection_scheme][storage_numbers_key]= [objective_function_value]
                        
    return each_storage_numbers_swappings,each_topology_plot_name




def get_each_scheme_EGR(file_result_path,spike_mean):
    each_scheme_each_storage_number_EGRs = {}
    num_of_paths = []
    number_of_storages = []
    each_num_of_storage_num_of_paths = {}
    
    topologies = set([])
    life_times = set([])
    unique_topologies = []
    all_selected_topologies = []
    threshold_ranges = []
    each_topology_plot_name = {}
    available_networks = []
    available_storage_capacities = []
    with open(file_result_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in (reader):##[network_topology,number_of_storages,num_paths,life_time,
            #objective_value,spike_mean,num_spikes,i,storage_node_selection_scheme,fidelity_threshold_range]
            topology = line[0]
            threshold_range = float(line[9])
            storage_capacity = int(line[12])
            experiment_id = int(line[7])
            if spike_mean == int(line[5]):
                if storage_capacity not in available_storage_capacities:
                    available_storage_capacities.append(storage_capacity)
                if threshold_range not in threshold_ranges:
                    threshold_ranges.append(threshold_range)
                if topology not in unique_topologies:
                    unique_topologies.append(topology)
                if "erdos" in topology and "erdos_renyi2" not in topology:
                    topology = "G_n_p_0.1"
                    plot_name = "life_time_feasibility_G_n_p_0.1_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"

                elif "barabasi_albert_" in topology and "barabasi_albert2_" not in topology:
                    topology= "G_n_m_3"
                    plot_name = "life_time_feasibility_G_n_m_3_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
                elif "erdos_renyi2" in topology:
                    topology = "G_n_p_0.05"
                    plot_name = "life_time_feasibility_G_n_p_0.05_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
                elif "barabasi_albert2" in topology:
                    topology= "G_n_m_2"
                    plot_name = "life_time_feasibility_G_n_m_2_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
                else:
                    topology = topology
                    plot_name = "life_time_feasibility_"+str(topology)+"_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
    #             if topology in "G(n,p=0.1)":
    #                 print(line)
                if topology not in available_networks:
                    available_networks.append(topology)
                try:
                    each_topology_plot_name[topology][threshold_range][storage_capacity]=plot_name
                except:
                    try:
                        each_topology_plot_name[topology][threshold_range] = {}
                        each_topology_plot_name[topology][threshold_range][storage_capacity]=plot_name
                    except:
                        each_topology_plot_name[topology]={}
                        each_topology_plot_name[topology][threshold_range]={}
                        each_topology_plot_name[topology][threshold_range][storage_capacity]=plot_name
                        
                if topology not in all_selected_topologies:
                    all_selected_topologies.append(topology)
                topologies.add(topology)
                storage_numbers = int(line[1])
                num_paths = int(line[2])
                life_time =float(line[3])
                life_times.add(life_time)
                objective_function_value =float(line[4])
                storage_selection_scheme = line[8]

                if int(life_time)==1000:
                    scheme_key = str(float('inf'))+" time slots, "+storage_selection_scheme
                else:
                    scheme_key = "One time slot, "+storage_selection_scheme

                if num_paths not in num_of_paths:
                        num_of_paths.append(num_paths)
                if storage_numbers not in number_of_storages:
                        number_of_storages.append(storage_numbers)        
                if objective_function_value >0.0:
                    #print(line,"one satisfied case")
                    try:
                        each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers].append(objective_function_value)
                    except:
                        try:
                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
                        except:
                            try:
                                each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
                            except:
                                try:
                                    each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range]= {}
                                    each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                    each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
                                except:
                                    try:
                                        each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity] ={}
                                        each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range]= {}
                                        each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                        each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]

                                    except:
                                        
                                        try:
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology] = {}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity] ={}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range]= {}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]

                                        except:
                                            each_scheme_each_storage_number_EGRs[scheme_key]={}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology]= {}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity] ={}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range]= {}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                            each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
#             else:
#                 print(line)
#     print("unique_topologies ",storage_selection_scheme,unique_topologies,storage_selection_scheme)
#     print("all_selected_topologies",storage_selection_scheme,all_selected_topologies)
    return each_scheme_each_storage_number_EGRs,each_topology_plot_name,number_of_storages,threshold_ranges,available_networks,available_storage_capacities


def get_each_scheme_available_satisfied(file_result_path,spike_mean):    
    
    each_scheme_each_storage_number_satisfying = {}
    num_of_paths = []
    number_of_storages = []
    each_num_of_storage_num_of_paths = {}
    each_topology_each_storage_available = {}
    topologies = set([])
    life_times = set([])
    unique_topologies = []
    all_selected_topologies = []
    threshold_ranges = []
    each_topology_plot_name = {}
    available_networks = []
    available_storage_capacities = []
    with open(file_result_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in (reader):##[network_topology,number_of_storages,num_paths,life_time,
            #objective_value,spike_mean,num_spikes,i,storage_node_selection_scheme,fidelity_threshold_range]
            topology = line[0]
            threshold_range = float(line[9])
            storage_capacity = int(line[12])
            experiment_id = int(line[7])
            if spike_mean == int(line[5]):
                if storage_capacity not in available_storage_capacities:
                    available_storage_capacities.append(storage_capacity)
                
                if threshold_range not in threshold_ranges:
                    threshold_ranges.append(threshold_range)
                if topology not in unique_topologies:
                    unique_topologies.append(topology)
                if "erdos" in topology and "erdos_renyi2" not in topology:
                    topology = "G_n_p_0.1"
                    plot_name = "life_time_feasibility_G_n_p_0.1_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"

                elif "barabasi_albert_" in topology and "barabasi_albert2_" not in topology:
                    topology= "G_n_m_3"
                    plot_name = "life_time_feasibility_G_n_m_3_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
                elif "erdos_renyi2" in topology:
                    topology = "G_n_p_0.05"
                    plot_name = "life_time_feasibility_G_n_p_0.05_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
                elif "barabasi_albert2" in topology:
                    topology= "G_n_m_2"
                    plot_name = "life_time_feasibility_G_n_m_2_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
                else:
                    topology = topology
                    plot_name = "life_time_feasibility_"+str(topology)+"_"+str(threshold_range)+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf"
    #             if topology in "G(n,p=0.1)":
    #                 print(line)
                if topology not in available_networks:
                    available_networks.append(topology)
                try:
                    each_topology_plot_name[topology][threshold_range][storage_capacity]=plot_name
                except:
                    try:
                        each_topology_plot_name[topology][threshold_range] = {}
                        each_topology_plot_name[topology][threshold_range][storage_capacity]=plot_name
                    except:
                        each_topology_plot_name[topology]={}
                        each_topology_plot_name[topology][threshold_range]={}
                        each_topology_plot_name[topology][threshold_range][storage_capacity]=plot_name
                        
                if topology not in all_selected_topologies:
                    all_selected_topologies.append(topology)
                topologies.add(topology)
                storage_numbers = int(line[1])
                num_paths = int(line[2])
                life_time =float(line[3])
                life_times.add(life_time)
                objective_function_value =float(line[4])
                storage_selection_scheme = line[8]

                if int(life_time)==1000:
                    scheme_key = str(float('inf'))+" time slots, "+storage_selection_scheme
                else:
                    scheme_key = "One time slot, "+storage_selection_scheme

                try:
                    each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers]+=1
                except:
                    try:
                        each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers]=1
                    except:
                        try:
                            each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths]={}
                            each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers]=1
                        except:
                            try:
                                each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range]={}
                                each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths]={}
                                each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers]=1
                            except:
                                try:
                                
                                    each_topology_each_storage_available[scheme_key][topology][storage_capacity]={}
                                    each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range] = {}
                                    each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths]={}
                                    each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers]=1

                                except:
                                    try:
                                        each_topology_each_storage_available[scheme_key][topology]={}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity]={}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range] = {}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths]={}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers]=1

                                    except:
                                        each_topology_each_storage_available[scheme_key]={}
                                        each_topology_each_storage_available[scheme_key][topology]={}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity]={}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range] = {}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths]={}
                                        each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers]=1

                if num_paths not in num_of_paths:
                        num_of_paths.append(num_paths)
                if storage_numbers not in number_of_storages:
                        number_of_storages.append(storage_numbers)        
                if objective_function_value >0.0:
                    #print(line,"one satisfied case")
                    try:
                        each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers].append(objective_function_value)
                    except:
                        try:
                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
                        except:
                            try:
                                each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
                            except:
                                try:
                                    each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range]= {}
                                    each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                    each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
                                except:
                                    try:
                                        each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity] ={}
                                        each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range]= {}
                                        each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                        each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]

                                    except:
                                        
                                        try:
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology] = {}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity] ={}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range]= {}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]

                                        except:
                                            each_scheme_each_storage_number_satisfying[scheme_key]={}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology]= {}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity] ={}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range]= {}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths]= {}
                                            each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][num_paths][storage_numbers] = [objective_function_value]
#             else:
#                 print(line)
#     print("unique_topologies ",storage_selection_scheme,unique_topologies,storage_selection_scheme)
#     print("all_selected_topologies",storage_selection_scheme,all_selected_topologies)
    return each_scheme_each_storage_number_satisfying,each_topology_each_storage_available,each_topology_plot_name,number_of_storages,threshold_ranges,available_networks,available_storage_capacities


# In[44]:



for spike_mean in [1500,1200,280,350]:
    file_result_path = '../quantum_storage/results/results_feasibility.csv'
    each_scheme_each_storage_number_satisfying , each_topology_each_storage_available,each_topology_plot_name,number_of_storages, threshold_ranges,available_networks,available_storage_capacities = get_each_scheme_available_satisfied(file_result_path,spike_mean)


#     print(list(each_scheme_each_storage_number_satisfying.keys()))
#     print(threshold_ranges,available_networks)
    

    # print('each_scheme_each_storage_number_satisfying',each_scheme_each_storage_number_satisfying)
    # print('num_of_paths',num_of_paths)
    # print('number_of_storages',number_of_storages)
    # print("each_topology_each_storage_available",each_topology_each_storage_available)
    indx =0
    num_of_paths = [3]
    for n_path in num_of_paths:
        for storage_capacity in available_storage_capacities:
            for topology in list(available_networks):
                print("topology is",topology)
                for threshold_range in [0.8]:
                    print("threshold",threshold_range)
                    each_life_time_each_storage_numbers_satisfying_percentage = {}
                    each_scheme_each_storage_numbers_satisfying_percentage = {}
                    for scheme_key in each_scheme_each_storage_number_satisfying:
                        print("for scheme ",scheme_key)
                        each_scheme_each_storage_numbers_satisfying_percentage[scheme_key] = {}

                        for storage_num in number_of_storages:
        #                     print("storage nodes ",storage_num)
        #                     print(each_topology_each_storage_available[scheme_key][topology][threshold_range][n_path][storage_num])
        #                     print(each_scheme_each_storage_number_satisfying[scheme_key][topology][threshold_range][n_path][storage_num])
                            try:
                                all_solutions =each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][n_path][storage_num]
                            except ValueError:
                                print(ValueError)
                                all_solutions=0
                            try:
                                satisfied_work_loads = len(each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][n_path][storage_num])
                            except:
        #                         print(ValueError)
                                satisfied_work_loads = 0
                            satisfied_percentage = (satisfied_work_loads/all_solutions)*100
                            print("for storage %s we have %s satisfied from %s available"%(storage_num,satisfied_work_loads,all_solutions))
                            each_scheme_each_storage_numbers_satisfying_percentage[scheme_key][storage_num] = satisfied_percentage
            #                 each_scheme_each_storage_numbers_satisfying_percentage[scheme_key][storage_num] = 1

                    print("each_scheme_each_storage_numbers_satisfying_percentage",each_scheme_each_storage_numbers_satisfying_percentage)    
                    print("each_topologmy_plot_name",each_topology_plot_name[topology].keys())
                    plot_bar_plot("Number of storages",'Percentage of \n satisfied workloads',
                              each_scheme_each_storage_numbers_satisfying_percentage,number_of_storages,
                              "plots/"+each_topology_plot_name[topology][threshold_range][storage_capacity])
    


# In[ ]:





# In[45]:




for spike_mean in [300]:
#     file_result_path = '../quantum_storage/results/results_maximizing_egr_dynamic_population.csv'
    file_result_path = '../quantum_storage/results/results_maximizing_egr_dynamic_weight.csv'
    each_scheme_each_storage_number_satisfying , each_topology_each_storage_available,each_topology_plot_name,number_of_storages, threshold_ranges,available_networks,available_storage_capacities = get_each_scheme_available_satisfied(file_result_path,spike_mean)
    num_of_paths = [3]
    for n_path in num_of_paths:
        for storage_capacity in available_storage_capacities:
            for topology in list(available_networks):
                #print("topology is",topology)
                for threshold_range in threshold_ranges:
                    
                    for scheme_key in each_scheme_each_storage_number_satisfying:
                        print("topology %s for scheme %s ,threshold_range %s"%(topology, scheme_key,threshold_range))
                        
                        each_scheme_each_storage_number_EGR = {}
                        x_axis_max_value = 0
                        number_of_storages.sort()
                        y_axis_labels=[]
                        x_axis_data=[]
                        for storage_num in number_of_storages:
                            
                            
                            #print("for topology %s spike mean %s  capacity %s threshold %s scheme %s storage %s"
                             #    %(topology,spike_mean,storage_capacity,threshold_range,scheme_key,storage_num))
                            #print("each_scheme_each_storage_number_satisfying",each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][n_path])
                            try:
                                EGRs =each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][n_path][storage_num]
                            except:
                                EGRs = [0]
                            y_axis_labels.append(storage_num)
                            new_EGRs = []
                            for EGR in EGRs:
                                EGR = EGR/100
                                if EGR> x_axis_max_value:
                                    x_axis_max_value = EGR
                                new_EGRs.append(EGR)
                            x_axis_data.append(new_EGRs)
                            new_EGRs.sort()
                            #print("for storage %s we have %s"%(storage_num,new_EGRs))
                            try:
                                each_scheme_each_storage_number_EGR[topology][storage_num] = sum(EGRs)/len(EGRs)/1000
                            except:
                                each_scheme_each_storage_number_EGR[topology]={}
                                each_scheme_each_storage_number_EGR[topology][storage_num] = sum(EGRs)/len(EGRs)/1000

#                         print("x_axis_data for topollgy %s is %s"%(topology,x_axis_data))
                        horizontal_box_plat("EGR (in houndered)","",x_axis_data,y_axis_labels,x_axis_max_value,"plots/horizontal_box_plot_topology_"+each_topology_plot_name[topology][threshold_range][storage_capacity]+".pdf")
                                                                                                


# In[ ]:





# In[46]:


for spike_mean in [300]:
    file_result_path = '../quantum_storage/results/results_maximizing_egr_dynamic_weight.csv'
    each_scheme_each_storage_number_EGRs ,each_topology_plot_name,number_of_storages,threshold_ranges,available_networks,available_storage_capacities = get_each_scheme_EGR(file_result_path,spike_mean)
    print("available_networks",available_networks)
    # print("each_scheme_each_storage_number_satisfying",each_scheme_each_storage_number_satisfying)
    print("each_scheme_each_storage_number_EGRs",each_scheme_each_storage_number_EGRs.keys())
    

    indx =0
    num_of_paths = [3]
    threshold_ranges.sort()
    for n_path in num_of_paths:
        for storage_num in [5]:
            for topology in list(available_networks):
                #print("topology is",topology)
                for storage_capacity in available_storage_capacities:
                    each_scheme_each_storage_numbers_avg_EGRs = {}
                    schemes_title_in_order = []
                    max_value_on_y_axis = 0
                    selected_thresholds = []
                    for scheme_key in each_scheme_each_storage_number_EGRs:
                        #print("for scheme ",scheme_key)
                        for threshold_range in threshold_ranges:
                            if threshold_range>0.65:
                                if threshold_range not in selected_thresholds:
                                    selected_thresholds.append(threshold_range)
                                #print("threshold",threshold_range)
                                if scheme_key not in schemes_title_in_order:
                                    schemes_title_in_order.append(scheme_key)


                                try:
                                    EGRs = each_scheme_each_storage_number_EGRs[scheme_key][topology][storage_capacity][threshold_range][n_path][storage_num]
                                except:
            #                         print(ValueError)
                                    EGRs = [0]
                                if max(EGRs)>max_value_on_y_axis:
                                    max_value_on_y_axis = max(EGRs)
                                avg_EGRs = sum(EGRs)/len(EGRs)
                                try:
                                    each_scheme_each_storage_numbers_avg_EGRs[scheme_key][threshold_range] = avg_EGRs
                                except:
                                    each_scheme_each_storage_numbers_avg_EGRs[scheme_key]={}
                                    each_scheme_each_storage_numbers_avg_EGRs[scheme_key][threshold_range] = avg_EGRs
                                print("for topology %s scheme %s storage %s and range %s we have %s"%
                                      (topology, scheme_key,storage_num,threshold_range,avg_EGRs))
                                #time.sleep(3)
                #                 each_scheme_each_storage_numbers_satisfying_percentage[scheme_key][storage_num] = 1

        #         print("each_scheme_each_storage_numbers_satisfying_percentage",each_scheme_each_storage_numbers_satisfying_percentage)    
                    selected_thresholds.sort()
#                     for scheme in schemes_title_in_order:
#                         for threshold_range in threshold_ranges:
#                             print("for scheme %s range %s we have %s "%(scheme,threshold_range,each_scheme_each_storage_numbers_satisfying_percentage[scheme][threshold_range]))
#                             print(threshold_range,each_scheme_each_storage_numbers_satisfying_percentage[scheme].keys())
                    ploting_simple_y_as_x("Fidelity threshold",'EGR',
                                          min(selected_thresholds),max_value_on_y_axis,
                                          list(schemes_title_in_order),
                                          each_scheme_each_storage_numbers_avg_EGRs,
                                          selected_thresholds,selected_thresholds,
                                          False,"plots/EGR_as_threshold_range_"+topology+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf")


# In[ ]:





# In[47]:


for spike_mean in [1200,1500,650,300,700]:
    file_result_path = '../quantum_storage/results/results_feasibility2.csv'
    each_scheme_each_storage_number_satisfying , each_topology_each_storage_available,each_topology_plot_name,number_of_storages,threshold_ranges,available_networks,available_storage_capacities = get_each_scheme_available_satisfied(file_result_path,spike_mean)
    print("available_networks",available_networks)
    # print("each_scheme_each_storage_number_satisfying",each_scheme_each_storage_number_satisfying)
    print("each_topology_each_storage_available",each_topology_each_storage_available.keys())
    print(list(each_scheme_each_storage_number_satisfying.keys()))

    indx =0
    num_of_paths = [3]
    threshold_ranges.sort()
    for n_path in num_of_paths:
        for storage_num in [5]:
            for topology in list(available_networks):
                print("topology is",topology)
                for storage_capacity in available_storage_capacities:
                    each_scheme_each_storage_numbers_satisfying_percentage = {}
                    schemes_title_in_order = []
                    for scheme_key in each_scheme_each_storage_number_satisfying:
                        print("for scheme ",scheme_key)
                        for threshold_range in threshold_ranges:
                            print("threshold",threshold_range)
                            if scheme_key not in schemes_title_in_order:
                                schemes_title_in_order.append(scheme_key)

        #                     print(each_topology_each_storage_available[scheme_key][topology][threshold_range][n_path][storage_num])
        #                     print(each_scheme_each_storage_number_satisfying[scheme_key][topology][threshold_range][n_path][storage_num])
                            try:
                                all_solutions =each_topology_each_storage_available[scheme_key][topology][storage_capacity][threshold_range][n_path][storage_num]
                            except:
                                all_solutions=0
                            try:
                                satisfied_work_loads = len(each_scheme_each_storage_number_satisfying[scheme_key][topology][storage_capacity][threshold_range][n_path][storage_num])
                            except:
        #                         print(ValueError)
                                satisfied_work_loads = 0
                            if all_solutions==0:
                                satisfied_percentage = 0
                            else:
                                satisfied_percentage = (satisfied_work_loads/all_solutions)*100
                            try:
                                each_scheme_each_storage_numbers_satisfying_percentage[scheme_key][threshold_range] = satisfied_percentage
                            except:
                                each_scheme_each_storage_numbers_satisfying_percentage[scheme_key]={}
                                each_scheme_each_storage_numbers_satisfying_percentage[scheme_key][threshold_range] = satisfied_percentage
                            print("for scheme %s storage %s and range %s we have  available %s satisfied %s and percentage is %s"%
                                  (scheme_key,storage_num,threshold_range,all_solutions,satisfied_work_loads,satisfied_percentage))
                            #time.sleep(3)
            #                 each_scheme_each_storage_numbers_satisfying_percentage[scheme_key][storage_num] = 1

        #         print("each_scheme_each_storage_numbers_satisfying_percentage",each_scheme_each_storage_numbers_satisfying_percentage)    
                    threshold_ranges.sort()
                    for scheme in schemes_title_in_order:
                        for threshold_range in threshold_ranges:
                            print("for scheme %s range %s we have %s "%(scheme,threshold_range,each_scheme_each_storage_numbers_satisfying_percentage[scheme][threshold_range]))
                            print(threshold_range,each_scheme_each_storage_numbers_satisfying_percentage[scheme].keys())
                    ploting_simple_y_as_x("Fidelity threshold",'Percentage of \n satisfied workloads',
                                          min(threshold_ranges),100,
                                          list(schemes_title_in_order),
                                          each_scheme_each_storage_numbers_satisfying_percentage,
                                          threshold_ranges,threshold_ranges,
                                          False,"plots/feasibility_percentage_as_threshold_range_"+topology+"_"+str(spike_mean)+"_"+str(storage_capacity)+".pdf")


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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




