# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and 
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#
"""
Created on Mar 20, 2013

.. moduleauthor:: Bogdan Neacsa <bogdan.neacsa@codemart.ro>
"""

from tvb.tests.library.base_testcase import BaseTestCase
from tvb.datatypes import equations


class TestEquations(BaseTestCase):
    """
    Tests that the equations in the `tvb.datatypes.equations` module can be instantiated.
    """

    def test_equation(self):
        dt = equations.Equation()
        assert dt.parameters == {}

    def test_finitesupportequation(self):
        dt = equations.FiniteSupportEquation()
        assert dt.parameters == {}

    def test_discrete(self):
        dt = equations.DiscreteEquation()
        assert dt.parameters == {}

    def test_linear(self):
        dt = equations.Linear()
        assert dt.parameters == {'a': 1.0, 'b': 0.0}

    def test_gaussian(self):
        dt = equations.Gaussian()
        assert dt.parameters == {'amp': 1.0, 'sigma': 1.0, 'midpoint': 0.0, 'offset': 0.0}

    def test_doublegaussian(self):
        dt = equations.DoubleGaussian()
        assert dt.parameters == {'midpoint_2': 0.0, 'midpoint_1': 0.0,
                                 'amp_2': 1.0, 'amp_1': 0.5, 'sigma_2': 10.0,
                                 'sigma_1': 20.0}

    def test_sigmoid(self):
        dt = equations.Sigmoid()
        assert dt.parameters == {'amp': 1.0, 'radius': 5.0, 'sigma': 1.0, 'offset': 0.0}

    def test_generalizedsigmoid(self):
        dt = equations.GeneralizedSigmoid()
        assert dt.parameters == {'high': 1.0, 'midpoint': 1.0, 'sigma': 0.3, 'low': 0.0}

    def test_sinusoiddata(self):
        dt = equations.Sinusoid()
        assert dt.parameters == {'amp': 1.0, 'frequency': 0.01}

    def test_cosine(self):
        dt = equations.Cosine()
        assert dt.parameters == {'amp': 1.0, 'frequency': 0.01}

    def test_alpha(self):
        dt = equations.Alpha()
        assert dt.parameters == {'onset': 0.5, 'alpha': 13.0, 'beta': 42.0}

    def test_pulsetrain(self):
        dt = equations.PulseTrain()
        assert dt.parameters == {'onset': 30.0, 'tau': 13.0, 'T': 42.0, 'amp': 1.0}
