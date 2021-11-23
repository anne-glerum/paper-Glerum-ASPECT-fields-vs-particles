# -*- coding: utf-8 -*-
"""
Created on Thur Oct 7 by David Quiroga
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import ConnectionPatch
from cmcrameri import cm
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [km]
z_moho=25 		# Depth of the Moho [km]
z_lab=100 		# Depth of the LAB [km]
z_upper_mantle=200 	# Depth of upper region of the mantle to show in detail in subplots [km]
z_bottom=670 		# Depth of the bottom boundary [km]
x_left=0 		# Distance of left lateral boundary [km]
x_right=1600 		# Distance of right lateral boundary [km]
A=25			# Amplitude of sinusoidal instability (km)
mu=1600  		# Wavelength of sinusoidal instability (km)


# -------------------------------------Setup-------------------------------------------

#  Array definitions
M=np.ones((670,1600))				# Array for material model 
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [km]
zs=np.linspace(z_surface,670,len(M[:,0]))	# Depth array [km]
z_RT=z_lab+A*-np.cos(2*(np.pi/mu)*x)		# RT instability [km]
density=np.ones(len(zs))			# Density Array [km]
viscosity=np.ones(len(zs))			# Viscosity Array [km]

# Create setup structure (alternatively can load data)
for i in range(len(M[:,0])):
	for j in range(len(M[0,:])):
		if(zs[i]<=z_moho):			# Crust
			M[i,j]=1
			density[i]=2900
			viscosity[i]=1e25
		if(zs[i]>z_moho and zs[i]<z_RT[j]): # Mantle Lithosphere
			M[i,j]=3
			density[i]=3300
			viscosity[i]=1e21
		if(zs[i]>z_RT[j]):			# Mantle
			M[i,j]=2
			density[i]=3100
			viscosity[i]=1e20

#-----------------------------------------Plotting--------------------------------------------

# Create subplots
fig, (ax,ax1,ax2) = plt.subplots(1,3,figsize=(14,4), gridspec_kw={'width_ratios': [4,0.8,0.8],'wspace':0.07,'hspace':0.25},sharex=False, squeeze=True)

cmap = colors.ListedColormap(['darkblue', 'lightsteelblue', 'pink']) # Create customized discrete colormap

im=ax.imshow(M,extent=[x_left, x_right, z_bottom, z_surface], cmap=cmap)
ax.spines['top'].set_visible(False)
ax.set_yticks([25,75,200,670])
ax.set_xticks([x_left,x_right])
ax.set_xlabel('Distance $[km]$',fontsize=13)
ax.set_ylabel('Depth $[km]$',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_bottom,z_surface)
ax.text(-10,-20,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Colorbar
cb=fig.colorbar(im,ax=ax, orientation='horizontal',aspect=50, fraction=0.031,pad=0.2,ticks=[1.35, 2, 2.65])
cb.ax.tick_params(labelsize=10, direction='out',pad=5)
cb.ax.set_xticklabels(['$Crust$', '$Mantle$\n $Lithosphere$','$Sublithosphere$\n $Mantle$'])

# Annotations - Boundary Conditions
ax.text(20,330,'$Free$\n $Slip$',fontsize=9)
ax.text(1505,330,'$Free$\n $Slip$',fontsize=9)
ax.text(760,640,'$No$ $Slip$',fontsize=9)
ax.text(720,-30,'$Free$ $Surface$',fontsize=9)

# Density subplot (create small individual line segments with different colors given by _ colormap)
points=np.transpose(np.array([density, zs])).reshape(-1, 1, 2)
segments=np.concatenate([points[:-1], points[1:]], axis=1)
norm=plt.Normalize(2950, 3200)
lc=LineCollection(segments, cmap=cmap, norm=norm,linewidth=2)
lc.set_array(density)
ax1.add_collection(lc)
#ax1.plot(density,zs,c='C0',linewidth=2)
ax1.set_xlabel(r'$\rho$ $[kg/m^3]$',fontsize=13)
ax1.set_ylim(z_surface,z_upper_mantle)
ax1.set_xlim(2850,3350)
ax1.set_yticks([25,75,200])
ax1.text(2850,-5,'(b)',fontsize=15)
ax1.get_shared_y_axes().join(ax1, ax2) # Share y axis between subplots
plt.setp(ax1.get_xticklabels(),fontsize=13, visible=True)
plt.setp(ax1.get_yticklabels(),fontsize=13, visible=True)

# Viscosity subplot (create small individual line segments with different colors given by _ colormap)
points=np.transpose(np.array([viscosity, zs])).reshape(-1, 1, 2)
segments=np.concatenate([points[:-1], points[1:]], axis=1)
norm=plt.Normalize(19,25)
cmap2 = colors.ListedColormap(['darkblue','pink','lightsteelblue']) # Create customized discrete colormap
lc=LineCollection(segments, cmap=cmap2.reversed(), norm=norm,linewidth=2)
lc.set_array(np.log10(viscosity))
ax2.add_collection(lc)
#ax2.plot(viscosity,zs,c='k',linewidth=2)
ax2.set_xscale('log')
ax2.set_xlabel(r'$\eta$ $[Pa \cdot s]$',fontsize=13)
ax2.set_ylim(z_surface,z_upper_mantle)
ax2.set_xlim(5e18,5e25)
ax2.set_yticks([25,75,200])
ax2.text(5e18,-5,'(c)',fontsize=15)
plt.setp(ax2.get_xticklabels(),fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(),fontsize=12, visible=False)
plt.gca().invert_yaxis()

# Annotations in viscosity subplot
ax2.plot(np.linspace(5e18,5e25,100),np.ones(100)*25,linestyle='--',c='k',linewidth=1)
ax2.plot(np.linspace(5e18,5e25,100),np.ones(100)*75,linestyle='--',c='k',linewidth=1)
ax2.text(2e21,20,'Crust',fontsize=8)
ax2.text(2e21,72,'Mantle\nLithosphere',fontsize=8)
ax2.text(2e21,150,'Sublithospheric\nMantle',fontsize=8)
ax2.text(6e18,34,r'$\mathbf{Moho}$',fontsize=8)
ax2.text(6e18,84,r'$\mathbf{LAB}$',fontsize=8)

# Add Connection Patch
ax.add_patch(ConnectionPatch(xyA=(x_right,z_surface),coordsA='data',xyB=(2850,z_surface),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))
ax.add_patch(ConnectionPatch(xyA=(x_right,z_upper_mantle),coordsA='data',xyB=(2850,z_upper_mantle),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))

# Save Figure
plt.savefig('RT_drip_setup.pdf',bbox_inches="tight")
plt.close()
