"""
Script for gathering speed vs. # atom data from MD directories prefixed with `nrep-`.

Usage:

    python gather.py
"""

import numpy as np
import  matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker

# Find all directories with MD.
dirs = [x[0] for x in os.walk('.')]
dirs = [d for d in dirs if 'nrep' in d]
# Loop over all MD directories and store atom/speed data in `dat`.
ndat = len(dirs)
dat = np.zeros((ndat, 2))
for i, d in enumerate(dirs):

    with open(f"{d}/log.lammps") as fh:
        for line in fh:
            if ("Created" in line and "atoms" in line):
                natoms = int(line.split()[1])
            if ("Performance:" in line):
                speed = float(line.split()[-2])
                units = line.split()[-1]
                if 'k' in units:
                    speed *= 1e-3
                dat[i,0] = natoms
                dat[i,1] = speed

# Sort by # atoms and write data.
argsort = np.argsort(dat[:,0])
dat = dat[argsort,:]
np.savetxt("speed-vs-atoms.dat", dat)

# Plot.

fig, ax = plt.subplots()
ax.set_xscale('log', base=10)
ax.plot(dat[:,0], dat[:,1], 'o-')
ax.set_xlabel("# atoms")
ax.set_ylabel("Speed (Matom-step/s")
# Remove log notation
#ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
#xlabels = ['{:,.0f}'.format(x) + 'K' for x in ax.get_xticks()/1000]
xlabels = [f'{int(x)}' + 'K' for x in ax.get_xticks()/1000]
ax.set_xticklabels(xlabels)
# turn on grid
ax.grid()
plt.savefig("speed-vs-atoms.png")
"""
plt.plot(dat[:,0], dat[:,1], '.')
plt.xlabel("# atoms")
plt.ylabel("Speed (Matom-step/s")
plt.xscale('log', base=2)
plt.savefig("speed-vs-atoms.png")
"""


