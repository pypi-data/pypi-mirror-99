// -*- C++ -*-
//
// Copyright (C) 2008-2011 Jakob Schiotz and Center for Individual
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


#ifndef _MPIMODULE_H
#define _MPIMODULE_H
#include <Python.h> /* Not AsapPython.h as that would break AsapParallel.cpp */
#include <mpi.h>
#include "AsapMPI.h"
#include "Asap.h"

namespace ASAPSPACE {

typedef struct
{
  PyObject_HEAD
  int size;
  int rank;
  MPI_Comm comm;   // Remove real soon now.
  Communicator *cobj;    
  PyObject* parent;
} MPIObject;

int PyAsap_InitMpiInterface(PyObject *module);

} // end namespace

#endif /* _MPIMODULE_H */
