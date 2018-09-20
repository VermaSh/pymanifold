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

    def translate(self):
        """Create SMT expressions for bounding the parameters of an output port
        to be within the constraints defined by the user

        :param str name: Name of the port to be constrained
        :returns: None -- no issues with translating the port parameters to SMT
        """

        incoming_channels = self.get_incoming_channels()
        if len(incoming_channels) <= 0:
            raise ValueError("Port %s must have 1 or more connections" % self.get_name())
        
        # Currently don't support this, and I don't think it would be the case
        # in real circuits, an output port is considered the end of a branch
        outgoing_channels = self.get_outgoing_channels()
        if len(outgoing_channels) != 0:
            raise ValueError("Cannot have channels out of output port %s" % self.get_name())

        
        # Since input is just a specialized node, call translate node
        self.exprs.append(Node.Node().translate(self)) #TODO: test this

        # Calculate flow rate for this port based on pressure and channels out
        # if not specified by user
        if not self.get_min_flow_rate(name):
            # The flow rate at this node is the sum of the flow rates of the
            # the channel coming in (I think, should be verified)
            total_flow_in = []
            for incoming_channel in incoming_channels:
                # TODO: This is where the flow rate calls to the input nodes get triggered
                self.exprs.append(incoming_channel)
                total_flow_in.append(incoming_channel.get_flow_rate())
            
            if len(total_flow_in) == 1: # only one incoming channel
                self.exprs.append(Equals(self.get_flow_rate(),
                                         total_flow_in[0]))
            else:
                self.exprs.append(Equals(self.get_flow_rate(),
                                         Plus(total_flow_in)))
            
            self.expers.append(incomming_channel.translate())
            # Once it gets back from translating we can get the flow rate
            total_flow_in.append(channel_in.get_channel_flow_rate())

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


    def translate(self):
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
            raise ValueError("Cannot have channels into input port %s" % self.get_name())


        # Since input is a type of node, call translate node
        self.exprs.append(Port.translate())

        # Calculate flow rate for this port based on pressure and channels out
        # if not specified by user
        if not self.get_min_flow_rate():
            flow_rate = self.calculate_flow_rate()
            self.exprs.append(Equals(self.get_flow_rate(), flow_rate))

        #TODO: We don't need to do anything since this is an input port
        # # To recursively traverse, call on all successor channels
        # for outgoing_channel in self.outgoing_channels:
        #     self.expers.append(outgoing_channel.translate())

        return self.expers


class TJunction(Port):

    def __init__(self, input_node1, input_node2, output_node3):
        
        if not isinstance(input_node1, IncomingPort) or not isinstance(input_node2, IncomingPort):
            raise TypeError("The first two parameters should be of type IncomingPort")

        self.input_nodes = {}
        self.input_nodes[input_node1] = input_node1
        self.input_nodes[input_node2] = input_node2
        
        if not isinstance(output_node3, OutputPort):
            raise TypeError("The first two parameters should be of type OutputPort")
        self.output_node = output_node3

    def get_input_nodes(self):
        return self.input_nodes       
    
    def get_output_node(self):
        return self.output_node

    def cosine_law_crit_angle(self):
        """Use cosine law to find cos^2(theta) between three points
        node1---node2---node3 to assert that it is less than cos^2(thetaC)
        where thetaC is the critical crossing angle

        :param node1: Outside node
        :param node2: Middle connecting node
        :param node3: Outside node
        :returns: cos^2 as calculated using cosine law (a_dot_b^2/a^2*b^2)
        """
        node1 = self.get_input_nodes().values()[0]
        node2 = self.get_input_nodes().values()[1]
        node3 = self.get_output_node()

        # Lengths of channels
        aX = Minus(node1.get_x(), node2.get_x())
        aY = Minus(node1.get_y(), node2.get_y())
        bX = Minus(node3.get_x(), node2.get_x())
        bY = Minus(node3.get_y(), node2.get_y())
        # Dot products between each channel
        a_dot_b_squared = Pow(Plus(Times(aX, bX),
                                 Times(aY, bY)
                                 ),
                            Real(2)
                            )
        a_squared_b_squared = Times(Plus(Times(aX, aX),
                                       Times(aY, aY)
                                       ),
                                  Plus(Times(bX, bX),
                                       Times(bY, bY)
                                       ),
                                  )
        return Div(a_dot_b_squared, a_squared_b_squared)

    def calculate_droplet_volume(self, h, w, wIn, epsilon, qD, qC):
        """From paper DOI:10.1039/c002625e.
        Calculating the droplet volume created in a T-junction
        Unit is volume in m^3

        :param Symbol h: Height of channel
        :param Symbol w: Width of continuous/output channel
        :param Symbol wIn: Width of dispersed_channel
        :param Symbol epsilon: Equals 0.414*radius of rounded edge where
                               channels join
        :param Symbol qD: Flow rate in dispersed_channel
        :param Symbol qC: Flow rate in continuous_channel
        """
        q_gutter = Real(0.1)
        # normalizedVFill = 3pi/8 - (pi/2)(1 - pi/4)(h/w)
        v_fill_simple = Minus(
                Times(Real((3, 8)), Real(math.pi)),
                Times(Times(
                            Div(Real(math.pi), Real(2)),
                            Minus(Real(1),
                                  Div(Real(math.pi), Real(4)))),
                      Div(h, w)))

        hw_parallel = Div(Times(h, w), Plus(h, w))

        # r_pinch = w+((wIn-(hw_parallel - eps))+sqrt(2*((wIn-hw_parallel)*(w-hw_parallel))))
        r_pinch = Plus(w,
                       Plus(Minus(
                                  wIn,
                                  Minus(hw_parallel, epsilon)),
                            Pow(Times(
                                      Real(2),
                                      Times(Minus(wIn, hw_parallel),
                                            Minus(w, hw_parallel)
                                            )),
                                Real(0.5))))
        r_fill = w
        alpha = Times(Minus(
                            Real(1),
                            Div(Real(math.pi), Real(4))
                            ),
                      Times(Pow(
                                Minus(Real(1), q_gutter),
                                Real(-1)
                                ),
                            Plus(Minus(
                                       Pow(Div(r_pinch, w), Real(2)),
                                       Pow(Div(r_fill, w), Real(2))
                                       ),
                                 Times(Div(Real(math.pi), Real(4)),
                                       Times(Minus(
                                                   Div(r_pinch, w),
                                                   Div(r_fill, w)
                                                   ),
                                             Div(h, w)
                                             )))))

        return Times(Times(h, Times(w, w)),
                     Plus(v_fill_simple, Times(alpha, Div(qD, qC))))

    def channels_in_straight_line(self):
        """Create expressions to assert that 2 channels are in a straight
        line with each other by asserting that a triangle between the 2
        end nodes and the middle node has zero area

        :returns: Expression asserting area of triangle formed between all
            three nodes to be 0
        """
        # TODO: will this be an issue with classes!
        # Check that these nodes connect
        # try:
        #     self.dg[node1_name][node2_name]
        #     self.dg[node2_name][node3_name]
        # except TypeError as e:
        #     raise TypeError("Tried asserting that 2 channels are in a straight\
        #         line but they aren't connected")

        node1 = self.get_input_nodes().values()[0]
        node2 = self.get_input_nodes().values()[1]
        node3 = self.get_output_node()

        # Constrain that continuous and output ports are in a straight line by
        # setting the area of the triangle formed between those two points and
        # the center of the t-junct to be 0
        # Formula for area of a triangle given 3 points
        # x_i (y_p − y_j ) + x_p (y_j − y_i ) + x_j (y_i − y_p ) / 2
        return Equals(Real(0),
                      Div(Plus(Times(node1.get_x(),
                                     Minus(node3.get_y(), node2.get_y())
                                     ),
                               Plus(Times(node3.get_x(),
                                          Minus(node2.get_y(), node1.get_y())
                                          ),
                                    Times(node2.get_x(),
                                          Minus(node1.get_y(), node3.get_y())
                                          ))),
                          Real(2)
                          ))

    def translate(self, crit_crossing_angle=0.5):
        """Create SMT expressions for a t-junction node that generates droplets
        Must have 2 input channels (continuous and dispersed phases) and one
        output channel where the droplets leave the node. Continuous is usually
        oil and dispersed is usually water

        :param crit_crossing_angle: The angle of the dispersed channel to
            the continuous must be great than this to have droplet generation
        :returns: None -- no issues with translating channel parameters to SMT
        :raises: KeyError, if channel is not found in the list of defined edges
        """
        # Validate input
        ''' TODO: check if the nodes are valid, need a list of parameters
                to check
        '''
        # if self.dg.size(name) != 3:
        #     raise ValueError("T-junction %s must have 3 connections" % name)

        # Since T-junction is just a specialized node, call translate node
        Port.translate(name) # self.translate_node(name)

        # Renaming for consistency with the other nodes
        junction_node_name = self.get_name()

        # these will be found later from iterating through the dict of
        # predecessor nodes to the junction node
        continuous_node = ''
        continuous_node_name = ''
        continuous_channel = ''
        dispersed_node = ''
        dispersed_node_name = ''
        dispersed_channel = ''

        #TODO: reWrite this!
        # NetworkX allows for the creation of dicts that contain all of
        # the edges containing a certain attribute, in this case phase is
        # of interest
        phases = nx.get_edge_attributes(self.dg, 'phase')
        for pred_node, phase in phases.items(): #This can be achieved with a local list
            if phase == 'continuous':
                continuous_node_name = pred_node[0]
                continuous_node = self.dg.nodes[continuous_node_name]
                continuous_channel = self.dg[continuous_node_name][junction_node_name]
                # assert width and height to be equal to output
                self.exprs.append(Equals(continuous_channel['width'],
                                         output_channel['width']
                                         ))
                self.exprs.append(Equals(continuous_channel['height'],
                                         output_channel['height']
                                         ))
            elif phase == 'dispersed':
                dispersed_node_name = pred_node[0]
                dispersed_node = self.dg.nodes[dispersed_node_name]
                dispersed_channel = self.dg[dispersed_node_name][junction_node_name]
                # Assert that only the height of channel be equal
                self.exprs.append(Equals(dispersed_channel['height'],
                                         output_channel['height']
                                         ))
            elif phase == 'output':
                continue
            else:
                raise ValueError("Invalid phase for T-junction: %s" % name)

        # Epsilon, sharpness of T-junc, must be greater than 0
        epsilon = Symbol('epsilon', REAL)
        self.exprs.append(GE(epsilon, Real(0)))

        # TODO: Figure out why original had this cause it doesn't seem true
        #  # Pressure at each of the 4 nodes must be equal
        #  self.exprs.append(Equals(junction_node['pressure'],
        #                           continuous_node['pressure']
        #                           ))
        #  self.exprs.append(Equals(junction_node['pressure'],
        #                           dispersed_node['pressure']
        #                           ))
        #  self.exprs.append(Equals(junction_node['pressure'],
        #                           output_node['pressure']
        #                           ))

        # Viscosity in continous phase equals viscosity at output
        self.exprs.append(Equals(continuous_node['viscosity'],
                                 output_node['viscosity']
                                 ))

        # Flow rate into the t-junction equals the flow rate out
        self.exprs.append(Equals(Plus(continuous_channel['flow_rate'],
                                      dispersed_channel['flow_rate']
                                      ),
                                 output_channel['flow_rate']
                                 ))

        # Assert that continuous and output channels are in a straight line
        self.exprs.append(self.channels_in_straight_line(continuous_node_name,
                                                         junction_node_name,
                                                         output_node_name
                                                         ))

        # Droplet volume in channel equals calculated droplet volume
        # TODO: Manifold also has a table of constraints in the Schematic and
        # sets ChannelDropletVolume equal to dropletVolumeConstraint, however
        # the constraint is void (new instance of RealTypeValue) and I think
        # could conflict with calculated value, so ignoring it for now but
        # may be necessary to add at a later point if I'm misunderstand why
        # its needed
        v_output = output_channel['droplet_volume']
        self.exprs.append(Equals(v_output,
                                 self.calculate_droplet_volume(
                                     output_channel['height'],
                                     output_channel['width'],
                                     dispersed_channel['width'],
                                     epsilon,
                                     dispersed_node['flow_rate'],
                                     continuous_node['flow_rate']
                                 )))

        # Assert critical angle is <= calculated angle
        cosine_squared_theta_crit = Real(math.cos(
            math.radians(crit_crossing_angle))**2)
        # Continuous to dispersed
        self.exprs.append(LE(cosine_squared_theta_crit,
                             self.cosine_law_crit_angle(continuous_node_name,
                                                        junction_node_name,
                                                        dispersed_node_name
                                                        )))
        # Continuous to output
        self.exprs.append(LE(cosine_squared_theta_crit,
                             self.cosine_law_crit_angle(continuous_node_name,
                                                        junction_node_name,
                                                        output_node_name
                                                        )))
        # Output to dispersed
        self.exprs.append(LE(cosine_squared_theta_crit,
                             self.cosine_law_crit_angle(output_node_name,
                                                        junction_node_name,
                                                        dispersed_node_name
                                                        )))
        # Call translate on output
        self.translation_strats[output_node['kind']](output_node_name)