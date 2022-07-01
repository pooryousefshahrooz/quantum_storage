# quantum_storage

Feasibility experiment:

You need to run script IBM_cplex_feasibility.py with arguments arg1 arg2 where arg1 can be one of real/random1/random2 where each indicates different topology sets. arg2 is indicating the way the workload would be generated. User python_library to use tgem spike model or use random in order to have demands generated randomly.

The results would be saved in results/results_feasibility.csv file.

The columns are: network_topology,number_of_storages,num_paths,life_time,
                                                                        objective_value,spike_mean,num_spikes,experiment_num,
                                                                        storage_node_selection_scheme,
                                                                        fidelity_threshold_range,cyclic_or_sequential_workload,
                                                                        hops_between_user_pairs,storage_capacity]
                                                                        
                                                                        
Maximizing entanglement generation rate experiment:

You need to run script maximizing_EGR.py with arguments real/random1/random2 dynamic_weight where the first argument indicates the set of topologies and the second argument indicates the case that the weight of users is changing over time.

The results would be in file results/results_maximizing_egr_dynamic_weight.csv.

The columns are: network_topology,number_of_storages,num_paths,life_time,
                                                                        objective_value,spike_mean,num_spikes,experiment_num,
                                                                        storage_node_selection_scheme,
                                                                        fidelity_threshold_range,cyclic_workload,
                                                                        distance_between_users,storage_capacity
                                                                        
                                                                        
Be sure you have folder results in your root folder.