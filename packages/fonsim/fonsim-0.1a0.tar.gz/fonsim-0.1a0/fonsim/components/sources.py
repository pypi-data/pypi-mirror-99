"""
2020, July 21
"""

import collections

from ..core.component import *
from ..core.terminal import *
from ..core.variable import *
import fluid.fluid as fd

import constants.physical as cphy
import constants.norm as cnorm

terminal_fluidic = [Variable('pressure', 'across', cnorm.pressure_atmospheric),
                    Variable('massflow', 'through')]


class PressureSource(Component):
    def __init__(self, label=None, fluid=None, pressure=None):
        Component.__init__(self, label)

        terminal0 = Terminal('a', terminal_fluidic)
        self.set_terminals(terminal0)
        self.set_arguments(terminal0('pressure'), terminal0('massflow'))
        self.nb_equations = 1

        # Custom functionality
        self.pressure = pressure

    def evaluate(self, values, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        if callable(self.pressure):
            values[0] = arguments[0] - self.pressure(elapsed_time)
        else:
            values[0] = arguments[0] - self.pressure
        jacobian_arguments[0, 0] = 1


class MassflowSource(Component):
    def __init__(self, label=None, fluid=None, massflow=None):
        Component.__init__(self, label)

        terminal0 = Terminal('a', terminal_fluidic)
        self.set_terminals(terminal0)
        self.set_arguments(terminal0('massflow'), terminal0('pressure'))
        self.nb_equations = 1

        # Custom functionality
        self.massflow = massflow

    def evaluate(self, values, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        if callable(self.massflow):
            values[0] = arguments[0] + self.massflow(elapsed_time)
        else:
            values[0] = arguments[0] + self.massflow
        jacobian_arguments[0, 0] = 1


class VolumeflowSource(Component):
    def __init__(self, label=None, fluid=None, volumeflow=None):
        Component.__init__(self, label)

        terminal0 = Terminal('a', terminal_fluidic)
        self.set_terminals(terminal0)
        self.set_arguments(terminal0('pressure'), terminal0('massflow'))
        self.nb_equations = 1

        # Custom functionality
        self.fluid = fluid
        self.volumeflow = volumeflow

        # Continue init based on fluid
        # Compatible fluids
        initfunction_by_compatible_fluids = collections.OrderedDict([
            (fd.IdealCompressible, volumeflowsource_compressible),
            (fd.IdealIncompressible, volumeflowsource_incompressible),
        ])
        # Continue init based on fluid
        self.fluid.select_object_by_fluid(initfunction_by_compatible_fluids)(self)


def volumeflowsource_incompressible(self):
    def evaluate(values, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        vf = self.volumeflow(elapsed_time) if callable(self.volumeflow) else self.volumeflow
        values[0] = arguments[1] + vf*self.fluid.rho
        jacobian_arguments[0, 1] = 1
    self.evaluate = evaluate


def volumeflowsource_compressible(self):
    def evaluate(values, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        vf = self.volumeflow(elapsed_time) if callable(self.volumeflow) else self.volumeflow
        a = self.fluid.rho_stp/cnorm.pressure_atmospheric
        values[0] = arguments[1] + a*vf*arguments[0]
        jacobian_arguments[0, 0] = a*vf
        jacobian_arguments[0, 1] = a*arguments[0]
    self.evaluate = evaluate
