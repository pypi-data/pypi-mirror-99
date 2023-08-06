// EMTParameterProviderInterface.h: Python interface to the EMT parameter providers.
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

#ifndef _EMTPARAMETERPROVIDER_INTERFACE_H
#define _EMTPARAMETERPROVIDER_INTERFACE_H

#include "AsapPython.h"
#include "Asap.h"
#include "EMTParameterProvider.h"

namespace ASAPSPACE {

extern PyTypeObject PyAsap_EMTParamProvType;

int PyAsap_InitEMTParameterProviderInterface(PyObject *module);

// Factory functions for creating ParameterProviders (needed by AsapModule.cpp)
PyObject *PyAsap_EMTDefaultParamProvNew(PyObject *noself, PyObject *noargs);
extern char EMTDefaultParamProv_Docstring[];
PyObject *PyAsap_EMTRasmussenParamProvNew(PyObject *noself, PyObject *noargs);
extern char EMTRasmussenParamProv_Docstring[];

} // end namespace

#endif // _EMTPARAMETERPROVIDER_INTERFACE_H
