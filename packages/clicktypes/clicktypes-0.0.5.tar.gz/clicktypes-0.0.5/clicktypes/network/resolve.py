# -*- coding: utf-8 -*-

"""

Click Parameter Types - Resolve Hostnames

These parameters will resolve hostnames to an IPv4 and/or IPv6 address (if they are not already an IP).

Threads are used for parallel resolution of both IPv4 and IPv6 addresses when appropriate to allow faster processing.

"""

from click import ParamType
from dns import resolver, rdatatype
from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import List, Union

def _lookup(hostname: str, type: Union[rdatatype.A, rdatatype.AAAA]) -> Union[List[Union[IPv4Address, IPv6Address]], None]:
    return None

def _resolve(hostname: str, type: Union[List[Union[rdatatype.A, rdatatype.AAAA]], rdatatype.A, rdatatype.AAAA]) -> Union[List[Union[IPv4Address, IPv6Address]], None]:
    """Create threads (if required) and perform the appropriate DNS lookups

    If multiple lookup types are requested (A and AAAA), each lookup will be executed in a thread concurrently.

    Arguments:
        hostname (str): The hostname to lookup
        type (Union[List[Union[rdatatype.A, rdatatype.AAAA]], rdatatype.A, rdatatype.AAAA])): The lookup type or types to execute

    Returns:
        Union[List[Union[IPv4Address, IPv6Address]], None]: If the lookup was successful a list of IPv4 and/or IPv6 address objects will be returned.
        If the lookup failed, None will be returned.
    """
    ## If only a single lookup type is required, don't use threads
    if type in [rdatatype.A, rdatatype.AAAA]:
        results = _lookup(hostname = hostname, type = type)
    else:
        ## Use threads
        from functools import partial
        from concurrent.futures import ThreadPoolExecutor

        ## Create partial for _lookup
        lookup = partial(_lookup, hostname = hostname)

        ## Submit the lookup jobs
        with ThreadPoolExecutor() as executor:
            results = executor.map(lookup, type)

    print('asd')

class ResolveIPAddressParam(ParamType):
    """Attempt to resolve hostnames to an IPv4 and IPv6 address.)
    """

    def convert(self, value: str, param, context) -> List[Union[IPv4Address, IPv6Address]]:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The hostname or IP address

        Returns:
            List[Union[IPv4Address, IPv6Address]]: The list of IP addresses that were resolved
        """
        ## If the supplied parameter is an IP address the DNS resolution process can be skipped
        try:
            ip: Union[IPv4Address, IPv6Address] = ip_address(value)
        except Exception:
            ## Could not parse as an IP address, do nothing
            pass
        else:
            ## Appears to be an IP address, no need to resolve it
            return [ip]

        ## Try resolving