import os
from os.path import exists

# Generate a new prm file and jobscript for each refinement level and timestep.
def generate_and_run( refine, timestep ):
  prmfile = open("viscoelastic_stress_build-up_particles.prm", "r")
  label = "particles_dt" + str(timestep) + "_GR" + str(refine)
  new_prmfile = "viscoelastic_stress_build-up_" + label + ".prm"
  outfile = open(new_prmfile, "w")
  for l in prmfile.readlines():
    if 'Output directory' in l:
      outfile.write('set Output directory = /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/ve_build-up_%s\n'%(label) )
    elif 'Initial global refinement' in l:
      outfile.write('  set Initial global refinement          = %i\n'%(refine) )
    elif 'Maximum time step' in l:
      outfile.write('set Maximum time step                      = %i\n'%(timestep) )
    elif 'Fixed elastic time step' in l:
      outfile.write('    set Fixed elastic time step     = %i\n'%(timestep) )
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
      outjobscript.write('#SBATCH -J ve_build-up_%s\n'%(label) )
    elif 'mpirun' in l:
      outjobscript.write('mpirun --map-by socket:pe=$OMP_NUM_THREADS /home/bbpanneg/software/aspect/build_release__fix_stresses_elasticity/aspect ' + new_prmfile + ' > /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/ve_build-up_' + label + '/opla' )
    else:
      outjobscript.write(l)
  jobscript.close()
  outjobscript.close()

  # Make new output directory
  if not exists('/scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/ve_build-up_' + label):
    os.system('mkdir /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/ve_build-up_' + label)
  
  # Submit simulation to run queue
  submit = 'sbatch '+ new_jobscript
  os.system(submit)

  print ('Model output in /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_11072022/ve_build-up_' + label)

# Run the model at different refinement levels and timesteps
refinements = range(0,2)
timesteps = [125, 250, 500]
for r in refinements:
  for t in timesteps:
    generate_and_run(r,t)