"""
Python script for plotting comparisons.

Usage:

    python plot_comparisons.py system

Args:
    system: string representing system to compare potentials for (e.g. `Si`)
"""
import numpy as np
import sys
import matplotlib.pyplot as plt

pots = ['ace', 'snap']
colors = ['r', 'b']

system = sys.argv[1]

print(f"Comparing results for {system}")

fig, ax = plt.subplots()
for i, pot in enumerate(pots):
    dat = np.loadtxt(f"{pot}/{system}/speed-vs-atoms.dat")
    ax.set_xscale('log', base=10)
    ax.plot(dat[:,0], dat[:,1], 'o-', color=colors[i])

ax.set_title(f"{system}")
ax.set_xlabel("# atoms")
ax.set_ylabel("Speed (Matom-step/s)")
ax.legend(pots)

# Remove log notation
#ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
#xlabels = ['{:,.0f}'.format(x) + 'K' for x in ax.get_xticks()/1000]
xlabels = [f'{int(x)}' + 'K' for x in ax.get_xticks()/1000]
ax.set_xticklabels(xlabels)
# turn on grid
ax.grid()
plt.savefig(f"speed-vs-atoms-{system}.png", dpi=500)
    

