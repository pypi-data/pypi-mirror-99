"""Asap module ParallelListOfAtoms.

Defines the parallel list of atoms object (`ParallelAtoms`), and a factory
method for creating them (`MakeParallelAtoms`).

Importing this module also installs a Python exit function causing
MPI_Abort to be called if an uncaught exception occurs.
"""


__docformat__ = "restructuredtext en"

import ase
import ase.units
try:
    from ase.geometry.cell import Cell
except ImportError:
    # Cell was introduced in ASE in April 2019.
    Cell = None
from asap3 import _asap
from asap3.Internal.BuiltinPotentials import AsapPotential
import asap3.mpi
import numpy as np
import pickle
import sys, time
import ase.parallel
import numbers
from ase.utils import deprecated

class ParallelPotential(_asap.ParallelPotential, AsapPotential):
    def __init__(self, potential, *args, **kwargs):
        super().__init__(potential, *args, **kwargs)
        self._calc = potential
        
    def get_stress(self, atoms):
        stress = self.get_virial(atoms)
        if not getattr(atoms, "_ase_handles_dynamic_stress", False):
            p = atoms.get_momenta()
            masses = atoms.get_masses()
            invmass = 1.0 / masses
            dynstress = np.zeros_like(stress)
            for alpha in range(3):
                for beta in range(alpha, 3):
                    dynstress[self._stresscomp[alpha,beta]] = -(p[:,alpha] * p[:,beta] * invmass).sum()
            asap3.mpi.world.sum(dynstress)
            stress += dynstress
        stress /= atoms.get_volume()
        return stress

    # Some Potentials may have non-standard methods and attributes.
    # In those cases, pass through to the original Potential.
    def __getattr__(self, name):
        return getattr(self._calc, name)

class NoCalculatorWrapper:
    """Object proxy hiding the calculator of an Atoms object."""
    def __init__(self, wrappee):
        self._wrappee = wrappee

    def get_calculator(self):
        return None

    def __getattr__(self, attr):
        return getattr(self._wrappee, attr)

    @property
    def calc(self):
        """Calculator object."""
        return None



class ParallelAtoms(ase.Atoms):
    """Atoms class for parallel Asap simulations.

    It is recommended to create ParallelAtoms objects using
    `MakeParallelAtoms`.
    """
    parallel = 1
    def __init__(self, nCells, comm, atoms, cell=None, pbc=None,
                 distribute=True):
        """Create a ParallelAtoms object.

        WARNING: ParallelAtoms object should normally not be created
        explicitly.  Use MakeParallelAtoms instead.
        """
        # Initialize the atoms.  Hide the calculator: Often there will
        # be a SinglePointCalculator (or anothter calculator) on the
        # master but nothing on the slaves, causing a deadlock.  And a
        # ParallelPotential cannot be reused on a new ParallelAtoms
        # object.
        super().__init__(NoCalculatorWrapper(atoms), cell=cell, pbc=pbc, constraint=None)

        # Sanity checks
        assert self.arrays["positions"].dtype == np.dtype(float)
        assert self.arrays["positions"].shape == (len(atoms), 3)
        assert self.arrays["numbers"].shape ==  (len(atoms),)

        # The initializer of the parent class (ase.Atoms) only copies
        # known arrays.  Copy the rest.
        for k, v in atoms.arrays.items():
            if k not in self.arrays:
                self.arrays[k] = v.copy()

        self.nCells = np.array(nCells, int)
        if self.nCells.shape != (3,):
            raise ValueError("ParallelAtoms: nCells must be 3 integers.")
        self.comm = comm

        self.ghosts = {}
        self.ghosts["positions"] = np.zeros((0,3), float)
        self.ghosts["numbers"] = np.zeros(0, self.arrays["numbers"].dtype)

        # Now make the IDs
        mynatoms = np.array([len(self)])
        natoms_all = np.zeros(self.comm.size, int)
        self.comm.all_gather(mynatoms, natoms_all)
        if "ID" not in self.arrays:
            firstID = sum(natoms_all[:self.comm.rank])
            self.arrays["ID"] = np.arange(firstID, firstID+len(atoms))
        self.total_number_of_atoms = sum(natoms_all)

        if distribute:
            self.distribute()

    def distribute(self, verbose=None):
        if verbose is None:
            verbose = _asap.verbose
        _asap.DistributeAtoms(self, verbose)

    def get_global_number_of_atoms(self):
        n = len(self)
        return self.comm.sum(n)
        
    # Compatibility with ASE 3.18.0 and earlier
    get_number_of_atoms = get_global_number_of_atoms

    def get_list_of_elements(self):
        """Get a list of elements.

        The list is cached to prevent unnecessary communication.
        """
        try:
            return self.listofelements
        except AttributeError:
            z = self.get_atomic_numbers()
            present = np.zeros(100, int)
            if len(z):
                zmax = z.max()
                zmin = z.min()
                present[zmin] = present[zmax] = 1
                for i in range(zmin+1, zmax):
                    if np.equal(z, i).any():
                        present[i] = 1
            self.comm.sum(present)
            self.listofelements = []
            for i, p in enumerate(present):
                if p:
                    self.listofelements.append(i)
            return self.listofelements

    def set_atomic_numbers(self, numbers):
        """Set the atomic numbers."""
        try:
            # Discard the cached list of elements
            del self.listofelements
        except AttributeError:
            pass
        ase.Atoms.set_atomic_numbers(self, numbers)

    def get_ids(self):
        """Get the atom IDs in a parallel simulation."""
        return self.arrays["ID"].copy()

    def is_master(self):
        """Return 1 on the master node, 0 on all other nodes."""
        return (self.comm.rank == 0)

    def get_comm(self):
        return self.comm
    
    def wrap_calculator(self, calc):
        "Make an ASAP calculator compatible with parallel simulations."
        try:
            parallelOK = calc.supports_parallel()
        except AttributeError:
            parallelOK = False
        if not parallelOK:
            raise ValueError("The calculator does not support parallel ASAP calculations.")
        try:
            verbose = calc.verbose
        except AttributeError:
            verbose = _asap.verbose
        return ParallelPotential(calc, verbose)

    def set_calculator(self, calc, wrap=True):
        """Sets the calculator in a way compatible with parallel simulations.
        
        calc: 
            The Calculator to be used.  Normally only Asap calculators will work.
            
        wrap (optional, default=True):
            Indicates if a calculator should be wrapped in a ParallelCalculator object.  
            Wrapping is the default, and should almost always be used, the only exception
            being if the Calculator is implemented as a Python object wrapping an Asap
            calculator, in which case the Asap calculator should first be wrapped in
            a ParallelCalculator object (use atoms.wrap_calculator) and this one should then
            be used by the Python calculator.  The Python calculator is then attached
            without being wrapped again.
        """
        if wrap and calc is not None:
            parcalc = self.wrap_calculator(calc)
        else:
            parcalc = calc
        ase.Atoms.calc.fset(self, parcalc)

    @property
    def calc(self):
        """Calculator object."""
        return ase.Atoms.calc.fget(self)
    
    @calc.setter
    def calc(self, calc):
        self.set_calculator(calc)

    @calc.deleter  # type: ignore
    @deprecated(DeprecationWarning('Please use atoms.calc = None'))
    def calc(self):
        self.set_calculator(None)

    def get_kinetic_energy(self):
        local_ekin = ase.Atoms.get_kinetic_energy(self)
        return self.comm.sum(local_ekin)
    
    def get_temperature(self):
        """Get the temperature. in Kelvin"""
        ekin = self.get_kinetic_energy() / self.get_global_number_of_atoms()
        return ekin / (1.5 * ase.units.kB)

    def get_ghost_positions(self):
        return self.ghosts['positions'].copy()
    
    def get_ghost_atomic_numbers(self):
        return self.ghosts['numbers'].copy()
    
    def get_center_of_mass(self, scaled=False):
        """Get the center of mass.

        If scaled=True the center of mass in scaled coordinates
        is returned."""
        m = self.get_masses()
        rsum = np.dot(m, self.arrays['positions'])
        msum = m.sum()
        data = np.zeros(4)
        data[:3] = rsum
        data[3] = msum
        self.comm.sum(data)
        com = data[:3] / data[3]
        if scaled:
            return np.linalg.solve(self._cell.T, com)
        else:
            return com

    def get_stress(self, voigt=True, apply_constraint=True, include_ideal_gas=False):
        """Calculate stress tensor.

        Returns an array of the six independent components of the
        symmetric stress tensor, in the traditional Voigt order
        (xx, yy, zz, yz, xz, xy) or as a 3x3 matrix.  Default is Voigt
        order.

        The ideal gas contribution to the stresses is added if the 
        atoms have momenta, unless it is explicitly disabled.
        """

        if self._calc is None:
            raise RuntimeError('Atoms object has no calculator.')

        stress = self._calc.get_stress(self)
        assert stress.shape == (6,)

        if apply_constraint:
            for constraint in self.constraints:
                if hasattr(constraint, 'adjust_stress'):
                    constraint.adjust_stress(self, stress)

        # Add ideal gas contribution, if applicable
        if getattr(self, "_ase_handles_dynamic_stress", False) and include_ideal_gas and self.has('momenta'):
            stresscomp = np.array([[0, 5, 4], [5, 1, 3], [4, 3, 2]])
            invvol = 1.0 / self.get_volume()
            p = self.get_momenta()
            masses = self.get_masses()
            invmass = 1.0 / masses
            dynstress = np.zeros_like(stress)
            for alpha in range(3):
                for beta in range(alpha, 3):
                    dynstress[stresscomp[alpha,beta]] -= (p[:,alpha] * p[:,beta] * invmass).sum() * invvol
            asap3.mpi.world.sum(dynstress)
            stress += dynstress

        if voigt:
            return stress
        else:
            xx, yy, zz, yz, xz, xy = stress
            return np.array([(xx, xy, xz),
                             (xy, yy, yz),
                             (xz, yz, zz)])


    # We need to redefine __getitem__ since __init__ does not
    # take the expected arguments.
    def __getitem__(self, i):
        """Return a subset of the atoms.

        i -- scalar integer, list of integers, or slice object
        describing which atoms to return.

        If i is a scalar, return an Atom object. If i is a list or a
        slice, return an Atoms object with the same cell, pbc, and
        other associated info as the original Atoms object. The
        indices of the constraints will be shuffled so that they match
        the indexing in the subset returned.

        The returned object is an ordinary Atoms object, not a
        ParallelAtoms object.
        """
        if isinstance(i, numbers.Integral):
            natoms = len(self)
            if i < -natoms or i >= natoms:
                raise IndexError('Index out of range.')

            return ase.Atom(atoms=self, index=i)

        import copy
        from ase.constraints import FixConstraint, FixBondLengths

        atoms = ase.Atoms(cell=self._cell, pbc=self._pbc, info=self.info)

        atoms.arrays = {}
        for name, a in self.arrays.items():
            atoms.arrays[name] = a[i].copy()

        # Constraints need to be deepcopied, since we need to shuffle
        # the indices
        atoms.constraints = copy.deepcopy(self.constraints)
        condel = []
        for con in atoms.constraints:
            if isinstance(con, (FixConstraint, FixBondLengths)):
                try:
                    con.index_shuffle(self, i)
                except IndexError:
                    condel.append(con)
        for con in condel:
            atoms.constraints.remove(con)
        return atoms

def MakeParallelAtoms(atoms, nCells, cell=None, pbc=None,
                      distribute=True):
    """Build parallel simulation from serial lists of atoms.

    Call simultaneously on all processors.  Each processor having
    atoms should pass a list of atoms as the first argument, or None
    if this processor does not contribute with any atoms.  If the
    cell and/or pbc arguments are given, they must be given on
    all processors, and be identical.  If it is not given, a supercell
    is attempted to be extracted from the atoms on the processor with
    lowest rank.

    Any atoms object passed to this method cannot have a calculator or a
    contraint attached.

    This is the preferred method for creating parallel simulations.
    """
    mpi = asap3.mpi
    #comm = mpi.world.duplicate()
    comm = mpi.world

    # Sanity check: No contraint.
    if atoms is not None:
        if getattr(atoms, "contraints", None):
            raise ValueError("The atoms on node {} have contraints: {}".format(
                comm.rank, str(atoms.constraints)))

    # Sanity check: is the node layout reasonable
    nNodes = nCells[0] * nCells[1] * nCells[2]
    if nNodes != comm.size:
        raise RuntimeError("Wrong number of CPUs: %d != %d*%d*%d" %
                           (comm.size, nCells[0], nCells[1], nCells[2]))
    t1 = np.zeros((3,))
    t2 = np.zeros((3,))
    comm.min(t1)
    comm.max(t2)
    if (t1[0] != t2[0] or t1[1] != t2[1] or t1[2] != t2[2]):
        raise RuntimeError("CPU layout inconsistent.")

    # If pbc and/or cell are given, they may be shorthands in need of
    # expansion.
    if pbc:
        try:
            plen = len(pbc)
        except TypeError:
            # It is a scalar, interpret as a boolean.
            if pbc:
                pbc = (1,1,1)
            else:
                pbc = (0,0,0)
        else:
            if plen != 3:
                raise ValueError("pbc must be a scalar or a 3-sequence.")
    if cell:
        cell = array(cell)  # Make sure it is a numeric array.
        if cell.shape == (3,):
            cell = array([[cell[0], 0, 0],
                          [0, cell[1], 0],
                          [0, 0, cell[2]]])
        elif cell.shape != (3,3):
            raise ValueError("Unit cell must be a 3x3 matrix or a 3-vector.")

    # Find the lowest CPU with atoms, and let that one distribute
    # which data it has.  All other CPUs check for consistency.
    if atoms is None:
        hasdata = None
        mynum = comm.size
    else:
        hasdata = {}
        for name in atoms.arrays.keys():
            datatype = np.sctype2char(atoms.arrays[name])
            shape = atoms.arrays[name].shape[1:]
            hasdata[name] = (datatype, shape)
        mynum = comm.rank
        if pbc is None:
            pbc = atoms.get_pbc()
        if cell is None:
            cell = np.array(atoms.get_cell())
    root = comm.min(mynum)   # The first CPU with atoms
    # Now send hasdata, cell and pbc to all other CPUs
    package = pickle.dumps((hasdata, cell, pbc), 2)
    package = comm.broadcast_string(package, root)
    rootdata, rootcell, rootpbc = pickle.loads(package)
    if rootdata is None or len(rootdata) == 0:
        raise ValueError("No data from 'root' atoms.  Empty atoms?!?")
    
    # Check for consistent cell and pbc arguments
    if cell is not None:
        if rootcell is None:
            raise TypeError("Cell given on another processor than the atoms.")
        if (cell.ravel() - rootcell.ravel()).max() > 1e-12:
            raise ValueError("Inconsistent cell specification.")
    else:
        cell = rootcell   # May still be None
    if pbc is not None:
        if rootpbc is None:
            raise TypeError("PBC given on another processor than the atoms.")
        if (pbc != rootpbc).any():
            raise ValueError("Inconsistent pbc specification.")
    else:
        pbc = rootpbc

    # Check for consistent atoms data
    if hasdata is not None:
        if hasdata != rootdata:
            raise ValueError("Atoms do not contain the sama data on different processors.")
    if "positions" not in rootdata:
        raise ValueError("Atoms do not have positions!")
    
    # Create empty atoms
    if atoms is None:
        atoms = ase.Atoms(cell=cell, pbc=pbc)
        for name in rootdata.keys():
            if name in atoms.arrays:
                assert np.sctype2char(atoms.arrays[name]) == rootdata[name][0]
                assert len(atoms.arrays[name]) == 0
            else:
                shape = (0,) + rootdata[name][1]
                atoms.arrays[name] = np.zeros(shape, rootdata[name][0])
        
    return ParallelAtoms(nCells, comm, atoms, cell=cell, pbc=pbc, 
                         distribute=distribute)



# A cleanup function should call MPI_Abort if python crashes to
# terminate the processes on the other nodes.
ase.parallel.register_parallel_cleanup_function()

# _oldexitfunc = getattr(sys, "exitfunc", None)
# def _asap_cleanup(lastexit = _oldexitfunc, sys=sys, time=time,
#                   comm = asap3.mpi.world):
#     error = getattr(sys, "last_type", None)
#     if error:
#         sys.stdout.flush()
#         sys.stderr.write("ASAP CLEANUP (node " + str(comm.rank) +
#                          "): " + str(error) +
#                          " occurred.  Calling MPI_Abort!\n")
#         sys.stderr.flush()
#         # Give other nodes a moment to crash by themselves (perhaps
#         # producing helpful error messages).
#         time.sleep(3)
#         comm.abort(42)
#     if lastexit:
#         lastexit()
# sys.exitfunc = _asap_cleanup
        
# END OF PARALLEL STUFF
