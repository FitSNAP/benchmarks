# ML potential GPU benchmarks

This project contains fits and LAMMPS input scripts for benchmarking accuracy and performance of 
ML potentials.

### Organization

The following directories for fits are organized like:

    <potential>
        <system>

E.g. `<potential>` can be SNAP, ACE, etc. and `<system>` can be `Si`, `Li`, `Mo`, etc.

Training data is stored in the `data` directory.

### Instructions on fitting and benchmarking

First activate your Python environment:

    source ~/venv-fitsnap-pace/bin/activate

Proceed into a `<potential>/<system>` directory and run a fit with:

    mpirun -np 4 python -m fitsnap3 input.in --overwrite

Obtain CPU benchmarks on a 10x10x10 unit cell system with:

    mpirun -np P ~/lammps_compute_PACE/build-fitsnap/lmp -in in.run -v nrep 10

Obtain GPU/Kokkos benchmarks on a 10x10x10 unit cell system with:

    mpirun -np 2 ~/lammps_compute_PACE/build-kokkos/lmp -k on g 2 -sf kk -pk kokkos newton on neigh half -in in.run -v nrep 10

  
