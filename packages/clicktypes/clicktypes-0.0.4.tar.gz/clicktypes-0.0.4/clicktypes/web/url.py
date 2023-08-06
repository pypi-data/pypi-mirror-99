# -*- coding: utf-8 -*-

"""

Click Parameter Types - URL

"""

from click import ParamType
from validators import url as url_validator

class UrlParam(ParamType):
    """Validate the parameter is a URL.

    Examples:
        'https://example.com/?test=test'
    """

    def convert(self, value: str, param, context) -> str:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The URL

        Returns:
            str: The validated URL
        """
        ## Make sure URL is a string
        url = f'{value}'

        ## Check if the URL is valid
        if not url_validator(url):
            self.fail(f'Could not validate "{value!r}" as a URL')

        ## Return the lower case domain
        return url