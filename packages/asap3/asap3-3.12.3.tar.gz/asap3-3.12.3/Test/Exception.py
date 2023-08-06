from __future__ import print_function
from asap3 import *
from ase.lattice.cubic import *

testname = "Illegal elements are an error."
atoms = FaceCenteredCubic(size=(10, 10, 10), symbol="Cu")
z = atoms.get_atomic_numbers()
z[7]=8
atoms.set_atomic_numbers(z)

try:
    atoms.set_calculator(EMT())
except AsapError:
    print("Test passed:", testname)
else:
    raise RuntimeError("Test failed: "+testname)
    
testname = "Atoms on top of each other."
atoms = FaceCenteredCubic(size=(10, 10, 10), symbol="Cu")
r = atoms.get_positions()
r[10] = r[11]
atoms.set_positions(r)
atoms.set_calculator(EMT())
try:
    e = atoms.get_potential_energy()
except AsapError:
    print("Test passed:", testname)
else:
    raise RuntimeError("Test failed: "+testname)
