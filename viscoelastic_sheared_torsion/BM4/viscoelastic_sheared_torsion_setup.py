# -*- coding: utf-8 -*-
"""
Created on Thur Oct 7 by David Quiroga
Modified on Tues Oct 19 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import ConnectionPatch
import matplotlib as mpl
#mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [m]
z_bottom=1 		# Depth of the bottom boundary [m]
x_left=0 		# Distance of left lateral boundary [m]
x_right=1 		# Distance of right lateral boundary [m]

# -------------------------------------Setup-------------------------------------------

#  Array definitions
M=np.ones((100,100))				# Array for material model 
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [m]
zs=np.linspace(z_surface,z_bottom,len(M[:,0]))	# Depth array [m]
density=np.ones(len(zs))			# Density Array [m]
viscosity=np.ones(len(zs))			# Viscosity Array [m]

# Create setup structure; only one material fills the domain
for i in range(len(M[:,0])):
	for j in range(len(M[0,:])):
			M[i,j]=1
			density[i]=1
			viscosity[i]=1e2

#-----------------------------------------Plotting--------------------------------------------

# Create subplots
fig, (ax) = plt.subplots(1,2,figsize=(10,4),sharex=False, squeeze=True)

cmap = colors.ListedColormap(['lightsteelblue', 'pink','darkblue']) # Create customized discrete colormap
im=ax[0].imshow(M,extent=[x_left, x_right, z_surface, z_bottom], cmap=cmap)
im2=ax[1].imshow(M,extent=[x_left, x_right, z_surface, z_bottom], cmap=cmap)
#ax.spines['top'].set_visible(False)
# a)
ax[0].set_yticks([z_bottom/2, z_surface])
ax[0].set_xticks([x_left,x_right/2, x_right])
ax[0].set_xlabel('X [m]',fontsize=13)
ax[0].set_ylabel('Z [m]',fontsize=13)
ax[0].set_xlim(x_left,x_right)
ax[0].set_ylim(z_surface,z_bottom)
ax[0].text(0,1.05,'(a) front view',fontsize=15)
plt.setp(ax[0].get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax[0].get_yticklabels(),fontsize=12, visible=True)
# b)
ax[1].set_yticks([z_bottom/2])
ax[1].set_xticks([x_left,x_right/2, x_right])
ax[1].set_xlabel('X [m]',fontsize=13)
ax[1].set_ylabel('Y [m]',fontsize=13)
#ax2 = ax[1].twinx()
#ax2.set_ylabel('Y [m]',fontsize=13)
#ax2.set_ylim(z_surface,z_bottom)
#ax2.set_yticks([z_bottom/2, z_surface, z_bottom])
ax[1].set_xlim(x_left,x_right)
ax[1].set_ylim(z_surface,z_bottom)
ax[1].text(0,1.05,'(b) top view',fontsize=15)
plt.setp(ax[1].get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax[1].get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax[0].text(0.05,0.50,'Prescribed v',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax[0].text(0.95,0.50,'Prescribed v',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax[0].text(0.50,0.05,'Prescribed v',fontsize=9, va = 'center', ha = 'center')
ax[0].text(0.50,0.95,'Prescribed v',fontsize=9, va = 'center', ha = 'center')
ax[1].text(0.05,0.50,'Prescribed v',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax[1].text(0.95,0.50,'Prescribed v',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax[1].text(0.50,0.05,'Prescribed v',fontsize=9, va = 'center', ha = 'center')
ax[1].text(0.50,0.95,'Prescribed v',fontsize=9, va = 'center', ha = 'center')
# Left boundary
ax[0].arrow(-0.06,0.20,0.012,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(-0.07,0.40,0.024,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(-0.08,0.60,0.036,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(-0.09,0.80,0.048,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(-0.10,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')
# Top boundary
ax[0].arrow(0.20,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(0.50,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(0.75,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')

# Rotation: -sin(atan2(y,x))*sqrt(y*y+x*x)*42/360
def rotationx(x,y):
  cx = 0.5
  cy = 0.5
  return -np.sin(np.arctan2(y-cy,x-cx))*np.sqrt((y-cy)*(y-cy)+(x-cx)*(x-cx))*42/360
def rotationy(x,y):
  cx = 0.5
  cy = 0.5
  return np.cos(np.arctan2(y-cy,x-cx))*np.sqrt((y-cy)*(y-cy)+(x-cx)*(x-cx))*42/360
  
F = 0.06/0.3  
S = 0.3

print ("Vx (0,0), Vy (0,0)", (rotationx(0.,0)),rotationy(0,0))
print ("Vx (0,1), Vy (0,1)", (rotationx(0.,1)),rotationy(0,1))
print ("Vx (1,1), Vy (1,1)", (rotationx(1.,1)),rotationy(1,1))
print ("Vx (1,0), Vy (1,0)", (rotationx(1.,0)),rotationy(1,0))


ax[1].arrow(-0.10,1.00,F*(S+rotationx(-0.1,1)),F*rotationy(-0.1,1),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.20,1.00,F*(S+rotationx(0.20,1.00)),F*rotationy(0.20,1.00),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.50,1.00,F*(S+rotationx(0.5,1)),F*rotationy(0.5,1),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.75,1.00,F*(S+rotationx(0.75,1)),F*rotationy(0.75,1),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(1,1.00,F*(S+rotationx(1,1)),F*rotationy(1,1),width=0.008, clip_on=False, fill=True, facecolor='black')

ax[1].arrow(-0.10,0.80,F*(S+rotationx(-0.1,0.8)),F*rotationy(-0.1,0.8),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.2,0.80,F*(S+rotationx(0.2,0.8)),F*rotationy(0.2,0.8),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.50,0.80,F*(S+rotationx(0.5,0.8)),F*rotationy(0.5,0.8),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.75,0.80,F*(S+rotationx(0.75,0.8)),F*rotationy(0.75,0.8),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(1,0.80,F*(S+rotationx(1,0.8)),F*rotationy(1,0.8),width=0.008, clip_on=False, fill=True, facecolor='black')

ax[1].arrow(-0.10,0.60,F*(S+rotationx(-0.1,0.6)),F*rotationy(-0.1,1),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.2,0.60,F*(S+rotationx(0.2,0.6)),F*rotationy(0.2,0.6),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.50,0.60,F*(S+rotationx(0.5,0.6)),F*rotationy(0.5,0.6),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.75,0.60,F*(S+rotationx(0.75,0.6)),F*rotationy(0.75,0.6),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(1,0.60,F*(S+rotationx(1,0.6)),F*rotationy(1,0.6),width=0.008, clip_on=False, fill=True, facecolor='black')

ax[1].arrow(-0.10,0.40,F*(S+rotationx(-0.1,0.4)),F*rotationy(-0.1,0.4),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.2,0.40,F*(S+rotationx(0.2,0.4)),F*rotationy(0.2,0.4),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.50,0.40,F*(S+rotationx(0.5,0.4)),F*rotationy(0.5,0.4),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.75,0.40,F*(S+rotationx(0.75,0.4)),F*rotationy(0.75,0.4),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(1,0.40,F*(S+rotationx(1,0.4)),F*rotationy(1,0.4),width=0.008, clip_on=False, fill=True, facecolor='black')

ax[1].arrow(-0.10,0.20,F*(S+rotationx(-0.1,0.2)),F*rotationy(-0.1,0.2),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.2,0.20,F*(S+rotationx(0.2,0.2)),F*rotationy(0.2,0.2),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.50,0.20,F*(S+rotationx(0.5,0.2)),F*rotationy(0.5,0.2),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.75,0.20,F*(S+rotationx(0.75,0.2)),F*rotationy(0.75,0.2),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(1,0.20,F*(S+rotationx(1,0.2)),F*rotationy(1,0.2),width=0.008, clip_on=False, fill=True, facecolor='black')

ax[1].arrow(-0.10,0.00,F*(S+rotationx(-0.1,0)),F*rotationy(-0.1,0),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.2,0.00,F*(S+rotationx(0.2,0)),F*rotationy(0.2,0),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.50,0.00,F*(S+rotationx(0.5,0)),F*rotationy(0.5,0),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(0.75,0.00,F*(S+rotationx(0.75,0)),F*rotationy(0.75,0),width=0.008, clip_on=False, fill=True, facecolor='black')
ax[1].arrow(1,0.00,F*(S+rotationx(1,0.)),F*rotationy(1,0),width=0.008, clip_on=False, fill=True, facecolor='black')

# Right boundary
ax[0].arrow(1,0.20,0.012,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(1,0.40,0.024,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(1,0.60,0.036,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(1,0.80,0.048,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax[0].arrow(1,1.00,0.06,0,width=0.008, clip_on=False, fill=True, facecolor='black')
# Annotations velocity
ax[0].text(0.15,0.30,'$\mathrm{if} \, (t \leq 0.5)$', fontsize=8)
ax[0].text(0.15,0.25,'  $\mathrm{v_x}=-42/360 y + 0.3 z$ [m/s]', fontsize=8)
ax[0].text(0.15,0.20,'  S = 0.15', fontsize=8)
ax[0].text(0.15,0.15,'else', fontsize=8)
ax[0].text(0.15,0.10,'  $\mathrm{v_x}= $-42/360 y [m/s]', fontsize=8)
ax[0].text(0.15,0.05,'  S = 0.0', fontsize=8)
ax[0].text(0.6,0.20,'$\mathrm{v_y}=42/360 x$ [m/s]', fontsize=8)
ax[0].text(0.6,0.15,'$\mathrm{v_z}=0$ [m/s]', fontsize=8)
# Annotations material properties
ax[0].text(0.3,0.70,r'$\rho=1$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax[0].text(0.3,0.75,'$\eta_{\mathrm{viscous}}=10^{2} \,\mathrm{Pa} \cdot s$\n$G=10^{2} \, \mathrm{Pa}$', fontsize=9, ha='left')
# Annotations material properties
ax[0].text(0.3,0.60,r'$\dot{\epsilon} = \left( \begin{matrix} 0 & 0 & 0.15 \\ 0 & 0 & 0 \\ 0.15 & 0 & 0 \end{matrix}\right)$ 1/s', fontsize=9, ha='left', va='center',usetex=True)
ax[0].text(0.3,0.43,r'$\mathrm{W} = \left( \begin{matrix} 0 & -0.12 & S \\ 0.12 & 0 & 0 \\ -S & 0 & 0 \end{matrix}\right)$ 1/s', fontsize=9, ha='left', va='center',usetex=True)

# Add Connection Patch
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_surface),coordsA='data',xyB=(2850,z_surface),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_bottom),coordsA='data',xyB=(2850,z_bottom),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))

# Save Figure
plt.savefig('4_viscoelastic_sheared_torsion_setup.png',bbox_inches="tight")
plt.close()
