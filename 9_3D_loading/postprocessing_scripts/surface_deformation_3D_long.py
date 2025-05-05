import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import interpolate
import os

output_dir_base = '/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/'
### TODO: remove all exec

### load data ##################################################################

# import colormap
Dir = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/Colormaps/" 
os.chdir(Dir)
cm_data = np.loadtxt("romaO.txt")
romaO_map = LinearSegmentedColormap.from_list(cm_data, cm_data)
cm_data2 = np.loadtxt("roma.txt")
roma_map = LinearSegmentedColormap.from_list(cm_data2, cm_data2)

# time array
Time = np.arange(0,200.1,5.) # [yr]

Time_list = []
for i in range(len(Time)):
    Time_list.append(int(Time[i]))
    Time_list[i] = "%01d" % Time_list[i]
 
Time_list2 = []
for i in range(len(Time)):
    Time_list2.append(int(Time[i]/2.5))
    Time_list2[i] = "%05d" % Time_list2[i]

Time_list3 = []
for i in range(len(Time)):
    Time_list3.append(int(Time[i]/2.5))
    Time_list3[i] = "%01d" % Time_list3[i]

# load numerical data ASPECT
label_as = ['old_cf_ref','old_p_ref','new_cf_ref','new_p_ref']
label_as = ['new_cf_ref','new_p_ref']
model_name = ['RL9_viscoelastic_3D_loading_AMG_dtc2.5_dte2.5_averaginggeometric_IGR1_IAR2','RL9_viscoelastic_3D_loading_particles_AMG_avegeometric_intbilinear_least_squares_limTrue_dtc2.5_dte2.5_IGR1_IAR0_np4']
label_as = ['new_cf_ref']
model_name = ['RL9_viscoelastic_3D_loading_AMG_dtc2.5_dte2.5_averaginggeometric_IGR1_IAR2']
label_as = ['new_p_ref']
model_name = ['RL9_viscoelastic_3D_loading_particles_AMG_avegeometric_intbilinear_least_squares_limTrue_dtc2.5_dte2.5_IGR1_IAR0_np4']

label_as = ['AMG_geometric_BLSlim_dtc2_5_dte2_5_IGR1_IAR2_np4']
model_name = ['RL9_viscoelastic_3D_loading_particles_AMG_avegeometric_intbilinear_least_squares_limTrue_dtc2.5_dte2.5_IGR1_IAR2_np4']
for k in range(len(model_name)):
    print ("Reading in: ", model_name[k])
    Dir = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/"+model_name[k]+"/"
    os.chdir(Dir) # change directory
    for i in range(len(Time)):
        exec("topo_"+Time_list[i]+"_as_"+label_as[k]+" = np.genfromtxt('topography."+Time_list2[i]+"')")
        
# load numerical data ABAQUS
Dir = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/ABAQUS_TABOO/abaqus"
os.chdir(Dir) # change directory
for i in range(int(len(Time))):
    exec("topo_"+Time_list[i]+"_ab = np.genfromtxt('incomp_flat_FE_U3_E_"+Time_list[i]+"yr.dat')")

# set parameters for loading analytical data
R = 6371.0 # Earth radius analytical model [km]

t_start = 0.0 # start time [ka]
t_end   = 0.2 # end time [ka]
t_step  = 0.0025 # time step size [ka]

colat_start = 0.0  # start observer locations co-latitude [degree]
colat_end   = 5.0  # end observer locations co-latitude [degree]
colat_step  = 0.01 # observer locations co-latitude step size

time = np.arange(t_start,t_end+0.0001,t_step)
colat = np.arange(colat_start,colat_end+0.0001,colat_step) # observer locations co-latitude [degree]
loc = colat/360.*2*np.pi*R # observer locations distance from pole [km]

# load analytical data
print ("Loading in analytical data")
Dir = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/ABAQUS_TABOO/taboo"
os.chdir(Dir) # change directory
disp = np.genfromtxt('disp.his')
for i in range(len(time)):
    exec("disp_time"+str(i)+" = np.zeros((1,6))")
    for j in range(len(colat)):
        exec("disp_time"+str(i)+" = np.vstack([disp_time"+str(i)+",disp[len(time)*j+i,:]])")
    exec("disp_time"+str(i)+" = disp_time"+str(i)+"[1:,:]")
del disp

for i in range(len(Time)):
    exec("topo_"+Time_list[i]+"_t = disp_time"+Time_list3[i]+"")
for i in range(len(time)):
    exec("del disp_time"+str(i)+"")
    
### create surface plots: ASPECT ###############################################

print ("Creating surface plots")
# determine max and min of all numerical data for colorbar
for k in range(len(label_as)):
    exec("vmin_"+label_as[k]+" = np.zeros([len(Time),]); vmax_"+label_as[k]+" = np.zeros([len(Time),])")
    for i in range(len(Time)):
        exec("vmin_"+label_as[k]+"[i] = topo_"+Time_list[i]+"_as_"+label_as[k]+"[:,3].min()")          
        exec("vmax_"+label_as[k]+"[i] = topo_"+Time_list[i]+"_as_"+label_as[k]+"[:,3].max()")
    exec("vminm_as_"+label_as[k]+" = vmin_"+label_as[k]+".min(); vmaxm_as_"+label_as[k]+" = vmax_"+label_as[k]+".max()")
    exec("del vmin_"+label_as[k]+", vmax_"+label_as[k]+" ")
    
vmin = np.zeros([len(Time),]); vmax = np.zeros([len(Time),])
for i in range(len(Time)):
    exec("vmin[i] = topo_"+Time_list[i]+"_ab[:,3].min()")          
    exec("vmax[i] = topo_"+Time_list[i]+"_ab[:,3].max()")
vminm_ab = vmin.min(); vmaxm_ab = vmax.max()
del vmin, vmax

# plot surface topography ASPECT
for k in range(len(label_as)):
    fig = plt.figure(figsize=(20,15))
    plt.rc('axes', axisbelow=True)
    for i in range(1,int((len(Time)-1)/2+1)):
        ax = fig.add_subplot(4,5,i)
        ax.set_title("Time = "+str(Time[2*i])+" yr",fontsize=10) # change  
        exec("im=plt.scatter(topo_"+Time_list[2*i]+"_as_"+label_as[k]+"[:,0]/1000,topo_"+Time_list[2*i]+"_as_"+label_as[k]+"[:,1]/1000,c=topo_"+Time_list[2*i]+"_as_"+label_as[k]+"[:,3],cmap=roma_map,vmin=-0.8,vmax=0.1)")
        plt.ylim([0,500])
        plt.xlim([0,500])
        ax.set_yticks([0,100,200,300,400,500]); ax.tick_params(axis="y", labelsize=12)
        ax.set_xticks([0,100,200,300,400,500]); ax.tick_params(axis="x", labelsize=12)
        if np.mod(i,5) != 0:
            plt.gca().tick_params(axis='y',labelleft=False)
        if i <= 15:
            plt.gca().tick_params(axis='x',labelbottom=False)
    cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])
    cbar_ax.tick_params(labelsize=15)
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Surface displacement [m]',rotation=90,labelpad=10,fontsize=18)
    fig.text(0.5, 0.04, 'x-direction [km]',ha='center',fontsize=18)
    fig.text(0.06, 0.5, 'y-direction [km]',va='center',rotation='vertical',fontsize=18)
    #plt.show()
    filename = output_dir_base + model_name[k] + '/' + label_as[k] + '_surface_topo.png'
    # plot looks good
    plt.savefig(filename, dpi=300)

### create radial deformation profile plots: ASPECT and TABOO and ABAQUS #######
print ("Creating radial deformation plots")
# select ASPECT profile: y=x
for k in range(len(label_as)):
    for i in range(len(Time)):
        exec("topo = topo_"+Time_list[i]+"_as_"+label_as[k]+"")
        topo_radial = np.zeros((1,4))
        for j in range(topo.shape[0]):
            if topo[j,1] == topo[j,0]:
                topo_radial = np.vstack([topo_radial,topo[j,:]])
        exec("topo_"+Time_list[i]+"_as_"+label_as[k]+"_radial = topo_radial[1:,:]")
    del topo, topo_radial
    
    for i in range(len(Time)):
        exec("topo_"+Time_list[i]+"_as_"+label_as[k]+"_radial = np.unique(topo_"+Time_list[i]+"_as_"+label_as[k]+"_radial, axis=0)")
        exec("topo_"+Time_list[i]+"_as_"+label_as[k]+"_R = np.sqrt((topo_"+Time_list[i]+"_as_"+label_as[k]+"_radial[:,0]/1000)**2+(topo_"+Time_list[i]+"_as_"+label_as[k]+"_radial[:,1]/1000)**2)")

# select ABAQUS profile: y=x, upper left quadrant
for i in range(int(len(Time))):
    exec("topo = topo_"+Time_list[i]+"_ab")
    topo_radial = np.zeros((1,4))
    for j in range(topo.shape[0]):
        if topo[j,1] == topo[j,0] and topo[j,0] >= 1500.e3 and topo[j,1] >= 1500.e3:
            topo_radial = np.vstack([topo_radial,topo[j,:]])
    exec("topo_"+Time_list[i]+"_ab_radial = topo_radial[1:,:]")
    exec("topo_"+Time_list[i]+"_ab_radial[:,0] = topo_"+Time_list[i]+"_ab_radial[:,0]-1500.e3")
    exec("topo_"+Time_list[i]+"_ab_radial[:,1] = topo_"+Time_list[i]+"_ab_radial[:,1]-1500.e3")
del topo, topo_radial

for i in range(int(len(Time))):
    exec("topo_"+Time_list[i]+"_ab_radial = np.unique(topo_"+Time_list[i]+"_ab_radial, axis=0)")
    exec("topo_"+Time_list[i]+"_ab_R = np.sqrt((topo_"+Time_list[i]+"_ab_radial[:,0]/1000)**2+(topo_"+Time_list[i]+"_ab_radial[:,1]/1000)**2)") 

# create plot: deformation profiles through time, ASPECT
for k in range(len(label_as)):
    fig = plt.figure(figsize=(8,6))
    for i in range(int((len(Time)-1)/2+1)):
        j = 12*i
        exec("plt.plot(topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_R,topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_radial[:,3],color=cm_data[j,:])")
    plt.xlim([0,500])
    #plt.ylim([-0.8,0.1])
    ax = plt.gca()
    plt.tick_params(labelsize=12)
    plt.title('ASPECT',fontsize=15)
    plt.xlabel('Horizontal distance from load center, y=x [km]',fontsize=15, ha='center')
    plt.ylabel('Vertical surface deformation [m]',fontsize=15)
    plt.legend(['t=0 yr','t=10 yr','t=20 yr','t=30 yr','t=40 yr','t=50 yr','t=60 yr','t=70 yr','t=80 yr','t=90 yr','t=100 yr','t=110 yr','t=120 yr','t=130 yr','t=140 yr','t=150 yr','t=160 yr','t=170 yr','t=180 yr','t=190 yr','t=200 yr'],ncol=2,loc=4,fontsize=15)
    plt.grid(which='major')
    #plt.show()
    # plot looks good
    filename = output_dir_base + model_name[k] + "/"  + label_as[k] + '_profile_ASPECT.png'
    plt.savefig(filename, dpi=300)

# create plot: deformation profiles through time, ABAQUS
fig = plt.figure(figsize=(8,6))
for i in range(int((len(Time)-1)/2+1)):
    j = 12*i
    exec("plt.plot(topo_"+Time_list[2*i]+"_ab_R,topo_"+Time_list[2*i]+"_ab_radial[:,3],color=cm_data[j,:])")
plt.xlim([0,500])
plt.ylim([-0.8,0.1])
ax = plt.gca()
plt.tick_params(labelsize=12)
plt.title('ABAQUS',fontsize=15)
plt.xlabel('Horizontal distance from load center [km]',fontsize=15, ha='center')
plt.ylabel('Vertical surface deformation [m]',fontsize=15)
plt.legend(['t=0 yr','t=10 yr','t=20 yr','t=30 yr','t=40 yr','t=50 yr','t=60 yr','t=70 yr','t=80 yr','t=90 yr','t=100 yr','t=110 yr','t=120 yr','t=130 yr','t=140 yr','t=150 yr','t=160 yr','t=170 yr','t=180 yr','t=190 yr','t=200 yr'],ncol=2,loc=4,fontsize=15)
plt.grid(which='major')
#plt.show()
# plot looks good
filename = output_dir_base + '_profile_ABAQUS.png'
plt.savefig(filename, dpi=300)

# create plot: deformation profiles through time ASPECT and TABOO, time step = 10 yr
for k in range(len(label_as)):
    title_plot = ['ASPECT','TABOO','Abaqus']
    fig = plt.figure(figsize=(24,10))
    for l in range(3):
        ax = fig.add_subplot(1,3,l+1)
        for i in range(1,int((len(Time)-1)/2+1)):
            j = 12*i
            if l == 0:
                exec("plt.plot(topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_R,topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_radial[:,3],color=cm_data[j,:])")
            elif l == 1:
                exec("plt.plot(loc,topo_"+Time_list[2*i]+"_t[:,1],color=cm_data[j,:])")    
            elif l == 2:
                exec("plt.plot(topo_"+Time_list[2*i]+"_ab_R,topo_"+Time_list[2*i]+"_ab_radial[:,3],color=cm_data[j,:])")
        if l == 0:
            plt.axvline(1.5,c='r',linewidth='3')
            plt.axvline(100.0,c='gold',linewidth='3')
            plt.axvline(250.0,c='b',linewidth='3')
        plt.xlim([0,500])
        plt.ylim([-1.2,1.2])
        ax.tick_params(labelsize=20)
        exec("ax.set_title('"+title_plot[l]+"',fontsize=25)")
        if l != 0:
            plt.gca().tick_params(axis='y',labelleft=False)
        if l == 0:
            plt.ylabel('Vertical surface deformation [m]',fontsize=15)
        if l == 2:
            plt.legend(['t=10 yr','t=20 yr','t=30 yr','t=40 yr','t=50 yr','t=60 yr','t=70 yr','t=80 yr','t=90 yr','t=100 yr','t=110 yr','t=120 yr','t=130 yr','t=140 yr','t=150 yr','t=160 yr','t=170 yr','t=180 yr','t=190 yr','t=200 yr'],ncol=2,loc=1,fontsize=10)
        plt.grid(which='major')
        if l == 1:
            plt.xlabel('Horizontal distance from load center [km]',fontsize=15)
        #plt.show()
        # plot looks bad
        plt.tight_layout()
        filename = output_dir_base + model_name[k] + "/"  + label_as[k] + '_profile_ASPECT_TABOO_ABAQUS.png'
        plt.savefig(filename, dpi=300)

### create maximum deformation plots ###########################################
print ("Creating maximum deformation plots")
for k in range(len(label_as)):
    exec("topo_max_as_"+label_as[k]+" = np.zeros((int(len(Time)),2)); topo_max_as_"+label_as[k]+"[:,0] = Time[::1]")
    for i in range(len(Time)):
        exec("topo_max_as_"+label_as[k]+"[i,1] = topo_"+Time_list[i]+"_as_"+label_as[k]+"_radial[:,3].min()")

topo_max_t = np.zeros((int(len(Time)),2)); topo_max_t[:,0] = Time[::1]
for i in range(len(Time)):
    exec("topo_max_t[i,1] = topo_"+Time_list[i]+"_t[:,1].min()")
        
topo_max_ab = np.zeros((int(len(Time)),2)); topo_max_ab[:,0] = Time[::1]
for i in range(len(Time)):
    exec("topo_max_ab[i,1] = topo_"+Time_list[i]+"_ab_radial[:,3].min()")

for k in range(len(label_as)): 
    fig = plt.figure()
    exec("plt.plot(topo_max_as_"+label_as[k]+"[:,0],topo_max_as_"+label_as[k]+"[:,1],c='k',zorder=0,label='_nolegend_')")
    for i in range(len(Time)):
        j = 6*i
        if i == 0:
            exec("plt.scatter(topo_max_as_"+label_as[k]+"[i,0],topo_max_as_"+label_as[k]+"[i,1],color=cm_data[j,:],marker='*',s=100)")
        else:
            exec("plt.scatter(topo_max_as_"+label_as[k]+"[i,0],topo_max_as_"+label_as[k]+"[i,1],color=cm_data[j,:],marker='*',s=100,label='_nolegend_')")
    plt.plot(topo_max_t[:,0],topo_max_t[:,1],c='k',zorder=0,label='_nolegend_')
    for i in range(len(Time)):
        j = 6*i
        if i == 0:
            plt.scatter(topo_max_t[i,0],topo_max_t[i,1],color=cm_data[j,:],marker='^',s=100)
        else:
            plt.scatter(topo_max_t[i,0],topo_max_t[i,1],color=cm_data[j,:],marker='^',s=100,label='_nolegend_')
    for i in range(len(Time)):
        j = 6*i
        if i == 0:
            plt.scatter(topo_max_ab[i,0],topo_max_ab[i,1],color=cm_data[j,:],marker='+',s=100)
        else:
            plt.scatter(topo_max_ab[i,0],topo_max_ab[i,1],color=cm_data[j,:],marker='+',s=100,label='_nolegend_')
    plt.xlim([0,200]) 
    plt.ylim([-0.8,0.1])
    ax = plt.gca()
    plt.tick_params(labelsize=20)
    ax.tick_params(axis='both',labelsize=20)
    plt.xlabel('Time [yr]',fontsize=25)
    plt.ylabel('Maximum vertical surface deformation [m]',fontsize=15)
    plt.legend(['ASPECT','TABOO','Abaqus'],loc='upper right',fontsize=20)
    plt.grid(which='major')
    #plt.show()
    # plot looks bad: color bars, axis labels
    plt.tight_layout()
    filename = output_dir_base + model_name[k] + "/"  + label_as[k] + '_max_def_ASPECT_TABOO_ABAQUS.png'
    plt.savefig(filename, dpi=300)

### create combined uplift and uplift rate plots ###############################
print ("Creating uplift and uplift rate plots")
# interpolate
x_des = np.linspace(0.,500.,501)
for k in range(len(label_as)):
    for i in range(int((len(Time)-1)/2+1)):
        exec("f_as_"+Time_list[2*i]+"_"+label_as[k]+" = interpolate.interp1d(topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_R,topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_radial[:,3],kind='cubic')")
        exec("topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_radial_intp = f_as_"+Time_list[2*i]+"_"+label_as[k]+"(x_des)")

for i in range(int((len(Time)-1)/2+1)):
    exec("f_t_"+Time_list[2*i]+" = interpolate.interp1d(loc,topo_"+Time_list[2*i]+"_t[:,1],kind='cubic')")
    exec("topo_"+Time_list[2*i]+"_t_intp = f_t_"+Time_list[2*i]+"(x_des)")
    
for i in range(int((len(Time)-1)/2+1)):
    exec("f_ab_"+Time_list[2*i]+" = interpolate.interp1d(topo_"+Time_list[2*i]+"_ab_R,topo_"+Time_list[2*i]+"_ab_radial[:,3],kind='cubic')")
    exec("topo_"+Time_list[2*i]+"_ab_radial_intp = f_ab_"+Time_list[2*i]+"(x_des)")    
    
# extract deformation at specified distances
distances = np.array([0,100,250,500])
for k in range(len(label_as)):
    for p in range(len(distances)):
        exec("topo_1loc_as_"+label_as[k]+"_"+str(distances[p])+" = np.array(())")
        idx = np.where(x_des == distances[p])
        for i in range(int((len(Time)-1)/2+1)):   
            exec("topo_1loc_as_"+label_as[k]+"_"+str(distances[p])+" = np.hstack([topo_1loc_as_"+label_as[k]+"_"+str(distances[p])+",topo_"+Time_list[2*i]+"_as_"+label_as[k]+"_radial_intp[idx[0][0]]])")

for p in range(len(distances)):
    exec("topo_1loc_t_"+str(distances[p])+" = np.array(())")
    idx = np.where(x_des == distances[p])
    for i in range(int((len(Time)-1)/2+1)): 
        exec("topo_1loc_t_"+str(distances[p])+" = np.hstack([topo_1loc_t_"+str(distances[p])+",topo_"+Time_list[2*i]+"_t_intp[idx[0][0]]])")


for p in range(len(distances)):
    exec("topo_1loc_ab_"+str(distances[p])+" = np.array(())")
    idx = np.where(x_des == distances[p])
    for i in range(int((len(Time)-1)/2+1)):   
        exec("topo_1loc_ab_"+str(distances[p])+" = np.hstack([topo_1loc_ab_"+str(distances[p])+",topo_"+Time_list[2*i]+"_ab_radial_intp[idx[0][0]]])")


# compute deformation rates at specified distances (max. at x=0 km)
for k in range(len(label_as)):
    for p in range(len(distances)):
        exec("topo_rate_as_"+label_as[k]+"_"+str(distances[p])+" = np.zeros((int((len(Time)-1)/2),2)); topo_rate_as_"+label_as[k]+"_"+str(distances[p])+"[:,0] = Time[2::2]-5")
        for i in range(int((len(Time)-1)/2)):
            exec("topo_rate_as_"+label_as[k]+"_"+str(distances[p])+"[i,1] = (topo_1loc_as_"+label_as[k]+"_"+str(distances[p])+"[i+1]-topo_1loc_as_"+label_as[k]+"_"+str(distances[p])+"[i])/1000")


for p in range(len(distances)):
    exec("topo_rate_t_"+str(distances[p])+" = np.zeros((int((len(Time)-1)/2),2)); topo_rate_t_"+str(distances[p])+"[:,0] = Time[2::2]-5")
    for i in range(int((len(Time)-1)/2)):
        exec("topo_rate_t_"+str(distances[p])+"[i,1] = (topo_1loc_t_"+str(distances[p])+"[i+1]-topo_1loc_t_"+str(distances[p])+"[i])/1000")


for p in range(len(distances)):
    exec("topo_rate_ab_"+str(distances[p])+" = np.zeros((int((len(Time)-1)/2),2)); topo_rate_ab_"+str(distances[p])+"[:,0] = Time[2::2]-5")
    for i in range(int((len(Time)-1)/2)):
        exec("topo_rate_ab_"+str(distances[p])+"[i,1] = (topo_1loc_ab_"+str(distances[p])+"[i+1]-topo_1loc_ab_"+str(distances[p])+"[i])/1000")


# create uplift and uplift rate plots at specified distances
dist_color = ['r','gold','b','k']
for k in range(len(label_as)):
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1,2,1)
    for p in range(len(distances)-1):
        exec("plt.plot(Time[::2],topo_1loc_as_"+label_as[k]+"_"+str(distances[p])+",color=dist_color[p],linestyle='-')")
        exec("plt.plot(Time[::2],topo_1loc_t_"+str(distances[p])+",color=dist_color[p],linestyle='--')")
        exec("plt.plot(Time[::2],topo_1loc_ab_"+str(distances[p])+",color=dist_color[p],linestyle='dashdot')")
    plt.xlim([0,200]) 
    plt.ylim([-0.8,0.1])
    ax = plt.gca()
    ax.tick_params(axis='both',labelsize=20)
    plt.xlabel('Time [yr]',fontsize=25)
    plt.ylabel('Vertical surface deformation [m]',fontsize=15)
    plt.grid(which='major')
    ax = fig.add_subplot(1,2,2)
    for p in range(len(distances)-1):
        exec("plot_as_"+str(distances[p])+", = plt.plot(topo_rate_as_"+label_as[k]+"_"+str(distances[p])+"[:,0],topo_rate_as_"+label_as[k]+"_"+str(distances[p])+"[:,1]*1000,color=dist_color[p],linestyle='-')")
        exec("plot_t_"+str(distances[p])+", = plt.plot(topo_rate_t_"+str(distances[p])+"[:,0],topo_rate_t_"+str(distances[p])+"[:,1]*1000,color=dist_color[p],linestyle='--')")
        exec("plot_ab_"+str(distances[p])+", = plt.plot(topo_rate_ab_"+str(distances[p])+"[:,0],topo_rate_ab_"+str(distances[p])+"[:,1]*1000,color=dist_color[p],linestyle='dashdot')")
    plt.xlim([0,200]) 
    plt.ylim([-0.08,0.01])
    plt.xlabel('Time [yr]',fontsize=25)
    plt.ylabel('Vertical surface deformation rate [mm/yr]',fontsize=15)
    legend1 = plt.legend([plot_as_0,plot_t_0,plot_ab_0],['ASPECT','TABOO','Abaqus'],fontsize=20,loc=4,bbox_to_anchor=(-1.0, 1.00))
    plt.legend([plot_as_0,plot_as_100,plot_as_250],['0 km','100 km','250 km'],loc=4,fontsize=20,bbox_to_anchor=(1, 1))
    ax = plt.gca()
    ax.tick_params(axis='both',labelsize=20)
    plt.grid(which='major')
    plt.gca().add_artist(legend1)
    fig.subplots_adjust(wspace=0.3)
    #plt.show()
    # plot looks bad
    plt.tight_layout()
    filename = output_dir_base + model_name[k] + "/"  + label_as[k] + '_uplift.png'
    plt.savefig(filename, dpi=300)
       

if False:
  # average absolute and percentage difference aspect (new_cf) and taboo
  topo1_1loc_0_avg_dev = np.sum(np.abs(topo_1loc_t_0-topo_1loc_as_new_cf_ref_0))/len(topo_1loc_t_0)
  topo1_1loc_0_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_0[1:]-topo_1loc_as_new_cf_ref_0[1:])/topo_1loc_t_0[1:]*100))/len(topo_1loc_t_0)
  topo1_1loc_100_avg_dev = np.sum(np.abs(topo_1loc_t_100-topo_1loc_as_new_cf_ref_100))/len(topo_1loc_t_100)
  topo1_1loc_100_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_100[1:]-topo_1loc_as_new_cf_ref_100[1:])/topo_1loc_t_100[1:]*100))/len(topo_1loc_t_100)
  topo1_1loc_250_avg_dev = np.sum(np.abs(topo_1loc_t_250-topo_1loc_as_new_cf_ref_250))/len(topo_1loc_t_250)
  topo1_1loc_250_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_250[1:]-topo_1loc_as_new_cf_ref_250[1:])/topo_1loc_t_250[1:]*100))/len(topo_1loc_t_250)
  topo1_1loc_500_avg_dev = np.sum(np.abs(topo_1loc_t_500-topo_1loc_as_new_cf_ref_500))/len(topo_1loc_t_500)
  topo1_1loc_500_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_500[1:]-topo_1loc_as_new_cf_ref_500[1:])/topo_1loc_t_500[1:]*100))/len(topo_1loc_t_500)
  
  topo1_rate_0_avg_dev = np.sum(np.abs(topo_rate_t_0[:,1]-topo_rate_as_new_cf_ref_0[:,1]))/len(topo_rate_t_0[:,1])
  topo1_rate_0_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_0[:,1]-topo_rate_as_new_cf_ref_0[:,1])/topo_rate_t_0[:,1]*100))/len(topo_rate_t_0)
  topo1_rate_100_avg_dev = np.sum(np.abs(topo_rate_t_100[:,1]-topo_rate_as_new_cf_ref_100[:,1]))/len(topo_rate_t_100[:,1])
  topo1_rate_100_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_100[:,1]-topo_rate_as_new_cf_ref_100[:,1])/topo_rate_t_100[:,1]*100))/len(topo_rate_t_100)
  topo1_rate_250_avg_dev = np.sum(np.abs(topo_rate_t_250[:,1]-topo_rate_as_new_cf_ref_250[:,1]))/len(topo_rate_t_250[:,1])
  topo1_rate_250_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_250[:,1]-topo_rate_as_new_cf_ref_250[:,1])/topo_rate_t_250[:,1]*100))/len(topo_rate_t_250)
  topo1_rate_500_avg_dev = np.sum(np.abs(topo_rate_t_500[:,1]-topo_rate_as_new_cf_ref_500[:,1]))/len(topo_rate_t_500[:,1])
  topo1_rate_500_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_500[:,1]-topo_rate_as_new_cf_ref_500[:,1])/topo_rate_t_500[:,1]*100))/len(topo_rate_t_500)
  
  # average absolute and percentage difference aspect (old_cf) and taboo
  topo2_1loc_0_avg_dev = np.sum(np.abs(topo_1loc_t_0-topo_1loc_as_old_cf_ref_0))/len(topo_1loc_t_0)
  topo2_1loc_0_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_0[1:]-topo_1loc_as_old_cf_ref_0[1:])/topo_1loc_t_0[1:]*100))/len(topo_1loc_t_0)
  topo2_1loc_100_avg_dev = np.sum(np.abs(topo_1loc_t_100-topo_1loc_as_old_cf_ref_100))/len(topo_1loc_t_100)
  topo2_1loc_100_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_100[1:]-topo_1loc_as_old_cf_ref_100[1:])/topo_1loc_t_100[1:]*100))/len(topo_1loc_t_100)
  topo2_1loc_250_avg_dev = np.sum(np.abs(topo_1loc_t_250-topo_1loc_as_old_cf_ref_250))/len(topo_1loc_t_250)
  topo2_1loc_250_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_250[1:]-topo_1loc_as_old_cf_ref_250[1:])/topo_1loc_t_250[1:]*100))/len(topo_1loc_t_250)
  topo2_1loc_500_avg_dev = np.sum(np.abs(topo_1loc_t_500-topo_1loc_as_old_cf_ref_500))/len(topo_1loc_t_500)
  topo2_1loc_500_avg_dev_perc2 = np.sum(np.abs((topo_1loc_t_500[1:]-topo_1loc_as_old_cf_ref_500[1:])/topo_1loc_t_500[1:]*100))/len(topo_1loc_t_500)
  
  topo2_rate_0_avg_dev = np.sum(np.abs(topo_rate_t_0[:,1]-topo_rate_as_old_cf_ref_0[:,1]))/len(topo_rate_t_0[:,1])
  topo2_rate_0_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_0[:,1]-topo_rate_as_old_cf_ref_0[:,1])/topo_rate_t_0[:,1]*100))/len(topo_rate_t_0)
  topo2_rate_100_avg_dev = np.sum(np.abs(topo_rate_t_100[:,1]-topo_rate_as_old_cf_ref_100[:,1]))/len(topo_rate_t_100[:,1])
  topo2_rate_100_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_100[:,1]-topo_rate_as_old_cf_ref_100[:,1])/topo_rate_t_100[:,1]*100))/len(topo_rate_t_100)
  topo2_rate_250_avg_dev = np.sum(np.abs(topo_rate_t_250[:,1]-topo_rate_as_old_cf_ref_250[:,1]))/len(topo_rate_t_250[:,1])
  topo2_rate_250_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_250[:,1]-topo_rate_as_old_cf_ref_250[:,1])/topo_rate_t_250[:,1]*100))/len(topo_rate_t_250)
  topo2_rate_500_avg_dev = np.sum(np.abs(topo_rate_t_500[:,1]-topo_rate_as_old_cf_ref_500[:,1]))/len(topo_rate_t_500[:,1])
  topo2_rate_500_avg_dev_perc2 = np.sum(np.abs((topo_rate_t_500[:,1]-topo_rate_as_old_cf_ref_500[:,1])/topo_rate_t_500[:,1]*100))/len(topo_rate_t_500)
  
  # average absolute and percentage difference aspect (new_cf) and abaqus
  topo3_1loc_0_avg_dev = np.sum(np.abs(topo_1loc_ab_0-topo_1loc_as_new_cf_ref_0))/len(topo_1loc_ab_0)
  topo3_1loc_0_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_0[1:]-topo_1loc_as_new_cf_ref_0[1:])/topo_1loc_ab_0[1:]*100))/len(topo_1loc_ab_0)
  topo3_1loc_100_avg_dev = np.sum(np.abs(topo_1loc_ab_100-topo_1loc_as_new_cf_ref_100))/len(topo_1loc_ab_100)
  topo3_1loc_100_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_100[1:]-topo_1loc_as_new_cf_ref_100[1:])/topo_1loc_ab_100[1:]*100))/len(topo_1loc_ab_100)
  topo3_1loc_250_avg_dev = np.sum(np.abs(topo_1loc_ab_250-topo_1loc_as_new_cf_ref_250))/len(topo_1loc_ab_250)
  topo3_1loc_250_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_250[1:]-topo_1loc_as_new_cf_ref_250[1:])/topo_1loc_ab_250[1:]*100))/len(topo_1loc_ab_250)
  topo3_1loc_500_avg_dev = np.sum(np.abs(topo_1loc_ab_500-topo_1loc_as_new_cf_ref_500))/len(topo_1loc_ab_500)
  topo3_1loc_500_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_500[1:]-topo_1loc_as_new_cf_ref_500[1:])/topo_1loc_ab_500[1:]*100))/len(topo_1loc_ab_500)
  
  topo3_rate_0_avg_dev = np.sum(np.abs(topo_rate_ab_0[:,1]-topo_rate_as_new_cf_ref_0[:,1]))/len(topo_rate_ab_0[:,1])
  topo3_rate_0_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_0[:,1]-topo_rate_as_new_cf_ref_0[:,1])/topo_rate_ab_0[:,1]*100))/len(topo_rate_ab_0)
  topo3_rate_100_avg_dev = np.sum(np.abs(topo_rate_ab_100[:,1]-topo_rate_as_new_cf_ref_100[:,1]))/len(topo_rate_ab_100[:,1])
  topo3_rate_100_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_100[:,1]-topo_rate_as_new_cf_ref_100[:,1])/topo_rate_ab_100[:,1]*100))/len(topo_rate_ab_100)
  topo3_rate_250_avg_dev = np.sum(np.abs(topo_rate_ab_250[:,1]-topo_rate_as_new_cf_ref_250[:,1]))/len(topo_rate_ab_250[:,1])
  topo3_rate_250_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_250[:,1]-topo_rate_as_new_cf_ref_250[:,1])/topo_rate_ab_250[:,1]*100))/len(topo_rate_ab_250)
  topo3_rate_500_avg_dev = np.sum(np.abs(topo_rate_ab_500[:,1]-topo_rate_as_new_cf_ref_500[:,1]))/len(topo_rate_ab_500[:,1])
  topo3_rate_500_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_500[:,1]-topo_rate_as_new_cf_ref_500[:,1])/topo_rate_ab_500[:,1]*100))/len(topo_rate_ab_500)
  
  # average absolute and percentage difference aspect (old_cf) and abaqus
  topo4_1loc_0_avg_dev = np.sum(np.abs(topo_1loc_ab_0-topo_1loc_as_old_cf_ref_0))/len(topo_1loc_ab_0)
  topo4_1loc_0_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_0[1:]-topo_1loc_as_old_cf_ref_0[1:])/topo_1loc_ab_0[1:]*100))/len(topo_1loc_ab_0)
  topo4_1loc_100_avg_dev = np.sum(np.abs(topo_1loc_ab_100-topo_1loc_as_old_cf_ref_100))/len(topo_1loc_ab_100)
  topo4_1loc_100_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_100[1:]-topo_1loc_as_old_cf_ref_100[1:])/topo_1loc_ab_100[1:]*100))/len(topo_1loc_ab_100)
  topo4_1loc_250_avg_dev = np.sum(np.abs(topo_1loc_ab_250-topo_1loc_as_old_cf_ref_250))/len(topo_1loc_ab_250)
  topo4_1loc_250_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_250[1:]-topo_1loc_as_old_cf_ref_250[1:])/topo_1loc_ab_250[1:]*100))/len(topo_1loc_ab_250)
  topo4_1loc_500_avg_dev = np.sum(np.abs(topo_1loc_ab_500-topo_1loc_as_old_cf_ref_500))/len(topo_1loc_ab_500)
  topo4_1loc_500_avg_dev_perc2 = np.sum(np.abs((topo_1loc_ab_500[1:]-topo_1loc_as_old_cf_ref_500[1:])/topo_1loc_ab_500[1:]*100))/len(topo_1loc_ab_500)
  
  topo4_rate_0_avg_dev = np.sum(np.abs(topo_rate_ab_0[:,1]-topo_rate_as_old_cf_ref_0[:,1]))/len(topo_rate_ab_0[:,1])
  topo4_rate_0_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_0[:,1]-topo_rate_as_old_cf_ref_0[:,1])/topo_rate_ab_0[:,1]*100))/len(topo_rate_ab_0)
  topo4_rate_100_avg_dev = np.sum(np.abs(topo_rate_ab_100[:,1]-topo_rate_as_old_cf_ref_100[:,1]))/len(topo_rate_ab_100[:,1])
  topo4_rate_100_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_100[:,1]-topo_rate_as_old_cf_ref_100[:,1])/topo_rate_ab_100[:,1]*100))/len(topo_rate_ab_100)
  topo4_rate_250_avg_dev = np.sum(np.abs(topo_rate_ab_250[:,1]-topo_rate_as_old_cf_ref_250[:,1]))/len(topo_rate_ab_250[:,1])
  topo4_rate_250_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_250[:,1]-topo_rate_as_old_cf_ref_250[:,1])/topo_rate_ab_250[:,1]*100))/len(topo_rate_ab_250)
  topo4_rate_500_avg_dev = np.sum(np.abs(topo_rate_ab_500[:,1]-topo_rate_as_old_cf_ref_500[:,1]))/len(topo_rate_ab_500[:,1])
  topo4_rate_500_avg_dev_perc2 = np.sum(np.abs((topo_rate_ab_500[:,1]-topo_rate_as_old_cf_ref_500[:,1])/topo_rate_ab_500[:,1]*100))/len(topo_rate_ab_500)
  
  # average absolute and percentage difference aspect (new_cf) and aspect (old_cf)
  topo5_1loc_0_avg_dev = np.sum(np.abs(topo_1loc_as_old_cf_ref_0-topo_1loc_as_new_cf_ref_0))/len(topo_1loc_as_old_cf_ref_0)
  topo5_1loc_0_avg_dev_perc2 = np.sum(np.abs((topo_1loc_as_old_cf_ref_0[1:]-topo_1loc_as_new_cf_ref_0[1:])/topo_1loc_as_old_cf_ref_0[1:]*100))/len(topo_1loc_as_old_cf_ref_0)
  topo5_1loc_100_avg_dev = np.sum(np.abs(topo_1loc_as_old_cf_ref_100-topo_1loc_as_new_cf_ref_100))/len(topo_1loc_as_old_cf_ref_100)
  topo5_1loc_100_avg_dev_perc2 = np.sum(np.abs((topo_1loc_as_old_cf_ref_100[1:]-topo_1loc_as_new_cf_ref_100[1:])/topo_1loc_as_old_cf_ref_100[1:]*100))/len(topo_1loc_as_old_cf_ref_100)
  topo5_1loc_250_avg_dev = np.sum(np.abs(topo_1loc_as_old_cf_ref_250-topo_1loc_as_new_cf_ref_250))/len(topo_1loc_as_old_cf_ref_250)
  topo5_1loc_250_avg_dev_perc2 = np.sum(np.abs((topo_1loc_as_old_cf_ref_250[1:]-topo_1loc_as_new_cf_ref_250[1:])/topo_1loc_as_old_cf_ref_250[1:]*100))/len(topo_1loc_as_old_cf_ref_250)
  topo5_1loc_500_avg_dev = np.sum(np.abs(topo_1loc_as_old_cf_ref_500-topo_1loc_as_new_cf_ref_500))/len(topo_1loc_as_old_cf_ref_500)
  topo5_1loc_500_avg_dev_perc2 = np.sum(np.abs((topo_1loc_as_old_cf_ref_500[1:]-topo_1loc_as_new_cf_ref_500[1:])/topo_1loc_as_old_cf_ref_500[1:]*100))/len(topo_1loc_as_old_cf_ref_500)
  
  topo5_rate_0_avg_dev = np.sum(np.abs(topo_rate_as_old_cf_ref_0[:,1]-topo_rate_as_new_cf_ref_0[:,1]))/len(topo_rate_as_old_cf_ref_0[:,1])
  topo5_rate_0_avg_dev_perc2 = np.sum(np.abs((topo_rate_as_old_cf_ref_0[:,1]-topo_rate_as_new_cf_ref_0[:,1])/topo_rate_as_old_cf_ref_0[:,1]*100))/len(topo_rate_as_old_cf_ref_0)
  topo5_rate_100_avg_dev = np.sum(np.abs(topo_rate_as_old_cf_ref_100[:,1]-topo_rate_as_new_cf_ref_100[:,1]))/len(topo_rate_as_old_cf_ref_100[:,1])
  topo5_rate_100_avg_dev_perc2 = np.sum(np.abs((topo_rate_as_old_cf_ref_100[:,1]-topo_rate_as_new_cf_ref_100[:,1])/topo_rate_as_old_cf_ref_100[:,1]*100))/len(topo_rate_as_old_cf_ref_100)
  topo5_rate_250_avg_dev = np.sum(np.abs(topo_rate_as_old_cf_ref_250[:,1]-topo_rate_as_new_cf_ref_250[:,1]))/len(topo_rate_as_old_cf_ref_250[:,1])
  topo5_rate_250_avg_dev_perc2 = np.sum(np.abs((topo_rate_as_old_cf_ref_250[:,1]-topo_rate_as_new_cf_ref_250[:,1])/topo_rate_as_old_cf_ref_250[:,1]*100))/len(topo_rate_as_old_cf_ref_250)
  topo5_rate_500_avg_dev = np.sum(np.abs(topo_rate_as_old_cf_ref_500[:,1]-topo_rate_as_new_cf_ref_500[:,1]))/len(topo_rate_as_old_cf_ref_500[:,1])
  topo5_rate_500_avg_dev_perc2 = np.sum(np.abs((topo_rate_as_old_cf_ref_500[:,1]-topo_rate_as_new_cf_ref_500[:,1])/topo_rate_as_old_cf_ref_500[:,1]*100))/len(topo_rate_as_old_cf_ref_500)
