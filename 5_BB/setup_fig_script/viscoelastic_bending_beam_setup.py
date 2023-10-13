# -*- coding: utf-8 -*-
"""
Created by David Quiroga
Modified by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import ConnectionPatch
import matplotlib as mpl
mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [m]
z_bottom=5000 		# Depth of the bottom boundary [m]
x_left=0 		# Distance of left lateral boundary [m]
x_right=7500 		# Distance of right lateral boundary [m]

# -------------------------------------Setup-------------------------------------------

#  Array definitions
M=np.ones((100,100))				# Array for material model 
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [m]
zs=np.linspace(z_surface,z_bottom,len(M[:,0]))	# Depth array [m]
density=np.ones(len(zs))			# Density Array [m]
viscosity=np.ones(len(zs))			# Viscosity Array [m]

# Create setup structure; two materials fill the domain
for i in range(len(M[:,0])):
	for j in range(len(M[0,:])):
			if (x[j]<=4800 and zs[i]<=2800 and zs[i]>=2200):
				M[i,j]=2
			density[i]=2800
			viscosity[i]=1e18

#-----------------------------------------Plotting--------------------------------------------

# Create subplots
fig, (ax) = plt.subplots(1,1,figsize=(6,4),sharex=False, squeeze=True)

cmap = colors.ListedColormap(['lightsteelblue', 'darkblue','pink']) # Create customized discrete colormap
im=ax.imshow(M,extent=[x_left, x_right, z_surface, z_bottom], cmap=cmap)
#ax.spines['top'].set_visible(False)
ax.set_yticks([z_bottom,z_bottom/2, z_surface])
ax.set_xticks([x_left,x_right/2, x_right])
ax.set_xlabel('X [m]',fontsize=13)
ax.set_ylabel('Y [m]',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_surface,z_bottom)
#ax.text(0,5055,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax.text(300,3900,'Zero slip',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(7200,2500,'Free slip',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(3750,300,'Free slip',fontsize=9, va = 'center', ha = 'center')
ax.text(3750,4700,'Free slip',fontsize=9, va = 'center', ha = 'center')

# Annotations material properties
# Medium
ax.text(3050,4100,'$\mathrm{if} \, (t \leq 50000 \, \mathrm{yr})$', fontsize=9, ha='left')
ax.text(3050,3800,'  $\mathrm{g}= 10 \, \mathrm{m/s^2}$', fontsize=9)
ax.text(3050,3500,'$\mathrm{else}$', fontsize=9, ha='left')
ax.text(3050,3200,'  $\mathrm{g}= 0 \, \mathrm{m/s^2}$', fontsize=9)
ax.text(3050,1200,r'$\eta_{\mathrm{viscous}}=10^{18} \,\mathrm{Pa} \cdot s$', fontsize=9, ha='left')
ax.text(3050,900,r'$G=10^{11} \, \mathrm{Pa}$', fontsize=9, ha='left')
ax.text(3050,600,r'$\rho=2800$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
# Beam
ax.text(700,1800,r'$\eta_{\mathrm{viscous}}=10^{24} \,\mathrm{Pa} \cdot s$', fontsize=9, ha='left')
ax.text(700,1500,r'$G=10^{10} \, \mathrm{Pa}$', fontsize=9, ha='left')
ax.text(700,1200,r'$\rho=3300$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax.arrow(690,1900,100,500,width=6,head_width=0, clip_on=False, fill=True, facecolor='black')

# Add Connection Patch
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_surface),coordsA='data',xyB=(2850,z_surface),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_bottom),coordsA='data',xyB=(2850,z_bottom),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))

# Save Figure
plt.savefig('5_viscoelastic_bending_beam_setup.png',bbox_inches="tight")
plt.close()
