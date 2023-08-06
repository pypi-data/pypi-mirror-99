# -*- coding: utf-8 -*-

"""

Click Parameter Types - Email Addresses

"""

from click import ParamType
from validators import email as email_validator


class EmailParam(ParamType):
    """Validate the parameter is an email address. The email address will be converted to lower case and returned if valid.

    Examples:
        'tEsT@exAmple.com' becomes 'test@example.com'
    """

    def convert(self, value: str, param, context) -> str:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The email address

        Returns:
            str: The normalized and validated email address
        """
        ## Lower case email
        email = f"{value.lower()}"

        ## Check if the email is valid
        if not email_validator(email):
            self.fail(f'Could not validate "{value!r}" as an email address')

        ## Return the lower case domain
        return email
