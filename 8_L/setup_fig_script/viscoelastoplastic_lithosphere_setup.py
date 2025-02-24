# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import ConnectionPatch
import matplotlib as mpl
mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [km]
z_bottom=80 		# Depth of the bottom boundary [km]
x_left=0 		# Distance of left lateral boundary [km]
x_right=160 		# Distance of right lateral boundary [km]

# -------------------------------------Setup-------------------------------------------

#  Array definitions
M=np.ones((230,80))				# Array for material model 
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [km]
zs=np.linspace(z_surface,z_bottom,len(M[:,0]))	# Depth array [km]
density=np.ones(len(zs))			# Density Array [kg/m3]
viscosity=np.ones(len(zs))			# Viscosity Array [Pas]

# Create setup structure; two materials fill the domain
for i in range(len(M[:,0])):
	for j in range(len(M[0,:])):
			if (zs[i]<=70 and 80-zs[i]<=185+2-7./4.*x[j] and 80-zs[i]>=185-2-7./4.*x[j]):
				M[i,j]=2
			density[i]=2900
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
ax.text(5,40,'Prescribed $v_x$,',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(10,40,'$v_y$ free',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(-2,7.5,'$v_x=-2.5$ mm/yr',fontsize=9, rotation = 0, va = 'center', ha = 'right')
ax.text(150,40,'Prescribed $v_x$,',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(155,40,'$v_y$ free',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(162,7.5,'$v_x=2.5$ mm/yr',fontsize=9, rotation = 0, va = 'center', ha = 'left')
ax.text(80,5,'Prescribed $v_y$, $v_x$ free. T = 1649 K.',fontsize=9, va = 'center', ha = 'center')
ax.text(80,75,'Free surface. T = 273 K.',fontsize=9, va = 'center', ha = 'center')

# Annotations material properties
# Mantle lithosphere
ax.text(20,61.0,r'$A_{\mathrm{disl}}=5.71 \cdot 10^{-23} \,\mathrm{Pa}^{-n} 1/\mathrm{s}$', fontsize=9, ha='left')
ax.text(20,56.0,r'$n=3$', fontsize=9, ha='left')
ax.text(20,51.0,r'$E_{\mathrm{disl}}=345 \cdot \mathrm{kJ/mol}$', fontsize=9, ha='left')
ax.text(20,46.0,r'$V_{\mathrm{disl}}=0 \cdot \mathrm{m}^3 1/\mathrm{mol}$', fontsize=9, ha='left')
ax.text(20,41,r'$G=1 \cdot 10^{11} \, \mathrm{Pa}$', fontsize=9, ha='left')
ax.text(20,36,r'$\phi=30^\circ$', fontsize=9, ha='left')
ax.text(20,31,r'$C=20$ $\mathrm{MPa}$', fontsize=9, ha='left')
ax.text(20,26,r'$\eta_{\mathrm{d}}=10^{21} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
ax.text(20,21,r'$\eta_{\mathrm{min}}=10^{18} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
ax.text(20,16,r'$\eta_{\mathrm{max}}=10^{26} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
ax.text(100,61,r'$k=2.5 \,\mathrm{W/m/K}$', fontsize=9, ha='left')
ax.text(100,56,r'$\alpha=2 \cdot 10^{-5}  \,\mathrm{1/K}$', fontsize=9, ha='left')
ax.text(100,51,r'$C_p=750 \,\mathrm{J/kg/K}$', fontsize=9, ha='left')
ax.text(100,46,'$g= 9.81 \, \mathrm{m/s^2}$', fontsize=9)
ax.text(100,41,r'$\rho=2900$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax.text(100,36,r'$H=0.25 \cdot 10^{-6}$ $\mathrm{W/m^3}$', fontsize=9, ha='left')
# Crust
#ax.text(25,-2,r'$\eta_{\mathrm{viscous}}=10^{20} \,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=9, ha='left')
#ax.text(25,-3.5,r'$G=10^{50} \, \mathrm{Pa}$', fontsize=9, ha='left')
#ax.text(25,-5,r'$C=10^{14} \, \mathrm{MPa}$', fontsize=9, ha='left')
#ax.arrow(20,0.2,4.9,-2,width=0.001,head_width=0, clip_on=False, fill=True, facecolor='black')
# Boundary velocity
ax.arrow(-0.10,15.00,-5,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.10,30.00,-5,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.10,45.00,-5,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.10,60.00,-5,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.10,75.00,-5,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(160.10,15.00,10,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(160.10,30.00,10,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(160.10,45.00,10,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(160.10,60.00,10,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(160.10,75.00,10,0,width=0.04,head_width=0.8, clip_on=False, fill=True, facecolor='black')

# Add Connection Patch
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_surface),coordsA='data',xyB=(2850,z_surface),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_bottom),coordsA='data',xyB=(2850,z_bottom),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))

# Save Figure
plt.savefig('8_viscoelastoplastic_lithosphere_setup.png',bbox_inches="tight",dpi=300)
plt.close()
