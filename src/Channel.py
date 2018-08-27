import Constants
import Port
from pysmt.shortcuts import Symbol, Plus, Times, Div, Pow, Equals, Real
from pysmt.shortcuts import Minus, GE, GT, LE, LT, And, get_model, is_sat
from pysmt.typing import REAL

class Channel():

    # TODO: look into using reprlib instead of repr

    # DONE - inits
    # DONE - pythagorean_length
    # DONE - calculate_resistance
    # DONE - Calculate channel output pressure
    # DONE - simple_pressure_flow
    '''TODO: More info regarding dix graph
           - Can we store the ports in each channel instead of the graph?
    '''
    # channels_in_straight_line
    # translate
    # translate_channel
        # LIne 473 is just checking if the variables have been assigned

    def __init__(self, 
                 port_in,
                 port_out,
                 name='channel',
                 min_length=False, 
                 min_width=False, 
                 min_hegiht=False, 
                 kind='rectangle', 
                 phase='None'):

        if (Constants.ChannelTypes().isChannelTypeValid(kind)):

            # Add the information about that connection to another dict
            # There's extra parameters in here than in the arguments because they
            # are values calculated by later methods when creating the SMT eqns
            # Channels do not have pressure though, since it decreases linearly
            # across the channel
            self.attributes = {}
            self.set_kind(kind)
            self.set_length(Symbol('_'.join([port_in, port_out, 'length']), REAL))
            self.set_min_length(min_length)
            self.set_width(Symbol('_'.join([port_in, port_out, 'width']), REAL))
            self.set_min_width(min_width)
            self.set_height(Symbol('_'.join([port_in, port_out, 'height']), REAL))
            self.set_min_height(min_height)
            self.set_flow_rate(Symbol('_'.join([port_in, port_out, 'flow_rate']), REAL))
            self.set_droplet_volume(Symbol('_'.join([port_in, port_out, 'Dvol']), REAL))
            self.set_viscosity(Symbol('_'.join([port_in, port_out, 'viscosity']), REAL))
            self.set_resistance(Symbol('_'.join([port_in, port_out, 'res']), REAL))
            self.set_phase(phase.lower())
            self.set_port_in(port_in)
            self.set_port_out(port_out)
            self.exprs = {}

            #TODO: Move the extra to outside of channel class, back to caller class

 
    def __repr__(self):
        return repr((self.attributes['kind'],
                     self.attributes['length'],
                     self.attributes['min_length'],
                     self.attributes['width'],
                     self.attributes['min_width'],
                     self.attributes['height'],
                     self.attributes['min_height'],
                     self.attributes['flow_rate'],
                     self.attributes['droplet_volume'],
                     self.attributes['viscosity'],
                     self.attributes['resistance'],
                     self.attributes['phase'],
                     self.attributes['port_in'],
                     self.attributes['port_out']
                    ))

    def __str__(self):
        return ('kind          : ' + self.get_kind()
                + '\nlength        : ' + str(self.get_length())
                + '\nmin_length    : ' + str(self.get_min_length())
                + '\nwidth         : ' + str(self.get_width())
                + '\nmin_width     : ' + str(self.get_min_width())
                + '\nheight        : ' + str(self.get_height())
                + '\nmin_height    : ' + str(self.get_min_height())
                + '\nflow_rate     : ' + str(self.get_flow_rate())
                + '\ndroplet_volume: ' + str(self.get_droplet_volume())
                + '\nviscosity     : ' + str(self.get_viscosity())
                + '\nresistance    : ' + str(self.get_resistance())
                + '\nphase         : ' + str(self.get_phase())
                + '\nport_in       : ' + self.get_port_in()
                + '\nport_out      : ' + self.get_port_out()
                )


    def set_name(self, name):
        self.attributes['name'] = name

    def get_name(self):
        return self.attributes['name']

    def set_kind(self, kind):
        self.attributes['kind'] = kind

    def get_kind(self):
        return self.attributes['kind']

    def set_length(self, length):
        self.attributes['length'] = length

    def get_length(self):
        return self.attributes['length']

    def error_check(self, value, param_name):
        try:
            if value < 0 and (value is not False) :
                raise ValueError("channel value parameter '%s' must be >= 0" %param_name)
        except TypeError as e:
            raise TypeError("channel '%s' parameter must be int" % param_name)
        except ValueError as e:
            raise ValueError(e)

        return False


    def set_min_length(self, min_length):
        # TODO: look up value error and type error
        try:
            if min_length < 0 and (min_length is not False) :
                raise ValueError("channel min_length parameter min_length must be >= 0")
        except TypeError as e:
            raise TypeError("channel min_length parameter must be int" % param)
        except ValueError as e:
            raise ValueError(e)

        self.attributes['min_length'] = min_length

    def get_min_length(self):
        return self.attributes['min_length']

    def set_width(self, width):
        self.attributes['width'] = width

    def get_width(self):
        return self.attributes['width']

    def set_min_width(self, min_width):

        try:
            if min_width < 0 and (min_width is not False):
                raise ValueError("channel min_width parameter, min_width must be >= 0")
        except TypeError as e:
            raise TypeError("channel min_width parameter must be int")
        except ValueError as e:
            raise ValueError(e)

        self.attributes['min_width'] = min_width

    def get_min_width(self):
        return self.attributes['min_width']

    def set_height(self, height):
        self.attributes['height'] = height

    def get_height(self):
        return self.attributes['height']

    def set_min_height(self, min_height):

        try:
            if min_height < 0 and (min_height is not False):
                raise ValueError("channel min_height parameter, min_width must be >= 0")
        except TypeError as e:
            raise TypeError("channel min_height parameter must be int")
        except ValueError as e:
            raise ValueError(e)

        self.attributes['min_height'] = min_height

    def get_min_height(self):
        return self.attributes['min_height']

    def set_flow_rate(self, flow_rate):
        self.attributes['flow_rate'] = flow_rate

    def get_flow_rate(self):
        ''' TODO: ask, What value should we be looking for as an indication
                  that the flow rate value needs to be calculated
        '''
        return self.attributes['flow_rate']

    def set_droplet_volume(self, droplet_volume):
        self.attributes['droplet_volume'] = droplet_volume

    def get_droplet_volume(self):
        return self.attributes['droplet_volume']

    def set_viscosity(self, viscosity):
        self.attributes['viscosity'] = viscosity

    def get_viscosity(self):
        return self.attributes['viscosity']

    def set_resistance(self, resistance):
        self.attributes['resistance'] = resistance

    def get_resistance(self):
        return self.attributes['resistance']

    def set_phase(self, phase):
        self.attributes['phase'] = phase

    def get_phase(self):
        return self.attributes['phase']

    def set_port_in(self, port_in):
        self.attributes['port_in'] = port_in

    def get_port_in(self):
        return self.attributes['port_in']

    def set_port_out(self, port_out):
        self.attributes['port_out'] = port_out

    def get_port_out(self):
        return self.attributes['port_out']

    def pythagorean_length(self):
        # TODO: How do I test this!!
        """Use Pythagorean theorem to assert that the channel length
        (hypoteneuse) squared is equal to the legs squared so channel
        length is solved for

        :param str channel_name: Name of the channel
        :returns: SMT expression of the equality of the side lengths squared
            and the channel length squared
        """

        port_in = self.get_port_in(self)
        port_out = self.get_port_out(self)
        side_a = Minus(port_in.get_x(), port_in.get_x())
        side_b = Minus(port_in.get_y(), port_in.get_y())

        a_squared = Pow(side_a, Real(2))
        b_squared = Pow(side_b, Real(2))

        a_squared_plus_b_squared = Plus(a_squared, b_squared)

        c_squared = Pow(self.get_length(), Real(2))

        return Equals(a_squared_plus_b_squared, c_squared)

    def calculate_resistance(self):
        """Calculate the droplet resistance in a channel using:
        R = (12 * mu * L) / (w * h^3 * (1 - 0.630 (h/w)) )
        This formula assumes that channel height < width, so
        the first term returned is the assertion for that
        Unit for resistance is kg/(m^4*s)

        :param str channel_name: Name of the channel
        :returns: list -- two SMT expressions, first asserts
            that channel height is less than width, second
            is the above expression in SMT form
        """
        w = self.get_width()
        h = self.get_height()
        mu = self.get_viscosity()
        chL = self.get_length()
        return (LT(h, w),
                Div(Times(Real(12),
                          Times(mu, chL)
                          ),
                    Times(w,
                          Times(Pow(h, Real(3)),
                                Minus(Real(1),
                                      Times(Real(0.63),
                                            Div(h, w)
                                            ))))))        
    
    def calculate_channel_output_pressure(self):
        """Calculate the pressure at the output of a channel using
        P_out = R * Q - P_in
        Unit for pressure is Pascals - kg/(m*s^2)

        :param str channel_name: Name of the channel
        :returns: SMT expression of the difference between pressure
            into the channel and R*Q
        """
        P_in = self.get_port_in().get_pressure()
        R = self.get_resistance()
        Q = self.get_flow_rate()
        return Minus(P_in,
                     Times(R, Q))

    # TODO: In Manifold this has the option for worst case analysis, which is
    #       used to adjust the constraints in the case when there is no
    #       solution to try and still find a solution, should implement
    def simple_pressure_flow(self):
        """Assert difference in pressure at the two end nodes for a channel
        equals the flow rate in the channel times the channel resistance
        More complicated calculation available through
        analytical_pressure_flow method (TBD)

        :param str channel_name: Name of the channel
        :returns: SMT expression of equality between delta(P) and Q*R
        """
        port_in_name = self.get_port_in().get_name()
        port_in = self.get_port_in()
        port_out = self.get_port_out()
        p1 = port_in.get_pressure()
        p2 = port_out.get_pressure()
        Q = self.get_flow_rate()
        R = self.get_resistance()
        return Equals(Minus(p1, p2),
                      Times(Q, R)
                      )


    def calculate_channel_area(self):
        return Times(self.get_length(),
                     self.get_width() #TODO: We don't need min width do we?
                     )

    def translate(self):
        """Create SMT expressions for a given channel (edges in NetworkX naming)
        currently only works for channels with a rectangular shape, but should
        be expanded to include circular and parabolic

        :returns: None -- no issues with translating channel parameters to SMT
        :raises: KeyError, if channel is not found in the list of defined edges
        """

        # Create expression to force length to equal distance between end nodes
        self.exprs.append(self.pythagorean_length())

        # Set the length determined by pythagorean theorem equal to the user
        # provided number if provided, else assert that the length be greater
        # than 0, same for width and height
        if self.get_min_length():
            self.exprs.append(Equals(self.get_length(),
                                     Real(self.get_min_length())))
        else:
            self.exprs.append(GT(self.get_length(), Real(0)))
        if self.get_min_width():
            self.exprs.append(Equals(self.get_width(),
                                     Real(self.get_min_width())))
        else:
            self.exprs.append(GT(self.get_width(), Real(0)))
        if self.get_min_height():
            self.exprs.append(Equals(self.get_height(),
                                     Real(self.get_min_height())))
        else:
            self.exprs.append(GT(self.get_height(), Real(0)))

        # Assert that viscosity in channel equals input node viscosity
        # Set output viscosity to equal input since this should be constant
        # This must be performed before calculating resistance
        self.exprs.append(Equals(self.get_viscosity(),
                                 self.get_port_in().get_viscoscity()))
        self.exprs.append(Equals(self.get_port_out().get_viscoscity(),
                                 self.get_port_in().get_viscoscity()))

        # Pressure at end of channel is lower based on the resistance of
        # the channel as calculated by calculate_resistance and
        # pressure_out = pressure_in * (flow_rate * resistance)
        resistance_list = self.calculate_resistance()

        # First term is assertion that each channel's height is less than width
        # which is needed to make resistance formula valid, second is the SMT
        # equation for the resistance, then assert resistance is >0
        self.exprs.append(resistance_list[0])
        resistance = resistance_list[1]
        self.exprs.append(Equals(self.get_resistance(), resistance))
        self.exprs.append(GT(self.get_resistance(), Real(0)))

        # Assert flow rate equal to the flow rate coming in
        self.exprs.append(Equals(self.get_flow_rate(),
                                 self.get_port_in().get_flow_rate()))

        # Channels do not have pressure because it decreases across channel
        
        # Call translate on the input to continue traversing the channel
        self.exprs.append(self.get_port_in().translate())
        
        # We need to return this so that the caller can have a list of all the exprs
        return self.exprs
