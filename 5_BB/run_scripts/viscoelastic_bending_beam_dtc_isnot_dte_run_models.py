import os
from os.path import exists
import re

# Generate a new prm file and jobscript for each refinement level and timestep.
def generate_and_run( iar, igr, timestep, elastic_timestep, averaging ):
  prmfile = open("viscoelastic_bending_beam_smooth_dtc_isnot_dte_12062024.prm", "r")
  #prmfile = open("viscoelastic_bending_beam_dtc_isnot_dte_12062024.prm", "r")
  base_label = "RL9_viscoelastic_bending_beam_smooth25m_DGlimiter_Newton_"
  #base_label = "RL9_viscoelastic_bending_beam_DGlimiter_Newton_"
  label = "dtc" + str(timestep) + "_dte" + str(elastic_timestep) + "_averaging" + averaging + "_IGR" + str(igr) + "_IAR" + str(iar)
  new_prmfile = base_label + label + ".prm"
  outfile = open(new_prmfile, "w")
  for l in prmfile.readlines():
    if 'Output directory' in l:
      outfile.write('set Output directory = /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM5/' + base_label + label + '\n')
    elif 'Initial global refinement' in l:
      outfile.write('  set Initial global refinement          = %i\n'%(igr) )
    elif 'Initial adaptive refinement' in l:
      outfile.write('  set Initial adaptive refinement        = %i\n'%(iar) )
    elif 'set Function expression = if (x<=5.2e3 && y>=1.6e3 && y<=3.0e3' in l:
      outfile.write('    set Function expression = if (x<=5.2e3 && y>=1.6e3 && y<=3.0e3, %i, %i)\n'%(iar+igr,igr) )
    elif 'set Maximum time step' in l:
      outfile.write('set Maximum time step                      = %f\n'%(timestep) )
    elif 'Fixed elastic time step' in l:
      outfile.write('    set Fixed elastic time step     = %f\n'%(elastic_timestep) )
    elif 'Use fixed elastic time step' in l and timestep != elastic_timestep:
      outfile.write('    set Use fixed elastic time step = true \n' )
    elif 'Viscosity averaging scheme' in l:
      outfile.write('    set Viscosity averaging scheme = %s\n'%(re.sub('_',' ',averaging)) )
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
    elif '#SBATCH -N 1' in l and igr == 2 and iar == 0:
      outjobscript.write('#SBATCH -N 4\n')
    elif '#SBATCH -N 1' in l and igr == 2 and iar == 1:
      outjobscript.write('#SBATCH -N 6\n')
    elif 'mpirun' in l:
     outjobscript.write('mpirun --map-by socket:pe=$OMP_NUM_THREADS /home/bbpanneg/software/aspect/build_RL9__fix_stresses_elasticity/aspect-release ' + new_prmfile + ' > /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM5/' + base_label + label + '/opla' )
#     outjobscript.write('mpirun --map-by socket:pe=$OMP_NUM_THREADS /home/bbpanneg/software/aspect/build_RL9__fix_stresses_elasticity/aspect-debug ' + new_prmfile + ' > /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM5/' + base_label + label + '/opla' )
    else:
      outjobscript.write(l)
  jobscript.close()
  outjobscript.close()

  # Make new output directory
  if not exists('/scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM5/' + base_label + label):
    os.system('mkdir /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM5/' + base_label + label)
  
  # Submit simulation to run queue
  submit = 'sbatch '+ new_jobscript
  os.system(submit)

  print ('Model output in /scratch/usr/bbpanneg/runs/fix_stresses_elasticity/paper_14072023/BM5/' + base_label + label)

# Run the model at different refinement levels and timesteps
IAR = [0]
IGR = [1]
elastic_timesteps = [500]
timesteps = [500]
#averaging = ["harmonic", "geometric", "arithmetic", "maximum_composition"]
#averaging = ["harmonic", "arithmetic", "maximum_composition"]
averaging = ["geometric"]
#averaging = ["maximum_composition"]
for iar in IAR:
  for igr in IGR:
    for et in elastic_timesteps:
      for t in timesteps:
        for av in averaging:
          generate_and_run(iar,igr,t,et,av)
