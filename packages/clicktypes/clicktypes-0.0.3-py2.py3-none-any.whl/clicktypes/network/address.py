# -*- coding: utf-8 -*-

"""

Click Parameter Types - IP Addresses

These parameters are related to IPv4 and IPv6 addresses.

"""

from click import ParamType
from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Union

class IPAddressParam(ParamType):
    """Validate the parameter is an IPv4/IPv6 address and normalize into an IPv4Address or IPv6Address object.

    Examples:
        '192.0.2.0' will become IPv4Address('192.0.2.0')
        '2001:0DB8:0004:3f:00::2' will become IPv6Address('2001:db8:4:3f::2')
    """

    def convert(self, value: str, param, context) -> Union[IPv4Address, IPv6Address]:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The IPv4/IPv6 address

        Returns:
            Union[IPv4Address, IPv6Address]: The IPv4Address or IPv6Address object
        """
        ## Attempt address creation
        try:
            address: Union[IPv4Address, IPv6Address] = ip_address(value)
        except ValueError:
            ## Not a valid IPv4/IPv6 address
            self.fail(f'Could not validate "{value!r}" as an IPv4 or IPv6 IP address')
        except Exception as e:
            ## Other exception types should be handled
            self.fail(f'Exception validating "{value!r}" as an IPv4 or IPv6 IP address: {e}', param, context)
        else:
            return address

class IPv4AddressParam(ParamType):
    """Validate the parameter is an IPv4 address and normalize into an IPv4Address object.

    Examples:
        '192.0.2.0' will become IPv4Address('192.0.2.0')
    """

    def convert(self, value: str, param, context) -> IPv4Address:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The IPv4 address

        Returns:
            IPv4Address: The IPv4Address object
        """
        ## Attempt address creation
        try:
            address: IPv4Address = IPv4Address(value)
        except ValueError:
            ## Not a valid IPv4 address
            self.fail(f'Could not validate "{value!r}" as an IPv4 IP address')
        except Exception as e:
            ## Other exception types should be handled
            self.fail(f'Exception validating "{value!r}" as an IPv4 IP address: {e}', param, context)
        else:
            return address

class IPv6AddressParam(ParamType):
    """Validate the parameter is an IPv6 address and normalize into an IPv6Address object.

    Examples:
        '2001:0DB8:0004:3f:00::2' will become IPv6Address('2001:db8:4:3f::2')
    """

    def convert(self, value: str, param, context) -> IPv6Address:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The IPv6 address

        Returns:
            IPv6Address: The IPv6Address object
        """
        ## Attempt address creation
        try:
            address: IPv6Address = IPv6Address(value)
        except ValueError:
            ## Not a valid IPv6 address
            self.fail(f'Could not validate "{value!r}" as an IPv6 IP address')
        except Exception as e:
            ## Other exception types should be handled
            self.fail(f'Exception validating "{value!r}" as an IPv6 IP address: {e}', param, context)
        else:
            return address