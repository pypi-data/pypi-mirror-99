"""
2020, July 21
"""

import collections

from ..core.component import *
from ..core.terminal import *
from ..core.variable import *
import fonsim.fluid.fluid as fd

import fonsim.constants.physical as cphy
import fonsim.constants.norm as cnorm

terminal_fluidic = [Variable('pressure', 'across', cnorm.pressure_atmospheric),
                    Variable('massflow', 'through')]


class Container(Component):
    def __init__(self, label=None, fluid=None, volume=None):
        super().__init__(label)

        terminal0 = Terminal('a', terminal_fluidic)
        self.set_terminals(terminal0)
        self.set_arguments(terminal0('pressure'), terminal0('massflow'))
        self.set_states(Variable('mass', 'local'))

        self.nb_equations = 1

        # Custom functionality
        self.volume = volume
        self.fluid = fluid

        # Continue init based on fluid
        # Compatible fluids
        initfunction_by_compatible_fluids = collections.OrderedDict([
            (fd.IdealCompressible, container_compressible),
            (fd.IdealIncompressible, container_incompressible),
        ])
        # Continue init based on fluid
        self.fluid.select_object_by_fluid(initfunction_by_compatible_fluids)(self)
        self.set_states(Variable('mass', 'local', volume*self.density))

    def update_state(self, state_new, jacobian, state, arguments, dt):
        state_new[0] = state[0] + dt * arguments[1]
        jacobian[0, 0] = 0
        jacobian[0, 1] = dt


# Type hinting: mention Container class in arguments
def container_incompressible(self: Container):
    def evaluate_incompressible(values, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        values[0] = arguments[1]
        jacobian_arguments[0, 1] = 1
    self.evaluate = evaluate_incompressible

    self.density = self.fluid.rho


def container_compressible(self: Container):
    self.mass_stp = self.volume * self.fluid.rho_stp

    def evaluate_compressible(values, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        values[0] = state[0] * cnorm.pressure_atmospheric - self.mass_stp * arguments[0]
        jacobian_state[0, 0] = cnorm.pressure_atmospheric
        jacobian_arguments[0, 0] = -self.mass_stp
    self.evaluate = evaluate_compressible

    p0 = sum([t('pressure').initial_value for t in self.terminals]) / len(self.terminals)
    self.density = p0 / cnorm.pressure_atmospheric * self.fluid.rho_stp
