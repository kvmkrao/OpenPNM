#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: CEF PNM Team
# License: TBD
# Copyright (c) 2012

#from __future__ import print_function
"""

module __FickianDiffusion__: Fick's Law Diffusion
========================================================================

.. warning:: The classes of this module should be loaded through the 'Algorithms.__init__.py' file.

"""

import OpenPNM
import scipy as sp
from __LinearSolver__ import LinearSolver

class FickianDiffusion(LinearSolver):
    r"""

    FickianDiffusion - Class to run Fick's law mass transfer diffusion on constructed networks

                        It returns conecentration gradient inside the network.


    Parameter
    ----------
    -loglevel : int
        Level of the logger (10=Debug, 20=INFO, 30=Warning, 40=Error, 50=Critical)


    """

    def __init__(self,loglevel=10,**kwargs):
        r"""
        Initializing the class
        """
        super(FickianDiffusion,self).__init__(**kwargs)
        self._logger.info("Create Fick's Diffusion Algorithm Object")


    def _setup(self,**params):
        r"""
        This function executes the essential methods specific to Fickian diffusion simulations
        """
        self._fluid = params['active_fluid']
        # Variable transformation for Fickian Algorithm from xA to ln(xB)
        Dir_pores = self._net.pore_properties['numbering'][self.BCtypes==1]
        self.BCvalues[Dir_pores] = sp.log(1-self.BCvalues[Dir_pores])
        g = self._fluid.throat_conditions['diffusive_conductance']
        s = self._fluid.throat_conditions['occupancy']
        self._conductance = g*s

    def _do_inner_iteration_stage(self):
        r"""

        """
        X = self._do_one_inner_iteration()
        xA = 1-sp.exp(X)
        self._fluid.pore_conditions['mole_fraction'] = xA
        print xA

