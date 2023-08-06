'''
Class Component

2020, July 21

'''

import numpy as np

from conversion import indexmatch


class Component:
    def __init__(self, label):
        # component name
        self.label = label
        # terminals of component
        self.terminals = []
        # variables for the evaluation of the left-hand side of the residual
        # and for the state update equation
        self.arguments = []
        # other variables that are updated based on the solutions for the arguments
        self.states = []
        self.state_initial = []
        # number of evaluation equations
        self.nb_equations = 1
        # maximum step change of arguments for iterative stepping
        self.arguments_stepsize = []

        # References to calculated values
        self.state_history = None
        self.argument_history = None

    # only evaluate left-hand side (LH) of equation, equation should be structured such that RH is always zero
    def evaluate(self, values, jacobian_state, jacobian_arguments, state, arguments, elapsed_time):
        pass

    def update_state(self, state_new, jacobian, state, arguments, dt):
        pass

    def set_terminals(self, *terminals):
        """
        Overwrite component terminals list with the provided terminal
        objects and attach those terminals to the component

        :param terminals: terminal objects with which to replace the
        component terminals
        :return: None
        """
        self.terminals = list(terminals)
        for t in self.terminals:
            t.component = self

    def set_arguments(self, *arguments):
        """
        Overwrite component arguments list with the provided variable
        objects

        :param arguments: variable objects with which to replace the
        component arguments
        :return: None
        """
        self.arguments = list(arguments)

    def set_states(self, *states):
        """
        Overwrite component states list with the provided variable
        objects

        :param states: variable objects with which to replace the
        component states
        :return: None
        """
        self.states = list(states)

    def get_terminal(self, terminallabel=None):
        # no terminallabel -> try to give an unconnected terminal
        # terminallabel -> return that terminal
        if terminallabel is None:
            for terminal in self.terminals:
                if terminal.isconnected is False:
                    return terminal
            return self.terminals[0]
        else:
            for terminal in self.terminals:
                if terminal.label == terminallabel:
                    return terminal

    # The states are saved in the components themselves.
    # However, the argument data (e.g. pressure, flow in/out)
    # is saved centrally by the solver, and components
    # get pointers to this data.
    # That way, one can easily access all data from the components,
    # yet duplication of across variables is avoided.
    def initialize_memory(self, nb_steps):
        """
        Initialize matrices to hold the component state and argument
        variable values for a number of time steps

        :param nb_steps: amount of time steps for which to initialize
        memory
        :return: None
        """
        self.state_history = np.zeros((nb_steps, len(self.states)))
        self.argument_history = [None]*len(self.arguments)

    def extend_memory(self, extra_steps):
        """
        Extend size of the matrix that holds the component state variable
        values to accomodate a number of extra time steps

        :param extra_steps: amount of time steps for which to allocate
        additional memory
        :return: None
        """
        self.state_history = np.append(self.state_history,
                                       np.zeros((extra_steps, len(self.states))),
                                       axis=0)

    def slice_memory(self, start_ind, end_ind):
        """
        Reduce size of the matrix that holds the component state variable
        values by taking a slice of time steps

        :param start_ind: first index of the range of steps to maintain
        :param end_ind: first index outside the range of steps to
        maintain
        :return: None
        """
        self.state_history = self.state_history[start_ind:end_ind,:]

    def fill_initial_states(self):
        """
        Fill in initial state for the component state variables

        :return: None
        """
        for i in range(len(self.states)):
            self.state_history[0, i] = self.states[i].initial_value

    def get_state(self, label):
        """
        Get simulation results
        Supports 'smart matching' by comparing string distances

        :param label: state label, e.g. 'volume'
        :return: Numpy ndarray object
        """
        labels = [state.key for state in self.states]
        state_index = indexmatch.get_index_of_best_match(label, labels)
        return self.state_history[:, state_index]

    def get_all(self, variable_key, terminal_label=None):
        """
        Get simulation results
        Supports 'smart matching' by comparing string distances

        :param variable_key: key of variable, e.g. 'pressure'
        :param terminal_label: label of terminal, e.g. 'a'
        :return: Numpy ndarray object
        """
        sim_var = np.array([indexmatch.similar(variable_key, a.key) for a in self.arguments])
        sim_tmn = np.array([indexmatch.similar(terminal_label, a.terminal.label) for a in self.arguments])\
            if terminal_label is not None else np.ones(len(self.arguments))
        sim_com = np.multiply(sim_var, sim_tmn)
        i = np.argmax(sim_com)
        variable = self.arguments[i]
        term = variable.terminal
        return self.argument_history[i], term

    def get(self, variable_key, terminal_label=None):
        a, b = self.get_all(variable_key, terminal_label)
        return a
