"""
Class system

Collection of interconnected components

2020, July 22
"""

from . import component as cmp
from . import terminal as tmn
from . import node


class System:
    def __init__(self, label=None):
        # Label
        self.label = label
        # List with objects of all the components in the system
        self.components = []
        # Dict to get an object pointer from its label property
        self.components_by_label = {}
        # Dict with as keys the components and as values integers
        # identifying the part of the network the component is connected
        # to. In case all components are connected together, all
        # dict values are the same, but they can be different if there
        # are two or more subsystems that are not connected to each other
        self.component_system = {}
        # List with nodes where two or more terminals connect together
        self.nodes = []

    def add(self, *components):
        """
        Introduce component to the system

        :param *components: Component objects to be added to the system
        :return: None
        """
        for component in components:
            if component.label not in self.components_by_label.keys():
                # Add component to the system
                self.components.append(component)
                self.components_by_label[component.label] = component
                # Create separate subsystem for the component
                if len(self.component_system) <= 0:
                    system_id = 0
                else:
                    system_id = max(self.component_system.values()) + 1
                self.component_system[component] = system_id
                # Create separate node for every component terminal
                for terminal in component.terminals:
                    self.nodes.append(node.Node(terminal))
            else:
                error_str = "Error: component labels need to be unique"
                error_str += " but {} already".format(component.label)
                error_str += " exists in system {}".format(self.label)
                print(error_str)

    def connect(self, *args):
        """
        Connect component terminals together. In case terminals are not
        specified directly, the component objects decide on which of
        their terminals to connect

        :param *args: component terminals. Every instance can be a
            - string specifying a component label present in the system
            - Component object
            - Terminal object
            - Tuple with first the component label and then the terminal
              label as strings
        :return: None
        """
        terminals = []
        components = []
        # Resolve references
        for arg in args:
            if type(arg) is str:
                component = self.components_by_label[arg]
                terminal = component.get_terminal()
            elif isinstance(arg, cmp.Component):
                component = arg
                terminal = component.get_terminal()
            elif type(arg) is tmn.Terminal:
                component = arg.component
                terminal = arg
            elif type(arg) is tuple:
                component = self.components_by_label[arg[0]]
                terminal = component.get_terminal(arg[1])
            else:
                print("Error: did not recognize {}. Aborting connection".format(arg))
                return
            components.append(component)
            terminals.append(terminal)
            # Make sure the terminal is present in the system
            if terminal.component not in self.components:
                self.add(terminal.component)

        # Connect terminals
        for i in range(len(terminals)-1):
            self.connect_two_terminals(terminals[i], terminals[i+1])

        # Merge component subsystems
        merged_id = min([self.component_system[c] for c in components])
        for component in components:
            self.component_system[component] = merged_id

    def connect_two_terminals(self, terminal_a, terminal_b):
        """
        Connect system terminals together in a node

        :param terminal_a: Terminal object
        :param terminal_b: Terminal object
        :return: None
        """
        # Make sure the requested terminals are present in the system
        for terminal in (terminal_a, terminal_b):
            if terminal.component not in self.components:
                self.add(terminal.component)

        # Mark the terminals as connected
        terminal_a.isconnected = True
        terminal_b.isconnected = True

        # Find nodes containing the terminals
        node_a = None
        node_b = None
        for node in self.nodes:
            if node.contains_terminal(terminal_a):
                node_a = node
            if node.contains_terminal(terminal_b):
                node_b = node

        # Merge nodes into one
        if node_a != node_b:
            node_a.merge_node(node_b)
            self.nodes.remove(node_b)

    def get(self, component_label):
        return self.components_by_label[component_label]

    def get_connectivity_message(self):
        """
        Get a message describing the connectivity of the system
        in case not every component is connected together

        :return: message string
        """
        message = ""

        # Check whether all components are connected together or not
        if len(set(self.component_system.values())) > 1:
            # Get dictionary with as keys the subsystem identifiers
            # and as values the components in those subsystems
            system_components = dict([])
            for comp, sys in self.component_system.items():
                if sys not in system_components.keys():
                    system_components[sys] = [comp,]
                else:
                    system_components[sys].append(comp)

            # Check whether any subsystem contains only a single component
            singles = []
            for sys, comps in system_components.items():
                if len(comps) <= 1:
                    singles.append("'{}'".format(comps[0].label))

            # Create message
            if len(singles) >= 1:
                message = "Component{} ".format("s"*(len(singles)>1))
                message += ", ".join(singles[:-1])
                message += " and "*(len(singles)>1) + singles[-1]
                message += " is " if len(singles)==1 else " are "
                message += "not connected to any other components"
            else:
                message = "Not all components are connected together"

        return message
