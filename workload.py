#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tmgen.models import uniform_tm,spike_tm,modulated_gravity_tm,random_gravity_tm,gravity_tm,exp_tm
import csv
import os
import random


# In[ ]:


class Work_load(object):
    def __init__(self,number_of_time_slots,file_result_path):
        self.T = []
        self.num_requests = 2
        
        self.each_t_requests = {0:[(1,6),(2,5),(10,12)],1:[(1,6),(2,5),(10,12)],2:[(1,6),(2,5),(10,12)]}
        self.each_t_real_requests = {1:[(1,6)],2:[(1,6)]}
        self.time_intervals = 2
        self.each_t_each_request_demand = {0:{(1,6):10,(2,5):0,(10,12):0},
                                           1:{(1,6):1,(2,5):0,(10,12):0},2:{(1,6):10,(2,5):0,(10,12):0}}
        self.each_request_threshold= {(1,6):{0:0.9,1:0.8,2:0.9},
                                     (2,5):{0:0.3,1:0.3,2:0.3},
                                     (10,12):{0:0.3,1:0.3,2:0.3}
                                     }
        self.each_user_request_fidelity_threshold = {(1,6):0.8,(2,10):0.9,(4,8):0.8,(6,11):0.9,
                                                          (5,10):0.8,(3,9):0.9,(8,10):0.8,(0,3):0.9,(1,10):1.0,(2,5):0.9}
        self.each_t_requests = {}
        self.each_t_real_requests = {}
        self.time_intervals = 2

        self.each_request_threshold= {}
        self.each_user_each_t_weight = {}
        
        for time in range(number_of_time_slots):
            if time not in self.T:
                self.T.append(time)
    def reset_variables(self):
        self.each_t_requests = {}
        self.each_t_real_requests = {}
    def set_each_user_weight_over_time(self,each_t_user_pairs):
        for t,user_pairs in each_t_user_pairs.items():
            for k in user_pairs:
                random_weight = random.uniform(0, 1)
                try:
                    self.each_user_each_t_weight[k][t] = random_weight
                except:
                    self.each_user_each_t_weight[k]= {}
                    self.each_user_each_t_weight[k][t] = random_weight
    def get_each_user_weight_over_time(self,k,t):
        return self.each_user_each_t_weight[k][t]
    def set_each_time_requests(self,each_t_user_pairs,storage_pairs):
        for t,user_pairs in each_t_user_pairs.items():
            for pair in user_pairs:
                try:
                    if pair not in self.each_t_requests[t]:
                        try:
                            self.each_t_requests[t].append(pair)
                        except:
                            self.each_t_requests[t] = [pair]
                except:
                    self.each_t_requests[t] = [pair]
            for pair in storage_pairs:
                try:
                    if pair not in self.each_t_requests[t]:
                        try:
                            self.each_t_requests[t].append(pair)
                        except:
                            self.each_t_requests[t] = [pair]
                except:
                    self.each_t_requests[t] = [pair]
                    
    def set_each_time_real_requests(self,each_t_user_pairs):
        for t,user_pairs in each_t_user_pairs.items():
            for pair in user_pairs:
                try:
                    if pair not in self.each_t_real_requests[t]:
                        try:
                            self.each_t_real_requests[t].append(pair)
                        except:
                            self.each_t_real_requests[t] = [pair]
                except:
                    self.each_t_real_requests[t] = [pair]
    def set_each_testing_user_pair_demands(self,number_of_time_slots,each_t_user_pairs,spike_mean,num_spikes):
        self.each_t_each_request_demand = {}
        num_of_pairs= len(list(each_t_user_pairs[0]))
        #print(num_of_pairs,num_spikes,spike_mean,number_of_time_slots)
        tm = spike_tm(num_of_pairs+1,num_spikes,spike_mean,number_of_time_slots)
#         for time in range(number_of_time_slots):
#             traffic = tm.at_time(time)
#             printed_pairs = []
#             user_indx = 0
#             for i in range(num_of_pairs+1):
#                 for j in range(num_of_pairs+1):
#                     if i!=j:
#                         if (i,j) not in printed_pairs and (j,i) not in printed_pairs:
#                             printed_pairs.append((i,j))
#                             printed_pairs.append((j,i))
#                             #print("time %s traffic from %s to %s is %s"%(time,i,j,traffic[i][j]))
#                             request = each_t_user_pairs[time][user_indx]
#                             user_indx+=1
#                             demand = max(1,traffic[i][j])
#                             try:
#                                 self.each_t_each_request_demand[time][request] = demand
#                             except:
#                                 self.each_t_each_request_demand[time] = {}
#                                 self.each_t_each_request_demand[time][request] = demand
                                
        for time in range(0,number_of_time_slots):
            each_pair_demand = {}
            if time%2==0:
                for user_pair in each_t_user_pairs[time]:
                    demand  = random.randint(1, 1)
                    each_pair_demand[user_pair] = demand
            else:
                for user_pair in each_t_user_pairs[time]:
                    demand  = random.randint(1, 1)
                    each_pair_demand[user_pair] = demand
            if time==number_of_time_slots-1:
                for user_pair in each_t_user_pairs[time]:
                    demand  = random.randint(60, 60)
                    each_pair_demand[user_pair] = demand
#             each_pair_demand[user_pairs[0]] = demand1
#             each_pair_demand[user_pairs[1]] = demand2
            for request in each_t_user_pairs[time]:
                demand =each_pair_demand[request]
                try:
                    self.each_t_each_request_demand[time][request] = demand
                except:
                    self.each_t_each_request_demand[time] = {}
                    self.each_t_each_request_demand[time][request] = demand
                
                
        for request in each_t_user_pairs[time]:
            try:
                self.each_t_each_request_demand[0][request] = 0
            except:
                self.each_t_each_request_demand[0]={}
                self.each_t_each_request_demand[0][request] = 0
    def set_each_user_pair_demands_online(self,number_of_time_slots,given_each_t_each_pair_demands):
        #self.each_t_each_request_demand = {}
        for time,request_demand in given_each_t_each_pair_demands.items():
            for request,demand in request_demand.items():
                try:
                    self.each_t_each_request_demand[time][request] = given_each_t_each_pair_demands[time][request]
                except:
                    self.each_t_each_request_demand[time] = {}
                    self.each_t_each_request_demand[time][request] = given_each_t_each_pair_demands[time][request]
                                
            for request in given_each_t_each_pair_demands[time]:
                try:
                    self.each_t_each_request_demand[0][request] = 0
                except:
                    self.each_t_each_request_demand[0]={}
                    self.each_t_each_request_demand[0][request] = 0
    def set_each_user_pair_demands(self,number_of_time_slots,each_t_user_pairs,spike_mean,num_spikes):
        self.each_t_each_request_demand = {}
        num_of_pairs= len(list(each_t_user_pairs[0]))
        print(num_of_pairs,num_spikes,spike_mean,number_of_time_slots)
        tm = spike_tm(num_of_pairs+1,num_spikes,spike_mean,number_of_time_slots)
        for time in range(number_of_time_slots):
            traffic = tm.at_time(time)
            printed_pairs = []
            user_indx = 0
            for i in range(num_of_pairs):
                for j in range(num_of_pairs):
                    if i!=j:
                        if (i,j) not in printed_pairs and (j,i) not in printed_pairs:
                            printed_pairs.append((i,j))
                            printed_pairs.append((j,i))
#                             print("num_of_pairs %s time %s traffic from %s to %s is %s and user_indx %s"%(num_of_pairs, time,i,j,traffic[i][j],user_indx))
                            request = each_t_user_pairs[time][user_indx]
                            user_indx+=1
                            demand = max(1,traffic[i][j])
                            try:
                                self.each_t_each_request_demand[time][request] = demand
                            except:
                                self.each_t_each_request_demand[time] = {}
                                self.each_t_each_request_demand[time][request] = demand
                                
#         for time in range(0,number_of_time_slots):
#             each_pair_demand = {}
#             if time%2==0:
#                 for user_pair in each_t_user_pairs[time]:
#                     demand  = random.randint(2, 3)
#                     each_pair_demand[user_pair] = demand
#             else:
#                 for user_pair in each_t_user_pairs[time]:
#                     demand  = random.randint(2, 3)
#                     each_pair_demand[user_pair] = demand
#             if time==number_of_time_slots-1:
#                 for user_pair in each_t_user_pairs[time]:
#                     demand  = random.randint(1000, 1500)
#                     each_pair_demand[user_pair] = demand
# #             each_pair_demand[user_pairs[0]] = demand1
# #             each_pair_demand[user_pairs[1]] = demand2
#             for request in each_t_user_pairs[time]:
#                 demand =each_pair_demand[request]
#                 try:
#                     self.each_t_each_request_demand[time][request] = demand
#                 except:
#                     self.each_t_each_request_demand[time] = {}
#                     self.each_t_each_request_demand[time][request] = demand
                
                
        for request in each_t_user_pairs[time]:
            try:
                self.each_t_each_request_demand[0][request] = 0
            except:
                self.each_t_each_request_demand[0]={}
                self.each_t_each_request_demand[0][request] = 0
#         with open(file_result_path, "r") as f:
#             reader = csv.reader(f, delimiter=",")
#             for line in (reader):
#                 time = int(line[0])
#                 request  = int(line[1])
#                 if time <15 and request <2:
                    
#                     request = each_user_id[request]
#                     demand = float(line[2])
                    
#                     if up_flag:
#                         demand = random.randint(2, 100)
#                         up_flag = False
#                     else:
#                         demand = random.randint(1, 3)
#                         up_flag  =True
#                     #print("demand is ",demand)
#                     try:
#                         self.each_t_each_request_demand[time][request] = demand
#                     except:
#                         self.each_t_each_request_demand[time] = {}
#                         self.each_t_each_request_demand[time][request] = demand
#                     if time not in self.T:
#                         self.T.append(time)
#                     try:
#                         if request not in self.each_t_requests[time]:
#                             self.each_t_requests[time].append(request)
#                     except:
#                         self.each_t_requests[time] = [request]

#                     if time >0:
#                         try:
#                             if self.each_t_real_requests[time]:
#                                 pass
#                         except:
#                             self.each_t_real_requests[time] = user_pairs
    def set_each_user_pair_demands_randomly(self,number_of_time_slots,each_t_user_pairs,spike_mean,num_spikes):
        self.each_t_each_request_demand = {}
        num_of_pairs= len(list(each_t_user_pairs[0]))
        
        for time in range(0,number_of_time_slots):
            each_pair_demand = {}
            if time%2==0:
                for user_pair in each_t_user_pairs[time]:
                    demand  = random.randint(2, 3)
                    each_pair_demand[user_pair] = demand
            else:
                for user_pair in each_t_user_pairs[time]:
                    demand  = random.randint(1, 2)
                    each_pair_demand[user_pair] = demand
            if time==number_of_time_slots-1:
                for user_pair in each_t_user_pairs[time]:
                    demand  = random.randint(200, spike_mean)
                    #demand = 1200
                    each_pair_demand[user_pair] = demand
#             each_pair_demand[user_pairs[0]] = demand1
#             each_pair_demand[user_pairs[1]] = demand2
            for request in each_t_user_pairs[time]:
                demand =each_pair_demand[request]
                try:
                    self.each_t_each_request_demand[time][request] = demand
                except:
                    self.each_t_each_request_demand[time] = {}
                    self.each_t_each_request_demand[time][request] = demand
                
                
        for request in each_t_user_pairs[time]:
            try:
                self.each_t_each_request_demand[0][request] = 0
            except:
                self.each_t_each_request_demand[0]={}
                self.each_t_each_request_demand[0][request] = 0
    def get_each_t_whole_demands(self,time,user_pairs):
        sum_demands = 0
        for user_pair in user_pairs:
            sum_demands+= self.each_t_each_request_demand[time][user_pair]
        return sum_demands
    def check_demands_per_each_time(self,each_t_user_pairs):
        for time in self.T:
            for user_pair in each_t_user_pairs[time]:
                if self.each_t_each_request_demand[time][user_pair]==0:
                    self.each_t_each_request_demand[time][user_pair] = 1.0
            
    def set_storage_pairs_as_user_pairs(self, storage_pairs):
        for time in self.T:
            for pair in storage_pairs:
                try:
                    if pair not in self.each_t_requests[time]:
                        self.each_t_requests[time].append(pair)
                except:
                    self.each_t_requests[time] =[pair]
                try:
                    self.each_t_each_request_demand[time][pair] = 0
                except:
                    self.each_t_each_request_demand[time] = {}
                    self.each_t_each_request_demand[time][pair] = 0
    def set_threshold_fidelity_for_request_pairs(self,each_t_user_pairs,storage_pairs,each_user_request_fidelity_threshold):
        higest_threshold = []
        for time,pairs in each_t_user_pairs.items():
            for pair in pairs:
                try:
                    self.each_request_threshold[pair][time]= each_user_request_fidelity_threshold[pair]
                except:
                    self.each_request_threshold[pair] = {}
                    self.each_request_threshold[pair][time] = each_user_request_fidelity_threshold[pair] 
                higest_threshold.append(each_user_request_fidelity_threshold[pair])
        for pair in storage_pairs:
            for time in self.T:
                try:
                    self.each_request_threshold[pair][time] = 0.6
                except:
                    self.each_request_threshold[pair]= {}
                    self.each_request_threshold[pair][time] = 0.6
                    
#         print("higest_threshold",max(higest_threshold))
#         import time
#         time.sleep(5)
    def get_each_request_threshold(self,k,t):
        return self.each_request_threshold[k][t]
    def generate_workload_circle(self,alpha,T,request_pairs):
        new_t_request_demands = {}
        for t,request_demand in self.each_t_each_request_demand.items():
            new_t_request_demands[t] = {}
            for req,d in request_demand.items():
                new_t_request_demands[t][req] = d*alpha
        for k,v in new_t_request_demands.items():
            self.each_t_each_request_demand[k] = v
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# def generate_demands(num_user_pairs, time_epochs):
#     each_minute_average_demand = {}
#     #for method in ["uniform","spike","exponential"]:
#     for method in ["spike"]:
#         each_minute_average_demand[method] = {}
#         each_minute_demands = {}
#         if method =="spike":
#             tm = spike_tm(num_user_pairs,2,100,time_epochs)
#         elif method =='uniform':
#             tm = uniform_tm(num_user_pairs,1,30,time_epochs)
#         elif method =="modulated_gravity":
#             tm = modulated_gravity_tm(num_user_pairs,time_epochs,100)
#         elif method == "random_gravity":
#             tm = random_gravity_tm(num_user_pairs,20,time_epochs)
#         elif method == "gravity":
#             tm = 1
#         elif method == "exponential":
#             tm = exp_tm(num_user_pairs,10,time_epochs)
#         print(tm)
#         for time in range(time_epochs):
#             traffic = tm.at_time(time)
#             print('for time %s we have traffic %s'%(time,traffic))
#             for demands in traffic:
#                 print('demands',demands)
#                 sum_demands= 0
#                 user_pair_indx = 0
#                 for demand in demands:
#                     print('demand',demand)
# #                     if not os.path.exists(time_demands_file):
# #                         os.mknod(time_demands_file)
#                     with open(time_demands_file, 'a') as newFile:                                
#                         newFileWriter = csv.writer(newFile)
#                         newFileWriter.writerow([user_pair_indx,time,demand]) 
#                     user_pair_indx+=1

#     return each_minute_average_demand
# time_demands_file = 'time_demands_file.csv'
# generate_demands(2,2)
# print("done!")


# In[ ]:


# tm = spike_tm(3,2,100,2)
# print(tm)


# In[ ]:


# #for time in [0,1]:
#     #traffic_time = tm.at_time(time) 
#     #print(traffic_time)
# time_demands_file = 'time_demands_file.csv'
# each_pair_src_dst = {(0,0):0,(0,1):1,(0,2):2,(0,3):3,(0,4):4,(0,5):5}
# pairs = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)]
# tm = spike_tm(6,3,100,120)
# for pair in pairs:
#     traffic_over_times = tm.between(pair[0],pair[1],'all')
#     for time in range(120):
#         #print("at time %s from %s we have %s"%(time, each_pair_src_dst[pair],traffic_over_times[time]))
#         with open(time_demands_file, 'a') as newFile:                                
#             newFileWriter = csv.writer(newFile)
#             newFileWriter.writerow([time,each_pair_src_dst[pair],traffic_over_times[time]])


# In[ ]:


# from tmgen.models import uniform_tm
# tm = uniform_tm(3, 100, 300)
# print(tm) 


# In[ ]:


# from tmgen.models import exp_tm
# tm = exp_tm(3, 500, 2)


# In[ ]:


# tm.matrix


# In[ ]:


# tm.at_time(0) 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




