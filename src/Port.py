# import Constants
# import Fluid
import Node
from pysmt.shortcuts import Symbol, Plus, Times, Div, Pow, Equals, Real
from pysmt.shortcuts import Minus, GE, GT, LE, LT, And, get_model, is_sat
from pysmt.typing import REAL

class Port(Node.Node):

    def __init__(self,
                 name,
                 kind,
                 min_pressure=False,
                 min_flow_rate=False,
                 x=False,
                 y=False,
                 fluid_name='default'):
        self.attributes = {}

        if not isinstance(name, str) or not isinstance(kind, str):
            raise TypeError("name and kind must be strings")        
        else:
            self.attributes['name'] = name.lower()
            self.attributes['kind'] = kind.lower() # Types of ports we'll be supporting

        fluid_properties = Fluid.Fluid(fluid_name)

        self.set_viscoscity(Symbol(name+'_viscosity', REAL))
        self.set_min_viscoscity(fluid_properties.min_viscoscity)
        self.set_pressure(Symbol(name+'_pressure', REAL))
        self.set_min_pressure(min_pressure)
        self.set_flow_rate(Symbol(name+'_flow_rate', REAL))
        self.set_min_flow_rate(min_flow_rate)
        self.set_density(Symbol(name+'_density', REAL))
        self.set_min_density(fluid_properties.min_density)
        self.set_x(Symbol(name+'_X', REAL))
        self.set_min_x(x)
        self.set_y(Symbol(name+'_Y', REAL))
        self.set_min_y(y)

    def __repr__(self):
        return repr((self.get_name(),
                     self.get_port_kind(),
                     self.get_viscoscity(),
                     self.get_min_viscoscity(),
                     self.get_pressure(),
                     self.get_min_pressure(),
                     self.get_flow_rate(),
                     self.get_min_flow_rate(),
                     self.get_density(),
                     self.get_min_density(),
                     self.get_x(),
                     self.get_min_x(),
                     self.get_y(),
                     self.get_min_y()
                     ))

    def get_name(self):
        return self.attributes['name']

    def get_port_kind(self):
        return self.attributes['kind']

    def set_viscoscity(self, viscoscity):
        self.attributes['viscoscity'] = viscoscity

    def get_viscoscity(self):
        return self.attributes['viscoscity']

    def set_min_viscoscity(self, min_viscoscity):
        try:
            if min_viscoscity < 0 and min_viscoscity is not False:
                raise ValueError("port '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_viscoscity))
        except TypeError as e:
            raise TypeError("port '%s' parameter '%s' must be int" %
                            (self.get_name(), min_viscoscity))
        except ValueError as e:
            raise ValueError(e)

        self.attributes['min_viscoscity'] = min_viscoscity

    def get_min_viscoscity(self):
        return self.attributes['min_viscoscity']

    def set_pressure(self, pressure):
        self.attributes['pressure'] = pressure

    def get_pressure(self):
       return self.attributes['pressure']

    def set_min_pressure(self, min_pressure):
        try:
            if min_pressure < 0 and min_pressure is not False:
                raise ValueError("port '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_pressure))
        except TypeError as e:
            raise TypeError("port '%s' parameter '%s' must be int" %
                            (self.get_name(), min_pressure))
        except ValueError as e:
            raise ValueError(e)

        self.attributes['min_pressure'] = min_pressure

    def get_min_pressure(self):
        return self.attributes['min_pressure']

    def set_flow_rate(self, flow_rate):
        self.attributes['flow_rate'] = flow_rate

    def get_flow_rate(self):
        return self.attributes['flow_rate']

    def set_min_flow_rate(self, min_flow_rate):
        try:
            if min_flow_rate < 0 and min_flow_rate is not False:
                raise ValueError("port '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_flow_rate))
        except TypeError as e:
            raise TypeError("port '%s' parameter '%s' must be int" %
                            (self.get_name(), min_flow_rate))
        except ValueError as e:
            raise ValueError(e)

        self.attributes['min_flow_rate'] = min_flow_rate

    def get_min_flow_rate(self):
        return self.attributes['min_flow_rate']

    def set_density(self, density):
        self.attributes['density'] = density

    def get_density(self):
        return self.attributes['density']

    def set_min_density(self, min_density):
        try:
            if min_density < 0 and min_density is not False:
                raise ValueError("port '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_density))
        except TypeError as e:
            raise TypeError("port '%s' parameter '%s' must be int" %
                            (self.get_name(), min_density))
        except ValueError as e:
            raise ValueError(e)

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
                raise ValueError("port '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_x))
        except TypeError as e:
            raise TypeError("port '%s' parameter '%s' must be int" %
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
                raise ValueError("port '%s' parameter '%s' must be >= 0" %
                                 (self.get_name(), min_y))
        except TypeError as e:
            raise TypeError("port '%s' parameter '%s' must be int" %
                            (self.get_name(), min_y))
        except ValueError as e:
            raise ValueError(e)

        self.attributes['min_y'] = min_y

    def get_min_y(self):
        return self.attributes['min_y']


class OutputPort(Port):

    def __init__(self,
                 name,
                 kind,
                 min_pressure=False,
                 min_flow_rate=False,
                 x=False,
                 y=False,
                 fluid_name='default'):

        Port.__init__(self,
                      name,
                      'output',
                      min_presure,
                      min_flow_rate,
                      x,
                      y,
                      fluid_name)

    def translate_output(self):
        """Create SMT expressions for bounding the parameters of an output port
        to be within the constraints defined by the user

        :param str name: Name of the port to be constrained
        :returns: None -- no issues with translating the port parameters to SMT
        """
        if len(self.incoming_channels) <= 0:
            raise ValueError("Port %s must have 1 or more connections" % self.get_name())
        if self.incoming_channels
        
        
        # Currently don't support this, and I don't think it would be the case
        # in real circuits, an output port is considered the end of a branch
        if len(self.outgoing_channels) != 0:
            raise ValueError("Cannot have channels out of output port %s" % self.get_name())

        
        # Since input is just a specialized node, call translate node
        self.exprs.append(Node.Node().translate(self)) #TODO: test this

        # Calculate flow rate for this port based on pressure and channels out
        # if not specified by user
        if not self.get_min_flow_rate(name):
            # The flow rate at this node is the sum of the flow rates of the
            # the channel coming in (I think, should be verified)
            total_flow_in = []
            for incoming_channel in self.incoming_channels:
                # TODO: This is where the flow rate calls to the input nodes get triggered
                self.exprs.append(incoming_channel)
                total_flow_in.append(incoming_channel.get_flow_rate())
            
            if len(total_flow_in) == 1: # only one incoming channel
                self.exprs.append(Equals(self.get_flow_rate(),
                                         total_flow_in[0]))
            else:
                self.exprs.append(Equals(self.get_flow_rate(),
                                         Plus(total_flow_in)))

        '''
            Here iterate over the incoming channels and call translate over them
            for incomming_channel in self.incoming_channels:
                self.expers.append(incomming_channel.translate())
                # Once it gets back from translating we can get the flow rate
                total_flow_in.append(channel_in.get_channel_flow_rate())
        '''
        
        return self.exprs

class IncomingPort(Port):

    def __init__(self,
                 name,
                 kind,
                 min_pressure=False,
                 min_flow_rate=False,
                 x=False,
                 y=False,
                 fluid_name='default'):

        Port.__init__(self,
                      name,
                      'input',
                      min_presure,
                      min_flow_rate,
                      x,
                      y,
                      fluid_name)

    def calculate_flow_rate(self):
        """Calculate the flow rate into a port based on the cross sectional
        area of the channel it flows into, the pressure and the density
        eqn from https://en.wikipedia.org/wiki/Hagen-Poiseuille_equation
        flow_rate = area * sqrt(2*pressure/density)
        Unit for flow rate is m^3/s

        :param str name: Name of the port
        :returns: Flow rate determined from port pressure and area of
                  connected channels
        """
        areas = []
        for outgoing_channel in self.outgoing_channels:
            areas.append(outgoing_channel.calculate_channel_area())

        total_area = Plus(areas)

        return Times(total_area,
                     Pow(Div(Times(Real(2),
                                   self.get_pressure()
                                   ),
                             self.get_density()
                             ),
                         Real(0.5)
                         ))


    def translate_input(self, name):
        """Create SMT expressions for bounding the parameters of an input port
        to be within the constraints defined by the user

        :param name: Name of the port to be constrained
        :returns: None -- no issues with translating the port parameters to SMT
        """
        if len(self.outgoing_channels) <= 0:
            raise ValueError("Port %s must have 1 or more connections" % self.get_name())
        

        # Currently don't support this, and I don't think it would be the case
        # in real circuits, an input port is the beginning of the traversal
        if len(self.incoming_channels) != 0:
            raise ValueError("Cannot have channels into input port %s" % name)


        # Since input is a type of node, call translate node
        self.exprs.append(self.translate_node(name))

        # Calculate flow rate for this port based on pressure and channels out
        # if not specified by user
        if not self.get_min_flow_rate():
            flow_rate = self.calculate_flow_rate(name)
            self.exprs.append(Equals(self.get_flow_rate(), flow_rate))

        #TODO: We don't need to do anything since this is an input port
        # # To recursively traverse, call on all successor channels
        # for outgoing_channel in self.outgoing_channels:
        #     self.expers.append(outgoing_channel.translate())

        return self.expers
