# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
#from scipy.integrate import simpson
from numpy import trapz
rc("pdf", fonttype=42)
rc("lines", linewidth=3, markersize=3)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_14072023/BM1/"

# Change file name modifiers as needed depending on your file structure
names = [
         "ve_relaxation_bgvel1e-12_IColdisnew_shearheating_dtc250_dte250_GR2_g0",
         "ve_relaxation_bgvel1e-12_IColdisnew_shearheating_dtc125_dte125_GR2_g0",
         "ve_relaxation_bgvel1e-12_IColdisnew_shearheating_dtc62.5_dte62.5_GR2_g0",
         "ve_relaxation_bgvel1e-12_IColdisnew_shearheating_dtc15.625_dte15.625_GR2_g0",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          r'dtc = dte = 250 yr',
          r'dtc = dte = 125 yr',
          r'dtc = dte = 62.5 yr',
          r'dtc = dte = 15.625 yr',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color2, color3, color4, color5, color6, color4, color5, color3, color4, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'dashdot', 'dashdot', 'dotted',  'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', '', '', '', '', '', ''] 

# Set up a row of two plots, one with heating rates
# and one with the percentage difference of tau^0_c to the analytical solution
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 2)]

# y-locations of text labels
y=[2.5e-8,2.0e-8,1.5e-8,1.0e-8,0.5e-8]
# timestep sizes
yr_in_secs = 3600. * 24. * 365.2425
dt=[250*yr_in_secs,125*yr_in_secs,62.5*yr_in_secs,15.625*yr_in_secs]

counter = 0 

# Create file path
for name in names: 
  path = base+name+tail

  # Read in the time, the mininum value of the xx component of the 
  # tau^0_c tensor, and the heating rate term.
  # The correct columns are selected with usecols.
  time,stress_xx_min,shear_heating = np.genfromtxt(path, comments='#', usecols=(1,18,39), unpack=True)

  # Plot shear heating rate against time in J/m3/s in
  # categorical batlow colors. We have to divide
  # by the model domain area, as the heating term is
  # integrated over the domain (J/s=W).
  ax[0].plot(time/1e3,shear_heating/1e10,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter])
  print ("Heating t=0: ", shear_heating[0]/1e10, " $\mathrm{Jm^{-3}s^1$")
  # Compute and plot the total integrated energy density (the area under the shear heating, i.e., integrated energy density, curve)
  area = trapz(shear_heating/1e10,time*yr_in_secs)
  print (r"Time-integrated released energy density: ", area, " J/m3")
  ax[0].text(135,y[counter],r"Released $\mathcal{E}$ density: " + "%.2f" % area + r" $\mathrm{Jm^{-3}}$",color=colors[counter])
  # Plot the error between ve_stress_xx and the analytical solution in %.
#  ax[1].plot(time/1e3,(stress_xx_min-(20e6*np.exp(-1e10*time*yr_in_secs/1e22)))/(20e6*np.exp(-1e10*time*yr_in_secs/1e22))*100.,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter])
  
  counter += 1

# Print the initial stored elastic energy density E = 1/2 1/G tau : 1/2 tau
# for each timestep size
mu=1e10 #Pas
eta_v=1e22 #Pas
tau0c = np.zeros((2,2)) #Pa
tau0c[0,0] = 20e6 #Pa
tau0c[1,1] = -20e6 #Pa
counter = 0
eps_T = np.zeros((2,2)) # 1/s
for timestep in dt:
  eta_el=timestep*mu
  eta_eff=1./(1./eta_v+1./eta_el)
  tau = tau0c * (eta_eff/eta_el)
  A = (0.5 * tau)
  B = (0.5 / mu * tau)
  E = np.einsum("ij,ij->",A,B)
  
  print ("Total stored elastic energy E: ", E, " J/m3 for dt = ", timestep/yr_in_secs)
  ax[0].text(25,y[counter],r"Stored $\mathcal{E}_{el}$ density t0: " + "%.2f" % E + r" $\mathrm{Jm^{-3}}$",color=colors[counter])
  
  # Also compute what heating statistics *should* output
  eps_vp = eps_T - ((tau - tau0c)/(2.*timestep*mu))
  Hs = np.einsum("ij,ij->",tau,eps_vp)
  print ("Shear heating Hs(t=0): ", Hs, " J/m3/s")
  counter += 1

# Labelling of plot
ax[0].set_xlabel("Time [ky]")
ax[0].set_ylabel(r"Shear heating rate [$\mathrm{Jm^{-3}s^{-1}}$]")
#ax[1].set_ylabel(r"Error for $\tau_{xx}$ [%]")
# Manually place legend in lower right corner. 
ax[0].legend(loc='upper right',ncol=2,handlelength=4)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].grid(axis='y',color='0.95')
#ax[1].grid(axis='x',color='0.95')
#ax[1].grid(axis='y',color='0.95')
#ax[1].set_yticks([0,2,4,6,8,10])

# Ranges of the axes
ax[0].set_xlim(0,250) # kyr
#ax[1].set_xlim(0,250) # kyr
#ax[1].set_ylim(0,10) # %

# Add labels a) and b)
ax[0].text(-15,4.2e-8,"d)")
#ax[1].text(-15,10,"b)")

# Save as png
png_name = '1_viscoelastic_relaxation_dte_isnot_dtc_fields_dtcdte_IColdisnew_shear_heating_fixedE_dh25km.png'
plt.savefig(png_name,dpi=300)
print ('Plot can be found in: ', png_name)
