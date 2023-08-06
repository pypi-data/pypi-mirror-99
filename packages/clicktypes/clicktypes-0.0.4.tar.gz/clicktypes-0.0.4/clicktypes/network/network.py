# -*- coding: utf-8 -*-

"""

Click Parameter Types - Network Prefixes

These parameters are related to IPv4 and IPv6 network prefixes.

"""

from click import ParamType
from ipaddress import IPv4Network, IPv6Network
from typing import Union

class IPNetworkParam(ParamType):
    """Validate the parameter is an IPv4/IPv6 address or prefix and normalize into an IPv4Network or IPv6Network object.

    Examples:
        '192.0.2.0' will become IPv4Network('192.0.2.0/32')
        '2001:0DB8:0004:3f:00::2' will become IPv6Network('2001:db8:4:3f::2/128')
        '192.168.1.1/24' will become IPv4Network('192.0.2.0/24')
    """

    def convert(self, value: str, param, context) -> Union[IPv4Network, IPv6Network]:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The IPv4/IPv6 address or network

        Returns:
            Union[IPv4Network, IPv6Network]: The IPv4Network or IPv6Network object
        """
        ## First attempt to create as IPv4 network
        try:
            network: IPv4Network = IPv4Network(value)
        except ValueError:
            ## Does not appear to be an IPv4 IP or network; retry with IPv6
            pass
        except Exception as e:
            ## Other exception types should be handled
            self.fail(f'Exception validating "{value!r}" as an IPv4 IP or network: {e}', param, context)
        else:
            return network

        ## Now try IPv6
        try:
            network: IPv6Network = IPv6Network(value)
        except ValueError:
            ## Could not be validated as an IPv4 or IPv6 IP or network
            self.fail(f'Could not validate "{value!r}" as an IPv4 or IPv6 IP or network')
        except Exception as e:
            ## Other exception types should be handled
            self.fail(f'Exception validating "{value!r}" as an IPv6 IP or network: {e}', param, context)
        else:
            return network

class IPv4NetworkParam(ParamType):
    """Validate the parameter is an IPv4 address or prefix and normalize into an IPv4Network object.

    Examples:
        '192.0.2.0' will become IPv4Network('192.0.2.0/32')
        '192.168.1.1/24' will become IPv4Network('192.0.2.0/24')
    """

    def convert(self, value: str, param, context) -> IPv4Network:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The IPv4 address or network

        Returns:
            IPv4Network: The IPv4Network object
        """
        ## Attempt IPv4Network object creation
        try:
            network: IPv4Network = IPv4Network(value)
        except ValueError:
            self.fail(f'Could not validate "{value!r}" as an IPv4 IP or network')
        except Exception as e:
            ## Other exception types should be handled
            self.fail(f'Exception validating "{value!r}" as an IPv4 IP or network: {e}', param, context)
        else:
            return network

class IPv6NetworkParam(ParamType):
    """Validate the parameter is an IPv6 address or prefix and normalize into an IPv6Network object.

    Examples:
        '2001:0DB8:0004:3f:00::2' will become IPv6Network('2001:db8:4:3f::2/128')
    """

    def convert(self, value: str, param, context) -> IPv6Network:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The IPv6 address or network

        Returns:
            IPv6Network: The IPv6Network object
        """
        ## Attempt IPv4Network object creation
        try:
            network: IPv6Network = IPv6Network(value)
        except ValueError:
            self.fail(f'Could not validate "{value!r}" as an IPv6 IP or network')
        except Exception as e:
            ## Other exception types should be handled
            self.fail(f'Exception validating "{value!r}" as an IPv6 IP or network: {e}', param, context)
        else:
            return network