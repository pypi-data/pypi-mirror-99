"""
Some tools to make plotting results less repetitive

2020, September 5

"""

from fonsim.conversion import unitconversion


def plot(axs, sim, label, unit, components):
    """
    Easily plot terminal data of components

    :param axs: matplotlib plotting axis
    :param sim: simulation object
    :param label: variable label, e.g. 'pressure'
    :param unit: unit, e.g. 'bar'
    :param components: iterable with components or (component, terminal) pairs
    :return: None
    """
    # Get unit multiplier
    m = 1/unitconversion.get_unit_multiplier(unit, label)

    # Plot data of all components
    for comp in components:
        if len(comp) == 2:
            comp = comp[0]
            term = comp[1]
        else:
            term = None
        comp = sim.system.get(comp)
        data, term = comp.get_all(label, term)
        datalabel = comp.label + ", " + term.label
        axs.plot(sim.times, data*m, label=datalabel)

    # Plot zero axis
    axs.plot((sim.times[0], sim.times[-1]), (0, 0), color='black', linewidth=1, linestyle='dashed')

    # Add legend
    axs.legend()
    # Axis label
    axs.set_ylabel(label + " [" + unit + "]")


def plot_state(axs, sim, label, unit, components):
    """
    Easily plot state data of components

    :param axs: matplotlib plotting axis
    :param sim: simulation object
    :param label: variable label, e.g. 'pressure'
    :param unit: unit, e.g. 'bar'
    :param components: iterable with components
    :return: None
    """
    # Get unit multiplier
    m = 1/unitconversion.get_unit_multiplier(unit, label)

    # Plot data of all components
    for comp in [sim.system.get(c) for c in components]:
        axs.plot(sim.times, comp.get_state(label)*m, label=comp.label)

    # Plot zero axis
    axs.plot((sim.times[0], sim.times[-1]), (0, 0), color='grey', linewidth=1, linestyle='dashed')

    # Add legend
    axs.legend()
    # Axis label
    axs.set_ylabel(label + " [" + unit + "]")
