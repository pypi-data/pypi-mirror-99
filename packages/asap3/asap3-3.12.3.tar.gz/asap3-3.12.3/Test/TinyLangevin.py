#! /usr/bin/env python
#PBS -N TinyLangevin
#PBS -q long
#PBS -l nodes=1:opteron4

"""testLangevin.py - test the Langevin dynamics.

Usage: python testLangevin.py

Tests Langevin dynamics using the EMT Copper potential.
"""
from __future__ import print_function

import sys, time
from numpy import *
import asap3
from asap3.testtools import ReportTest
from asap3.md.langevin import Langevin
from asap3.md.verlet import VelocityVerlet
from ase.lattice.cubic import FaceCenteredCubic
from ase import units
from asap3.io import Trajectory

nequil = 10000
nequilprint = 25
nsteps = 500000
nprint = 250
tolerance = 0.01
nminor = 25
timestep = 5 * units.fs

# Use Langevin from ASE if --ase argument is given
if len(sys.argv) > 1 and sys.argv[1] == "--ase":
    print("--ase specified: Using unmodified ASE Langevin dynamics.")
    from ase.md.langevin import Langevin

# Set up atoms in a regular simple-cubic lattice.
atoms = FaceCenteredCubic(size=(1,1,2), symbol="Cu", pbc=False,
                        latticeconstant = 3.5)
atoms.set_calculator(asap3.EMT())
    
ReportTest("Number of atoms", len(atoms), 8, 0)

# Make a small perturbation of the momenta
atoms.set_momenta(1e-6 * random.random([len(atoms), 3]))
print("Initializing ...")
predyn = VelocityVerlet(atoms, 0.5)
predyn.run(2500)

initr = atoms.get_positions()
initp = atoms.get_momenta()


def targetfunc(params, x):
    return params[0] * exp(-params[1] * x) + params[2]

output =open("Langevin.dat", "w")

results = []

for temp, frict, fixcm in ((0.025, 0.001, True), (0.025, 0.0001, False),):
    dyn = Langevin(atoms, timestep, temperature_K=temp/units.kB, friction=frict, fixcm=fixcm)
    traj = Trajectory("Langevin-{0}-{1}-{2}.traj".format(temp, frict, fixcm),
                      "w", atoms)
    print("")
    print("Testing Langevin dynamics with T = %f eV and lambda = %f" % (temp, frict))
    ekin = atoms.get_kinetic_energy()/len(atoms)
    print(ekin)
    output.write("%.8f\n" % ekin)
    temperatures = [(0, 2.0 / 3.0 * ekin)]
    a = 0.1
    b = frict
    c = temp
    print("Equilibrating ...")
    tstart = time.time()
    for i in range(1,nequil+1):
        dyn.run(nminor)
        ekin = atoms.get_kinetic_energy() / len(atoms)
        if i % nequilprint == 0:

            print("%.6f  T = %.6f (goal: %f)" % \
                  (ekin, 2.0/3.0 * ekin, temp))
        output.write("%.8f\n" % ekin)
    tequil = time.time() - tstart
    print("This took %s minutes." % (tequil / 60))
    output.write("&\n")
    temperatures = []
    print("Taking data")
    tstart = time.time()
    for i in range(1,nsteps+1):
        dyn.run(nminor)
        ekin = atoms.get_kinetic_energy() / len(atoms)
        temperatures.append(2.0/3.0 * ekin)
        if i % nprint == 0:
            tnow = time.time() - tstart
            tleft = (nsteps-i) * tnow / i
            print("%.6f    (time left: %.1f minutes)" % (ekin, tleft/60))
            traj.write()
        output.write("%.8f\n" % ekin)
    output.write("&\n")
    temperatures = array(temperatures)
    mean = sum(temperatures) / len(temperatures)
    print("Mean temperature:", mean, "eV")
    print("")
    print("This test is statistical, and may in rare cases fail due to a")
    print("statistical fluctuation.")
    print("")
    expected = temp
    if fixcm:
        expected *= 7.0 / 8.0
    results.append((mean, (mean - expected)/expected))
    ReportTest("Mean temperature:", mean, expected, tolerance*temp)

print("RESULTS:")
for r in results:
    print("%.8f  %.8f" % r)
    
output.close()

