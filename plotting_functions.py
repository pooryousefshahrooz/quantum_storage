#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[7]:


import numpy
import matplotlib.pyplot as plt

#import globalsvariables
import glob
import os
import datetime
import calendar
import glob, os
import itertools
from collections import OrderedDict
import sys
import csv
import numpy as np

from collections import OrderedDict
import numpy
colors = ['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','LIME','GREEN','AQUA','TEAL']

import numpy as np
from pylab import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import glob
import os
import datetime
import calendar
import glob, os
import itertools
from collections import OrderedDict
import numpy as np


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import glob
import os
import datetime

import calendar
import glob, os
import itertools
from collections import OrderedDict

import numpy as np
import numpy
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from pylab import *
import numpy as np

import matplotlib.pyplot as plt


from collections import OrderedDict
import numpy
colors = ['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','AQUA','LIME','GREEN','TEAL']
markers=['3','4','8','s','p','P','o','v','^','<','*','h','H','+','x','X','D','d','|','_']
import numpy as np

global_font_size = 32
figure_width = 10
figure_highth = 10

space_from_x_y_axis = 25
style=itertools.cycle(["-","--","-.",":","None",""," ","-","--","-.",":"])




markers=['4','<','8','s','p','P','o','v','^','<','*','h','H','+','x','X','D','d','|','_']
descriptions=['point', 'pixel', 'circle', 'triangle_down', 'tri_down', 'octagon', 'square', 'pentagon', 'plus (filled)','star', 'hexagon1', 'hexagon2', 'plus', 'x', 'x (filled)','diamond', 'thin_diamond', 'vline', 'hline']
csfont = {'fontname':'Times New Roman'}
import statistics
from pylab import *


# In[2]:


def get_arrs(x_values,my_dictionary):
    import csv
    summation = 0
    for key,value in my_dictionary.items():
        summation  = summation +(value)
    arrs= []
    import os
    cum=0.0
    for i in x_values:
        cum = cum + my_dictionary[i]
        
        
        arrs.append(float(cum)/float(summation))


    return arrs


# In[3]:


def messages_in_human_redable(messages_in_last):
    messages_in_hr = []
    
    for num in messages_in_last:
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        hr_format =  '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
        messages_in_hr.append(hr_format)
    return messages_in_hr


# In[ ]:


# table_sizes_dictionary={}
# table_sizes_dictionary = {'1k':{'Routing table checking \n by root router':0.0007,'Path exploration':0.0001},
#                           '5k':{'Routing table checking \n by root router':0.01,'Path exploration':0.008},
#                           '15k':{'Routing table checking \n by root router':0.067,'Path exploration':0.009},
#                           '20k':{'Routing table checking \n by root router':0.187,'Path exploration':0.08},
#                           '25k':{'Routing table checking \n by root router':0.332,'Path exploration':0.18},
#                           '30k':{'Routing table checking \n by root router':0.5,'Path exploration':0.3},
#                           '80k':{'Routing table checking \n by root router':1.2,'Path exploration':0.8},
#                           '130k':{'Routing table checking \n by root router':2.7,'Path exploration':1.4}
#                          }
# cross_all_topologies_table_sizes = ['1k','5k','15k','20k','25k','30k','80k','130k']
# print ('cross_all_topologies_table_sizes',cross_all_topologies_table_sizes)
# plot_bar_chart('Root router routing table size','Time(sec)',table_sizes_dictionary,['Routing table checking \n by root router','Path exploration'],cross_all_topologies_table_sizes,'plots_for_delay/table_size_delay_convergence_time_cross_all.pdf',False)


# In[ ]:





# In[72]:


def set_plotting_global_attributes(x_axis_label,y_axis_label):
    import matplotlib.pyplot as plt
    global global_font_size
    global figure_width
    global figure_highth
    global space_from_x_y_axis
    global style
    global markers
    global csfont
    global descriptions
    font_size = 44
    plt.figure(figsize=(8,8))
    global fig
    global global_mark_every
    global_mark_every = 1
    #matplotlib.rcParams['text.usetex'] = True
    fig = plt.figure()
    fig.set_size_inches(16, 8, forward=True)
    global style
    #matplotlib.rcParams['text.usetex'] = True
    global markers
    
    global descriptions

    label_size = 40
    #matplotlib.rcParams['text.usetex'] = True
    csfont = {'fontname':'Times New Roman'}
    #write your code related to basemap here
    #plt.title('title',**csfont)
    plt.rcParams['xtick.labelsize'] = label_size 
    #matplotlib.rcParams['text.usetex'] = True
    plt.rcParams['ytick.labelsize']= label_size
    #matplotlib.rcParams['text.usetex'] = True
    plt.xlabel(x_axis_label, fontsize=40,labelpad=15)
    #matplotlib.rcParams['text.usetex'] = True
    plt.ylabel(y_axis_label,fontsize=40,labelpad=15)
    plt.grid(True)
    plt.tight_layout()
    #matplotlib.rcParams['text.usetex'] = True
    #plt.ylim(ymin=0) 
    return plt
    



    
def plot_bar_chart(x_axis_label,y_axis_label,cdf_info_dictionary_over_multi_item,rows_keys,x_axis_values,plot_name,human_readable_format):
#     cdf_info_dictionary_over_multi_item= {20:{'before_path_exploration':60,'path_exploration':40},
#                                          60:{'before_path_exploration':60,'path_exploration':40},
#                                          180:{'before_path_exploration':60,'path_exploration':40},
#                                          540:{'before_path_exploration':60,'path_exploration':40},
#                                          1620:{'before_path_exploration':60,'path_exploration':40}}
    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    #print 'cdf_info_dictionary_over_multi_item',cdf_info_dictionary_over_multi_item
    x_vector = []
    header = []
    each_row_values = {}
    for topology in x_axis_values:
        for row in rows_keys:
            #print 'topology,row',topology,row
            percentage = cdf_info_dictionary_over_multi_item[topology][row]
            if (topology) not in x_vector:
                x_vector.append((topology))
            if row not in header:
                header.append(row)
            try:
                each_row_values[row].append(percentage)
            except:
                each_row_values[row]=[percentage]
                
    
    #print 'each_row_values',each_row_values
#     x_vector = ['typos_using_old_tlds','typos_using_new_tlds','typos_using_old_ammended']

#     header = ['same_owner','different_owner']
#     same_values = [len(set(same_registrar_for_typos_old)),len(set(same_registrar_for_typos_new)),len(set(same_registrar_for_typos_old_ammended))]
#     dif_values = [len(set(dif_registrar_for_typos_old)),len(set(dif_registrar_for_typos_new)),len(set(dif_registrar_for_typos_old_ammended))]


    dataset= [x_vector,each_row_values[rows_keys[0]],each_row_values[rows_keys[1]]]
#     print '=====================',dataset
#     print 'x_vector(should be topologies)',x_vector
#     print 'header(be delay and path exploration)',header
#     print 'length of items ',len(x_vector),len(each_row_values[rows_keys[0]]),len(each_row_values[rows_keys[1]])
    dataset = np.array(dataset, dtype=object)
    X_AXIS = dataset[0]
    #print '2header(be delay and path exploration)',header
    global global_font_size
    #print '3header(be delay and path exploration)',header
    fig = matplotlib.pyplot.gcf()
    configs = dataset[0]
    #print '4header(be delay and path exploration)',header
    N = len(configs)
    #print '5header(be delay and path exploration)',header
    ind = np.arange(N)
    #print '6header(be delay and path exploration)',header
    width = 0.2
    width = 0.2
    bar_width = 0.2
    #print '7header(be delay and path exploration)',header

    #print '8header(be delay and path exploration)',header
    # Save figure
    plt.xticks(rotation=90)
    p1 = plt.bar(ind, dataset[1], width, color='blue')
    p2 = plt.bar(ind, dataset[2], width, bottom=dataset[1], color='red')
    plt.xticks(ind, X_AXIS, fontsize=global_font_size)
    #print '9header(be delay and path exploration)',header
    #plt.tight_layout()
    plt.xticks(rotation=90)
    if human_readable_format:
        new_ticks = messages_in_human_redable(x_vector)
        plt.xticks(x_vector, new_ticks,fontsize=28)
    #print '10header(be delay and path exploration)',header
    plt.legend((p1[0], p2[0]), (header[0], header[1]), fontsize=global_font_size, ncol=4, framealpha=0, fancybox=True)
    plt.savefig(plot_name, format='pdf', dpi=1200)
    #print '11header(be delay and path exploration)',header
    plt.show()
    

        
    
    
    
    
def min_max_mean_median_plot(x_axis_label,y_axis_label,x_values,convergence_times,log_or_not,plot_name):

    try:
        compresson_factors = []
        average_Convergence_times = []
        plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
        labels = []
        labels.append(' ')
        list_of_list = []
        color_index = 0
        colors = ['black','red','blue','green']
        index = 0
        import numpy as np
        x = np.arange(len(x_values))+1
        for each_rho_value in x_values:
            
            
            convergences = convergence_times[each_rho_value]
            my_list_of_convergences = []
            for item in convergences:
                my_list_of_convergences.append(float(item))
            #print my_list_of_convergences
            #print sum(my_list_of_convergences)
            #print sum(my_list_of_convergences) / len(my_list_of_convergences)
            
            average_Convergence_times.append(sum(my_list_of_convergences)/len(my_list_of_convergences))
            compresson_factors.append(each_rho_value)
            labels.append(str(each_rho_value))
            costs = []
            import math
            from math import log
            for item in convergences:
                if log_or_not == 'log':
                    costs.append(log(item)/log(2))
                else:
                    costs.append(float(item))
            #print 'this should  not have negative values' ,  costs
            costs = tuple(costs)
            list_of_list.append(costs)
        #plt.xlabel('concurrency rate', fontsize=26)
        #plt.ylabel('Convergence time(s)',fontsize=26)
        #print list_of_list
        
        import numpy as np
        positions = np.arange(len(list_of_list)) + 1
        plt.boxplot([item for item in list_of_list], positions=positions,showmeans=True)
        
        #plt.plot(compresson_factors, average_Convergence_times,color=colors[color_index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20)
        plt.plot(x, average_Convergence_times,color="black",marker=markers[0],linewidth=4.0,markersize=20)
         
        index = index +1
        
        color_index = color_index +1
        xy = np.arange(len(labels))
        new_ticks = [ str(x) for x in labels]
        plt.xticks(xy, new_ticks,fontsize=34)
        axes = plt.gca()
        
#         axes.set_ylim([0,1])

        plt.savefig(plot_name)
    except ValueError:
        print (ValueError)

def scatter_plot_with_correlation_line(plt,x, y, graph_filepath,human_readable_format):

    # Scatter plot
    plt.scatter(x, y)
    
    # Add correlation line
    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0],axes.get_xlim()[1],100)
    plt.plot(X_plot, m*X_plot + b, '-',color = 'black')
    if human_readable_format:
        new_ticks = messages_in_human_redable(x)
        plt.xticks(x, new_ticks,fontsize=28)
    # Save figure
    plt.xticks(rotation=90)
    plt.savefig(graph_filepath, dpi=300, format='pdf', bbox_inches='tight')

def scatter(x_axis_title,y_axis_title,y_axis_values,x_axis_values,saved_file_name,human_readable_format):
    from scipy.stats import linregress

    xtitle = x_axis_title
    
    ytitle = y_axis_title
    
    plt = set_plotting_global_attributes(xtitle,ytitle)
#     print len(convergences_in_last_detection_case),len(messages_in_last_detection_case)
#     
    g1 = (x_axis_values, numpy.array(y_axis_values))
    data = (g1)

    colors = ("black", "green",'red')
    # Create plot
    ax = fig.add_subplot(1, 1,1)
    svalue = 700
    [i.set_linewidth(3.1) for i in ax.spines.itervalues()]
    ax.scatter(x_axis_values,numpy.array(y_axis_values) , c='black',s=svalue,linewidth=2.0, marker = "+")
    new_ticks = []
    x = np.arange(len(x_axis_values))
    
    #plt.savefig(saved_file_name)
    
    scatter_plot_with_correlation_line(plt,x_axis_values,y_axis_values, saved_file_name,human_readable_format)
    
    
def scatter_with_multiple_colors(x_axis_y_axis_values_over_lines,x_axis_values_key,y_axis_values_key,x_axis_label,y_axis_label,log_scale,plot_file_name):
    data = []
    groups = []
    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    
    
    for key,edit_distance_cost_info in x_axis_y_axis_values_over_lines.items():
        x_axis_values = x_axis_y_axis_values_over_lines[key][x_axis_values_key]
        y_axis_values = x_axis_y_axis_values_over_lines[key][y_axis_values_key]
        g1 = (x_axis_values, numpy.array(y_axis_values))
        data.append(g1)
        groups.append(key)
    #g2 = (old_amended_typos_distance, numpy.array(old_amended_typos_cost))
    #g3 = (new_typos_distance, numpy.array(new_typos_cost))
    
    #data = (g1, g2,g3)
    colors = ("black", "green",'red','blue')
    #groups = ("pre-2000 gTLDs",'2000-2012 gTLDs' ,"post-2012 gTLDs") 

    # Create plot
    import random
    ax = fig.add_subplot(1, 1,1)
    #ax.set_yscale("log")
    svalue = 700
    from math import exp, expm1
    import math
    for data, color, group in zip(data, colors, groups):
        x, y = data
        #print type(x),type(y)
        #print y
        #svalue = random.randint(400,701)
        #print 'svalue',svalue
        y_tmp = []
        for item in y:
            from math import exp, expm1
            import math
            from math import log
            if log_scale:
                y_tmp.append(log(item)/log(10))
            else:
                y_tmp.append((item))
        ax.scatter(x, y_tmp, c=color,s=svalue,alpha=0.5 ,label=group)
        #print 'the values for x and y are ',x, y_tmp
        #ax.set_yscale('log')
        
        svalue = svalue -300
#     from matplotlib import rcParams
    
#     plt.grid(True)
#     rcParams.update({'figure.autolayout': True})    
#     rcParams.update({'figure.autolayout': True})
#     #label_size = 29
#     plt.rcParams['xtick.labelsize'] = label_size 
#     plt.rcParams['ytick.labelsize']=label_size
    #plt.xlabel('Edit Distance', fontsize=33,labelpad=30)
    #plt.ylabel('Price of typo candidates(log scale, base: 10)',fontsize=33,labelpad=30)
    if len(x_axis_y_axis_values_over_lines) >1:
        plt.legend(loc=5,fontsize=28)
    plt.xticks(rotation=0)
#     plt.tight_layout()
    #plt.title('scatter plot of typo registration cost based on edit distance',fontsize=25)
    plt.savefig(plot_file_name)
    
    plt.show()
    



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[5]:



def plot_multiple_line_plot(data_dictionary,x_axis_label,y_axis_label,x_axis_values,y_axis_values,plot_name,value_attached_to_line_name):
 
 colors = ['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','LIME','GREEN','AQUA','TEAL']
 style=["-","--","-.",":","-"]
 color_index = 0
 plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
 
 my_dic = {}
 my_class_labels = []
 x = np.arange(len(x_axis_values))
 sizes = []
 index = 0
 
 for y_axis_value in y_axis_values:
     
     values = []
     for x_axis_value in x_axis_values:
         
         try:
             values.append(data_dictionary[y_axis_value][x_axis_value])
         except:
             pass
     
     if value_attached_to_line_name:
         sizes.append(str(value_attached_to_line_name)+' '+str(y_axis_value))
     else:
         sizes.append(str(y_axis_value))
     #print x_axis_values,values
     plt.plot(x_axis_values, values,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20)
     index = index +1
     color_index = color_index +1
 my_class_labels = sizes
 #plt.xlabel('MRAI (sec)', fontsize=34,labelpad=34)
 #plt.ylabel('Convergence Time (sec)',fontsize=34,labelpad=34)
 plt.grid(True)
#     plt.tight_layout()
 #plt.ylim(ymin=0) 
 plt.xlim(xmin=0) 
 new_ticks = [ str(y) for y in x_axis_values]
 #plt.xticks(x, new_ticks,fontsize=34)
 #matplotlib.rcParams.update({'font.size': 34})
 plt.legend([label for label in new_ticks ], loc='upper left',fontsize=30)
 plt.savefig(plot_name)
 plt.show()

def plot_multiple_line_plot_log_scale_on_x_axis(data_dictionary,x_axis_label,y_axis_label,x_axis_values,y_axis_values,plot_name,value_attached_to_line_name):
 
 colors = ['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','LIME','GREEN','AQUA','TEAL']
 style=["-","--","-.",":","-"]
 color_index = 0
 plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
 
 my_dic = {}
 my_class_labels = []
 x = np.arange(len(x_axis_values))
 sizes = []
 index = 0
 
 for y_axis_value in y_axis_values:
     
     values = []
     for x_axis_value in x_axis_values:
         
         try:
             values.append(data_dictionary[y_axis_value][x_axis_value])
         except:
             pass
     
     if value_attached_to_line_name:
         sizes.append(str(value_attached_to_line_name)+' '+str(y_axis_value))
     else:
         sizes.append(str(y_axis_value))
     #print x_axis_values,values
     plt.plot(x_axis_values, values,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20)
     index = index +1
     color_index = color_index +1
 my_class_labels = sizes
 #plt.xlabel('MRAI (sec)', fontsize=34,labelpad=34)
 #plt.ylabel('Convergence Time (sec)',fontsize=34,labelpad=34)
 plt.grid(True)
#     plt.tight_layout()
 #plt.ylim(ymin=0) 
 plt.xlim(xmin=0) 
 new_ticks = [ str(y) for y in x_axis_values]
 plt.xticks(x, new_ticks,fontsize=34)
 matplotlib.rcParams.update({'font.size': 34})
 plt.legend([label for label in my_class_labels ], loc='upper left',fontsize=30)
 plt.savefig(plot_name)
 plt.show()
 

 
def plot_convergence(Convergene_time_dictionary,MRAI_VALUES4,topology_size4,x_axis_label,y_axis_label,real_expectation,convergence_messages,label,type_of_convergence,plot_name):
 #print 'Convergene_time_dictionary is',Convergene_time_dictionary
 #print 'MRAI_VALUES4,topology_size4',MRAI_VALUES4,topology_size4
 plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
 colors = ['BLACK', 'RED', 'BLUE','GREEN','MAROON','AQUA','OLIVE','LIME','TEAL']
 style=[ 'solid', 'dashed', 'dashdot', 'dotted',"-","--","-.",":",'dashed','solid', 'dashed', 'dashdot']
 color_index = 0
#     my_dic = {}
 my_dic = {}
 my_class_labels = []
 x = np.arange(len(MRAI_VALUES4))
 sizes = []
 index = 0
 #print 'Convergene_time_dictionary',Convergene_time_dictionary
 for topology_size in topology_size4:
     topology_size = str(topology_size)
     Convergence_times = []
     for mrai in MRAI_VALUES4:
         mrai = str(mrai)
         try:
             #print 'Convergene_time_dictionary[(topology_size)][mrai]',Convergene_time_dictionary[(topology_size)][mrai]
             
             Convergence_times.append(Convergene_time_dictionary[(topology_size)][int(mrai)])
         except:
             #print ValueError
             pass
     #print 'Convergence_times',Convergence_times
     sizes.append('propagation delay='+str(topology_size))
     plt.plot(x, Convergence_times,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20,markerfacecolor='blue',markeredgewidth='5', markeredgecolor='black')
     #plt.plot(x_axis_values, values,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20)

     index = index +1
     color_index = color_index +1
 my_class_labels = sizes
 #matplotlib.rcParams['text.usetex'] = True
 #plt.xlabel('MRAI (sec)', fontsize=34,labelpad=34)
 #plt.ylabel('Convergence Time (sec)',fontsize=34,labelpad=34)
 plt.grid(True)
 #matplotlib.rcParams['text.usetex'] = True
#     plt.tight_layout()
 plt.xlim([0, max(x)+0.1])
 #matplotlib.rcParams['text.usetex'] = True
 new_ticks = [ str(y) for y in MRAI_VALUES4]
 plt.xticks(x, new_ticks,fontsize=34)
 #matplotlib.rcParams.update({'font.size': 34})
 if len(my_class_labels)>1:
     plt.legend([label for label in my_class_labels ], loc='upper left',fontsize=30)
 plt.savefig(plot_name)
 #matplotlib.rcParams['text.usetex'] = True  
 plt.show()
def plot_convergence_detection_alg_overhead(x_axix_label,y_axix_label,dictionary_keys_in_order,Read_and_Detection_time_with_convergence_Det_Alg,topologies,x_axis_new_tickets,log_scale,plot_name):
 
 
 colors = ['BLACK', 'RED', 'BLUE','GREEN','MAROON','AQUA','OLIVE','LIME','TEAL']
 style=[ 'solid', 'dashed', 'dashdot', 'dotted',"-","--","-.",":",'dashed']
 plt = set_plotting_global_attributes(x_axix_label,y_axix_label)
 #print Read_and_Detection_time_with_convergence_Det_Alg
 my_dic = {}


 my_class_labels = []

 
 x = np.arange(len(topologies))
 print('we have % as our x '%(x))
 sizes = []
 #plt.gca().set_color_cycle(['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','LIME','GREEN','AQUA','TEAL'])


 #print 'Convergene_time_dictionary',Convergene_time_dictionary
 index = 0
 color_index =0
 for real_detection_algorithm in dictionary_keys_in_order:
     label_of_result = str(real_detection_algorithm)
     Convergence_times = []
     import math
     from math import log
     
     for topology in topologies:
         topology = str(topology)
#             if log_scale:
             
#                 value = log(Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)])/log(2)
             
#                 print Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)],value
#             else:
         print(label_of_result,int(topology))
         value  = Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)]
         try:
             Convergence_times.append(value)
             
         except:
             pass
     sizes.append(str(label_of_result))
     print("these are the x and y axis values",Convergence_times,label_of_result)
     plot(x, Convergence_times,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=6.0, markersize=10,markerfacecolor='black',markeredgewidth='5', markeredgecolor='blue')
     index +=1
     color_index +=1
     if color_index >=len(colors):
         color_index = 1
     if index >= len(style):
         index = 2
     
     
     
 new_x_labels = []
 for item in topologies:
     if int(item) ==50:
         new_x_labels.append(inf)
     else:
         new_x_labels.append(item)

 plt.xticks(x,new_x_labels)

 
 my_class_labels = sizes

 plt.grid(True)
 plt.ylim(ymin=0)
 plt.ylim(ymin=0)
 plt.ylim(ymin=0)
 plt.xlim(xmin=0)
 plt.tight_layout()
 new_ticks = [ str(y) for y in topologies]
 plt.xticks(x, x_axis_new_tickets,fontsize=28)
 plt.grid(True)
 plt.tight_layout()
 if log_scale:
     plt.yscale('log')
#     plt.legend([label for label in my_class_labels ], loc='upper left',fontsize=28)
 #plt.legend([label for label in my_class_labels ],fontsize=23)
 plt.legend([label for label in my_class_labels ],fontsize=25, ncol=1,handleheight=2.4, labelspacing=0.05)
 
 plt.minorticks_on()
 plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

 plt.savefig(plot_name)
 plt.show()
 

def ploting_simple_y_as_x_with_vertical_lines(x_axix_label,y_axix_label,dictionary_keys_in_order,Read_and_Detection_time_with_convergence_Det_Alg,topologies,tickets_on_x_axis,log_scale,plot_name):
 
 
 colors = ['BLACK', 'RED', 'BLUE','GREEN','MAROON','AQUA','OLIVE','LIME','TEAL']
 style=[ 'solid', 'dashed', 'dashdot', 'dotted',":",'solid', 'dashed', 'dashdot']
 plt = set_plotting_global_attributes(x_axix_label,y_axix_label)
 #print Read_and_Detection_time_with_convergence_Det_Alg
 my_dic = {}


 my_class_labels = []

 
#     x = np.arange(len(topologies))
 x = np.arange(max(topologies))
 x = []
 for point_x_axis in topologies:
     x.append(int(point_x_axis))
 x.sort()
 print('we have %s as our x '%(x))
 sizes = []
 #plt.gca().set_color_cycle(['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','LIME','GREEN','AQUA','TEAL'])

 #print 'Convergene_time_dictionary',Convergene_time_dictionary
 index = 0
 color_index =0
 for real_detection_algorithm in dictionary_keys_in_order:
     label_of_result = str(real_detection_algorithm)
     Convergence_times = []
     import math
     from math import log
     
     for topology in topologies:
         topology = str(topology)
#             if log_scale:
             
#                 value = log(Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)])/log(2)
             
#                 print Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)],value
#             else:
         print('scheme %s x_axis value %s, result for this point %s '%(real_detection_algorithm,label_of_result,int(topology)))
         value  = Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)]
         try:
             Convergence_times.append(value)
             
         except:
             pass
     sizes.append(str(label_of_result))
     print("these are the x and y axis values",Convergence_times,label_of_result)
     plot(x, Convergence_times,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=6.0, markersize=10,markerfacecolor='black',markeredgewidth='5', markeredgecolor='blue')
     
     index = index +1
     color_index+=1
     if color_index >=len(colors):
         color_index = 1
     if index >= len(style):
         index = 2
         
#         if color_index >= len(colors):
#             index = 0
     
     
 
 # x coordinates for the lines
 xcoords = [10, 30]
 # colors for the lines
 colors = ['k','r']

 for xc,c in zip(xcoords,colors):
     plt.axvline(x=xc, label='k = {}'.format(xc), c=c)
 my_class_labels = sizes

 plt.grid(True)
 plt.ylim(ymin=0)
 plt.ylim(ymin=0)
 plt.xlim(xmin=0)
 plt.tight_layout()
#     new_ticks = [ str(y) for y in topologies]
#     plt.xticks(x, new_ticks,fontsize=32)
 plt.grid(True)
#     fig, ax = plt.subplots()
#     plt.grid(which='major', linestyle='-', linewidth='0.2', color='red')

 plt.grid(which='minor', linestyle=':', linewidth='0.2', color='black')

 plt.tight_layout()
 if log_scale:
     plt.yscale('log')
#     plt.legend([label for label in my_class_labels ], loc='upper left',fontsize=28)
#     plt.legend([label for label in my_class_labels ],fontsize=23)
 plt.legend([label for label in my_class_labels ],fontsize=25, ncol=2,handleheight=2.4, labelspacing=0.05)
 
#     plt.xticks(range(0, len(tickets_on_x_axis) * 2, 2), tickets_on_x_axis)
#     plt.xlim(-2, len(tickets_on_x_axis)*2)
 #plt.ylim(0, 1)
 plt.minorticks_on()
 plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
 
 
 plt.savefig(plot_name)
 plt.show()    

def ploting_simple_y_as_x(x_axix_label,y_axix_label,x_min_value,y_axis_provided_max_value,dictionary_keys_in_order,Read_and_Detection_time_with_convergence_Det_Alg,topologies,tickets_on_x_axis,log_scale,plot_name):
 
 
 colors = ['BLACK', 'RED', 'BLUE','GREEN','MAROON','AQUA','OLIVE','LIME','TEAL']
 style=[ 'solid', 'dashed', 'dashdot', 'dotted',":",'solid', 'dashed', 'dashdot']
 plt = set_plotting_global_attributes(x_axix_label,y_axix_label)
 #print Read_and_Detection_time_with_convergence_Det_Alg
 my_dic = {}


 my_class_labels = []

 
#     x = np.arange(len(topologies))
 x = np.arange(max(topologies))
 x = []
 for point_x_axis in topologies:
     x.append((point_x_axis))
 x.sort()
 print('we have %s as our x '%(x))
 sizes = []
 #plt.gca().set_color_cycle(['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','LIME','GREEN','AQUA','TEAL'])

 #print 'Convergene_time_dictionary',Convergene_time_dictionary
 index = 0
 color_index =0
 for real_detection_algorithm in dictionary_keys_in_order:
     label_of_result = (real_detection_algorithm)
     Convergence_times = []
     import math
     from math import log
     
     for topology in topologies:
         
#             if log_scale:
             
#                 value = log(Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)])/log(2)
             
#                 print Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)],value
#             else:
         print('scheme %s x_axis value %s, result for this point  '%(label_of_result,int(topology)))
         print("Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][topology]",Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][topology])
         value  = Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][topology]
         try:
             Convergence_times.append(value)
             
         except:
             pass
     sizes.append(str(label_of_result))
     #print("these are the x and y axis values",Convergence_times,label_of_result)
     plot(x, Convergence_times,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=6.0, markersize=10,markerfacecolor='black',markeredgewidth='5', markeredgecolor='blue')
     
     index = index +1
     color_index+=1
     if color_index >=len(colors):
         color_index = 1
     if index >= len(style):
         index = 2
         
#         if color_index >= len(colors):
#             index = 0
     
     
 
 
 my_class_labels = sizes

 plt.grid(True)
 plt.ylim(ymin=0)
 plt.ylim(ymin=0)
 plt.xlim(xmin=x_min_value)
 plt.tight_layout()
#     new_ticks = [ str(y) for y in topologies]
#     plt.xticks(x, new_ticks,fontsize=32)
 plt.grid(True)
#     fig, ax = plt.subplots()
#     plt.grid(which='major', linestyle='-', linewidth='0.2', color='red')

 plt.grid(which='minor', linestyle=':', linewidth='0.2', color='black')

 plt.tight_layout()
 if log_scale:
     plt.yscale('log')
#     plt.legend([label for label in my_class_labels ], loc='upper left',fontsize=28)
#     plt.legend([label for label in my_class_labels ],fontsize=23)
 plt.legend([label for label in my_class_labels ],fontsize=27, ncol=2,handleheight=2.4, labelspacing=0.02)
 
#     plt.xticks(range(0, len(tickets_on_x_axis) * 2, 2), tickets_on_x_axis)
#     plt.xlim(-2, len(tickets_on_x_axis)*2)
 plt.ylim(0, y_axis_provided_max_value)
 plt.minorticks_on()
 plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
 
 
 plt.savefig(plot_name)
 plt.show()
 
 
def ploting_simple_lines_printed_version(x_axix_label,y_axix_label,dictionary_keys_in_order,Read_and_Detection_time_with_convergence_Det_Alg,topologies,log_scale,plot_name):
 
 
 colors = ['BLACK', 'BLACK','RED', 'BLUE','GREEN','MAROON','AQUA','OLIVE','LIME','TEAL','PURPLE','PINK','CYAN']
 style=[ 'solid','dotted','dashed',"dashdot","-.", 'dashed' ,'solid', 'dashed', 'dashdot']
 
 plt = set_plotting_global_attributes(x_axix_label,y_axix_label)
 #print Read_and_Detection_time_with_convergence_Det_Alg
 my_dic = {}


 my_class_labels = []

 
#     x = np.arange(len(topologies))
 x = np.arange(max(topologies))
 x = []
 for point_x_axis in topologies:
     x.append(int(point_x_axis))
 x.sort()
 print('we have %s as our x '%(x))
 sizes = []
 #plt.gca().set_color_cycle(['BLACK', 'RED', 'MAROON', 'YELLOW','OLIVE','LIME','GREEN','AQUA','TEAL'])


 #print 'Convergene_time_dictionary',Convergene_time_dictionary
 index = 0
 color_index =0
 for real_detection_algorithm in dictionary_keys_in_order:
     label_of_result = str(real_detection_algorithm)
     Convergence_times = []
     import math
     from math import log
     
     for topology in topologies:
         topology = str(topology)
#             if log_scale:
             
#                 value = log(Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)])/log(2)
             
#                 print Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)],value
#             else:
         print("scheme %s and x-axis value %s "%(label_of_result,int(topology)))
         value  = Read_and_Detection_time_with_convergence_Det_Alg[label_of_result][int(topology)]
         try:
             Convergence_times.append(value)
             
         except:
             pass
     sizes.append(str(label_of_result))
     print("these are the x and y axis values",Convergence_times,label_of_result)
#         plot(x, Convergence_times,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=6.0, markersize=10,markerfacecolor='black',markeredgewidth='5', markeredgecolor='blue')
     plot(x, Convergence_times,colors[color_index],linestyle=style[index],markevery=(0.0,0.1),linewidth=6.0, markersize=10,markerfacecolor='black')
     
     index = index +1
     color_index+=1
     if color_index >=len(colors):
         color_index = 1
     if index >= len(style):
         index = 2
         
#         if color_index >= len(colors):
#             index = 0
     
 
 my_class_labels = sizes

 plt.grid(True)
 plt.ylim(ymin=0)
 plt.xlim(xmin=0)
 plt.tight_layout()
#     new_ticks = [ str(y) for y in topologies]
#     plt.xticks(x, new_ticks,fontsize=32)
 plt.grid(True)
 plt.tight_layout()
 if log_scale:
     plt.yscale('log')
#     plt.legend([label for label in my_class_labels ], loc='upper left',fontsize=28)
#     plt.legend([label for label in my_class_labels ],fontsize=23)
 plt.legend([label for label in my_class_labels ],fontsize=25,ncol=1,handleheight=2.4, labelspacing=0.05)
 

 plt.savefig(plot_name)
 plt.show()    
 
def plot_simple_points_multiple_lines(x_axis_label,y_axis_label,Convergene_time_dictionary,MRAI_VALUES4,topology_size4,plot_name):

 plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
 colors = ['BLACK', 'RED', 'BLUE','GREEN','MAROON', 'YELLOW','OLIVE','LIME','AQUA','TEAL']
 style=["-","--","-.",":","-"]
 color_index = 0
#     my_dic = {}
 my_dic = {}
 my_class_labels = []
 x = np.arange(len(MRAI_VALUES4))
 sizes = []
 index = 0
 #print 'Convergene_time_dictionary',Convergene_time_dictionary
 for topology_size in topology_size4:
     topology_size = (topology_size)
     Convergence_times = []
     for mrai in MRAI_VALUES4:
         mrai = (mrai)
         try:
             #print 'Convergene_time_dictionary[(topology_size)][mrai]',Convergene_time_dictionary[(topology_size)][mrai]
             
             Convergence_times.append(Convergene_time_dictionary[(topology_size)][(mrai)])
         except:
             #print ValueError
             pass
     #print 'Convergence_times',Convergence_times
     sizes.append(str(topology_size))
     plt.plot(x, Convergence_times,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20)
     #plt.plot(x_axis_values, values,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20)

     index = index +1
     color_index = color_index +1
 my_class_labels = sizes
 #plt.xlabel('MRAI (sec)', fontsize=34,labelpad=34)
 #plt.ylabel('Convergence Time (sec)',fontsize=34,labelpad=34)
 plt.grid(True)

#     plt.tight_layout()
 plt.xlim([0, max(x)+0.1])

 new_ticks = [ str(y) for y in MRAI_VALUES4]
 plt.xticks(x, new_ticks,fontsize=34)
 #matplotlib.rcParams.update({'font.size': 34})
 plt.legend([label for label in my_class_labels ],fontsize=30)
 plt.savefig(plot_name)
 plt.show()
 


# In[6]:





# In[ ]:





# In[ ]:


# data_dictionary_MRAI_0  = {20:{0:.003,1:0.7,2:0.9,4:1.3,8:1.8,16:2.5,32:3.4},
#                            60:{0:0.008,1:1.2,2:1.7,4:2.6,8:3.2,16:4.9,32:6.4},
#                            180:{0:0.01,1:1.6,2:2.5,4:3.5,8:4.3,16:6.3,32:8.3},
#                            540:{0:0.9,1:2.1,2:3.2,4:4.3,8:5.7,16:8.6,32:10.4},
#                            1200:{0:2.02,1:3.2,2:4.2,4:5.3,8:7.4,16:9.3,32:14.6}
                                
#                    }


# # with open('circa_final_results_for_mrai_experiment.csv', "rb") as f:
# #     reader = csv.reader(f, delimiter=",")
# #     for line in (reader):
# #         data_dictionary_MRAI_0[int(line[1])][int(line[0])] = float(line[2])

# x_axis_values_mrai_1 = [0,1,2,4,8,16,32]
# prefix_set_mrai_1 = [20,60,180,540,1200]

# #plot_multiple_line_plot_log_scale_on_x_axis(data_dictionary_MRAI_0,'MRAI(sec)','Convergence time(sec)',x_axis_values_mrai_1,prefix_set_mrai_1,'convergence_time_of_topologies_mrai','# of nodes')
# plot_convergence(data_dictionary_MRAI_0,x_axis_values_mrai_1,prefix_set_mrai_1,'real','convergence_messages','last_detection','cc-last_detection')


# In[ ]:


# x_axis_y_axis_values_over_lines={'down':{'convergence':[1.1,2.02,3.5],'messages':[100,200,300]},
#                                  'up':{'convergence':[2.1,3.02,4.5],'messages':[150,270,399]}}

# x_axis_values_key = 'messages'
# y_axis_values_key = 'convergence'
# x_axis_label = 'Sent messages'
# y_axis_label = 'Convergence time'
# plot_file_name = 'plots_for_delay/up_down_event_convergence_differentiation.pdf'
# log_scale = False
# scatter_with_multiple_colors(x_axis_y_axis_values_over_lines,x_axis_values_key,y_axis_values_key,x_axis_label,y_axis_label,log_scale,plot_file_name)



# In[7]:



def plot_multiple_methods_linear(each_method_values,x_values,methods_keys,plat_name):
    #print 'Convergene_time_dictionary is',Convergene_time_dictionary
    #print 'MRAI_VALUES4,topology_size4',MRAI_VALUES4,topology_size4
    plt = set_plotting_global_attributes('MRAI (sec)','Convergence time(sec)')
    colors = ['BLACK', 'RED', 'BLUE','GREEN','MAROON', 'YELLOW','OLIVE','LIME','AQUA','TEAL']
    style=["-","--","-.",":","-"]
    color_index = 0
#     my_dic = {}
    my_dic = {}
    my_class_labels = []
    x = np.arange(len(x_values))
    sizes = []
    index = 0
    #print 'Convergene_time_dictionary',Convergene_time_dictionary
    for topology_size in methods_keys:
        topology_size = str(topology_size)
        Convergence_times = []
        for mrai in x_values:
            mrai = str(mrai)
            try:
                #print 'Convergene_time_dictionary[(topology_size)][mrai]',Convergene_time_dictionary[(topology_size)][mrai]
                
                Convergence_times.append(each_method_values[int(topology_size)][int(mrai)])
            except:
                #print ValueError
                pass
        #print 'Convergence_times',Convergence_times
        sizes.append(str(topology_size))
        print('x, Convergence_times',x, Convergence_times)
        plt.plot(x, Convergence_times,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20,markerfacecolor='blue',markeredgewidth='5', markeredgecolor='black')
        #plt.plot(x_axis_values, values,colors[color_index],linestyle=style[index],marker=markers[index],markevery=(0.0,0.1),linewidth=4.0, markersize=20)

        index = index +1
        color_index = color_index +1
    my_class_labels = sizes
    #matplotlib.rcParams['text.usetex'] = True
    #plt.xlabel('MRAI (sec)', fontsize=34,labelpad=34)
    #plt.ylabel('Convergence Time (sec)',fontsize=34,labelpad=34)
    plt.grid(True)
    #matplotlib.rcParams['text.usetex'] = True
#     plt.tight_layout()
    plt.xlim([0, max(x)+0.1])
    #matplotlib.rcParams['text.usetex'] = True
    new_ticks = [ str(y) for y in x_values]
    plt.xticks(x, new_ticks,fontsize=34)
    #matplotlib.rcParams.update({'font.size': 34})
    plt.legend([label for label in my_class_labels ], loc='upper left',fontsize=30)
    plt.savefig(plat_name)
    #matplotlib.rcParams['text.usetex'] = True  
    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[8]:



        
def multiple_lines_cdf(x_axis_label,y_axis_label,cdf_info_dictionary_over_multi_item,log,plot_name,list_of_keys,y_min_value,y_max_value):

    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    for scheme, values in cdf_info_dictionary_over_multi_item.items():
        x_axis_min_value = min(values)
        x_axis_max_value = min(values)
    for scheme, values in cdf_info_dictionary_over_multi_item.items():
        #print(scheme,min(reductions), max(reductions),reductions)
        if min(values)<x_axis_min_value:
            x_axis_min_value = min(values)
        if  max(values)>x_axis_max_value:
            x_axis_max_value =  max(values)
#     print("******* this is the x_axis_min_value ******* ",x_axis_min_value)
#     for scheme in cdf_info_dictionary_over_multi_item.keys():
#         cdf_info_dictionary_over_multi_item[scheme][x_axis_min_value-(x_axis_min_value/1000000000000)] = 0
#     print('cdf_info_dictionary_over_multi_item ',cdf_info_dictionary_over_multi_item)
    colors = ['BLACK', 'RED', 'GREEN','BLUE','MAROON','OLIVE','LIME','AQUA','TEAL','YELLOW']
    #colors = ['BLACK', 'RED','BLUE','MAROON','OLIVE','LIME','AQUA','TEAL','YELLOW']
    
    style=["-","-.",":","-","--"]
    
    index = 0
    my_class_labels = []
    items_index = 0
    line_index = 0
    max_value_on_x_axis = []
    for key in list_of_keys:
        #print key
        this_scheme_min_value_on_x_axis = 0
        for scheme, values in cdf_info_dictionary_over_multi_item.items():
            if scheme ==key:
                #print(scheme,min(reductions), max(reductions),reductions)
                if min(values)>this_scheme_min_value_on_x_axis:
                    this_scheme_min_value_on_x_axis = min(values)
                
#                 print("******* this is the x_axis_min_value of scheme  ******* ",scheme,this_scheme_min_value_on_x_axis)
#                 for scheme2 in cdf_info_dictionary_over_multi_item.keys():
#                     if scheme2 ==key:
#                 cdf_info_dictionary_over_multi_item[key][this_scheme_min_value_on_x_axis] = this_scheme_min_value_on_x_axis
        
        
        my_class_labels.append(key)
        cdf_info_dictionary = cdf_info_dictionary_over_multi_item[key]


        #     cdf_info_dictionary = {1:8,3:4,2:4,4:1}
        x_values = list(cdf_info_dictionary.keys())
        #print ('x values are ',x_values,type(x_values))
        x_values.sort()
        max_value_on_x_axis.append(max(x_values))
        #print(x_values,type(x_values))
        CDF_values = get_arrs(list(x_values),cdf_info_dictionary)
        #print ('CDF_values,x_values',key,CDF_values,x_values)
        new_x_values = []
        
        new_cdf_values = []
#         new_x_values.append(0)
        new_x_values.append(this_scheme_min_value_on_x_axis- this_scheme_min_value_on_x_axis/10000000000000000000)
        for x_value_passed in x_values:
            new_x_values.append(x_value_passed)
#         new_cdf_values.append(0)
        new_cdf_values.append(0)
        for CDF_v in CDF_values:
            new_cdf_values.append(CDF_v)
        CDF_values = new_cdf_values
        x_values = new_x_values
        items_index = items_index +1


        ymin, ymax = ylim()  # return the current ylim
        ylim((0, 1))   # set the ylim to ymin, ymax
        ylim(0, 1)     # set the ylim to ymin, ymax
        ylim(y_min_value,y_max_value)
        plt.xlim([0, max(max_value_on_x_axis)])

        plt.xlim([0, x_axis_max_value])
#         print ('key, x_values , CDF_values are',key,x_values,CDF_values)
        plt.plot(x_values, CDF_values,color=colors[index],linestyle=style[line_index],marker=markers[index],markevery=(0.0,0.1),linewidth=6.0, markersize=20,markerfacecolor='blue',markeredgewidth='5', markeredgecolor='black')
        if index == len(colors)-1:
            index = 0
        else:
            index = index +1
        
        if line_index ==len(style)-1:
            line_index = 0
        else:
            line_index = line_index +1
        #plt.plot(x_values, CDF_values,color=colors[index],linestyle=style.next(),marker=markers[index],linewidth=2.0, markersize=20)
    if len(my_class_labels)>1:
        plt.legend([label for label in my_class_labels ],fontsize=26)
    plt.savefig(plot_name)
    plt.show()


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



def simple_plot(x_data,y_data,x_axis_label,y_axis_label,plot_name,x_data2,y_data2):
    
    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    
   
    plt.plot(x_data2, y_data2,color="black",marker=markers[0],markevery=(0.0,0.1),linewidth=4.0, markersize=20)
    #plt.boxplot([item for item in list_of_list],positions=x_data,showmeans=True,widths=(0,10, 10, 10,0),meanline=True)
    
    
    plt.grid(True)
#     plt.tight_layout()
#     new_ticks = [ (y) for y in x_data]
#     plt.xticks(x_data, new_ticks,fontsize=39)
#     plt.ylim(ymin=0) 
#     plt.xlim(xmin=0) 
    plt.savefig(plot_name,bbox_inches='tight')
    plt.show()
    


# In[ ]:



# simple_plot([0,500,1500,4500,18000],[0,1,2,3],'Number of prefixes','Concurrency control \n overhead(msec)','plots/concurrency_control_overhead.pdf',[0,500,1500,4500,18000],[0,100,200,350,700])



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# cdf_info_dictionary_over_multi_item = OrderedDict()
# rho = r'$\rho$'
# list_of_keys = ['random','neighborhood','degree']

# cdf_info_dictionary_over_multi_item = {
#                                        'random':{20:20,16:30,14:20,9:10,8:10,4:4,3:4,2:2,0:0},
#     'neighborhood':{21:20,18:30,15:20,13:10,12:10,4:4,3:4,2:2,0:0},
#     'degree':{27:20,23:30,20:20,18:10,14:10,4:4,3:4,2:2,0:0}            
#                                     }
# multiple_lines_cdf('Improvement rate','cumulative fraction \n of root cause events',cdf_info_dictionary_over_multi_item,False,'plots_for_delay/CDF_on_utilization.pdf',list_of_keys)


# In[ ]:





# In[9]:


def plot_multiple_lines_different_x_axis_values(x_axis_label,y_axis_label,approach_compression_average_values,plot_name):
    import numpy as np
#     from matplotlib.pylab import plt #load plot library
    import matplotlib.pyplot as plt
    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    
    # indicate the output of plotting function is printed to the notebook
#     %matplotlib inline 
    colors = ['BLACK', 'RED', 'MAROON','BLUE','OLIVE','LIME','AQUA','GREEN','TEAL','YELLOW']
    try:
        style=["-","-.",":","-","--"]
        index = 0
        my_class_labels = []
        items_index = 0
        line_index = 0
    #     print(len(x))
        my_class_labels = []
        for approach,compression_averages in approach_compression_average_values.items():
            if approach == 'overla_related':
                approach = 'overlap_related'
            try:
                x_axis_values = compression_averages['compression_values']
                y_axis_values = compression_averages['average_values']
                print('**** these are x and y axis values ',approach,x_axis_values,y_axis_values)
        #         if 'control' in approach and 'no' not in approach:
        #             my_class_labels.append('Concurrency control')
        #         else:
        #             my_class_labels.append('No concurrency control')
                plt.plot(x_axis_values, y_axis_values)
                #ymin, ymax = ylim()  # return the current ylim
#                 ylim((0, 1))   # set the ylim to ymin, ymax
#                 ylim(0, 1)     # set the ylim to ymin, ymax
#                 #plt.xlim([0, max(x_values)])
#                 plt.ylim([0, 1])
                plt.xlim([0, max(x_axis_values)])

                plt.plot(x_axis_values, y_axis_values,color=colors[index],linestyle=style[line_index],marker=markers[index],markevery=(0.0,0.1),linewidth=6.0, markersize=20,markerfacecolor='blue',markeredgewidth='5', markeredgecolor='black', label=approach)
                if index == len(colors)-1:
                    index = 0
                else:
                    index = index +1

                if line_index ==len(style)-1:
                    line_index = 0
                else:
                    line_index = line_index +1
            except ValueError:
                print("this is the valueerror",ValueError)
    #     if len(my_class_labels)>1:
    #         plt.legend([label for label in my_class_labels ],oc="upper left",fontsize=30)
    #         plt.plot([1,2,3,4,5], [1,2,4,5,6])
    #         plt.plot([1,5,7,9,11], [1,2,4,5,6])
    #         plt.plot([1,3,5,6], [1,2,4,5])
        plt.ylim(ymin=0) 
        plt.legend(fontsize=26)
        plt.savefig(plot_name)
        plt.show()
    except ValueError:
        print("this is the valueerror2",ValueError)


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



        
def multiple_lines_cdf_test(x_axis_label,y_axis_label,cdf_info_dictionary_over_multi_item,log,plot_name,list_of_keys):

    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    
    
    
    colors = ['BLUE','BLACK', 'RED', 'MAROON','OLIVE','LIME','AQUA','GREEN','TEAL','YELLOW']
    
    style=["-","-.",":","-","--"]
    index = 0
    my_class_labels = []
    items_index = 0
    line_index = 0
    for key in list_of_keys:
        #print key
        my_class_labels.append(key)
        cdf_info_dictionary = cdf_info_dictionary_over_multi_item[key]


        #     cdf_info_dictionary = {1:8,3:4,2:4,4:1}
        x_values = list(cdf_info_dictionary.keys())
        #print ('x values are ',x_values,type(x_values))
        x_values.sort()
        
        #print(x_values,type(x_values))
        CDF_values = get_arrs(list(x_values),cdf_info_dictionary)
        #print ('CDF_values,x_values',key,CDF_values,x_values)
        new_x_values = []
        new_cdf_values = []
        
        #print (items_index)
#         new_cdf_values.append(0.0)
#         new_x_values.append(x_items[items_index])
        #print ('x_values',x_values)
        for i in range(0,int(min(x_values))):
            new_cdf_values.append(0.0)
            new_x_values.append(i)
        #print ('min(CDF_values)',min(CDF_values))
#         if min(CDF_values)>0.1:
#             #print ('min(CDF_values)>0.1',min(CDF_values),0.1)
#             #print (10*min(CDF_values))
#             #for i in range(1,y_items[items_index]):
#             for i in range(0,int(10*min(CDF_values))):
#                 #print (i,items_index)
#                 #new_cdf_values.append(float(i)/10)
#                 new_cdf_values.append(float(i)/10)
#                 #new_x_values.append(x_items[items_index])
#                 new_x_values.append(min(x_values))
#         items_index = items_index +1
#         for item in CDF_values:
#             new_cdf_values.append(item)
#         for item in x_values:
#             new_x_values.append(item)
        x_values = new_x_values
        CDF_values = new_cdf_values
        #print (CDF_values,x_values)

        ymin, ymax = ylim()  # return the current ylim
        ylim((0, 1))   # set the ylim to ymin, ymax
        ylim(0, 1)     # set the ylim to ymin, ymax
        #plt.xlim([0, max(x_values)])
        plt.ylim([0, 1])
        if min(x_values) <0:
            
            plt.xlim([min(x_values), max(x_values)])
        else:
            plt.xlim([0, max(x_values)])
        
        print ('x_values is ',x_values)
        plt.plot(x_values, CDF_values,color=colors[index],linestyle=style[line_index],marker=markers[index],markevery=(0.0,0.1),linewidth=6.0, markersize=20,markerfacecolor='blue',markeredgewidth='5', markeredgecolor='black')
        if index == len(colors)-1:
            index = 0
        else:
            index = index +1
        
        if line_index ==len(style)-1:
            line_index = 0
        else:
            line_index = line_index +1
        #plt.plot(x_values, CDF_values,color=colors[index],linestyle=style.next(),marker=markers[index],linewidth=2.0, markersize=20)
    if len(my_class_labels)>1:
        plt.legend([label for label in my_class_labels ],fontsize=33)
    plt.savefig(plot_name)
    plt.show()

# cdf_info_dictionary_over_multi_item = {
                                       
                                       
#                                        'MRAI 2 sec'  :{4:60,3:30,2:7,0:0,1:3,6:0},
# #                                         'conc. control without transient mode'  :{0.2:80,0.2:10,0.1:5,0:0,0.1:5},
#                                         'batch processing'  :{5:60,3:30,2:1,4:9,0:0,6:0},
#                                         'MRAI zero'  :{6:60,5:30,4:5,0:0,2:5}
#                                     }
# list_of_keys = ['batch processing','MRAI zero','MRAI 2 sec']




# #         print(delay_repeatings[19806.0])
# # for i in range(1,70):
# #     cdf_info_dictionary_over_multi_item['third approach'][1000]=i
    
# # for i in range(1,60):
# #     cdf_info_dictionary_over_multi_item['first approach'][800]=i

# multiple_lines_cdf('Frequency of path changing','Cumulutive fraction of \n router-prefix pairs',cdf_info_dictionary_over_multi_item,False,'plots/CDF_on_path_changing.pdf',list_of_keys)
# # multiple_lines_cdf_test('Frequency of path changing','Cumulutive fraction of \n router-prefix pairs',cdf_info_dictionary_over_multi_item,False,'plots/CDF_on_path_changing.pdf',list_of_keys)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


def plot_bar_plot(x_axis_label,y_axis_label,each_scheme_each_x_axis_label_values,x_axis_labels,plot_file_name):

    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    
#     import matplotlib
#     import matplotlib.pyplot as plt
    #import numpy as np

    o = ''
    #labels = ['1', '2', '3', '4', '5']
    #print 'invalid_routes_percentage_based_on_rho_compression.keys()[0]',invalid_routes_percentage_based_on_rho_compression.keys()[0]
    #print 'invalid_routes_percentage_based_on_rho_compression[invalid_routes_percentage_based_on_rho_compression.keys()[0]]',invalid_routes_percentage_based_on_rho_compression[invalid_routes_percentage_based_on_rho_compression.keys()[0]]
    
    compression_times = len(each_scheme_each_x_axis_label_values[list(each_scheme_each_x_axis_label_values.keys())[0]])
    labels = []
    for item in range(1,(compression_times)+1):
        labels.append('e'+str(item))
    labels = x_axis_labels
    
    legends = []
    

    ind = np.arange(len(labels))
    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars
    #print 'x - width/3',x - width/3
    #print 'x + width/3',x + width/3
#     fig, ax = plt.subplots()
    margin_value = 0
    max_value_on_y_axis = 0
    #print("************ ",ind)
    width = 0.15  # the width of the bars
    colors = ['BLACK','RED',"GREY",'GREEN','BLUE','LIME','YELLOW', 'MAROON','OLIVE','AQUA','TEAL']
    color_index = 0
    patterns = [ "","-" ,"/" , "\\" , "|" , "+" , "x", "o", "O", ".", "*" ]
    hatch_pattern_indx = 0
    for scheme, values in each_scheme_each_x_axis_label_values.items():
        #print('values are ', ind+margin_value,',', invalid_percentage_based_on_overlap ,',', width,',',  o+':'+str(overlap))
#         print('values are ',len(invalid_percentage_based_on_overlap),invalid_percentage_based_on_overlap)
        values_for_this_scheme = []
        for x_axis_label in x_axis_labels:
            values_for_this_scheme.append(each_scheme_each_x_axis_label_values[scheme][x_axis_label])
        for y_value in values:
            if y_value >max_value_on_y_axis:
                max_value_on_y_axis = y_value
        rects1= plt.bar(ind+margin_value-0.2, values_for_this_scheme ,width,  label=scheme,color = colors[color_index])
        hatch_pattern_indx+=1
#         ,hatch=patterns[hatch_pattern_indx]
#         print('******** these are the values *****:',ind+margin_value, values_for_this_scheme ,width,  o+':'+str(overlap), colors[color_index])
        margin_value = margin_value+0.2
        legends.append(scheme)
        color_index = color_index +1

    
    plt.tight_layout()
    new_ticks = [ str(y) for y in labels]
    plt.xticks(x, new_ticks,fontsize=45)
    plt.legend([label for label in legends ],fontsize=24,ncol=2)
# #     s.plot( 
# #         kind='bar', 
# #         color=my_colors,
# #     )
    ax = plt.gca()
#     if int(max_value_on_y_axis)==0:
#         ax.set_ylim([0, 1])
#     else:
    ax.set_ylim([0, 100])
    plt.savefig(plot_file_name)
    plt.show()
    


# In[ ]:


def horizontal_box_plat(x_axis_label,y_axis_label,all_data,labels,x_axis_max_value,plot_name):
    import matplotlib.pyplot as plt
    import numpy as np

    # Random test data
    #np.random.seed(19680801)
    #all_data = [np.random.normal(0, std, size=10) for std in range(1, 5)]
    
    #for each_bar_values in all_data:
        #print("each bar values",each_bar_values)
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))

    # rectangular box plot
    bplot1 = ax1.boxplot(all_data,
                         vert=False,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels,widths=0.2)  # will be used to label x-ticks
    # ax1.set_title('Rectangular box plot')

    # notch shape box plot
    # bplot2 = ax2.boxplot(all_data,
    #                      notch=True,  # notch shape
    #                      vert=False,  # vertical box alignment
    #                      patch_artist=True,  # fill with color
    #                      labels=labels)  # will be used to label x-ticks
    # ax2.set_title('Notched box plot')

    # fill with colors
    colors = ['pink', 'lightblue', 'lightgreen']
    # for bplot in (bplot1, bplot2):
    for patch, color in zip(bplot1['boxes'], colors):
        patch.set_facecolor(color)

    xy = np.arange(1,len(labels)+1)
    new_ticks = [ str(x) for x in labels]
    plt.yticks(xy, new_ticks,fontsize=30)
#     x = np.arange(len(labels))
#     new_ticks = [ str(y) for y in labels]
#     plt.xticks(x, new_ticks,fontsize=35)
    # adding horizontal grid lines
    plt.xlim([0, x_axis_max_value])
    for ax in [ax1]:
        ax.yaxis.grid(True)
        ax.set_xlabel(x_axis_label,fontsize=27,labelpad=10)
        ax.set_ylabel(y_axis_label,fontsize=27,labelpad=10)
        ax.grid(True)
        ax.tick_params(axis='x', labelsize=27)
    # legends = [""]
    # plt.legend([label for label in legends ], loc='upper left',fontsize=30)   
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()


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


# #runs of the experimens: batch_processing_exp_800_prefixes_link_delay_inter_phy_machines,MRAI_0_exp_800_prefixes_link_delay_inter_phy_machines,MRAI_2_exp_800_prefixes_link_delay_inter_phy_machines,MRAI_200m_exp_800_prefixes_link_delay_inter_phy_machines,MRAI_0_exp_800_prefixes_8mic_p_link_delay_inter_phy_machines,batch_processing_exp_100_prefixes_8mic_p_link_delay_inter_phy_machines
# #MRAI_0_exp_800_prefixes_14mic_p_link_delay_inter_33_phy_machines,MRAI_0_exp_800_prefixes_link_delay_inter_phy_machines,batch_processing_exp_800_prefixes_link_delay_inter_phy_machines,batch_processing_exp_800_prefixes_14mic_p_link_delay_inter_48_phy_machines,MRAI_200m_exp_800_prefixes_link_delay_inter_phy_machines
# #202109,52320-link_down,45474,4637-link_up,7552,9498-link_down,7552,9498-link_up,
# result_file_name = 'batch_processing_result.csv'
# result_file_name= 'MRAIs_result.csv'
# result_file_name = 'each_scheme_each_link_convergence_time_result_500.csv'
# result_file_name = 'each_scheme_each_link_convergence_time_result_40.csv'
# # result_file_name = 'each_scheme_each_link_mean_convergence_time_result_500.csv'
# # result_file_name='all_schemes_result.csv'
# # result_file_name = 'MRAI_0_batch_processing_p=4_24_result.csv'
# topology = '40'
# each_scheme_key = {'batch_processing_p=4':'batch processing,p=4\u03BCs',
#                    'batch_processing_p=24':'batch processing,p=24\u03BCs',
#                    'batch_processing_p=12':'batch processing,p=12\u03BCs',
#                    'batch_processing_p=14':'batch processing,p=12\u03BCs',
#                    'batch_processing_p=54':'batch processing,p=54\u03BCs',
#                    'batch_processing_p=50':'batch processing,p=50\u03BCs',
#                    'fixed_batch_processing_p=54':'fixed batch processing,p=54\u03BCs',
#                    'fixed_batch_processing_p=4':'fixed batch processing,p=4\u03BCs',
#                    'batch_processing_p=104':'batch processing,p=104\u03BCs',
#                    'BP_p=4':'batch processing,p=4\u03BCs',
#                    'BP_p=54':'batch processing,p=54\u03BCs',
#                    '[batch_processing_p=104':'batch processing,p=104\u03BCs',
#                    '[batch_processing_p=54':'batch processing,p=54\u03BCs',
#                    'simple_batch_processing_p=4':'simple batch processing,p=4\u03BCs',
#                    'simple_batch_processing_p=54' :'simple batch processing,p=54\u03BCs',
#                     'enhanced_batch_processing_p=54':'enhanced_batch_processing,p=54\u03BCs',
#                   'MRAI=0_p=4':'FIFO NMRAI,p=4\u03BCs',
#                    'MRAI=0_p=24':'MRAI=0,p=24\u03BCs',
#                    'MRAI_0_p=104':'MRAI=0,p=104\u03BCs',
#                    'MRAI=0_p=104':'MRAI=0,p=104\u03BCs',
#                    '[MRAI=0_p=20':'MRAI=0,p=20\u03BCs',
#                   '[MRAI=0_p=12':'MRAI=0,p=12\u03BCs',
#                    '[MRAI=0_p=50':'MRAI=0,p=50\u03BCs',
#                    'MRAI=0_p=20':'MRAI=0,p=20\u03BCs',
#                    'MRAI=0_p=122':'MRAI=0,p=122\u03BCs',
#                    'MRAI=10_p=4':'MRAI=10ms,p=4\u03BCs',
#                    'MRAI=100_p=50':'MRAI=100ms,p=50\u03BCs',
#                    'MRAI=0_p=204':'MRAI=0,p=204\u03BCs',
#                   'MRAI=0_p=12':'MRAI=0,p=12\u03BCs',
#                   'MRAI_200ms=p=4':'MRAI=200ms,p=4\u03BCs','MRAI_200ms_p=4':'MRAI=200ms,p=4\u03BCs','MRAI=200ms_p=4':'MRAI=200ms, p=4\u03BCs',
#                   'MRAI=2_p=4':'MRAI=2s,p=4\u03BCs',
#                    'MRAI=2':'MRAI=2s,p=4\u03BCs',
#                    'MRAI=2_p=12':'MRAI=2s,p=12\u03BCs',
#                    'MRAI_30':'MRAI=30s,p=4\u03BCs',
#                    'batch':'batch,p=54\u03BCs',
#                    'MRAI=0_p=54':'MRAI=0,p=54\u03BCs',
#                    'MRAI=0_p=50':'FIFO NMRAI,p=50\u03BCs',
#                    'MRAI=0_p=16':'MRAI=0,p=16\u03BCs',
#                    '[MRAI=0_p=54':'MRAI=0,p=54\u03BCs',
#                    'MRAI_600':'MRAI=600ms,p=4\u03BCs',
#                    'MRAI=600_p=4':'MRAI=600ms,p=4\u03BCs',
#                   'MRAI=600_p=24':'MRAI=600ms,p=24\u03BCs',
#                  'MRAI=30_p=4':'MRAI=30s,p=4\u03BCs',
#                    'MRAI=2_p=54':'MRAI=2s,p=54\u03BCs',
#                    'MRAI=2_p=50':'MRAI=2s,p=50\u03BCs',
#                     'MRAI=6_p=50':'work.cons.=5,p=50\u03BCs',
#                   'MRAI=200_p=4' :'MRAI=200ms,p=4\u03BCs',
#                    'MRAI=4_p=50':'MRAI=0 plus work.cons.,p=54\u03BCs',
#                    'MRAI=4_p=4':'MRAI=4s,p=4\u03BCs',
#                    'MRAI=10_p=54':'MRAI=10ms,p=54\u03BCs',
#                   'MRAI=600_p=54' :'MRAI=600ms,p=54\u03BCs',
#                    'MRAI=4_p=50' :'infinit_work.c.MRAI=100,p=50\u03BCs',
#                    'MRAI=6002_p=54' :'MRAI=600ms per peer,p=54\u03BCs',
#                   '[MRAI=2_p=12':'MRAI=2s,p=12\u03BCs'}
# for mean_median in ['mean','median']:
#     schemes_in_order = []
#     each_approach_each_link_convergence_time = {}
#     with open(result_file_name, "r") as f:
#         reader = csv.reader(f, delimiter=",")
#         for line in (reader):
#             scheme= each_scheme_key[line[0]]
#             if scheme not in schemes_in_order:
#                 schemes_in_order.append(scheme)
#             each_approach_each_link_convergence_time[scheme]= {}
#     link_delays = []
#     print('schemes_in_order',schemes_in_order)
#     with open(result_file_name, "r") as f:
#         reader = csv.reader(f, delimiter=",")
#         for line in (reader):
            
#             scheme= each_scheme_key[line[0]]
#             link_delay = int(line[1])

#     #             link_delay = 1
#             if link_delay not in link_delays:
#                 link_delays.append(link_delay)
#             if mean_median =='mean':
#                 convergence_time = round(float(line[3]),4)
#             else:
#                 convergence_time = round(float(line[2]),4)

#                 #         if link_delay == 4 and scheme =='batch_processing_800':
#     #             convergence_time = each_approach_each_link_convergence_time['batch_processing_800'][10]-0.08
#     #         if '8' in scheme:
#     #             if 'MRAI' in scheme:
#     #                 scheme = "MRAI 0, p= 8\u03BCs"
#     #             else:
#     #                 scheme = "batch processing, p=8\u03BCs"
#     #         else:
#     #             if 'batch_processing_100' in scheme:
#     #                 scheme = "batch processing(100), p= 8\u03BCs"
#     #             else:
#     #                 scheme = scheme+", p= 4\u03BCs"

#             each_approach_each_link_convergence_time[scheme][link_delay] = convergence_time
#     print(each_approach_each_link_convergence_time)
#     dictionary_keys_in_order  = ["Batch processing delay","No MRAI scheme","MRAI=2 sec","MRAI=4 sec","MRAI=30 sec"]
#     link_delays = sort(link_delays)
#     dictionary_keys_in_order  = ["Batch processing delay","No MRAI scheme","MRAI=2 sec","MRAI=4 sec","MRAI=1 sec"]
#     # plot_convergence_detection_alg_overhead('Link delay(msec)','Convergence(sec)',dictionary_keys_in_order,Read_and_Detection_time_with_convergence_Det_Alg,topologies,False,'plots/CD_link_delay.pdf')
#     plot_convergence_detection_alg_overhead('Propagation delay(msec) log scale',mean_median+' of convergence delay(msec)',schemes_in_order,each_approach_each_link_convergence_time,link_delays,False,'plots/'+mean_median+'_CD_link_delay_real_'+topology+'.pdf')
#     ploting_simple_y_as_x('Propagation delay(msec)',mean_median+' of convergence delay(msec)',schemes_in_order,each_approach_each_link_convergence_time,link_delays,False,'plots/'+mean_median+'_CD_link_delay_real_no_log_on_x_axis'+topology+'.pdf')
# print("done")

# print(2%10)


# # MRAI_4_exp_800_prefixes_54mic_p_link_delay_inter_48_phy_machines/MRAI_MRAI_0/topology_size_500$ cp -r 1 2
# # these are the x and y axis values [25.0373125, 25.02177777777778] batch processing,p=54μs


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





# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
def set_3D_plotting_global_attributes(x_axis_label,y_axis_label,z_axis_label):
    import matplotlib.pyplot as plt
    global global_font_size
    global figure_width
    global figure_highth
    global space_from_x_y_axis
    global style
    global markers
    global csfont
    global descriptions
    font_size = 44
    plt.figure(figsize=(8,8))
    global fig
    global global_mark_every
    global_mark_every = 1
    #matplotlib.rcParams['text.usetex'] = True
    fig = plt.figure()
    fig.set_size_inches(16, 8, forward=True)
    global style
    #matplotlib.rcParams['text.usetex'] = True
    global markers
    
    global descriptions

    label_size = 40
    #matplotlib.rcParams['text.usetex'] = True
    csfont = {'fontname':'Times New Roman'}
    #write your code related to basemap here
    #plt.title('title',**csfont)
    plt.rcParams['xtick.labelsize'] = label_size 
    #matplotlib.rcParams['text.usetex'] = True
    plt.rcParams['ytick.labelsize']= label_size
    #matplotlib.rcParams['text.usetex'] = True
    plt.xlabel(x_axis_label, fontsize=36,labelpad=20)
    #matplotlib.rcParams['text.usetex'] = True
    plt.ylabel(y_axis_label,fontsize=36,labelpad=20)
    plt.zlabel('Convergence delay',fontsize=36,labelpad=20)
    plt.grid(True)
    plt.tight_layout()
    #matplotlib.rcParams['text.usetex'] = True
    #plt.ylim(ymin=0) 
    return plt

def plot_multi_dimention_results():
    #plt = set_3D_plotting_global_attributes('Propagation delay','Processing delay','Convergence delay')
    # propagation_delay = list(np.linspace(-4, 4, 100))
    # processing_delay = list(np.linspace(-4, 4, 100))
    #X, Y, Z = [1,2,3,4,5,6,7,8,9,10],[5,6,2,3,13,4,1,2,4,8],[2,3,3,3,5,7,9,11,9,10]
    X, Y = [1,2,4,10,40,80,160,320],[0.016,0.1,0.5,1,2,4,8]#milliseconds
    propagation_delay, processing_delay = np.meshgrid(X, Y)
    # print(X,Y)
    convergence_delay = np.array((propagation_delay* processing_delay))
    # X, Y, Z = [1,2,3,4,5,6,7,8,9,10],[5,6,2,3,13,4,1,2,4,8],[2,3,3,3,5,7,9,11,9,10]
    # Z = (np.sin((X**2 + Y**2)/4)).tolist() 
    print('propagation_delay, processing_delay,convergence_delay',propagation_delay, processing_delay,convergence_delay)
    convergence_delay_values= []
    for pro in X:
        for processing in Y:
            #print('pro*processing',pro,processing)
            if pro <=4 and processing <=0.1:
                CD = 2000
                convergence_delay_values.append(2000)
            else:
                convergence_delay_values.append(2000 + 10* (pro+processing))
                CD = 2000 + 10* (pro+processing)
            #print('propagation,processing, CD',pro,processing,CD)
    a = np.array(convergence_delay_values)
    print(type(convergence_delay),type(a))
    #print(convergence_delay)
    #print(a)
    fig = plt.figure()
    font_size = 33
    plt.figure(figsize=(8,8))
    global_mark_every = 1
    #matplotlib.rcParams['text.usetex'] = True
    fig.set_size_inches(16, 8, forward=True)
    ax = Axes3D(fig)
    #ax = plt.axes(projection='3d')
#     x = np.arange(len(X))
#     new_ticks = [ str(y) for y in X]
#     plt.xticks(x, new_ticks,fontsize=20)
#     plt.grid(True)
    plt.tight_layout()
#     ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis)
    ax.plot_surface(propagation_delay, processing_delay, convergence_delay, rstride=1, cstride=1, cmap=cm.viridis)
#     ax.plot_wireframe(propagation_delay, processing_delay, convergence_delay,color = 'blue')
    
#     ax.contour3D(propagation_delay, processing_delay, convergence_delay, 50, cmap='binary')
    ax.set_xlabel('Propagation delay',fontsize=32,labelpad=31)
    ax.set_ylabel('Processing delay',fontsize=32,labelpad=31)
    ax.set_zlabel('Convergence delay',fontsize=32,labelpad=22)
    #ax.view_init(60, 35)

    plt.show()


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





# 

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





# In[42]:


def check_if_event_has_CD_for_all_x_axises(scheme,each_approach_each_x_axis_each_y_value,x_axis_values):
    #print(x_axis_values,list(each_approach_each_x_axis_each_y_value[scheme].keys()) )
    for item in x_axis_values:
        if item not in list(each_approach_each_x_axis_each_y_value[scheme].keys()):
            #print('return Fasle')
            return False
    #print('return True')
    return True
    


# In[78]:




import matplotlib.pyplot as plt
import numpy as np

def multiple_box_plot_on_each_x_axis(x_axis_label,y_axis_label,tickets_on_x_axis,x_axis_values,
                                     each_approach_each_x_axis_pont_values,plot_file_name):

#     data_a = [[1,2,5], [5,7,2,2,5], [7,2,5]]
#     data_b = [[6,4,2], [1,2,5,3,2], [2,3,5,1]]
#     data_a = [[0.4,0.5,0.6,0.5,0.6,0.1,0.0],  [0.4,0.3,0.3,0.4,0.6,0.0], [0.2,0.2,0.2,0.1,0.0]]
#     data_b = [[0.3,0.3,0.4,0.3,0.6,0.2,0.0,0.0],  [0.2,0.3,0.2,0.2,0.5,0.0], [0.1,0.1,0.2,0.1,0.0]] 
    plt = set_plotting_global_attributes(x_axis_label,y_axis_label)
    #ticks = ['A', 'B', 'C']
    data_values ={}
    ID = 0
    maximum_value_of_y_axis = 0
    for scheme in each_approach_each_x_axis_pont_values:
        this_scheme_values = []
        for x_axis_value in x_axis_values:
            values = each_approach_each_x_axis_pont_values[scheme][x_axis_value]
            this_scheme_values.append(values)
            for value in values:
                if value >maximum_value_of_y_axis:
                    maximum_value_of_y_axis = value
        data_values[ID] = this_scheme_values
        ID +=1
    print('data_values',data_values)
    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)

    #plt.figure()
    colors = ['#D7191C','#2C7BB6','#8E44AD']
    color_index = 0
#     for scheme,x_axis_values in each_approach_each_x_axis_pont_values.items():
#         bpl = plt.boxplot(data_a, positions=np.array(range(len(data_a)))*2.0-0.4, sym='', widths=0.6)
#         set_box_color(bpl, '#D7191C')
    plt_values = []
    for ID,data_value in data_values.items():
        #print('data_value',data_value)
        if ID==0:
            bpl = plt.boxplot(data_value, showmeans=True,meanprops={"marker":"o",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"20"},positions=np.array(range(len(data_value)))*2.0-0.4, sym='', widths=0.4)
        elif ID==1:
            bpl = plt.boxplot(data_value,showmeans=True,meanprops={"marker":"o",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"20"}, positions=np.array(range(len(data_value)))*2.0+0.1, sym='', widths=0.4)
        elif ID==2:
            bpl = plt.boxplot(data_value,showmeans=True, meanprops={"marker":"o","markerfacecolor":"white", "markeredgecolor":"black","markersize":"20"},positions=np.array(range(len(data_value)))*2.0+0.7, sym='', widths=0.5)

#         if ID>0:
#             bpl = plt.boxplot(data_value, positions=np.array(range(len(data_value)))*2.0+0.4, sym='', widths=0.6)
#         else:
#             bpl = plt.boxplot(data_value, positions=np.array(range(len(data_value)))*2.0-0.4, sym='', widths=0.6)
        #print('positions',np.array(range(len(data_value)))*2.0-0.4)
        set_box_color(bpl, colors[color_index])
        color_index+=1
#     bpl = plt.boxplot(data_a, positions=np.array(range(len(data_a)))*2.0-0.4, sym='', widths=0.6)
#     bpr = plt.boxplot(data_b, positions=np.array(range(len(data_b)))*2.0+0.4, sym='', widths=0.6)
#     set_box_color(bpl, '#D7191C') # colors are from http://colorbrewer2.org/
#     set_box_color(bpr, '#2C7BB6')

    # draw temporary red and blue lines and use them to create a legend
    
    color_index = 0
    for scheme in each_approach_each_x_axis_pont_values:
        plt.plot([], c=colors[color_index], label=scheme)
        color_index +=1
#     plt.plot([], c='#D7191C', label='Apples')
#     plt.plot([], c='#2C7BB6', label='Oranges')
    #plt.legend()
    if len(list(each_approach_each_x_axis_pont_values.keys()))>1:
        plt.legend(fontsize=38)
    
    plt.xticks(range(0, len(tickets_on_x_axis) * 2, 2), tickets_on_x_axis)
    plt.xlim(-2, len(tickets_on_x_axis)*2)
    plt.ylim(0, maximum_value_of_y_axis+2)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    
    plt.tight_layout()
    plt.savefig(plot_file_name)


# In[81]:





# In[ ]:





# In[ ]:




