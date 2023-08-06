# -*- coding: utf-8 -*-

'''
consign.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of Consign's exceptions.
'''


class InvalidDataType(TypeError):
    '''The data provided was somehow invalid.'''


class InvalidPath(ValueError):
    '''The path provided was somehow invalid.'''


class InvalidCloudProvider(ValueError):
    '''The given cloud provider was not listed or was somehow invalid.'''


class InvalidConnectionString(ValueError):
    '''The connection string provided was somehow invalid.'''


class InvalidContainerName(ValueError):
    '''The container name provided was somehow invalid.'''


class InvalidBlobName(ValueError):
    '''The blob name provided was somehow invalid.'''


class InvalidTableName(ValueError):
    '''The table name provided was somehow invalid.'''


# Warnings


class ConsignWarning(Warning):
    '''Base warning for Consign.'''
