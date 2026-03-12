# -*- coding: utf-8 -*-
"""
Created on Thur Oct 7 by David Quiroga
Modified on Tues Oct 19 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Rectangle
import matplotlib as mpl
mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [km]
z_bottom=2891 		# Depth of the bottom boundary [km]
x_left=0 		# Distance of left lateral boundary [km]
x_right=1500 		# Distance of right lateral boundary [km]
y_front=0 		# Distance of front lateral boundary [km]
y_back=1500 		# Distance of back lateral boundary [km]

# -------------------------------------Setup-------------------------------------------

#  Array definitions
n_M=4                                           # Nr of materials
M=np.ones((1000,100))				# Array for material model 
Mtop=np.zeros((1000,1000))			# Array for surface
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [km]
zs=np.linspace(z_surface,z_bottom,len(M[:,0]))	# Depth array [km]
xtop=np.linspace(x_left,x_right,len(Mtop[0,:]))	# Distance array [km]
ytop=np.linspace(y_back,y_front,len(Mtop[:,0]))	# Distance array [km]
density=np.ones(len(zs))			# Density Array [kg/m3]
viscosity=np.ones(len(zs))			# Viscosity Array [Pa s]
shear_modulus=np.ones(len(zs))			# Shear modulus Array [Pa]
gravity=np.ones(len(zs))			# Gravity Array [m/s2]

# Create setup structure with depth; 4 materials fill the domain
for i in range(len(M[:,0])):
  for j in range(len(M[0,:])):
    if zs[i] <= 70.:
      M[i,j]=1
    elif zs[i] >= 70. and zs[i] < 420.:
      M[i,j]=2
    elif zs[i] >= 420. and zs[i] < 670.:
      M[i,j]=3
    elif zs[i] >= 670.:
      M[i,j]=4

# zero in ice load area, which has radius = 100 km
for i in range(len(Mtop[:,0])):
  for j in range(len(Mtop[0,:])):
    if xtop[j]*xtop[j] + ytop[i]*ytop[i] > 10000.:
      Mtop[i,j]=1

density[0]=3037
viscosity[0]=1e40
shear_modulus[0]=0.50605e11
gravity[0]=9.815
density[1]=3438
viscosity[1]=1e21
shear_modulus[1]=0.70363e11
gravity[1]=9.854
density[2]=3871
viscosity[2]=1e21
shear_modulus[2]=1.05490e11
gravity[2]=9.897
density[3]=4978
viscosity[3]=2e21
shear_modulus[3]=2.28340e11
gravity[3]=10.024
#-----------------------------------------Plotting--------------------------------------------

# Create subplots
fig, (ax) = plt.subplots(1,2,figsize=(8,4),sharex=False, squeeze=True)

cmap = colors.ListedColormap(['darkblue', 'pink', 'palevioletred', 'lightsteelblue']) # Create customized discrete colormap
cmaptop = colors.ListedColormap(['white','darkblue']) # Create customized discrete colormap
im=ax[0].imshow(M,extent=[x_left, x_right, z_bottom, z_surface], cmap=cmap)
im2=ax[1].imshow(Mtop,extent=[x_left, x_right, y_front, y_back], cmap=cmaptop)
# a)
ax[0].set_yticks([z_bottom,670,420,z_surface])
ax[0].set_xticks([x_left,x_right/2, x_right])
ax[0].set_xlabel('X km]',fontsize=13)
ax[0].set_ylabel('Depth km]',fontsize=13)
ax[0].set_xlim(x_left,x_right)
ax[0].set_ylim(z_bottom,z_surface)
ax[0].text(0,-105,'(a) front view',fontsize=15)
plt.setp(ax[0].get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax[0].get_yticklabels(),fontsize=12, visible=True)
secy = ax[0].secondary_yaxis('right')
secy.set_yticks([70])
secy.set_yticklabels(["70"])
# b)
ax[1].set_yticks([y_front, y_back/2, y_back])
ax[1].set_xticks([x_left,x_right/2, x_right])
ax[1].set_xlabel('X km]',fontsize=13)
ax[1].set_ylabel('Y km]',fontsize=13)
ax[1].set_xlim(x_left,x_right)
ax[1].set_ylim(y_front,y_back)
ax[1].text(0,1555,'(b) top view',fontsize=15)
plt.setp(ax[1].get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax[1].get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
# Everything free slip except the top
ax[0].text(750,2800,'Free slip',fontsize=9, rotation = 0, va = 'center', ha = 'center')
ax[0].text(100,2000,'Free slip',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax[0].text(1400,2000,'Free slip',fontsize=9, rotation = -90, va = 'center', ha = 'center')
ax[1].text(750,750,'Prescribed traction',fontsize=9, rotation = 0, va = 'center', ha = 'center', color='white')
ax[1].text(60,750,'Free slip',fontsize=9, rotation = 90, va = 'center', ha = 'center', color='white')
ax[1].text(1440,750,'Free slip',fontsize=9, rotation = -90, va = 'center', ha = 'center', color='white')
ax[1].text(750,1440,'Free slip',fontsize=9, rotation = 0, va = 'center', ha = 'center', color='white')
ax[1].text(750,60,'Free slip',fontsize=9, rotation = 0, va = 'center', ha = 'center', color='white')
ax[1].text(200,100,'Ice load',fontsize=9, rotation = 0, va = 'center', ha = 'center', color='white')

# Annotations material properties
ax[1].text(750,1200,r'$\rho=$'+str(density[0])+' $\mathrm{kg/m^3}$', fontsize=8, ha='center', va='center', color='white')
ax[1].text(750,1140,'$\eta_{\mathrm{v}}=$'+str(viscosity[0])+ '$\,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=8, ha='center', va='center', color='white')
ax[1].text(750,1060,'$G=$'+str(shear_modulus[0]/1e9)+'$\, \mathrm{GPa}$', fontsize=8, ha='center', va='center', color='white')
ax[1].text(750,1000,'$g=$'+str(gravity[0])+'$\, \mathrm{m/s^2}$', fontsize=8, ha='center', va='center', color='white')
#ax[0].add_patch(Rectangle((530, 1220), 950, 490,fill=False,lw=1,edgecolor='darkblue'))
#ax[0].arrow(1400,1220,-100,-1180,width=1,head_width=0, clip_on=False, fill=True, color='darkblue')
#ax[0].text(550,670+640,r'$\rho=$'+str(density[0])+' $\mathrm{kg/m^3}$', fontsize=8, ha='left', va='center')
#ax[0].text(550,670+750,'$\eta_{\mathrm{v}}=$'+str(viscosity[0])+ '$\,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=8, ha='left', va='center')
#ax[0].text(550,670+860,'$G=$'+str(shear_modulus[0]/1e9)+'$\, \mathrm{GPa}$', fontsize=8, ha='left', va='center')
#ax[0].text(550,670+970,'$g=$'+str(gravity[0])+'$\, \mathrm{m/s^2}$', fontsize=8, ha='left', va='center')

ax[0].text(35,70+70,r'$\rho=$'+str(density[1])+' $\mathrm{kg/m^3}$', fontsize=7, ha='left', va='center')
ax[0].text(35,70+180,'$\eta_{\mathrm{v}}=$'+str(viscosity[1])+ '$\,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=7, ha='left', va='center')
ax[0].text(35,70+290,'$G=$'+str(shear_modulus[1]/1e9)+'$\, \mathrm{GPa}$', fontsize=7, ha='left', va='center')
ax[0].text(830,70+290,'$g=$'+str(gravity[1])+'$\, \mathrm{m/s^2}$', fontsize=7, ha='left', va='center')

ax[0].add_patch(Rectangle((35, 680), 950, 490,fill=False,lw=1,edgecolor='palevioletred'))
ax[0].arrow(70,680,100,-100,width=1,head_width=0, clip_on=False, fill=True, color='palevioletred')
ax[0].text(55,670+100,r'$\rho=$'+str(density[2])+' $\mathrm{kg/m^3}$', fontsize=8, ha='left', va='center')
ax[0].text(55,670+210,'$\eta_{\mathrm{v}}=$'+str(viscosity[2])+ '$\,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=8, ha='left', va='center')
ax[0].text(55,670+320,'$G=$'+str(shear_modulus[2]/1e9)+'$\, \mathrm{GPa}$', fontsize=8, ha='left', va='center')
ax[0].text(55,670+430,'$g=$'+str(gravity[2])+'$\, \mathrm{m/s^2}$', fontsize=8, ha='left', va='center')

ax[0].text(750,2891-640,r'$\rho=$'+str(density[3])+' $\mathrm{kg/m^3}$', fontsize=8, ha='center', va='center')
ax[0].text(750,2891-530,'$\eta_{\mathrm{v}}=$'+str(viscosity[3])+ '$\,\mathrm{Pa} \cdot \mathrm{s}$', fontsize=8, ha='center', va='center')
ax[0].text(750,2891-420,'$G=$'+str(shear_modulus[3]/1e9)+'$\, \mathrm{GPa}$', fontsize=8, ha='center', va='center')
ax[0].text(750,2891-310,'$g=$'+str(gravity[3])+'$\, \mathrm{m/s^2}$', fontsize=8, ha='center', va='center')

# Save Figure
plt.savefig('9_viscoelastic_3D_loading_setup.png',bbox_inches="tight")
plt.close()
