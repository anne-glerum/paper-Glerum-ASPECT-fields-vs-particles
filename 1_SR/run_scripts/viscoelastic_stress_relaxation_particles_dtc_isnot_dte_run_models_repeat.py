import os
from os.path import exists
import re

# Generate a new prm file and jobscript for each refinement level and timestep.
def generate_and_run( refine, n_particles, timestep, elastic_timestep, interpolator, reps):
  prmfile = open("viscoelastic_relaxation_particles.prm", "r")
  base_label = "ve_relaxation_particles_main_"
  label = "interpolator" + interpolator + "_dtc" + str(timestep) + "_dte" + str(elastic_timestep) + "_GR" + str(refine) + "_np" + str(n_particles) + "_" + str(reps)
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
    elif 'Interpolation scheme' in l:
      outfile.write('  set Interpolation scheme        = %s\n'%(re.sub('_',' ',interpolator)) )
    elif 'Number of particles per cell per direction' in l:
      outfile.write('      set Number of particles per cell per direction = %i\n'%(n_particles) )
    elif 'Minimum particles per cell' in l:
      outfile.write('    set Minimum particles per cell = %i\n'%(n_particles*n_particles) )
    elif 'Maximum particles per cell' in l:
      outfile.write('    set Maximum particles per cell = %i\n'%(n_particles*n_particles) )
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
    elif 'mpirun' in l:
     outjobscript.write('mpirun --map-by socket:pe=$OMP_NUM_THREADS ~/../projects/bbp00039/aspect_subtopic/aspect_rift/aspect_initial_conditions_rift_dealii_v9.6.0/build_01072025/aspect-release ' + new_prmfile + ' > /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM1/' + base_label + label + '/opla' )
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
particles = [8,16]
elastic_timesteps = [250]
timesteps = [250]
# write with underscores instead of spaces
interpolator = ["cell_average"] 
#interpolator = ["bilinear_least_squares", "quadratic_least_squares", "harmonic_average"] 
#interpolator = ["bilinear_least_squares", "nearest_neighbor", "quadratic_least_squares", "harmonic_average"] 
#interpolator = ["cell_average", "bilinear_least_squares", "nearest_neighbor", "quadratic_least_squares"] 
repeats = [1,2,3] 
for r in refinements:
  for p in particles:
    for te in elastic_timesteps:
      for t in timesteps:
        for i in interpolator:
          for reps in repeats:
            generate_and_run(r,p,t,te,i,reps)
