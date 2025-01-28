import os
from os.path import exists
import re

# Generate a new prm file and jobscript for each refinement level and timestep.
def generate_and_run( refine, n_particles, timestep, elastic_timestep, interpolator ):
  prmfile = open("viscoelastic_relaxation_particles_dtc_isnot_dte_bgvel.prm", "r")
  base_label = "ve_relaxation_particles_bgvel_"
  label = "interpolator" + interpolator + "_dtc" + str(timestep) + "_dte" + str(elastic_timestep) + "_GR" + str(refine) + "_np" + str(n_particles) + "_g0"
  new_prmfile = "viscoelastic_stress_relaxation_particles_" + label + ".prm"
  outfile = open(new_prmfile, "w")
  for l in prmfile.readlines():
    if 'Output directory' in l:
      outfile.write('set Output directory = /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM1/' + base_label + label + '\n')
    elif 'Initial global refinement' in l:
      outfile.write('  set Initial global refinement          = %i\n'%(refine) )
    elif 'Maximum time step' in l:
      outfile.write('set Maximum time step                      = %f\n'%(timestep) )
    elif 'Fixed elastic time step' in l:
      outfile.write('    set Fixed elastic time step     = %f\n'%(elastic_timestep) )
    elif 'Use fixed elastic time step' in l:
      if (timestep != elastic_timestep):
        outfile.write('    set Use fixed elastic time step = true\n')
      else:
        outfile.write('    set Use fixed elastic time step = false\n')
    elif 'set Function expression = 20e6; -20e6' in l:
      if (timestep == 125):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20079050; -20079050; 0\n' )
      elif (timestep == 250):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20158412; -20158412; 0\n' )
      elif (timestep == 500):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20318079; -20318079; 0\n' )
      elif (timestep == 5):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20003156; -20003156; 0\n' )
      elif (timestep == 25000):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 44021241; -44021241; 0\n' )
      elif (timestep == 0.01):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20000006; -20000006; 0\n' )
      elif (timestep == 0.1):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20000063; -20000063; 0\n' )
      elif (timestep == 1):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20000631; -20000631; 0\n' )
      elif (timestep == 25):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20015785; -20015785; 0\n' )
      elif (timestep == 2500):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 21641792; -21641792; 0\n' )
      elif (timestep == 62.5):
        outfile.write('    set Function expression = 20e6; -20e6; 0; 20039486; -20039486; 0\n' )
      else:
        print ('Unknown timestep')
    elif 'Interpolation scheme' in l:
      outfile.write('    set Interpolation scheme        = %s\n'%(re.sub('_',' ',interpolator)) )
    elif 'Number of particles per cell per direction' in l:
      outfile.write('        set Number of particles per cell per direction = %i\n'%(n_particles) )
    else:
      outfile.write(l)
  prmfile.close()
  outfile.close()

  # Generate a new jobscript file for each refinement level and timestep.
  jobscript = open("jobscript", "r")
  new_jobscript = "jobscript_particles_"+ label
  outjobscript = open(new_jobscript, "w")
  for l in jobscript.readlines():
    if '#SBATCH -J' in l:
      outjobscript.write('#SBATCH -J ' + base_label + label + '\n')
    elif '#SBATCH --tasks' in l and refine == 2:
      outjobscript.write('#SBATCH --tasks-per-node 4\n')
    elif 'mpirun' in l:
      outjobscript.write('mpirun --map-by socket:pe=$OMP_NUM_THREADS /home/bbpanneg/software/aspect/build_release__fix_stresses_elasticity_dealii_9.4.0_on_main_14072023/aspect ' + new_prmfile + ' > /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM1/' + base_label + label + '/opla' )
    else:
      outjobscript.write(l)
  jobscript.close()
  outjobscript.close()

  # Make new output directory
  if not exists('/scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM1/' + base_label + label):
    os.system('mkdir /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM1/' + base_label + label)
  
  # Submit simulation to run queue
  submit = 'sbatch '+ new_jobscript
  os.system(submit)

  print ('Model output in /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM1/' + base_label + label)

# Run the model at different refinement levels and timesteps
refinements = [2]
particles = [4]
elastic_timesteps = [62.5]
timesteps = [62.5]
# write with underscores instead of spaces
interpolator = ["cell_average"] 
#interpolator = ["bilinear_least_squares", "nearest_neighbor", "quadratic_least_squares", "harmonic_average"] 
for r in refinements:
  for p in particles:
    for te in elastic_timesteps:
      for t in timesteps:
        for i in interpolator:
          generate_and_run(r,p,t,te,i)
