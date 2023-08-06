from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from asap3 import NeighborCellLocator
from asap3.setup.multidislocation import random_dislocations
from asap3.setup.dislocation import Dislocation
from asap3.memory import get_max_memory
from ase.atoms import Atoms
from ase.lattice.cubic import FaceCenteredCubic, BodyCenteredCubic
import ase.data
import numpy as np
import scipy.spatial
from multiprocessing import Pool, cpu_count
from . import plane_utils
from . import quat_utils
import math
import sys
import os

def make_nanocrystal(size, centres, rotations, min_dist=2.0, unit=None,
                     symbol=None, latticeconstant=None):
    """Create a nanocrystalline sample.

    Parameters:
      size:      Size of the system, in Angstrom (either a number or three numbers).
      centres:   Positions of grains in scaled coordinates.
      rotations: Rotation matrices for the grains.

      min_dist (optional):
                 If two atoms are closer than this distance, one of them is removed
                 (default: 2.0).

    In addition, either the 'unit' or the 'symbol' parameter must be specified.
      unit (optional):
                 A unit cell for building the crystals (Atoms object).
                 MUST be orthorhombic!
      symbol (optional):
                 If unit is None, then an FCC crystal of this element is used.
      latticeconstant (optional):
                 If symbol is specified, this overrides the default lattice constant.
    """

    assert type(size) == float or type(size) == list
    if type(size) == float:
        size = np.array([size, size, size])
    elif type(size) == list:
        size = np.array(size)
    assert size.shape == (3,)
    assert len(centres) == len(rotations)
    centres *= size
    if unit is None:
        unit = FaceCenteredCubic(symbol=symbol, size=(1,1,1), pbc=True,
                                 latticeconstant=latticeconstant)

    return create_atoms(centres, rotations, unit, size, min_dist)

def make_dislocated_nanocrystal(size, centres, rotations, 
                                dislocationdensity,
                                symbol, latticeconstant=None,
                                min_dist=2.0,
                                multiproc=False):
    """Create a nanocrystalline sample with pre-existing dislocation density.

    Parameters:
      size:      Size of the system, in Angstrom (either a number or three numbers).
      centres:   Positions of grains in scaled coordinates.
      rotations: Rotation matrices for the grains.
      dislocationdensity:
                 Dislocation density in m^-2
      symbol:    Chemical symbol or atomic number.
      latticeconstant (optional):
                 Overrides the default lattice constant.
      min_dist (optional):
                 If two atoms are closer than this distance, one of them is removed
                 (default: 2.0).
      multiproc: Use all cores to calculate dislocation strain fields (default: False).
    """

    assert type(size) == float or type(size) == list
    if type(size) == float:
        size = np.array([size, size, size])
    elif type(size) == list:
        size = np.array(size)
    assert size.shape == (3,)
    assert len(centres) == len(rotations)
    centres *= size
    if latticeconstant is None:
        # Get lattice constant from the element
        if isinstance(symbol, int):
            z = symbol
        else:
            z = ase.data.atomic_numbers[symbol]
        if ase.data.reference_states[z]['symmetry'] != 'fcc':
            raise ValueError("Cannot extract FCC lattice constant from non-fcc element ({})".format(symbol))
        latticeconstant = ase.data.reference_states[z]['a']
    unit = FaceCenteredCubic(symbol=symbol, size=(1,1,1), pbc=True,
                             latticeconstant=latticeconstant)
    # Create a dislocation field for each grain.  The radius of the dislocation
    # field should be half the sidelength of the overall system
    dislocationfields = []
    for i in range(len(centres)):
        disloc_params = random_dislocations(max(size)/2.0, dislocationdensity)
        n_dislocs = len(disloc_params)
        dislocs = [Dislocation(point, line, latticeconstant * burgers)
                   for point, burgers, line in disloc_params]
        dislocationfields.append(dislocs)

    return create_atoms(centres, rotations, unit, size, min_dist,
                        dislocations=dislocationfields, multiproc=multiproc)


# A function for generating random rotation matrices
random_rotation_matrix = quat_utils.random_rotation_matrix


def bcc_grains(size, perturbation=0.0):
    "Creates a grain layout based on a perturbed BCC lattice."
    graincenters = BodyCenteredCubic(symbol='H', latticeconstant=1.0, size=size)
    graincenters = graincenters.get_positions() + 0.25
    graincenters /= size
    pert = np.random.standard_normal(graincenters.shape) * perturbation
    graincenters += pert
    rotations = [random_rotation_matrix() for g in graincenters]
    return graincenters, rotations

def minimize_energy(atoms, nstep, pressure_interval=10, bulkmodulus = 140e9/1e5):
    """Helper function for minimizing the energy of a nanocrystalline structure.

    It minimizes the energy while eliminating the diagonal components of the stress.
    The atomic positions are optimized using the FIRE algorithm and the stress
    is minimized using the Inhomogeneous_Berendsen algorithm.

    Parameters:

    atoms: The atoms object to be energy-minimized.

    nsteps: Number of time steps in the FIRE algorithm

    pressure_interval=10: (optional) How often to call the stress minimizer.

    bulkmodulus=1.4e6: (optional).  The bulk modulus (in bar !!!) used by the
    stress optimizer.  This value is for Cu and is useful for all metals.
    The value is uncritical, but the order of magnitude should be reasonable. 
    """
    dyn = FIRE(atoms)
    unstress = Inhomogeneous_NPTBerendsen(atoms, 50*units.fs, 0,
                                          taup=5000*units.fs,
                                          compressibility=1/bulkmodulus)
    dyn.attach(unstress.scale_positions_and_cell, interval=10)
    dyn.run(steps=nstep)


###
###  Below are helper functions for make_nanocrystalline
###


def remove_close(atoms, min_dist):
    "Remove atoms that are too close"
    print("Removing atoms that are too close (d_cut = %.3f Angstrom)" % (min_dist,))
    remove = set()
    nblist = NeighborCellLocator(min_dist, atoms)
    # Loop over all pairs of too-close atoms
    for i in range(len(atoms)):
        for j in nblist[i]:
            # Pair (i,j) is too close
            if not (i in remove or j in remove):
                if len(remove) % 2:
                    remove.add(i)
                else:
                    remove.add(j)
    print("Removing %i atoms out of %i" % (len(remove), len(atoms)))
    del atoms[list(remove)]
    return atoms

def calculate_grain_bounding_planes(centres, size):

    a = (-1, 0, 1)
    ctr = [c for c in centres]
    for i in a:
        for j in a:
            for k in a:
                if i == j == k == 0: continue
                ctr += [size * [i, j, k] + c for c in centres]
    ctr = np.array(ctr)

    voronoi = scipy.spatial.Voronoi(ctr, furthest_site=False,
                                    incremental=False, qhull_options=None)
    regions = [voronoi.regions[voronoi.point_region[i]] for i in range(len(centres))]

    grain_cells = []
    for i, reg in enumerate(regions):

        cell_vertices = np.array([voronoi.vertices[v] for v in reg])
        hull = scipy.spatial.ConvexHull(cell_vertices)

        bounding_planes = [plane_utils.plane_equation(centres[i], h, cell_vertices)
                           for h in hull.simplices]
        grain_cells += [(cell_vertices, bounding_planes)]

    return grain_cells

_field_to_apply = None

def apply_fields(r):
    global _field_to_apply
    res = np.zeros_like(r)
    for f in _field_to_apply:
        res += f(r)
    return res

_positions_args = None
def create_layer_positions(i):
    global _positions_args
    y0, y1, z0, z1, unit = _positions_args
    positions = [np.dot((i, j, k), unit.cell) + atom_pos
                 for j in range(y0, y1+1)
                 for k in range(z0, z1+1)
                 for atom_pos in unit.get_positions()]
    return np.array(positions)

def create_atoms(centres, rotations, unit, size, min_dist, dislocations=None,
                 multiproc=False):
    "Create the nanocrystalline sample"
    global _field_to_apply, _positions_args

    if multiproc:
        if multiproc is True:
            multiproc_cpus = None  # Use default
        else:
            if not isinstance(multiproc, int) or multiproc <= 0:
                raise TypeError("multiproc argument must be a positive integer.")
            multiproc_cpus = multiproc  # Use specified number
            
    grain_cells = calculate_grain_bounding_planes(centres, size)

    ntotal = 0
    result = None
    for grain_num, (centre, rotation) in enumerate(zip(centres, rotations)):
        assert centre.shape == (3,)
        assert rotation.shape == (3,3)

        (bounding_vertices, bounding_planes) = grain_cells[grain_num]

        #find maximum extent in [x, y, z]
        U = rotation
        rot_basis = U / np.linalg.norm(U, axis=0)

        proj_vertices = np.dot(bounding_vertices, rot_basis)

        xmin = np.min(proj_vertices[:,0])
        ymin = np.min(proj_vertices[:,1])
        zmin = np.min(proj_vertices[:,2])

        xmax = np.max(proj_vertices[:,0])
        ymax = np.max(proj_vertices[:,1])
        zmax = np.max(proj_vertices[:,2])

        #calculate number of unit cells in each direction
        cubic_cell = [unit.cell[0][0], unit.cell[1][1], unit.cell[2][2]]

        x0 = int(math.floor(xmin / cubic_cell[0]))
        y0 = int(math.floor(ymin / cubic_cell[1]))
        z0 = int(math.floor(zmin / cubic_cell[2]))

        x1 = int(math.ceil(xmax / cubic_cell[0]))
        y1 = int(math.ceil(ymax / cubic_cell[1]))
        z1 = int(math.ceil(zmax / cubic_cell[2]))

        # If there are dislocations, make space for their worst-case
        # cumulative dislplacement
        if dislocations:
            field = dislocations[grain_num]
            n_disl = len(field)
            correction = int(n_disl // np.sqrt(2))
            x0 -= correction
            y0 -= correction
            z0 -= correction
            x1 += correction
            y1 += correction
            z1 += correction
            
        #create cube of atoms    #todo: outer product
        if multiproc:
            _positions_args = (y0, y1, z0, z1, unit)
            pool = Pool(multiproc_cpus)
            positions = pool.map(create_layer_positions, range(x0, x1+1))
            positions = np.concatenate(positions)
            pool.close()
        else:
            positions = [np.dot((i, j, k), unit.cell) + atom_pos
                         for i in range(x0, x1+1)
                         for j in range(y0, y1+1)
                         for k in range(z0, z1+1)
                         for atom_pos in unit.get_positions()]
            positions = np.array(positions)
        print("Temporary length of position array:", len(positions))
        sys.stdout.flush()
        # Apply dislocation field, if any
        if dislocations:
            centre_of_mass = positions.sum(axis=0)/len(positions)
            if multiproc:
                if multiproc_cpus:
                    ncores = multiproc_cpus
                else:
                    ncores = cpu_count()
                print("Using {} cores.".format(ncores))
                _field_to_apply = field  # Cannot pass a lambda to Pool.map
                arg = np.array_split(positions - centre_of_mass, ncores)
                pool = Pool(multiproc_cpus)
                res = pool.map(apply_fields, arg)
                totalfield = np.concatenate(res)
                pool.close()
                assert totalfield.shape == positions.shape
            else:
                totalfield = np.zeros_like(positions)
                for i, f in enumerate(field):
                    totalfield += f(positions - centre_of_mass)
            positions = positions + totalfield
            print(n_disl, "dislocations introduced.")
            sys.stdout.flush()
        # Apply rotation
        positions = np.dot(positions, U.transpose())
        
        #remove excess atoms
        print("Removing excess atoms.")
        in_cell = np.ones(len(positions)).astype(np.int8)
        for (p, n) in bounding_planes:
            in_cell = np.logical_and(in_cell, np.dot(n, (positions - p).T) > 0)

        positions = positions[in_cell]

        print("Creating Atoms object, and merging...")
        atoms = Atoms(positions = positions, cell=size, numbers = 29 * np.ones(len(positions)))
        atoms.set_tags(grain_num * np.ones(len(atoms), int))
        if result is None:
            result = atoms
            atoms.set_cell(size, scale_atoms=False)
            atoms.set_pbc(True)
        else:
            result.extend(atoms)
        print("grain %d contains %d atoms (max mem. %.1f GB)."
              % (grain_num, len(positions), get_max_memory()/1024))
        sys.stdout.flush()

    print("Total atoms:", len(result))
    result = remove_close(result, min_dist)
    print("Remaining atoms:", len(result))
    return result

