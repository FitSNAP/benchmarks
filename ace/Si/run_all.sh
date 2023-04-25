#export PATH=${PATH}:${HOME}/lammps_compute_PACE/build-kokkos
LAMMPS_DIR=${HOME}/lammps_compute_PACE/build-kokkos

for n in 5 10 20 30 40 50 70 90 110
do
  rm -rf nrep-$n
  cp -r md_files nrep-$n
  cd nrep-$n
  mpirun -np 2 ${LAMMPS_DIR}/lmp -k on g 2 -sf kk -pk kokkos newton on neigh half -in in.run -v nrep $n
  cd ..
done


