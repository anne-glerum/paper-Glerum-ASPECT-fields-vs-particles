#!/bin/bash

while read name;
do
  t_stokes=$(bc <<<"scale=4;0.0")
  t_advection=$(bc <<<"scale=4;0.0")
  echo $name
  for i in {1..3};
  do
    # The nr of processes
    echo 'Nr. of processes: ' $(grep 'MPI proc' $name'_'$i'/log.txt' | awk '{print $5}')

    # The nr of degrees of freedom
    echo 'Nr. of DOFs:' $(grep free $name'_'$i'/log.txt' | awk '{print $6}')

    # Get the last occurrence of the wall time statistics
    tail -25 $name'_'$i'/log.txt' > tmp.txt

    # The number of nonlinear iterations
    echo 'Nr. of NI:' $(grep 'Assemble Stokes system' tmp.txt | awk '{print $6}')

    readarray -t arr < <(grep 'Assemble Stokes system' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_stokes=$(bc <<<"scale=4;$t_stokes+${arr[0]}")
    readarray -t arr < <(grep 'Build Stokes preconditioner' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_stokes=$(bc <<<"scale=4;$t_stokes+${arr[0]}")
    readarray -t arr < <(grep 'Solve Stokes system' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_stokes=$(bc <<<"scale=4;$t_stokes+${arr[0]}")

    readarray -t arr < <(grep 'Assemble composition system' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep 'Build composition preconditioner' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")
    readarray -t arr < <(grep ' Solve composition system' tmp.txt | awk '{print substr($8, 1, length($8)-1)}')
    t_advection=$(bc <<<"scale=4;$t_advection+${arr[0]}")

  done
  t_stokes=$(bc <<<"scale=4;$t_stokes/3.0")
  t_advection=$(bc <<<"scale=4;$t_advection/3.0")
  echo "Average total advection time:" $t_advection
  echo "Average total Stokes time:" $t_stokes
  echo "--------"
done < list_of_model_names.txt
