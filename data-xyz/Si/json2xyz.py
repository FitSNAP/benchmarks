"""
Use fs library to create a fs list of structure dicts.
Then use this list of dicts to write xyz files.
"""

from mpi4py import MPI
from fitsnap3lib.fitsnap import FitSnap

# Declare a communicator (this can be a custom communicator as well).
comm = MPI.COMM_WORLD

# Create an input dictionary containing settings.
settings = \
{
"BISPECTRUM":
    {
    "numTypes": 1,
    "twojmax": 6,
    "rcutfac": 4.67637,
    "rfac0": 0.99363,
    "rmin0": 0.0,
    "wj": 1.0,
    "radelem": 0.5,
    "type": "Si",
    "wselfallflag": 0,
    "chemflag": 0,
    "bzeroflag": 0,
    "quadraticflag": 0,
    },
"CALCULATOR":
    {
    "calculator": "LAMMPSSNAP",
    "energy": 1,
    "force": 1,
    "stress": 1
    },
"ESHIFT":
    {
    "Si": 0.0
    },
"SOLVER":
    {
    "solver": "SVD",
    "compute_testerrs": 1,
    "detailed_errors": 1
    },
"SCRAPER":
    {
    "scraper": "JSON" 
    },
"PATH":
    {
    "dataPath": "/Users/adrohsk/benchmarks/data/Si_Zuo2020_JPCA" #"../../Ta_Linear_JCP2014/JSON"
    },
"OUTFILE":
    {
    "metrics": "Ta_metrics.md",
    "potential": "Ta_pot"
    },
"REFERENCE":
    {
    "units": "metal",
    "atom_style": "atomic",
    "pair_style": "zero 10.0",
    "pair_coeff": "* *"
    },
"GROUPS":
    {
    "group_sections": "name training_size testing_size eweight fweight vweight",
    "group_types": "str float float float float float",
    "smartweights": 0,
    "random_sampling": 0,
    "AIMD" :  "1.0    0.0       100             1               1.00E-08",
    "Elastic" :  "1.0    0.0       100             1               1.00E-08",
    "Surface" :  "1.0    0.0       100             1               1.00E-08",
    "Vacancy"   :  "1.0    0.0     1.00E-08        1.00E-08        0.0001"
    }
}

# Alternatively, settings could be provided in a traditional input file:
# settings = "../../Ta_Linear_JCP2014/Ta-example.in"
    
# Create a FitSnap instance using the communicator and settings:
fs = FitSnap(settings, comm=comm, arglist=["--overwrite"])

# Scrape configurations to create and populate the `snap.data` list of dictionaries with structural info.
fs.scrape_configs()
# Calculate descriptors for all structures in the `snap.data` list.
# This is performed in parallel over all processors in `comm`.
# Descriptor data is stored in the shared arrays.
fs.process_configs()

def write2xyz(s, namemap):
    """
    Args:
        s: Structure dictionary element of the fitsnap list of dictionaries.
        namemap: Map of filenames to corresponding file handles.
    """

    groupname = s['Group']

    if 'test' in s['File']:
        groupname += "_test"

    if groupname not in namemap:
        namemap[groupname] = open(f"{groupname}.xyz", 'w')
    
    fh = namemap[groupname]

    # Write the header for this structure.
    natoms = s['NumAtoms']
    fh.write(f"{natoms}\n")
    lat = s['Lattice']
    st = s['Stress'] # Stress tensor
    x = s['Positions']
    f = s['Forces']
    types = s['AtomTypes']
    header = f'Lattice = "{lat[0,0]} {lat[0,1]} {lat[0,2]} {lat[1,0]} {lat[1,1]} {lat[1,2]} {lat[2,0]} {lat[2,1]} {lat[2,2]}"'
    header += ' Properties=species:S:1:pos:R:3:forces:R:3'
    header += f' energy={s["Energy"]}'
    header += f' stress="{st[0,0]} {st[0,1]} {st[0,2]} {st[1,0]} {st[1,1]} {st[1,2]} {st[2,0]} {st[2,1]} {st[2,2]}"\n'
    fh.write(header)

    for n in range(natoms):
        fh.write(f"{types[n]} {x[n,0]} {x[n,1]} {x[n,2]} {f[n,0]} {f[n,1]} {f[n,2]}\n")

namemap = {}
for s in fs.data:
    print(f"{s['Group']} {s['File']}")

    write2xyz(s, namemap)
