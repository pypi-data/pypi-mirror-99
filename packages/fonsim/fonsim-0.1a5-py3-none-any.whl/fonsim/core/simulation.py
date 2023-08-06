"""
Class Simulation

Functionality to convert network information
(how the components are connected to each other)
and component information
(equations for each component)
to a single non-linear system of equations
(function vector + Jacobian)
describing the whole system.

Solving this system is to be done by a solver.
This object can interact with the solver object.

2020, July 22
"""

import math
import time

import numpy as np

from . import solver as slv


class Simulation:
    def __init__(self, system_to_simulate, duration=10, step=None,
                 step_min=None, step_max=None, max_steps=0, verbose=0):
        """
        Simulation class

        :param system_to_simulate: System object with components etc.
        :param duration: amount of time the system will be simulated for
        :param step: initial time increment
        :param step_min: minimal time increment during the simulation
        :param step_max: maximal time increment during the simulation
        :param max_steps: maximum amount of time increments before the
        simulation is terminated prematurely. A value of 0 disables this
        behavior (default)
        :param verbose: level of information printed in the console
        during the simulation. All messages belonging to a level with a
        number lower than or equal to the provided parameter will be
        displayed, with the possible levels being:
            -1: simulation start and end messages
             0 (default): simulation progress in % steps
             1: system matrices on iterations with bad convergence
        """
        self.verbose = verbose

        # Load system to simulate
        self.system = system_to_simulate
        connectivity_message = self.system.get_connectivity_message()
        if len(connectivity_message) > 0 and self.verbose >= -1:
            print('Warning: {}!'.format(connectivity_message))
            print('Are you sure you did not forget any connections?')

        # Timing
        self.duration = duration

        # Resolve stepping settings
        self.duration = duration
        if step is None:
            step_vals = [s for s in (step_max, step_min) if s is not None]
            if len(step_vals) > 0:
                step = sum(step_vals)/len(step_vals)
            else:
                step = self.duration/100.
        self.max_steps = max_steps

        # Initialize matrix construction (dicts etc.)
        self.arguments = []
        self.nb_arguments = 0
        self.phi_indices_by_component = {}
        self.phi_index_by_component_argument = {}
        self.nb_component_equations = 0
        self.nb_network_equations = 0
        self.init_matrixconstruction()

        # Construct the matrices
        # Jacobian
        self.H = np.zeros((self.nb_arguments,self.nb_arguments))
        # Fill network matrix
        self.fill_network_matrix(self.H)
        # Network matrix (= upper part of H)
        self.A = self.H[:self.nb_network_equations,:]

        # values vector = result of evaluated equations
        # leave this to the solver...
        #self.g = np.zeros(self.nb_arguments)

        # Create the argument matrix, aka the matrix with the vector
        # of all unknowns for each timestep
        # For now, only allocate for one timestep;
        # up to the solver to do the rest (to allow variable timestep etc.)
        self.phi = self.init_solutions()
        # Note: up to solver to call
        # map_phi_to_components so components know
        # where their data is!

        # Time series (to be set by solver)
        self.times = np.array(0)
        # Step counter - denotes current step of simulation
        self.simstep = 0

        # Select the solver
        # self.solver = slv.ImplicitEulerNewtonConstantTimeStep(self, step)
        self.solver = slv.ImplicitEulerNewtonAdaptiveTimeStep(self, step,
                                                              step_min, step_max)

    def init_matrixconstruction(self):
        """
        Create some LUT-style lists and dicts
        so data can be moved around quickly
        in the simulation loop.

        :return: None
        """
        # collocate arguments into a list
        self.arguments = []
        for component in self.system.components:
            self.arguments.extend(component.arguments)
        self.nb_arguments = len(self.arguments)
        # make a dict to quickly map arguments of a component
        # to the indices of phi
        self.phi_indices_by_component = {}
        self.phi_index_by_component_argument = {}
        for component in self.system.components:
            k = []
            for i in range(len(component.arguments)):
                arg = component.arguments[i]
                phi_index = self.arguments.index(arg)
                k.append(phi_index)
                self.phi_index_by_component_argument[arg] = phi_index
            self.phi_indices_by_component[component] = k
        # Count number of component equations
        self.nb_component_equations = 0
        for component in self.system.components:
            self.nb_component_equations += component.nb_equations

    def init_solutions(self):
        """
        Initialize the argument history matrix as a row vector filled
        with the initial value for all arguments

        :return: initialized argument history matrix, numpy nd array
        1 x n, n = len(self.arguments)
        """
        phi = np.zeros((1, self.nb_arguments))
        for arg, ind in self.phi_index_by_component_argument.items():
            phi[0,ind] = arg.initial_value
        return phi

    def fill_network_matrix(self, A):
        """
        Fill the network matrix.
        The network matrix is constant over the simulation, at least
        supposing the network configuration does not change. It is thus
        sufficient to calculate it a single time.

        There are two types of network equations, one for across
        variables and one for through variables. 
        At each node, all across variables have to be equal. Thus for
        each node n-1 equations, n being the number of components
        attached to that node.
        Concerning the through variables, the sum of all through
        variables should be zero at each node, thus one equation for each
        node.

        :param A: system Jacobian matrix, numpy ndarray n x n, n=len(phi)
        :return: None
        """
        irow = 0
        for node in self.system.nodes:
            # For now, suppose there is only one type of across variable
            # and one type of through variable per node...
            # Makes it far easier, and can be updated later.

            # Get across variables to relate together
            across_name = node.get_variables(orientation='across')[0].key
            across_variables = node.get_variables(orientation='across',
                                                  key=across_name)
            # Get their indices in the argument list
            phi_indices = []
            for arg in across_variables:
                arg_index = self.phi_index_by_component_argument[arg]
                phi_indices.append(arg_index)
            # Equate their values pair-wise
            nb_equations = len(phi_indices) - 1
            for i in range(nb_equations):
                a = np.zeros(self.nb_arguments)
                a[phi_indices[i]] = 1
                a[phi_indices[i+1]] = -1
                A[irow,:] = a
                irow += 1

            # Get through variables to relate together
            through_name = node.get_variables(orientation='through')[0].key
            through_variables = node.get_variables(orientation='through',
                                                   key=through_name)
            # Get their indices in the argument list
            phi_indices = []
            for arg in through_variables:
                arg_index = self.phi_index_by_component_argument[arg]
                phi_indices.append(arg_index)
            # Equate their sum to zero
            a = np.zeros(self.nb_arguments)
            for i in range(len(phi_indices)):
                a[phi_indices[i]] = 1
            A[irow,:] = a
            irow += 1

        self.nb_network_equations = irow

        # check whether system is solvable!
        is_solvable = self.nb_network_equations + self.nb_component_equations >= self.nb_arguments
        if not is_solvable:
            print("Warning: This system does not seem to be solvable !")
            print("  nb network eq:", irow)
            print("  nb_arguments: ", self.nb_arguments)

    def equation_to_string(self, equation_index):
        """
        Return a string describing the equation with the provided index
        in a human-readable format. For a network equation, this string
        contains the involved variables and their coefficients. For a
        component equation, this string mentions the component label and
        the index of the equation in the list of equations of that
        particular component.

        :param equation_index: index of the row in the simulation
        equation matrix corresponding to the desired equation
        :return eq_str: string representing the equation
        """
        eq_str = ""
        # handle network equations
        if equation_index < self.nb_network_equations:
            for coeff_ID, coeff in enumerate(self.A[equation_index,:]):
                if coeff != 0:
                    # add sign of coefficient
                    if coeff < 0:
                        eq_str += "- "
                    elif len(eq_str) > 0:
                        eq_str += "+ "
                    # add value of coefficient
                    if abs(coeff) != 1:
                        eq_str += "{}*".format(abs(coeff))
                    # add name of corresponding variable
                    eq_str += "{} ".format(self.arguments[coeff_ID].short_str())
        # handle component equations
        else:
            curr_eq_ind = self.nb_network_equations
            comp_ind = 0
            comp_eq_ind = 0
            # find the index of the component and the index of the equation in
            # the component matching with the global equation index
            while curr_eq_ind < equation_index:
                curr_eq_ind += 1
                if comp_eq_ind < self.system.components[comp_ind].nb_equations-1:
                    # transition to next equation in this component
                    comp_eq_ind += 1
                else:
                    # transition to next component
                    comp_eq_ind = 0
                    comp_ind += 1
            eq_str = "{} equation {}".format( \
                        self.system.components[comp_ind].label, comp_eq_ind)

        return eq_str.strip()

    def print_equations(self):
        """
        Print a human-readable representation of the full system of
        equations to the console.

        :return: None
        """
        # get every equation string
        eq_strs = [self.equation_to_string(i) for i in \
                  range(self.nb_network_equations+self.nb_component_equations)]
        # get maximum equation text width for alignment
        max_len = max([len(eq) for eq in eq_strs])
        # print equations
        for i,eq in enumerate(eq_strs):
            print('eq {}: {} = {}'.format(i, eq.rjust(max_len), 0))

    def map_phi_to_components(self, phi):
        """
        Send addresses of arguments over time to components, so one can
        get the data from the component without passing by the Simulation
        object. Furthermore, it avoids duplicating the data.

        :param phi: numpy ndarray m x n with the argument vector over
        time (m = nb timesteps and n = nb arguments)
        :return: None
        """
        for component in self.system.components:
            k = self.phi_indices_by_component[component]
            for i in range(len(component.arguments)):
                component.argument_history[i] = phi[:, k[i]]

    def initialize_memory(self, nb_steps):
        """
        Initialize all arrays that will hold the simulation results
        through time. This includes
            - The vector with time values
            - Component argument and state histories (in Component class)
            - The simulation phi matrix with all arguments over time
        All previously stored results are overwritten.
        
        :param nb_steps: estimated amount of time steps in the simulation
        :return: None
        """
        # Allocate time vector
        # The values it contains are filled in by the solver
        self.times = np.zeros(nb_steps)

        # Let components allocate memory for the calculation results and
        # put the initial state in this memory
        for component in self.system.components:
            component.initialize_memory(nb_steps)
            component.fill_initial_states()

        # Allocate phi matrix
        self.phi = self.phi * np.ones((nb_steps,1))
        self.map_phi_to_components(self.phi)

    def extend_memory(self, nb_extra_steps):
        """
        Increase the size of the simulation memory without overwriting
        previous results. This deals with the same entities as described
        in the documentation of initialize_memory

        :param nb_extra_steps: amount of time steps by which to increase
        the memory
        :return: None
        """
        # Extend time vector
        self.times = np.append(self.times, 
                               self.times[-1]*np.ones(nb_extra_steps))
        # Extend component state memories
        for component in self.system.components:
            component.extend_memory(nb_extra_steps)
        # Extend phi matrix
        self.phi = np.append(self.phi,
                             self.phi[0,:]*np.ones((nb_extra_steps,1)), 
                             axis=0)
        # Update links to argument results in components
        self.map_phi_to_components(self.phi)

    def slice_memory(self, start_step, end_step):
        """
        Decrease the size of the simulation memory by taking a slice out
        of it. This deals with the same entities as described in the
        documentation of initialize_memory

        :param start_step: index of the first time step in the range to
        maintain
        :param end_step: index of the first time step outside the range
        to maintain
        :return: None
        """
        # Truncate time vector
        self.times = self.times[start_step:end_step]
        # Truncate component state memories
        for component in self.system.components:
            component.slice_memory(start_step,end_step)
        # Truncate phi matrix
        self.phi = self.phi[start_step:end_step,:]
        # Update links to argument results in components
        self.map_phi_to_components(self.phi)

    def run(self):
        """
        Run simulation, with the parameters specified previously.

        :return: None
        """
        # Reset current simulation step index to zero
        self.simstep = 0
        # Reset simulation memory
        self.initialize_memory(self.solver.get_nb_steps_estimate())

        # Simulation time steps at which a progress message will be printed
        pstep = 5
        progress_pts = [(p/100.*self.duration, p) for p in range(pstep,101,pstep)]

        # Do the simulation loop
        if self.verbose >= -1:
            print("\nSimulation progress")
            start_time = time.process_time()

        solver_convergence = True
        while solver_convergence and \
              self.times[self.simstep] < self.duration and \
              (self.max_steps <= 0 or self.simstep <= self.max_steps):
            # Increase memory size if necessary
            if self.simstep+1 >= self.times.size:
                self.extend_memory(self.solver.get_nb_steps_estimate() - \
                                   self.times.size)
            # Run solver
            solver_status = self.solver.run_step(self.simstep)
            if solver_status is None:
                solver_convergence = True
            else:
                if isinstance(solver_status, (list, tuple)):
                    solver_convergence = solver_status[0]
                    solver_message = solver_status[1]
                else:
                    solver_convergence = solver_status
                    solver_message = ""
            # Update simulation step index
            self.simstep += 1
            # Print some progress information
            if self.verbose >= -1 and \
               self.times[self.simstep] >= progress_pts[0][0]:
                print(' {} %'.format(progress_pts[0][1]))
                del progress_pts[0]

        # Clean up excess memory when the simulation finishes
        self.slice_memory(0,self.simstep+1)

        # Print time data
        if self.verbose >= -1:
            # Get run time
            end_time = time.process_time()
            run_time = round(end_time - start_time, 2)
            # Print error messages
            if not solver_convergence and len(solver_message) > 0:
                print(solver_message)
            elif self.max_steps > 0 and self.simstep >= self.max_steps:
                print("Maximum number of simulation increments reached")
            # Print exit messages
            if self.times[self.simstep] < self.duration:
                print("Simulation terminated after", run_time, "s")
            else:
                print("Simulation finished in", run_time, "s")

    def evaluate_equations(self, simstep, g, H, elapsed_time, dt):
        """
        Evaulate component equations to obtain evaluated function vector
        and jacobian.

        Note: This function does not evaluate (or update) the network
        equations (upper part of the jacobian 'H')!

        :param simstep: simulation timestep index to start from
        :param g: numpy ndarray for the evaluated function vector
        :param H: numpy ndarray for the evaluated jacobian
        :param elapsed_time: time elapsed
        :param dt: timestep (0 for explicit Euler, dt for implicit Euler)
        :return: None
        """
        # yes, I'm aware the current memory management is crap

        # Row index to write to
        irow = self.nb_network_equations
        for component in self.system.components:
            # evaluate the functions
            arguments = self.phi[simstep+1, self.phi_indices_by_component[component]]

            state = component.state_history[simstep,:]

            state_new = np.zeros(len(component.states))
            j_state2arg = np.zeros((len(component.states), len(component.arguments)))

            component.update_state(state_new, j_state2arg, state, arguments, dt)

            value = np.zeros((component.nb_equations, 1))

            j_val2state = np.zeros((component.nb_equations, len(component.states)))
            j_val2arg = np.zeros((component.nb_equations, len(component.arguments)))

            # state_new = (state + state_new)/2

            component.evaluate(value, j_val2state, j_val2arg, state_new, arguments, elapsed_time)

            # combine state and argument jacobians
            jacobian_full = j_val2arg + np.inner(j_val2state, j_state2arg.T)

            # put the data of the small jacobian in the large one,
            # as well as the data from the equations
            for k in range(np.size(jacobian_full, 0)):
                H[irow, self.phi_indices_by_component[component]] = jacobian_full[k, :]
                g[irow] = value[k]
                irow += 1

    def update_state(self, simstep, dt):
        """
        Update the state variables in all components using the arguments
        in self.phi at step n + 1 (n = 'simstep').

        :param simstep: simulation timestep index to start from
        :param dt: timestep
        :return: None
        """
        for component in self.system.components:
            if len(component.states):
                arguments = self.phi[(self.simstep+1, self.phi_indices_by_component[component])]

                state = component.state_history[simstep,:]

                state_new = np.zeros(len(component.states))
                j_state2arg = np.zeros((len(component.states), len(component.arguments)))

                component.update_state(state_new, j_state2arg, state, arguments, dt)

                # state_new = (state_new + state)/2

                # Write out state to component
                component.state_history[simstep+1, :] = state_new
