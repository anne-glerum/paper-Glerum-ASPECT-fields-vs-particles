import os
from os.path import exists

# Generate a new prm file and jobscript for each refinement level and timestep.
def generate_and_run( refine, elastic_timestep, timestep ):
  prmfile = open("viscoelastic_stress_build-up_simple_shear_dtc_isnot_dte.prm", "r")
  base_label = "ve_build-up_simple_shear_"
  label = "dtc" + str(timestep) + "_dte" + str(elastic_timestep) + "_GR" + str(refine)
  new_prmfile = "viscoelastic_stress_build-up_simple_shear_" + label + ".prm"
  outfile = open(new_prmfile, "w")
  for l in prmfile.readlines():
    if 'Output directory' in l:
      outfile.write('set Output directory = /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/BM3/' + base_label + label + '\n')
    elif 'Initial global refinement' in l:
      outfile.write('  set Initial global refinement          = %i\n'%(refine) )
    elif 'Maximum time step' in l:
      outfile.write('set Maximum time step                      = %f\n'%(timestep) )
    elif 'Fixed elastic time step' in l:
      outfile.write('    set Fixed elastic time step     = %f\n'%(elastic_timestep) )
    elif 'Use fixed elastic time step' in l and timestep != elastic_timestep:
      outfile.write('    set Use fixed elastic time step = true \n' )
    else:
      outfile.write(l)
  prmfile.close()
  outfile.close()

  # Generate a new jobscript file for each refinement level and timestep.
  jobscript = open("jobscript", "r")
  new_jobscript = "jobscript_"+ label
  outjobscript = open(new_jobscript, "w")
  for l in jobscript.readlines():
    if '#SBATCH -J' in l:
      outjobscript.write('#SBATCH -J ' + base_label + label + '\n')
    elif '#SBATCH -t 0' in l and refine == 8:
      outjobscript.write('#SBATCH -t 03:30:00\n')
    elif '#SBATCH --tasks' in l and refine == 8:
      outjobscript.write('#SBATCH --tasks-per-node 96\n')
    elif '#SBATCH -p standard96' in l and refine == 8:
      outjobscript.write('#SBATCH -p standard96\n')
    elif 'mpirun' in l:
      outjobscript.write('mpirun --map-by socket:pe=$OMP_NUM_THREADS /home/bbpanneg/software/aspect/build_release__fix_stresses_elasticity_dealii_9.4.0/aspect ' + new_prmfile + ' > /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/BM3/' + base_label + label + '/opla' )
    else:
      outjobscript.write(l)
  jobscript.close()
  outjobscript.close()

  # Make new output directory
  if not exists('/scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/BM3/' + base_label + label):
    os.system('mkdir /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/BM3/' + base_label + label)
  
  # Submit simulation to run queue
  submit = 'sbatch '+ new_jobscript
  os.system(submit)

  print ('Model output in /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/BM3/' + base_label + label)

# Run the model at different refinement levels and timesteps
refinements = [8]
elastic_timesteps = [.005]
timesteps = [0.005]
for r in refinements:
  for et in elastic_timesteps:
    for t in timesteps:
      generate_and_run(r,et,t)
