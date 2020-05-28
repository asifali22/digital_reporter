"""
Custom exception for feedparse.
Author: adarshtri
Creation Date: 05/09/2020
Update Date: 05/09/2020
Updated by: adarshtri
"""


class BaseParserExceptions(Exception):
    """
    Base class for parsing package. See subclasses doc for further info.
    This class is not really necessary at the point of writing this class.
    """
    pass


class MissingCompulsoryArguments(BaseParserExceptions):

    """
    author: adarshtri
    date: 05/09/2020

    This class represents exceptions when few compulsory parameters to parser classes are
    required irrespective of which parser class is handling the parse request.
    """

    def __init__(self, missing_argument):
        self._missing_argument = missing_argument

    def __str__(self):
        return "Parser requires certain parameters to be present. Missing parameter \"{}\"."\
            .format(self._missing_argument)


class MissingDefaultParserArguments(MissingCompulsoryArguments):
    def __str__(self):
        return "Default parser requires certain parameters to be present. Missing parameter \"{}\"." \
            .format(self._missing_argument)


class ConfigurationException(Exception):
    pass


class MissingConfigurationSection(ConfigurationException):

    def __init__(self, missing_section):
        self._missing_section = missing_section

    def __str__(self):
        return "Missing section \"{}\" in configuration file.".format(self._missing_section)
