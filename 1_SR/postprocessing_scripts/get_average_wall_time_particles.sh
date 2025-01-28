#!/bin/bash

while read name;
do
  t_stokes=$(bc <<<"scale=4;0.0")
  t_advection=$(bc <<<"scale=4;0.0")
  t_PI=$(bc <<<"scale=4;0.0")
  t_PPU=$(bc <<<"scale=4;0.0")
  echo $name
  for i in {1..3};
  do
    # The nr of processes
    echo 'Nr. of processes: ' $(grep 'MPI proc' $name'_'$i'/log.txt' | awk '{print $5}')

    # The nr of degrees of freedom
    echo 'Nr. of DOFs:' $(grep free $name'_'$i'/log.txt' | awk '{print $6}')

    # Get the last occurrence of the wall time statistics
    tail -26 $name'_'$i'/log.txt' > tmp.txt

    # The number of nonlinear iterations
    echo 'Nr. of NI:' $(grep 'Assemble Stokes system' tmp.txt | awk '{print $6}')

    readarray -t arr < <(grep 'Assemble Stokes system' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_stokes=$(bc <<<"scale=4;$t_stokes+${arr[0]}")
    readarray -t arr < <(grep 'Build Stokes preconditioner' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_stokes=$(bc <<<"scale=4;$t_stokes+${arr[0]}")
    readarray -t arr < <(grep 'Solve Stokes system' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_stokes=$(bc <<<"scale=4;$t_stokes+${arr[0]}")

    # TODO if more than 1 proc is used, there is another entry: Particles: Exchange ghosts
    readarray -t arr < <(grep 'Particles: Advect' tmp.txt | awk '{print substr($7, 1, length($7)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep 'Particles: Copy' tmp.txt | awk '{print substr($7, 1, length($7)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep 'Particles: Generate' tmp.txt | awk '{printf "%.7f", substr($7, 1, length($7)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep 'Particles: Initialization' tmp.txt | awk '{print substr($7, 1, length($7)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep 'Particles: Initialize properties' tmp.txt | awk '{printf "%.7f", substr($8, 1, length($8)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep 'Particles: Interpolate' tmp.txt | awk '{print substr($7, 1, length($7)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    t_PI=$(bc <<<"scale=4;$t_PI+${arr[0]}")
    readarray -t arr < <(grep 'Particles: Sort' tmp.txt | awk '{print substr($7, 1, length($7)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep 'Particles: Update properties' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    t_PPU=$(bc <<<"scale=4;$t_PPU+${arr[0]}")

  done
  t_stokes=$(bc <<<"scale=4;$t_stokes/3.0")
  t_advection=$(bc <<<"scale=4;$t_advection/3.0")
  t_PI=$(bc <<<"scale=4;$t_PI/3.0")
  t_PPU=$(bc <<<"scale=4;$t_PPU/3.0")
  echo "Average total particle time :" $t_advection
  echo "Average total PI time :" $t_PI
  echo "Average total PPU time :" $t_PPU
  echo "Average total Stokes time:" $t_stokes
  echo "--------"
done < list_of_model_names.txt
