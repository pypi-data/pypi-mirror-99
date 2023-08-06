import csv
import json

from .models import Consignment, PreparedConsignment
from .adapters import StoreAdapter


class Session():
    '''
    '''

    def __init__(self):
        pass


    def __enter__(self):
        return self


    def __exit__(self, *args):
        self.close()


    def prepare_consignment(self, consign):
        '''
        '''
        p = PreparedConsignment()
        p.prepare(
            method=consign.method.upper(),
            data=consign.data,
            path=consign.path,
            delimiter=consign.delimiter,
            overwrite=consign.overwrite
        )
        return p


    def consign(self, method, data, path, delimiter=None, overwrite=True,
                provider=None, connection_string=None, container_name=None):
        '''Constructs a :class:`Consign <Consign>`, prepares it and stores it.
        '''

        # Creates the Consignment.
        csgn = Consignment(
            method=method.upper(),
            data=data,
            path=path,
            delimiter=delimiter,
            overwrite=overwrite,
            provider=provider,
            connection_string=connection_string,
            container_name=container_name
        )

        # Prepares the Consignment.
        luggage = self.prepare_consignment(csgn)

        # Stores the Luggage.
        resp = self.store(luggage)

        return resp


    def store(self, luggage):
        '''Stores a given PreparedConsignment.
        '''

        # Get the appropriate adapter to use
        adapter = StoreAdapter(
            method=luggage.method
        )

        # Start time (approximately) of the request
        # start = preferred_clock()

        # Store the luggage
        r = adapter.store(
            data=luggage.data,
            path=luggage.path,
            delimiter=luggage.delimiter,
            overwrite=luggage.overwrite,
            provider=luggage.provider,
            connection_string=luggage.connection_string,
            container_name=luggage.container_name
        )

        # Total elapsed time of the request (approximately)
        # elapsed = preferred_clock() - start
        # r.elapsed = timedelta(seconds=elapsed)

        return r


    def close(self):
        '''Closes all adapters and as such the session'''
        # for v in self.adapters.values():
        #     v.close()
        pass
