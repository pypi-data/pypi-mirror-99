// -*- C++ -*-
// MetalOxideInterface.h: A potential for metal oxide interfaces
//
// Copyright (C) 2014 Jacob Madsen, Jakob Schiotz and Center for
// Individual Nanoparticle Functionality, Department of Physics,
// Technical University of Denmark.  Email: jamad@fysik.dtu.dk
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

#ifndef MetalOxideInterface_H
#define MetalOxideInterface_H

#include "AsapPython.h"
#include "Asap.h"
#include "Potential.h"
#include "Vec.h"
#include "SymTensor.h"
#include <vector>

//~ using std::vector;

namespace ASAPSPACE {

class Atoms;
class NeighborList;

class MetalOxideInterface : public Potential
{
public:

	MetalOxideInterface(PyObject *self,
			    double P, double Q, double A, double xi, double r0, double RGL_cut,
			    const std::vector<double> &q, double kappa,
			    const std::vector<double> &D, const std::vector<double> &alpha, const std::vector<double> &R0,
			    const std::vector<double> &a, const std::vector<double> &b, double &f0, double &oxide_cut,
			    const std::vector<double> &beta_, double gamma, double &interface_cut,
			    int verbose);
	~MetalOxideInterface();
	
	virtual string GetName() const {return "MetalOxideInterface";}
	virtual long PrintMemory() const;
	double GetCutoffRadius() const {return 0;}
	double GetLatticeConstant() const {return 0;}

	void SetAtoms(PyObject *atoms, Atoms* accessobj = NULL);
	double GetPotentialEnergy(PyObject *atoms);
	const std::vector<Vec> &GetForces(PyObject *atoms);
	const std::vector<SymTensor> &GetVirials(PyObject *atoms);
	const std::vector<double> &GetPotentialEnergies(PyObject *atoms);

	void CheckNeighborLists();

	// Return the neighbor list
	PyObject *GetNeighborList() const {return neighborList_obj;}

	// This potential can be used in parallel simulations
	virtual bool Parallelizable() const {return true;}

private:
	// Allocate memory 
	void Allocate();

	// Get total energy
	double CalculateEnergyAndEnergies();
	
	// Assign atom type
	void AssignAtoms();
	
	// RGL potetial
	void RGL(vector<double>& atomicEnergies);
	void RGLForces(vector<Vec>& forces);
		
	// Oxide potetial
	void Oxide(vector<double>& atomicEnergies);
	void OxideForces(vector<Vec>& forces);
	double Erfc(double x);
	
	// Interface potential
	void InterfacePotential(vector<double>& atomicEnergies);
	void InterfaceForces(vector<Vec>& forces);
	
	// Calculate energy shift
	std::vector<double> OxideShift();

	// Reference to the neighborlist
	NeighborList *neighborList;
	PyObject *neighborList_obj;
	
	// Number and type of atoms
	int nAtoms, nSize, nMetals, nOxides;
	std::vector<asap_z_int> metals, oxides, assignment, monolayer;
	
	// Potential parameters
	double P, Q, A, xi, r0, qM, qO, kappa, f0, gamma;
	std::vector<double> q, D, alpha, R0, a, b, beta;
	
	// Cut-off radius
	double RGL_cut, oxide_cut, interface_cut, driftfactor;
  
	// Atomic energies for atoms
	std::vector<double> atomicEnergies, sigma_p, sigma_q;
		
	// GetStresses returns pointer in this
	std::vector<SymTensor> virials;

	// GetCartesianForces returns a pointer in this
	std::vector<Vec> forces;

	// Counters to check whether recalculations are necessary
	struct {
		int ids;
		int nblist;
		int energies;
		int forces;
		int stresses;
	} counters;
};
}

#endif //MetalOxideInterface
