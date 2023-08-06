# clicktypes

Additional types for the [click](https://pypi.org/project/click/) module that I find useful.

For a list of available types check the [README](clicktypes/README.md) file from the module.

## Installation

Install from PyPI:

```python
## Python 3
python3 -m pip install clicktypes

## PyPy3
pypy3 -m pip install clicktypes
```

## Examples

The following are some examples. For complete examples check the appropriate README.

### Networking

If you accept an IP address parameter:

```python
from clicktypes.network import IPAddressParam

@click.argument(
    'ip',
    nargs           = -1,
    required        = True,
    type            = IPAddressParam(),
)
```

This will validate the IP or IP's provided are IPv4 or IPv6 addresses and return them as an `IPv4Address` or `IPv6Address` object.
