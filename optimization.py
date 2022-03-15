#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import docplex.mp.model as cpx


# In[ ]:


def get_max_edge_capacity():
    return 12
def check_path_include_edge(edge,path):
    if edge in Paths[path]:
        return 1
    elif edge not  in Paths[path]:
        return 0
def check_request_has_path(k,p):
    if p in P[k]:
        return 1
    elif p not in P[k]:
        return 0
def get_f_value(p,n_variable):
    if n_variable == 4:
        return 0.9
    return 0.8
    


# In[ ]:


"""input parameters"""

T = [0,1]
"""request pairs at each t"""
K = [0,1] #0 ==(1,5), 1 == (2,4)


"""demand for each t"""
D = {0:{0 : 4},1:{0:6}}

"""summation of demands at each t"""
D_values = {0:4,1:6}

K_values = {0:1,1:1}

"""capacity of each edge"""
C = {0:8,1:9,2:6,3:12}


"""set of edges"""
set_E = [0,1,2,3]

"""set of paths"""
Paths= {0:[0,1,2,3],1:[1,2]}

# the lenght of each path
Paths_L = {0:4,1:3}

"""set of paths for each request pair"""
P = {0:[0],1:[1]}

"""the fixed purification values"""
N= {1:{1:0.8,2:.84,3:0.86,4:.88,5:.89,6:.9},
    2:{1:0.8,2:.84,3:0.86,4:.88,5:.89,6:.9},
    3:{1:0.8,2:.84,3:0.86,4:.88,5:.89,6:.9},
    4:{1:0.8,2:.84,3:0.86,4:.88,5:.89,6:.9}}


# In[ ]:


"""implement our OR model. When we want to code an optimization model,
we put a placeholder for that model (like a blank canvas), 
then add its elements (decision variables and constraints) to it."""

opt_model = cpx.Model(name="Storage problem model")


# In[ ]:





# In[ ]:





# In[ ]:


"""defining our decicion variables (that are integer)
store decision variables in Python dictionaries 
where dictionary keys are decision variables, and values are decision variable objects.
A decision variable is defined with three main properties: 
its type (continuous, binary or integer), 
its lower bound (0 by default), and 
its upper bound (infinity by default)"""

w_vars  = {(t,k,p): opt_model.integer_var(lb=0, ub= 12,
                              name="w_{0}_{1}_{2}".format(t,k,p)) for t in T for k in K for p in P}

n_vars  = {(t,k,p): opt_model.integer_var(lb=1, ub= 21,
                                          name="n_{0}_{1}_{2}".format(t,k,p)) for t in T for k in K for p in P}


# In[ ]:



    


# In[ ]:





# In[ ]:


"""set constraints. 
Any constraint has three parts: a left-hand side (normally a linear combination of decision variables),
a right-hand side (usually a numeric value), and
a sense (Less than or equal, Equal, or Greater than or equal).
To set up any constraints, we need to set each part:"""

for t in T:
    for e in set_E:
        opt_model.add_constraint(opt_model.sum(w_vars[t,k,p] * check_path_include_edge(e,p) * n_vars[t,k,p] for k in K for p in P) <= C[e])

for t in T:
    for k in K:
        opt_model.add_constraint(opt_model.sum(w_vars[t,k,p] * check_request_has_path(k,p) for p in P) <= D_values[t])


# In[ ]:


"""defining an objective, which is a linear expression"""

objective = opt_model.sum((w_vars[t,k,p]* (0.8 + (n_vars[t,k,p]-1)*0.01) for t in T for k in K for p in P))

# for maximization
opt_model.maximize(objective)


print('done')


# In[ ]:





# In[ ]:


"""we call the solver to solve our optimization model."""
# solving with local cplex
opt_model.solve()

# solving with cplex cloud
# opt_model.solve(url="your_cplex_cloud_url", key="your_api_key")


# In[ ]:





# In[ ]:


"""get results and post-process them
If the problem is solved to optimality, we can get and process results as follows:
"""
import pandas as pd
opt_df = pd.DataFrame.from_dict(w_vars, orient="index", 
                                columns = ["variable_object"])
opt_df.index =  pd.MultiIndex.from_tuples(opt_df.index, 
                               names=["column_t", "column_k","column_p"])
opt_df.reset_index(inplace=True)

opt_df["solution_value"] =  opt_df["variable_object"].apply(lambda item: item.solution_value)
    
opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("./optimization_solution.csv")


# In[ ]:


import pandas as pd
opt_df = pd.DataFrame.from_dict(n_vars, orient="index", 
                                columns = ["variable_object"])
opt_df.index =  pd.MultiIndex.from_tuples(opt_df.index, 
                               names=["column_t", "column_k","column_p"])
opt_df.reset_index(inplace=True)

opt_df["solution_value"] =  opt_df["variable_object"].apply(lambda item: item.solution_value)
    
opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("./optimization_solution_n_vars.csv")


# In[ ]:




