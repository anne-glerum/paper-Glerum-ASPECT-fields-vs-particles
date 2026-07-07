import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import interpolate
import os
from matplotlib import rc
rc("pdf", fonttype=42)
rc("lines", linewidth=3, markersize=8)

output_dir_base = '/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/'

### load data ##################################################################

# import colormap
cm_data = np.loadtxt("Colormaps/romaO.txt")
romaO_map = LinearSegmentedColormap.from_list(cm_data, cm_data)
cm_data2 = np.loadtxt("Colormaps/roma.txt")
roma_map = LinearSegmentedColormap.from_list(cm_data2, cm_data2)

# time array
dtc = 10.
dtc = 2.5
#Time = np.arange(0,200.1,dtc) # [yr]
Time = np.arange(0,200.1,dtc*2) # [yr]

Time_list = []
for i in range(len(Time)):
    Time_list.append(int(Time[i]))
    Time_list[i] = "%01d" % Time_list[i]
 
Time_list2 = []
for i in range(len(Time)):
    Time_list2.append(int(Time[i]/dtc))
    Time_list2[i] = "%05d" % Time_list2[i]
    
# load numerical data ASPECT

model_name = [
'RL9_viscoelastic_3D_loading_main_AMG_dtc2.5_dte2.5_averaginggeometric_IGR1_IAR2',
] 

label_as = [
'main_AMG_dtc2_5_dte2_5_avegeometric_IGR1_IAR2',
] 

for k in range(len(model_name)):
    print ("Reading in: ", model_name[k])
    topo_as_data = {}
    for i in range(len(Time)):
        topo_as_data[(Time_list[i], label_as[k])] = np.genfromtxt(model_name[k]+'/topography.' + Time_list2[i])
        
    
### create surface plots: ASPECT ###############################################
divide_time = 4
n_rows = 2
n_cols = 5
for k in range(len(label_as)):
    fig, ax = plt.subplots(n_rows, n_cols, sharex='col', sharey='row', layout='compressed')
    
    counter = 1
    for i in range(0,n_rows):
        for j in range (0,n_cols):
            ax[i, j].set_title("Time = "+str(int(Time[divide_time*counter]))+" yr", fontsize=6, pad=4)
            topo = topo_as_data[(Time_list[divide_time*counter], label_as[k])]
            # remove duplicates
            tmp = np.unique(topo, axis=0)
            # get unique coordinates in km
            tmp_x = np.unique(tmp[:,1])/1000
            tmp_x.sort()
            tmp_y = np.unique(tmp[:,0])/1000
            tmp_y.sort()
            # get the topography in the right shape
            Z = (tmp[:, 3]).reshape(len(tmp_x), len(tmp_y))
            im = ax[i, j].pcolormesh(tmp_x, tmp_y, Z, vmin=-0.8, vmax=0.1, cmap=roma_map, shading='nearest')
            ax[i, j].set_aspect('equal', adjustable='box')
            ax[i, j].set_yticks([0,100,200,300,400,500])
            ax[i, j].tick_params(axis="y", labelsize=5)
            ax[i, j].set_xticks([0,100,200,300,400,500])
            ax[i, j].tick_params(axis="x", labelsize=5)
            if i == n_rows-1:
                ax[i, j].set_xlabel("X [km]", fontsize=6)
            if j == 0:
                ax[i, j].set_ylabel("Y [km]", fontsize=6)
            ax[i, j].set_xlim([0,500])
            ax[i, j].set_ylim([0,500])
            counter += 1
    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', fraction=.04)
    cbar.set_label('Surface displacement [m]',
                labelpad=5, fontsize=6)
    cbar.ax.tick_params(labelsize=5)
    ax[0,0].text(-180,500,"a)",fontsize=6)
    filename = output_dir_base + model_name[k] + '/' + label_as[k] + '_surface_topo2.png'
    plt.savefig(filename, dpi=300)
    plt.cla()
plt.close(fig)
