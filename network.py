#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx
import matplotlib.pyplot as plt
import random


# In[ ]:


class Network:
    def __init__(self,topology_file_path):
        self.set_E = []
        self.each_edge_capacity = {(1,2):20,(2,3):20,(3,4):20,(4,5):20,(2,7):20,(7,8):20,(8,9):20,
                                   (9,5):20,(5,6):20,(2,10):20,(10,11):20,(11,12):20,(12,5):20}
        
        self.max_edge_capacity = 10
        #self.topology_file = data_dir + config.topology_file
        self.topology_file = topology_file_path
        self.set_E = [(1,2),(2,3),(3,4),(4,5),(2,7),(7,8),(8,9),(9,5),(5,6),(2,10),(10,11),(11,12),(12,5)]
        self.each_edge_capacity = {(1,2):20,(2,3):20,(3,4):20,(4,5):20,(2,7):20,(7,8):20,(8,9):20,
                                   (9,5):20,(5,6):20,(2,10):20,(10,11):20,(11,12):20,(12,5):20}
        
        self.max_edge_capacity = 10
        self.set_of_paths = {0:[(1,2),(2,10),(10,11),(11,12),(12,5),(5,6)],
                             1:[(2,3),(3,4),(4,5)],
                            2:[(2,7),(7,8),(8,9),(9,5)],
                             3:[(10,11),(11,12)],
                            4:[(1,2),(2,5),(5,6)],5:[(1,2),(2,5),(5,6)],
                            6:[(2,10),(10,12),(12,5)],
                            7:[(1,2),(2,10),(10,12),(12,5),(5,6)]}
        self.each_path_basic_fidelity = {0:0.7,
                             1:0.8,
                            2:0.75,
                             3:0.9,
                            4:0.7,
                            5:0.6,
                            6:0.8,
                            7:0.8}
        self.oracle_for_target_fidelity={0:{0.7:2,0.8:3,0.9:2},
                             1:{0.7:2,0.8:3,0.9:2},
                            2:{0.7:3,0.8:4,0.9:2},
                             3:{0.7:3,0.8:4,0.9:2},
                            4:{0.7:3,0.8:4,0.9:2},
                            5:{0.7:3,0.8:4,0.9:2},
                            6:{0.7:3,0.8:4,0.9:2},
                            7:{0.7:2,0.8:4,0.9:2}} 
        self.each_request_real_paths = {(1,6):[0],(2,5):[1,2],(10,12):[3]}
        self.each_request_virtual_paths = {(1,6):[3,4,7],(2,5):[6],(10,12):[]}
        self.each_request_real_paths = {}
        self.each_request_virtual_paths = {}
        self.storage_pairs = [(2,5),(10,12)]
        self.storage_nodes = [2,5,10,12]
        self.each_storage_capacity = {2:1000,5:1000,10:1000,12:1000}
        self.each_storage_capacity = {}
        self.storage_pairs = []
        self.storage_nodes = []
        self.each_user_pair_all_real_paths = {}
        self.each_user_pair_real_paths = {}
        self.each_user_pair_virtual_paths = {}
        self.nodes = []
        self.load_topology()
#         self.g = nx.Graph()
#         self.modified_g = nx.Graph()
#         for each_edge in self.each_edge_capacity:
#             self.g.add_edge(each_edge[0],each_edge[1],weight=1)
#         self.g.add_edge(2,3,weight=1)
#         self.g.add_edge(3,4,weight=2)
#         self.g.add_edge(4,5,weight=1)
#         self.g.add_edge(5,6,weight=1)
#         self.g.add_edge(2,10,weight=1)
#         self.g.add_edge(10,11,weight=1)
#         self.g.add_edge(11,12,weight=1)
#         self.g.add_edge(12,5,weight=1)
#         self.g.add_edge(2,7,weight=1)
#         self.g.add_edge(7,8,weight=1)
#         self.g.add_edge(8,9,weight=1)
#         self.g.add_edge(9,5,weight=1)
        #nx.draw(g,with_labels=True)
        #plt.show()
        self.user_pairs = []
        candidate_user_pairs = [(1,6),(2,10),(4,8),(6,11),(5,10),(3,9),(8,10),(0,3),(1,10),(2,5)]
        while(len(self.user_pairs)<2):
            user_pair = candidate_user_pairs[random.randint(0,len(candidate_user_pairs)-1)]
            if user_pair not in self.user_pairs:
                self.user_pairs.append(user_pair)
        
        self.each_path_legth = {}
        
        #self.shortest_paths_file = self.topology_file +'_shortest_paths'
        #self.DG = nx.DiGraph()

        #self.load_topology()
        #self.calculate_paths()
    def set_each_path_length(self,path_id,path):
        self.each_path_legth[path_id] = len(path)
    
                
        
    def remove_storage_pair_real_path_from_path(self,sub_path,path):
        A = path
        B = sub_path
        start_ind = None
        for i in range(len(A)):
            if A[i:i+len(B)] == B:
                start_ind = i
                break

        C = [x for i, x in enumerate(A) 
             if start_ind is None or not(start_ind <= i < (start_ind + len(B)))]
            
        return C
    def recursive_purification(self,n,f):
        if n==1:
            return f
        else:
            numerator=  f * self.recursive_purification(n-1,f)
            denominator = numerator + (1-f) * (1-self.recursive_purification(n-1,f))
            return round(numerator/(denominator),4)
    

    def set_required_EPR_pairs_for_path_fidelity_threshold(self):
        basic_threshold = 0.1
        for path in self.set_of_paths:
            for f in [0.6,0.7,0.8,0.9,1.0]:
                n = 1
                final_fidelity = f
                if final_fidelity!=1.0:
                    while final_fidelity <=0.999:
                        n+=1
                        final_fidelity = self.recursive_purification(n,f)
                else:
                    n=1
                try:
                    self.oracle_for_target_fidelity[path][f] = n
                except:
                    self.oracle_for_target_fidelity[path] = {}
                    self.oracle_for_target_fidelity[path][f] = n
    def set_storage_capacity(self):
        for storage_node in self.storage_nodes:
            self.each_storage_capacity[storage_node] =1000
    def get_required_purification_EPR_pairs(self,p,threshold):
        if threshold>=0.9:
            return self.oracle_for_target_fidelity[p][0.9]
        elif 0.8<threshold<0.9:
            return self.oracle_for_target_fidelity[p][0.8]
        elif threshold<0.8:
            return self.oracle_for_target_fidelity[p][0.7]
        else:
            return 1
    def get_new_storage_pairs(self,number_of_storages):
        new_selected_storage_nodes = []
        new_selected_storage_pairs = []
        user_pair_nodes = set([])
        for user_pair in self.user_pairs: 
            user_pair_nodes.add(user_pair[0])
            user_pair_nodes.add(user_pair[1])
        user_pair_nodes = list(user_pair_nodes)
        permitted_nodes = []
        for node in self.nodes:
            if node not in user_pair_nodes and node not in self.storage_nodes:
                permitted_nodes.append(node)
        #print("we have permitted node as ",permitted_nodes,len(self.storage_nodes),number_of_storages)
        while(len(self.storage_nodes)<number_of_storages):
            storage1 = permitted_nodes[0]
            while(storage1 in self.storage_nodes):
                storage1 = permitted_nodes[random.randint(0,len(permitted_nodes)-1)]
            #print("we selected new storage node %s"%(storage1))
            if  self.storage_pairs:
                for storage_node in self.storage_nodes:
                    if ((storage1,storage_node) not in self.storage_pairs and (storage_node,storage1) not in self.storage_pairs) and storage1!=storage_node:
                        self.storage_pairs.append((storage1,storage_node))
                if storage1 not in self.storage_nodes:
                    self.storage_nodes.append(storage1)
            else:
                storage1 = permitted_nodes[random.randint(0,len(permitted_nodes)-1)]
                storage2 = storage1
                while(storage1==storage2):
                    storage2 = permitted_nodes[random.randint(0,len(permitted_nodes)-1)]
                #print("for round  we have new storage node %s"%(storage1))
                if (storage1,storage2) not in self.storage_pairs and (storage2,storage1) not in self.storage_pairs:
                    self.storage_pairs.append((storage1,storage2))
                    self.storage_nodes.append(storage1)
                    self.storage_nodes.append(storage2)
                #print("this is our first storage pair",self.storage_pairs)
    def reset_pair_paths(self):
        self.each_user_pair_all_real_paths = {}
    
    def get_each_user_pair_real_paths(self,user_pairs):
        for user_pair in user_pairs:
            shortest_paths = nx.all_shortest_paths(self.g,source=user_pair[0],target=user_pair[1], weight='weight')
            self.each_user_pair_all_real_paths[user_pair] = shortest_paths
    def get_real_path(self,user_pair,number_of_paths):
        path_selecion_flag = False
        path_counter = 1
        paths = []
        
        for path in self.each_user_pair_all_real_paths[user_pair]:
            if path_counter<=number_of_paths:
                node_indx = 0
                path_edges = []
                for node_indx in range(len(path)-1):
                    path_edges.append((path[node_indx],path[node_indx+1]))
                    node_indx+=1
                paths.append(path_edges)

            path_counter+=1
        return paths
                    
    def load_topology(self):
       
        self.set_E=[]
        self.each_edge_capacity={}
        self.nodes = []
        self.max_edge_capacity = 0
        self.g = nx.Graph()
        print('[*] Loading topology...', self.topology_file)
        f = open(self.topology_file, 'r')
        header = f.readline()
        f.readline()
#         self.link_capacities = np.empty((self.num_links))
#         self.link_weights = np.empty((self.num_links))
        for line in f:
            link = line.split('\t')
            i, s, d, c = link
            if int(s) not in self.nodes:
                self.nodes.append(int(s))
            if int(d) not in self.nodes:
                self.nodes.append(int(d))
            
            self.set_E.append((int(s),int(d)))
            random_capacity = random.randint(180, 600)
            self.each_edge_capacity[(int(s),int(d))] = random_capacity
            if random_capacity>self.max_edge_capacity:
                self.max_edge_capacity  = random_capacity
            self.g.add_edge(int(s),int(d),weight=1)
#             self.link_capacities[int(i)] = float(c)
#             self.link_weights[int(i)] = int(w)
#             self.DG.add_weighted_edges_from([(int(s),int(d),int(w))])
#             self.set_E.append()
        
        f.close()
        #print('nodes: %d, links: %d\n'%(self.num_nodes, self.num_links))
#         nx.draw_networkx(self.DG)
#         plt.show()
        
    def get_virtual_path(self,user_pair,storage_pair,real_sub_path):
        path_selecion_flag = False
        shortest_paths = nx.all_shortest_paths(self.g,source=user_pair[0],target=user_pair[1], weight='weight')
        for path in shortest_paths:
            #print("for path with removed graph",path)
            node_indx = 0
            path_edges = []
            for node_indx in range(len(path)-1):
                path_edges.append((path[node_indx],path[node_indx+1]))
                node_indx+=1
            if not path_selecion_flag:
                try:
                    if path_edges not in self.each_user_pair_virtual_paths[user_pair] and storage_pair in path_edges:
                        self.each_user_pair_virtual_paths[user_pair].append(path_edges)
                        #print("we added path %s for user pair %s"%(path,user_pair))
                        path_selecion_flag = True

                except:
                    if storage_pair in path_edges:
                        self.each_user_pair_virtual_paths[user_pair]=[path_edges]
                        path_selecion_flag = True
                        #print("we added path %s for user pair %s"%(path,user_pair))
                    
    def join_users_to_storages(self,src,dst,str1,str2,real_sub_path,number_of_paths):
        #print("we are going to connect node %s to %s and %s to %s"%(src,str1,str2,dst))
        self.get_each_user_pair_real_paths([(src,str1)])
        self.get_each_user_pair_real_paths([(str2,dst)])
        sub_paths1 = self.get_real_path((src,str1),number_of_paths)
        sub_paths2 = self.get_real_path((str2,dst),number_of_paths)
        #print("we got these paths for them",sub_paths1,sub_paths2)
        set_of_paths = []
        for path_part1 in sub_paths1:
            new_path = []
            for edge in path_part1:
                new_path.append(edge)
            for edge in real_sub_path:
                new_path.append(edge)
            back_up_path = []
            for e in new_path:
                back_up_path.append(e)
            for path_part2 in sub_paths2:
                for edge in path_part2:
                    new_path.append(edge)
                set_of_paths.append(new_path)
                new_path = back_up_path
        return set_of_paths
    def get_paths_to_connect_users_to_storage(self,user_pair,real_sub_path,num_paths):
        #print("we are going to find shortest path to connect user pair %s to sub path %s"%(user_pair,real_sub_path))
        src= user_pair[0]
        dst= user_pair[1]
        str1 = real_sub_path[0][0]
        str2= real_sub_path[len(real_sub_path)-1][1]
        first_set_of_paths = self.join_users_to_storages(src,str1,str2,dst,real_sub_path,num_paths)
        second_set_of_paths = self.join_users_to_storages(dst,str1,str2,src,real_sub_path,num_paths)
#         print("we got first set of paths ",first_set_of_paths)
#         print("we got the second set of paths",second_set_of_paths)
        first_path_length = []
        second_path_length = []
        for path in first_set_of_paths:
            first_path_length.append(len(path))
        for path in second_set_of_paths:
            second_path_length.append(len(path))
        if sum(first_path_length)/len(first_path_length)>sum(second_path_length)/len(second_path_length):
            return second_set_of_paths
        else:
            return first_set_of_paths
        
    def set_each_path_basic_fidelity(self):
        basic_fidelities = [0.7,0.8,0.9]
        self.each_path_basic_fidelity = {}
        for path in self.set_of_paths:
            basic_fidelity = basic_fidelities[random.randint(0,len(basic_fidelities)-1)]
            self.each_path_basic_fidelity[path]= basic_fidelity
        
    def check_path_include_sub_path(self,sub_path,path):
        if self.set_of_paths[sub_path] in self.set_of_paths[path]:
            return True
        else:
            return False
    def get_edges(self):
        return self.set_E
    def get_storage_capacity(self,storage):
        return self.each_storage_capacity[storage]
    def check_path_include_edge(self,edge,path):
        #print('edge is %s and path is %s and Paths is %s'%(edge,path,self.set_of_paths))
        if edge in self.set_of_paths[path]:
            return True
        elif edge not  in self.set_of_paths[path]:
            return False
    def check_storage_pair_exist(self,s1,s2):
        if (s1,s2) in self.storage_pairs:
            return True
        else:
            return False
    def check_request_use_path(self,k,p):
        if p in self.each_request_virtual_paths[k] or (p in self.each_request_virtual_paths[k]):
            return True
        else:
            return False
    #         edge_capacity
    #         paths
    #         virtual_paths
    def get_path_length(self,path):
        return self.each_path_legth[path]-1
    def scale_network(self,each_edge_scaling):
        
        for edge in self.set_E:
            self.each_edge_capacity[edge] = self.each_edge_capacity[edge]*each_edge_scaling
            
        
    def generate_new_random_storage_nodes(self,storage_nodes,num_storage_nodes):
        return []
    
    
    def generate_each_pair_real_paths(self,user_request_pairs):
        return []
    def generate_each_pair_virtual_paths(self,user_request_pairs,storage_nodes):
        return []
    def get_set_of_paths(self):
        return []
        
    def load_shortest_path(self,k):
        return self.each_request_real_paths
    def load_virtual_paths(self):
        
        return self.each_request_virtual_paths

    
    


# In[ ]:


# selected_storage_nodes = []
# selected_storage_pairs = []
# nodes = [1,2,3,4,5,6,10,11,12,7,8,9]
# network = Network("topology_file_path")
# network.get_each_user_pair_real_paths(network.user_pairs)
# # nx.draw(network.g,with_labels=True)
# # plt.show()
# work_load = Work_load(network.user_pairs)
# for num_of_storages in range(1,2):
#     path_counter_id = 0
#     print("for number of storages round  ",num_of_storages)
#     """select and add new storage pairs"""
#     new_storage_nodes,new_storage_pairs = network.get_new_storage_pairs(num_of_storages)
#     network.get_each_user_pair_real_paths(network.storage_pairs)
#     for pair in network.storage_pairs:
#         for time in work_load.T:
#             work_load.each_t_each_request_demand[time][pair] = 0
#     """we add a new virtual link to the graph"""
# #     for new_pair in new_storage_pairs:
# #         print(new_pair[0],new_pair[1])
# #         network.g.add_edge(new_pair[0],new_pair[1],weight=0)
        
#     each_user_pair_real_paths = {}
#     each_user_pair_virtual_paths = {}
#     """with new storage pairs, we will check the solution for each number of paths(real and virtual)"""
#     for num_paths in range(1,10):
        
#         """first we add the real paths between storage pairs"""
        
#         print("for path number ",num_paths)
#         for storage_pair in network.storage_pairs:
#             paths = network.get_real_path(storage_pair,num_paths)
#             for path in paths:
#                 network.set_of_paths[path_counter_id] = path
#                 try:
#                     network.each_request_real_paths[storage_pair].append(path_counter_id)
#                 except:
#                     network.each_request_real_paths[storage_pair]=[path_counter_id]
#                 path_counter_id+=1
#                 try:
#                     network.each_user_pair_real_paths[storage_pair].append(path)
#                 except:
#                     network.each_user_pair_real_paths[storage_pair]=[path]
#             print("for new storage pair we got real paths and it is")
#             print(network.each_user_pair_real_paths[storage_pair])
#         for user_pair in network.user_pairs:
#             for storage_pair in network.storage_pairs:
#                 """add one new path to the previous paths"""
#                 paths = network.get_real_path(user_pair,num_paths)
#                 for path in paths:
#                     network.set_of_paths[path_counter_id] = path
#                     try:
#                         network.each_request_real_paths[user_pair].append(path_counter_id)
#                     except:
#                         network.each_request_real_paths[user_pair]=[path_counter_id]
#                     path_counter_id+=1
#                     try:
#                         network.each_user_pair_real_paths[user_pair].append(path)
#                     except:
#                         network.each_user_pair_real_paths[user_pair]=[path]
#                 print("for user pair  we got real paths and it is",user_pair)
#                 print(network.each_user_pair_real_paths[user_pair])
#                 for real_sub_path in network.each_user_pair_real_paths[storage_pair]:
#                     #for edge in real_sub_path:
#                         #network.g.remove_edge(edge[0],edge[1])
#                     #network.g.add_edge(storage_pair[0],storage_pair[1],weight=0)
#                     print("we are going to add a virtual path for user pair %s that includes %s"%(user_pair,real_sub_path))
#                     paths = network.get_paths_to_connect_users_to_storage(user_pair,real_sub_path,num_paths)
                    
#                     print(paths)
#                     for path in paths:
#                         network.set_of_paths[path_counter_id] = path
#                         try:
#                             network.each_request_virtual_paths[user_pair].append(path_counter_id)
#                         except:
#                             network.each_request_virtual_paths[user_pair]=[path_counter_id]
#                         path_counter_id+=1
                        
#                         try:
#                             network.each_user_pair_virtual_paths[user_pair].append(path)
#                         except:
#                             network.each_user_pair_virtual_paths[user_pair]=[path]
#                     for pair in network.storage_pairs:
#                         network.each_request_virtual_paths[pair]=[]
#                     #network.get_virtual_path(user_pair,storage_pair,real_sub_path)
#                     #print("for user pair %s to storage pair %s we got real paths and it is:"%(user_pair,storage_pair))
#                     #print(network.each_user_pair_virtual_paths[user_pair])
                
                
                
#                 """solve the optimization"""
                
                


# In[ ]:


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


# In[ ]:


# # Python3 program to find shortest path
# # with exactly k edges

# # Define number of vertices in the graph
# # and infinite value

# # A naive recursive function to count
# # walks from u to v with k edges
# def shortestPath(graph, u, v, k):
    
#     V = 4
#     INF = 999999999999

#     # Base cases
#     if k == 0 and u == v:
#         return 0
#     if k == 1 and graph[u][v] != INF:
#         print(graph[u][v],(u,v))
#         return graph[u][v],(u,v)
#     if k <= 0:
#         return INF

#     # Initialize result
#     res = INF

#     # Go to all adjacents of u and recur
#     for i in range(V):
#         if graph[u][i] != INF and u != i and v != i:
#             rec_res,edge = shortestPath(graph, i, v, k - 1)
#             if rec_res != INF:
#                 res = min(res, graph[u][i] + rec_res)
#                 print(res,edge)
#     return res

#     # Driver Code
# if __name__ == '__main__':
#     INF = 999999999999

#     # Let us create the graph shown
#     # in above diagram
#     graph = [[0, 8, 3, 2],
#             [INF, 0, INF, 1],
#             [INF, INF, 0, 6],
#             [INF, INF, INF, 0]]
#     u = 0
#     v = 3
#     k = 2
#     print("Weight of the shortest path is",
#             shortestPath(graph, u, v, k))

#     # This code is contributed by PranchalK


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:







# In[ ]:


# import networkx as nx
# import matplotlib.pyplot as plt
# g = nx.Graph()
# g.add_edge(1,2,weight=1)
# g.add_edge(2,3,weight=1)
# g.add_edge(3,4,weight=2)
# g.add_edge(4,5,weight=1)
# g.add_edge(5,6,weight=1)
# g.add_edge(2,10,weight=1)
# g.add_edge(10,11,weight=1)
# g.add_edge(11,12,weight=1)
# g.add_edge(12,5,weight=1)
# g.add_edge(2,7,weight=1)
# g.add_edge(7,8,weight=1)
# g.add_edge(8,9,weight=1)
# g.add_edge(9,5,weight=1)
# shortest_paths = nx.all_shortest_paths(g,source=1,target=6, weight='weight')

# for path in shortest_paths:
#     node_indx = 0
#     path_edges = []
#     for node_indx in range(len(path)-1):
#         path_edges.append((path[node_indx],path[node_indx+1]))
#         node_indx+=1
#     print(path_edges)

# import pdb
# pdb.set_trace()
# nx.draw(g,with_labels=True)
# plt.show()
# user_pairs = [(1,6),(2,5),(10,12)]
# selected_paths = {}
# selected_storage_nodes = []
# nodes = [1,2,3,4,5,6,10,11,12,7,8,9]
# for number_of_storages in range(2,10):
#     storage1 = nodes[randint(0,len(nodes)-1)]
#     if selected_storage_nodes:
#         if storage1 not in selected_storage_nodes:
#             for storage_node in selected_storage_nodes:
#                 new_pairs.append(storage1,storage_node)
#         selected_storage_nodes.extend(new_pairs)
#     else:
#         storage2 = storage1
#         while(storage1==storage2):
#             storage2 = nodes[randint(0,len(nodes)-1)]
#         selected_storage_nodes.append((storage1,storage2))
#     print("this is our first storage pair",selected_storage_nodes)
#     for k in range(int(nx.average_shortest_path_length(g)),10):
#         at_least_one_new_path = False
#         for user_pair in user_pairs:
#             if nx.has_path(g, user_pair[0], user_pair[1]):
#                 shortest_paths = nx.all_shortest_paths(g,source=user_pair[0],target=user_pair[1], weight='weight')
#                 path_selecion_flag = False
#                 path_counter = 0
#                 for path in shortest_paths:
#                     if not path_selecion_flag:
#                         try:
#                             if path not in selected_paths[user_pair]:
#                                 print("for k %s user pair %s we have path %s"%(k,user_pair,path))
#                                 if not at_least_one_new_path:
#                                     at_least_one_new_path = True
#                                 selected_paths[user_pair].append(path)
#                                 path_selecion_flag = True
#                         except:
#                             selected_paths[user_pair]=[path]
#                             path_selecion_flag = True
#                             if not at_least_one_new_path:
#                                 at_least_one_new_path = True
#                             print("for k %s user pair %s we have path %s"%(k,user_pair,path))
#                 if not path_selecion_flag:
#                     print("for k %s user pair %s we have path %s"%(k,user_pair,path))
#         if at_least_one_new_path:
#             print("do the rest of the optimization")
#         else:
#             print("better stop becasue no new paths")


