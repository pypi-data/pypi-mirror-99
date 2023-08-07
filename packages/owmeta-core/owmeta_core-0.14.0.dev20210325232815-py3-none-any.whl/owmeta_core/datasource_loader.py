# -*- coding: utf-8 -*-
'''
DataSourceLoaders take a data source identifier and retrieve the primary data (e.g., CSV
files, electrode recordings) from some location (e.g., a file store, via a bittorrent
tracker).

Each loader can treat the base_directory given as its own namespace and place directories
in there however it wants.
'''
from .utils import FCN
from os.path import exists, isdir, join as pth_join, isabs, realpath


class DataSourceDirLoader(object):
    '''
    Loads data files for a DataSource

    The loader is expected to organize files for each data source within the given
    base directory.

    .. automethod:: __call__
    '''
    def __init__(self, base_directory=None):
        self.base_directory = base_directory
        self.directory_key = FCN(type(self))

    def __call__(self, data_source):
        '''
        Load the data source. Calls `load`

        Parameters
        ----------
        data_source : .DataSource
            The data source to load files for

        Returns
        -------
        str
            A path to the loaded resource

        Raises
        ------
        LoadFailed
            If `load`:

            * throws an exception
            * doesn't return anything
            * returns a path that isn't under `base_directory`
            * returns a path that doesn't exist
        '''
        # Call str(·) to give a more uniform interface to the sub-class ``load``
        # Conventionally, types that tag or "enhance" a string have the base string representation as their __str__
        try:
            s = self.load(data_source)
        except LoadFailed:
            raise LoadFailed(data_source, self, 'Loader erred')

        if not s:
            raise LoadFailed(data_source, self, 'Loader returned an empty string')

        # N.B.: This logic is NOT intended as a security measure against directory traversal: it is only to make the
        # interface both flexible and unambiguous for implementers

        # Relative paths are allowed
        if not isabs(s):
            s = pth_join(self.base_directory, s)

        # Make sure the loader isn't doing some nonsense with symlinks or non-portable paths
        rpath = realpath(s)
        if not rpath.startswith(self.base_directory):
            msg = 'Loader returned a file path, "{}",' \
                    ' outside of the base directory, "{}"'.format(rpath, self.base_directory)
            raise LoadFailed(data_source, self, msg)

        if not exists(rpath):
            msg = 'Loader returned a non-existant file {}'.format(rpath)
            raise LoadFailed(data_source, self, msg)

        if not isdir(rpath):
            msg = 'Loader did not return a directory, but returned {}'.format(rpath)
            raise LoadFailed(data_source, self, msg)

        return rpath

    @property
    def base_directory(self):
        try:
            return self.__base_directory
        except AttributeError:
            return None

    @base_directory.setter
    def base_directory(self, base_directory):
        self.__base_directory = realpath(base_directory) if base_directory else None

    def load(self, data_source):
        '''
        Loads the files for the data source

        Parameters
        ----------
        data_source : .DataSource
            The data source to load files for

        Returns
        -------
        str
            A path to the loaded resource
        '''
        raise NotImplementedError()

    def can_load(self, data_source):
        '''
        Returns true if the `.DataSource` can be loaded by this
        loader

        Parameters
        ----------
        data_source : .DataSource
            The data source to load files for
        '''
        return False

    def __str__(self):
        return FCN(type(self)) + '()'


class LoadFailed(Exception):
    '''
    Thrown when loading fails for a .DataSourceDirLoader
    '''
    def __init__(self, data_source, loader, *args):
        '''
        Parameters
        ----------
        data_source : .DataSource
            The `.DataSource` on which loading was attempted
        loader : DataSourceDirLoader
            The loader that attempted to load the data source
        args[0] : str
            Message explaining why loading failed
        args[1:]
            Passed on to `Exception`
        '''
        msg = args[0]
        mmsg = 'Failed to load {} data with loader {}{}'.format(data_source, loader, ': ' + msg if msg else '')
        super(LoadFailed, self).__init__(mmsg, *args[1:])
