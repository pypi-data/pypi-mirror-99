"""
2020, July 21
"""

import collections
import pkgutil

from ..core.component import *
from ..core.terminal import *
from ..core.variable import *
from fonsim.data import pvcurve
from fonsim.data import dataseries
import fonsim.fluid.fluid as fd

import fonsim.constants.physical as cphy
import fonsim.constants.norm as cnorm

terminal_fluidic = [Variable('pressure', 'across', cnorm.pressure_atmospheric),
                    Variable('massflow', 'through')]


# Named it 'free' because the actuator cannot drive anything (in the simulation)
class FreeActuator(Component):
    def __init__(self, label=None, fluid=None, curve=None):
        Component.__init__(self, label)

        terminal0 = Terminal('a', terminal_fluidic)
        terminal1 = Terminal('b', terminal_fluidic)
        self.set_terminals(terminal0, terminal1)
        self.set_arguments(terminal0('pressure'), terminal0('massflow'), \
                           terminal1('pressure'), terminal1('massflow'))
        self.nb_equations = 2

        # Custom functionality
        self.fluid = fluid
        if curve is None:
            filepath = 'resources/Measurement_60mm_balloon_actuator_01.csv'
            bs = pkgutil.get_data('fonsim', filepath)
            ds = dataseries.DataSeries(filename='.csv', bytestring=bs)
            self.pvcurve = pvcurve.PVCurve(ds, autocorrect=True)
        elif isinstance(curve, str):
            filename = curve
            self.pvcurve = pvcurve.PVCurve(filename, autocorrect=True)
        else:
            self.pvcurve = curve

        # Continue init based on fluid
        # Compatible fluids
        initfunction_by_compatible_fluids = collections.OrderedDict([
            (fd.IdealCompressible, freeactuator_compressible),
            (fd.IdealIncompressible, freeactuator_incompressible),
        ])
        # Continue init based on fluid
        self.fluid.select_object_by_fluid(initfunction_by_compatible_fluids)(self)

        # initialize state
        p0 = sum([t('pressure').initial_value for t in self.terminals]) / len(self.terminals)
        V0 = self.pvcurve.get_initial_volume(p0)
        self.set_states(Variable('mass', 'local', V0*self.density))

    def update_state(self, state_new, jacobian, state, arguments, dt):
        if state[0] >= 0 or (arguments[1] + arguments[3]) >= 0:
            state_new[0] = state[0] + dt * (arguments[1] + arguments[3])
        else:
            state_new[0] = state[0]
        jacobian[0, 1] = dt
        jacobian[0, 3] = dt


def freeactuator_compressible(self: FreeActuator):
    def evaluate(value, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        # Evaluate pv-curve
        mass = state[0]
        normalvolume = mass/self.fluid.rho_stp
        volume = normalvolume * cnorm.pressure_atmospheric / arguments[0]
        # f, df: interpolation functionality, volume -> pressure
        f, df = self.pvcurve.fdf_volume(volume)
        value[0] = f - arguments[0]
        # both terminals have the same pressure
        value[1] = arguments[2] - arguments[0]
        jacobian_state[0, 0] = df * cnorm.pressure_atmospheric / (arguments[0] * self.fluid.rho_stp)
        jacobian_arguments[0,0] = -df * volume / arguments[0] - 1
        jacobian_arguments[1, 2] = 1
        jacobian_arguments[1, 0] = -1
    self.evaluate = evaluate

    p0 = sum([t('pressure').initial_value for t in self.terminals]) / len(self.terminals)
    self.density = p0 / cnorm.pressure_atmospheric * self.fluid.rho_stp

def freeactuator_incompressible(self: FreeActuator):
    def evaluate(value, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        # Evaluate pv-curve
        mass = state[0]
        volume = mass/self.fluid.rho
        # f, df: interpolation functionality, volume -> pressure
        f, df = self.pvcurve.fdf_volume(volume)
        value[0] = f - arguments[0]
        # both terminals have the same pressure
        value[1] = arguments[2] - arguments[0]
        jacobian_state[0, 0] = df/self.fluid.rho
        jacobian_arguments[0, 0] = -1
        jacobian_arguments[1, 2] = 1
        jacobian_arguments[1, 0] = -1
    self.evaluate = evaluate

    self.density = self.fluid.rho

