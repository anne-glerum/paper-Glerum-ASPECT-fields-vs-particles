# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import ConnectionPatch
import matplotlib as mpl
mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [km]
z_bottom=10 		# Depth of the bottom boundary [km]
x_left=0 		# Distance of left lateral boundary [km]
x_right=40 		# Distance of right lateral boundary [km]

# -------------------------------------Setup-------------------------------------------

#  Array definitions
M=np.ones((100,100))				# Array for material model 
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [km]
zs=np.linspace(z_surface,z_bottom,len(M[:,0]))	# Depth array [km]
density=np.ones(len(zs))			# Density Array [kg/m3]
viscosity=np.ones(len(zs))			# Viscosity Array [Pas]

# Create setup structure; two materials fill the domain
for i in range(len(M[:,0])):
	for j in range(len(M[0,:])):
			if (zs[i]>=9.6 and x[j]>=19.6 and x[j]<=20.4):
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
ax.set_xlabel('X [km]',fontsize=13)
ax.set_ylabel('Y [km]',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_surface,z_bottom)
#ax.text(0,5055,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax.text(1,5,'Prescribed $v_x$,',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(2,5,'$v_y$ free',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(-7,1.0,'$v_x=-1.2616$ mm/yr',fontsize=9, rotation = 0, va = 'center', ha = 'center')
ax.text(38,5,'Prescribed $v_x$,',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(39,5,'$v_y$ free',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(41,1.0,'$v_x=1.2616$ mm/yr',fontsize=9, rotation = 0, va = 'center', ha = 'left')
ax.text(4,1,'Free slip',fontsize=9, va = 'center', ha = 'left')
ax.text(20,9,'Free surface',fontsize=9, va = 'center', ha = 'center')

# Annotations material properties
# Medium
ax.text(4,7.0,r'$\eta_{\mathrm{viscous}}=10^{25} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
ax.text(4,5.5,r'$G=5 \cdot 10^{10} \, \mathrm{Pa}$', fontsize=9, ha='left')
ax.text(4,4,'$g= 10 \, \mathrm{m/s^2}$', fontsize=9)
ax.text(4,2.5,r'$\rho=2700$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax.text(25,7.0,r'$\phi=30^\circ$', fontsize=9, ha='left')
ax.text(25,5.5,r'$C=50$ $\mathrm{MPa}$', fontsize=9, ha='left')
ax.text(25,4.0,r'$\eta_{\mathrm{min}}=10^{20} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
ax.text(25,2.5,r'$\eta_{\mathrm{max}}=10^{25} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
# Beam
ax.text(25,-2,r'$\eta_{\mathrm{viscous}}=10^{20} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
ax.text(25,-3.5,r'$G=10^{50} \, \mathrm{Pa}$', fontsize=9, ha='left')
ax.text(25,-5,r'$C=10^{14} \, \mathrm{MPa}$', fontsize=9, ha='left')
ax.arrow(20,0.2,4.9,-2,width=0.001,head_width=0, clip_on=False, fill=True, facecolor='black')
# Boundary velocity
ax.arrow(-0.10,2.00,-1,0,width=0.04,head_width=0.4, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.10,8.00,-1,0,width=0.04,head_width=0.4, clip_on=False, fill=True, facecolor='black')
ax.arrow(40.10,2.00,1,0,width=0.04,head_width=0.4, clip_on=False, fill=True, facecolor='black')
ax.arrow(40.10,8.00,1,0,width=0.04,head_width=0.4, clip_on=False, fill=True, facecolor='black')

# Add Connection Patch
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_surface),coordsA='data',xyB=(2850,z_surface),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_bottom),coordsA='data',xyB=(2850,z_bottom),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))

# Save Figure
plt.savefig('7_viscoelastoplastic_brick_setup.png',bbox_inches="tight",dpi=300)
plt.close()
