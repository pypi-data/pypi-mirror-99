# encoding: utf-8
#
#Copyright (C) 2017-2021, P. R. Wiecha
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
    pyGDM2 - a full-field electrodynamical solver python toolkit.
    Based on the Green Dyadic Method.
    
"""
from pyGDM2 import core as core_py
from pyGDM2 import fields as fields_py
from pyGDM2 import linear as linear_py


__name__ = 'pyGDM2'
__version__ = '1.1.0rc2'
__date__ = "03/19/2021"
__author__ = 'Peter R. Wiecha'

__all__ = ["core", "materials", "structures", "fields", 
           "propagators", "propagators_2D",
           "linear", "nonlinear", 
           "tools", "visu",
           "core_py", "fields_py", "linear_py", 
           "EO", "EO.core", "EO.tools", "EO.models", "EO.problem"]


