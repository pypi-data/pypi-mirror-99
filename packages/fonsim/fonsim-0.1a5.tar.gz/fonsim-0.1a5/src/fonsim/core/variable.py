"""
Class Variable

2020, July 21
"""


class Variable:
    def __init__(self, key, orientation, initial_value=0., terminal=None):
        self.key = key
        self.orientation = orientation
        self.initial_value = initial_value
        self.terminal = terminal

    def __str__(self):
        var_str = "Variable {}".format(self.key)
        if self.terminal is not None:
            var_str += " of component {}".format(self.terminal.component.label)
        return var_str

    def short_str(self, nb_var_chars=1):
        """
        Return a short string describing the variable more as a symbol than in
        words. This string contains the first n letters of the variable name
        as well as (if applicable) the port and component it is attached to.

        :param nb_var_chars: number of characters with which the variable key
        is abbreviated. Set to 0 to avoid abbreviation.
        :return var_str: short string representing the variable
        """
        var_str = self.key
        if nb_var_chars > 0:
            var_str = var_str[:min(nb_var_chars,len(var_str))]
        if self.terminal is not None:
            var_str += '_{}_{}'.format(self.terminal.label,
                                       self.terminal.component.label)
        return var_str

    def copy_and_attach(self, terminal):
        """
        Return a copy of the variable object attached to a given terminal

        :param terminal: terminal object to attach the variable copy to
        :return variable: attached copy of the variable object
        """
        return Variable(self.key, self.orientation, self.initial_value, 
                        terminal)