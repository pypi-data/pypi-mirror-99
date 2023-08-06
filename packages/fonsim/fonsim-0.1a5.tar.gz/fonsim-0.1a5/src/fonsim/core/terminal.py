"""
Class Terminal

Component connection point with local through and across variables

2020, July 22
"""

from . import variable


class Terminal:
    def __init__(self, label, variables):
        self.label = label

        self.variables_across = {}
        self.variables_through = {}
        for variable in variables:
            local_variable = variable.copy_and_attach(self)
            if variable.orientation == 'across':
                self.variables_across[variable.key] = local_variable
            elif variable.orientation == 'through':
                self.variables_through[variable.key] = local_variable

        self.component = None
        self.isconnected = False

    def get_variables(self, orientation=None):
        """
        Get list of all terminal variables with the given orientation.
        The orientation can be either "through" or "across". If not
        provided or None, all variables regardless of orientation are
        returned

        :param orientation: optional string specifying desired
        variable orientation
        :return: list of Variable objects
        """
        if orientation == 'through':
            return list(self.variables_through.values())
        elif orientation == 'across':
            return list(self.variables_across.values())
        else:
            return self.get_variables('through') + \
                   self.get_variables('across')

    def get_variable(self, key):
        """
        Return the variable object attached to the terminal with the
        provided key. If there is no variable with the requested key,
        None is returned

        :param key: key of the variable to return
        :return variable: attached variable with the matching key
        """
        if key in self.variables_across.keys():
            return self.variables_across[key]
        if key in self.variables_through.keys():
            return self.variables_through[key]

    def __call__(self, arg):
        return self.get_variable(arg)
