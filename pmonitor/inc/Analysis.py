# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt;

"""
@author: Bethel Osuagwu
"""
def plot_separate(t,Ps,data_tissue_avg_h,data_tissue_fixed_h,data_tissue_inverse_h,data_tissue_continuous_h,data_tissue_linear_h,title,xlabel,ylabel,file_name,annotations={}):
    """
    A helper to plot health data in separate axes for each tissue.

    Parameters
    ----------
    t : Arraylike<float>
        Time data for all.
    Ps : Arraylike<float>
        Pressure data
    data_tissue_avg_h : Arraylike<float>
        Health data for tissue with averagin filter
    data_tissue_fixed_h : Arraylike<float>
        Health data for tissue with  fixed time decay method
    data_tissue_inverse_h : Arraylike<float>
        Health data for tissue with inverse time decay method
    data_tissue_continuous_h : Arraylike<float>
        Health data for tissue with continous filter.
    data_tissue_linear_h : Arraylike<float>
        Health data for tissue with linear decay
    title : string
        The general title of all plots.
    xlabel : string
        The Xlabel for all data
    ylabel : string
        Ylable of all data.
    file_name : string
        The full filename of the generated pdf plot
    annotations : dic
        The label for the data inputs. The keys include 'avg','fixed','inverse', 
        'linear' and 'continuous'
    

    Returns
    -------
    None.

    """
    
    fig2,axs=plt.subplots(5,2,sharex=True, sharey=True); # Note we won't use the second column but have to create it to help reduce the space
    for i in range(0,5):
        axs[i,1].remove();# Remove the column that we do not need
    
    
    #
    axs[0,0].set_title(title)
    line1,=axs[0,0].plot(t,data_tissue_avg_h,'-k')
    line1.set_label(annotations.get('avg','Average'))
    axs[0,0].annotate(s=line1.get_label(),
                      xy=(0.4,0.95),xycoords='axes fraction')
    
    line2,=axs[1,0].plot(t,data_tissue_fixed_h,'-k')
    line2.set_label(annotations.get('fixed','Fixed'))
    axs[1,0].annotate(s=line2.get_label(),
                      xy=(0.4,0.95),xycoords='axes fraction')
    
    line3,=axs[2,0].plot(t,data_tissue_inverse_h,'-k')
    line3.set_label(annotations.get('inverse','Inverse'))
    axs[2,0].annotate(s=line3.get_label(),
                      xy=(0.4,0.95),xycoords='axes fraction')
    
    
    
    line4,=axs[3,0].plot(t,data_tissue_linear_h,'-k')
    line4.set_label(annotations.get('linear','Linear'))
    axs[3,0].annotate(s=line4.get_label(),
                      xy=(0.4,0.95),xycoords='axes fraction')
    
    line5,=axs[4,0].plot(t,data_tissue_continuous_h,'-k')
    line5.set_label(annotations.get('continuous','Exponential'))
    axs[4,0].annotate(s=line5.get_label(),
                      xy=(0.4,0.95),xycoords='axes fraction')
    
    #
    color = '#000000';
    color_fainted='#888888';
    color_alpha=0.1;
    for i in range(0,5):
        axs[i,0].spines['top'].set_visible(False)
        
        axs2=axs[i,0].twinx();
        axs2.spines['right'].set_color(color_fainted);
        axs2.spines['top'].set_visible(False)
        axs2.tick_params(axis='y', colors=color_fainted)
        axs2.tick_params(axis='y', labelcolor=color_fainted)
        line0,=axs2.plot(t,Ps,'-',color=color,alpha=color_alpha)
        line0.set_label('Pressure');
        
        
        
        #
        if i==1:
            axs2.set_ylabel('Pressure (kPa)',color=color_fainted)
            
            axs[i,0].set_ylabel(ylabel)
        if i==4:
            line0.set_label('Pressure')
            axs[i,0].set_xlabel(xlabel)
            
    plt.savefig(file_name)
