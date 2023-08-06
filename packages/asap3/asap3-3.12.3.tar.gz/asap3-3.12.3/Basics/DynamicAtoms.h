// DynamicAtoms.h  --  Access the atoms from a dynamics object
// -*- c++ -*-
//
// Copyright (C) 2001-2011 Jakob Schiotz and Center for Individual
// Nanoparticle Functionality, Department of Physics, Technical
// University of Denmark.  Email: schiotz@fysik.dtu.dk
//
// This file is part of Asap version 3.
//
// This program is free software: you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// version 3 as published by the Free Software Foundation.  Permission
// to use other versions of the GNU Lesser General Public License may
// granted by Jakob Schiotz or the head of department of the
// Department of Physics, Technical University of Denmark, as
// described in section 14 of the GNU General Public License.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// and the GNU Lesser Public License along with this program.  If not,
// see <http://www.gnu.org/licenses/>.

#ifndef _DYNAMICATOMS_H
#define _DYNAMICATOMS_H

#include "AsapPython.h"
#include "Asap.h"
#include "Vec.h"
#include <vector>

namespace ASAPSPACE {

class DynamicAtoms
{
public:
    DynamicAtoms(PyObject *py_atoms);
    virtual ~DynamicAtoms();
    
    int GetNAtoms();
    Vec *GetPositions() {return GetVecData("positions");}
    Vec *GetMomenta() {return GetVecData("momenta");}
    const asap_z_int *GetAtomicNumbers();

    // GetMasses and GetInverseMasses return arrays that map from
    // atomic numbers to (inverse) atomic masses based on data 
    // extracted from the ase.data Python module.
    // A Dynamics module MUST check if these need to be overruled
    // by masses stored on the atoms.
    const std::vector<double> &GetMasses() {return masses;}
    const std::vector<double> &GetInverseMasses() {return invmasses;}

    double *GetDoubleData(PyObject *name);
    double *GetDoubleDataMaybe(PyObject *name);  // Get data if present, or NULL

private:
    Vec *GetVecData(const char *name);
    
private:
    PyObject *atoms;
    PyObject *arrays;
    std::vector<double> masses;
    std::vector<double> invmasses;
    std::vector<asap_z_int> conv_numbers;
};

} // end namespace

#endif  // _DYNAMICATOMS_H
