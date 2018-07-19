from pysmt.shortcuts import Symbol, Plus, Times, Div, Pow, Equals, Real
from pysmt.shortcuts import Minus, GE, GT, LE, LT, And, get_model, is_sat
from pysmt.typing import REAL

class Node():

    # DONE - node < init
    # DONE - translate_node
    # translate_chip

    def __init__ (self, name, x=False, y=False, kind='node'):
        """Create new node where fluids merge or split, kind of node (T-junction,
        Y-junction, cross, etc.) can be specified if not then a basic node
        connecting multiple channels will be created, units in brackets

        :param str name: Name of the node to use when connecting to a channel
        :param float x:  Set the X position of this node (m)
        :param float y:  Set the Y position of this node (m)
        :param str kind: The type of node this is, default is node, other
            option is t-junction
        :returns: None -- no issues with creating this node
        :raises: TypeError if an input parameter is wrong type
                 ValueError if an input parameter has an invalid value
        """
        # Checking that arguments are valid
        if not isinstance(name, str) or not isinstance(kind, str):
            raise TypeError("name and kind must be strings")
        if name in self.dg.nodes:
            raise ValueError("Must provide a unique name")
        if kind.lower() not in self.translation_strats.keys():
            raise ValueError("kind must be %s" % self.translation_strats.keys())

        self.incoming_channels = {}
        self.outgoing_channels = {}
        self.attributes = {}

        # Ports are stored with nodes because ports are just a specific type of
        # node that has a constant flow rate only accept ports of the right
        # kind (input or output)
        # While the user can't define most parameters for a node because it
        # doesnt take an input from outside the chip, they're still added
        # and set to zero so checks to each node to see if there is a min
        # value for each node doesn't raise a KeyError
        self.set_name(name)
        self.set_kind(kind.lower())
        self.set_pressure(Symbol(name+'_pressure', REAL))
        self.set_min_pressure(None)
        self.set_flow_rate(Symbol(name+'_flow_rate', REAL))
        self.set_min_flow_rate(None)
        self.set_viscosity(Symbol(name+'_viscosity', REAL))
        self.set_min_viscosity(None)
        self.set_density(Symbol(name+'_density', REAL))
        self.set_min_density(None)
        self.set_x(Symbol(name+'_X', REAL))
        self.set_min_x(x)
        self.set_y(Symbol(name+'_Y', REAL))
        self.set_min_y(y)
        return

    def set_name(self, name):
        self.attributes['name'] = name
    def get_name(self):
        return self.attributes['name']

    def set_kind(self, kind):
        self.attributes['kind'] = kind
    def set_kind(self):
        return self.attributes['kind']

    def set_pressure(self, pressure):
        self.attributes['pressure'] = pressure
    def get_pressure(self):
        return self.attributes['pressure']

    def set_min_pressure(self, min_pressure):
        self.attributes['min_pressure'] = min_pressure
    def sgt_min_pressure(self):
        return self.attributes['min_pressure']

    def set_flow_rate(self, flow_rate):
        self.attributes['flow_rate'] = flow_rate
    def get_flow_rate(self):
        return self.attributes['flow_rate']

    def set_min_flow_rate(self, min_flow_rate):
        self.attributes['min_flow_rate'] = min_flow_rate
    def get_min_flow_rate(self):
        return self.attributes['min_flow_rate']

    def set_viscosity(self, viscosity):
        self.attributes['viscosity'] = viscosity
    def get_viscosity(self):
        return self.attributes['viscosity']

    def set_min_viscosity(self, min_viscosity):
        self.attributes['min_viscosity'] = min_viscosity
    def get_min_viscosity(self):
        return self.attributes['min_viscosity']

    def set_density(self, density):
        self.attributes['density'] = density
    def get_density(self):
        return self.attributes['density']

    def set_min_density(self, min_density):
        self.attributes['min_density'] = min_density
    def get_min_density(self):
        return self.attributes['min_density']

    def set_x(self, x):
        self.attributes['x'] = x
    def get_x(self):
        return self.attributes['x']

    def set_min_x(self, min_x):
        try:
            if min_x < 0 and min_x is not False:
                raise ValueError("node '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_x))
        except TypeError as e:
            raise TypeError("node '%s' parameter '%s' must be int" %
                            (self.get_name(), min_x))
        except ValueError as e:
            raise ValueError(e)
        self.attributes['min_x'] = min_x
    def get_min_x(self):
        return self.attributes['min_x']

    def set_y(self, y):
        self.attributes['y'] = y
    def get_y(self):
        return self.attributes['y']

    def set_min_y(self, min_y):
        try:
            if min_y < 0 and min_y is not False:
                raise ValueError("node '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_y))
        except TypeError as e:
            raise TypeError("node '%s' parameter '%s' must be int" %
                            (self.get_name(), min_y))
        except ValueError as e:
            raise ValueError(e)
        
        self.attributes['min_y'] = min_y
    def get_min_y(self):
        return self.attributes['min_y']

    def translate(self):
        """Create SMT expressions for bounding the parameters of an node
        to be within the constraints defined by the user

        :param name: Name of the node to be constrained
        :returns: None -- no issues with translating the port parameters to SMT
        """

        # Pressure at a node is the sum of the pressures flowing into it
        output_pressures = []
        for incoming_connection in self.incoming_channels: # Shubham - Call incoming connections here
            # This returns the nodes with channels that flowing into this node
            # pressure calculated based on P=QR
            # Could modify equation based on https://www.dolomite-microfluidics.com/wp-content/uploads/Droplet_Junction_Chip_characterisation_-_application_note.pdf
            output_pressures.append(incoming_connection.calculate_channel_output_pressure())

        if len(output_pressures) == 1:
            self.exprs.append(Equals(self.get_node_pressure(name),
                                     output_pressures[0]
                                     ))                        
        elif len(output_pressures) > 1:
            self.exprs.append(Equals(self.get_node_pressure(name),
                                     Plus(output_pressures)
                                     ))

        # If parameters are provided by the user, then set the
        # their Symbol equal to that value, otherwise make it greater than 0

        # Checks if min pressure has been set
        if self.get_min_pressure():
            # named_node['pressure'] returns a variable for that node for its
            # pressure to be solved for by SMT solver, if min_pressure has a
            # value then a user defined value was provided and this variable
            # is set equal to this value, else simply set its value to be > 0
            # same is true for viscosity, pressure, flow_rate, X, Y and density
            self.exprs.append(Equals(self.get_pressure(),
                                     Real(self.get_min_pressure())
                                     ))
            # if it has, we want pressure to be equal to min pressure
        else:
            # else, we just want it to be positive
            self.exprs.append(GT(self.get_pressure(), Real(0)))

        # Checks if node min x has been set
        if self.get_min_x(): #TODO: is it ok to assume that if x is set both will be?
            # If it has, node min x or y has been set, then x or y must equal them
            self.exprs.append(Equals(self.get_x(), Real(self.get_min_x())))
            self.exprs.append(Equals(self.get_y(), Real(self.get_min_y())))
        else:
            # else, they must be positive
            self.exprs.append(GE(self.get_x(), Real(0)))
            self.exprs.append(GE(self.get_y(), Real(0)))

        # Checks if min flow rate has been set
        if self.get_min_flow_rate():
            # If it has, node flow rate must equal min flow rate
            self.exprs.append(Equals(self.get_flow_rate(),
                                     Real(self.get_min_flow_rate())
                                     ))
        else:
            # else, node flow rate must be positive
            self.exprs.append(GT(self.get_flow_rate(), Real(0)))
        
        # Checks if min viscosity has been set
        if self.get_min_viscosity():

            # If it has, node viscosity must equal min viscosity
            self.exprs.append(Equals(self.get_viscosity(),
                                     Real(self.get_min_viscosity())
                                     ))
        else:
            # else, node viscosity must be positive
            self.exprs.append(GT(self.get_viscosity(), Real(0)))

        # Checks if the min density has been set
        if self.get_min_density():
            # If it has been, node density must equal min_density
            self.exprs.append(Equals(self.get_density(),
                                     Real(self.get_min_density())
                                     ))
        else:
            # else, node density must be positive
            self.exprs.append(GT(self.get_density(), Real(0)))
        
        return self.exprs


    def append_outgoing_channel(self, outgoing_channel):
        self.outgoing_channels[outgoing_channel.get_name()] = outgoing_connection

    def append_incoming_channel(self, incoming_channel):
        self.incoming_channels[incoming_channel.get_name()] = incoming_channel

    class TJunction():
        # cosine_law_crit_angle


