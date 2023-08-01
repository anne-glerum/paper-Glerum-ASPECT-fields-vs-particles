#!/bin/bash

while read name;
do
  t_stokes=$(bc <<<"scale=4;0.0")
  t_advection=$(bc <<<"scale=4;0.0")
  for i in {1..3};
  do
    tail -25 $name'_'$i'/log.txt' > tmp.txt
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
  echo "Average total Stokes time:", $t_stokes
  echo "Average total advection time:", $t_advection
done < list_of_model_names.txt
