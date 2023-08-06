# -*- coding: utf-8 -*-

"""

Click Parameter Types - Domains

"""

from click import ParamType
from validators import domain as domain_validator

class DomainParam(ParamType):
    """Validate the parameter is a domain name. The parameter will be returned in lower case.

    Examples:
        'eXamPle.com' becomes 'example.com'
    """

    def convert(self, value: str, param, context) -> str:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The domain name

        Returns:
            str: The normalized and validated domain name
        """
        ## Lower case domain
        domain = f'{value.lower()}'

        ## Check if the email is valid
        if not domain_validator(domain):
            self.fail(f'Could not validate "{value!r}" as a domain name')

        ## Return the lower case domain
        return domain