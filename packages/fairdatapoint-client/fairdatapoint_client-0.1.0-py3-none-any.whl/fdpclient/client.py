import logging
import requests
from fdpclient import operations

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, host):
        """The Client object to connect to a FAIR Data Point server.

        FAIR Data Point server contains 4 types of metadata as described in the
        `specification`_:

        ============  ======================
        type          path
        ============  ======================
        fdp           <host>/fdp or <host>
        catalog       <host>/catalog
        dataset       <host>/dataset
        distribution  <host>/distribution
        ============  ======================

        A server may use the host URL to store the 'fdp' metadata, and then
        the 'fdp' path is the same as the host.

        .. _`specification`: https://github.com/FAIRDataTeam/FAIRDataPoint-Spec/blob/master/spec.md

        Args:
            host(str): the host URL

        Examples:
            >>> client = Client('http://fdp.fairdatapoint.nl`)
            >>> fdp_metadata = client.read_fdp()
            >>> catalog_metadata = client.read_catalog('catalog01')
            >>> print(fdp_metadata, catalog_metadata)
        """
        self.host = host.rstrip('/')
        self.fdp_id = self._detect_fdp_url()

    # Create metadata
    def create_fdp(self, data, format='turtle', **kwargs):
        """Create fdp metadata.

        Args:
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('create', self.fdp_id, data=data, format=format, **kwargs)

    def create_catalog(self, data, format='turtle', **kwargs):
        """Create a new catalog metadata.

        Args:
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('create', 'catalog', data=data, format=format, **kwargs)

    def create_dataset(self, data, format='turtle', **kwargs):
        """Create a new dataset metadata.

        Args:
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('create', 'dataset', data=data, format=format, **kwargs)

    def create_distribution(self, data, format='turtle', **kwargs):
        """Create a new distribution metadata.

        Args:
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('create', 'distribution', data=data, format=format, **kwargs)

    # Read metadata
    def read_fdp(self, format='turtle', **kwargs):
        """Read the fdp metadata.

        Args:
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.

        Returns:
            :class:`rdflib.Graph`: RDF graph of the requested metadata.
        """
        return self._request('read', self.fdp_id, id='', format=format, **kwargs)

    def read_catalog(self, id, format='turtle', **kwargs):
        """Read a catalog metadata.

        Args:
            id(str): the identifier of the metadata.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.

        Returns:
            :class:`rdflib.Graph`: RDF graph of the requested metadata.
        """
        return self._request('read', 'catalog', id=id, format=format, **kwargs)

    def read_dataset(self, id, format='turtle', **kwargs):
        """Read a dataset metadata.

        Args:
            id(str): the identifier of the metadata.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.

        Returns:
            :class:`rdflib.Graph`: RDF graph of the requested metadata.
        """
        return self._request('read', 'dataset', id=id, format=format, **kwargs)

    def read_distribution(self, id, format='turtle', **kwargs):
        """Read a distribution metadata.

        Args:
            id(str): the identifier of the metadata.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.

        Returns:
            :class:`rdflib.Graph`: RDF graph of the requested metadata.
        """
        return self._request('read', 'distribution', id=id, format=format, **kwargs)

    # Update metadata
    def update_fdp(self, data, format='turtle', **kwargs):
        """Update the fdp metadata.

        Args:
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('update', self.fdp_id, id='', data=data, format=format, **kwargs)

    def update_catalog(self, id, data, format='turtle', **kwargs):
        """Update a catalog metadata.

        Args:
            id(str): the identifier of the metadata.
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('update', 'catalog', id=id, data=data, format=format, **kwargs)

    def update_dataset(self, id, data, format='turtle', **kwargs):
        """Update a dataset metadata.

        Args:
            id(str): the identifier of the metadata.
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('update', 'dataset', id=id, data=data, format=format, **kwargs)

    def update_distribution(self, id, data, format='turtle', **kwargs):
        """Update a distribution metadata.

        Args:
            id(str): the identifier of the metadata.
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('update', 'distribution', id=id, data=data, format=format, **kwargs)

    # Delete metadata
    def delete_catalog(self, id, **kwargs):
        """Delete a catalog metadata.

        Args:
            id(str): the identifier of the metadata.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('delete', 'catalog', id=id, **kwargs)

    def delete_dataset(self, id, **kwargs):
        """Delete a dataset metadata.

        Args:
            id(str): the identifier of the metadata.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('delete', 'dataset', id=id, **kwargs)

    def delete_distribution(self, id, **kwargs):
        """Delete a distribution metadata.

        Args:
            id(str): the identifier of the metadata.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        self._request('delete', 'distribution', id=id, **kwargs)

    # Private methods
    def _detect_fdp_url(self):
        """Detect the internal path of fdp

        Raises:
            RuntimeError: failed to find the fdp url

        Returns:
            str: the internal path of fdp, i.e. 'fdp' or ''.
        """
        fmt = 'text/turtle'

        r = requests.get(self.host + '/fdp', params={'Accept':fmt})
        if r.status_code == 200 and r.headers['content-type'] == fmt:
            return 'fdp'

        r = requests.get(self.host, params={'Accept':fmt})
        if r.status_code == 200 and r.headers['content-type'] == fmt:
            return ''

        raise RuntimeError('Failed to detect the fdp url. Check if the server '
                        + 'uses "<host>" or "<host>/fdp" as the fdp url.')

    def _request(self, operation, type, id=None, data=None, format='turtle', **kwargs):
        """Private request method.

        Args:
            operation(str): the request operation.
                Available options: 'read', 'write', 'update' and 'delete'.
                See :class:`fdpclient.operations`.
            type(str): the type of metadata.
                Available types: 'fdp', 'catalog', 'dataset' and 'distribution'.
            id(str): the identifier of the metadata.
                Defaults to `None`.
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
                Defaults to `None`.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type`` or
                ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                See :const:`fdpclient.config.DATA_FORMATS`.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.

        Returns:
            `None` or :class:`rdflib.Graph`: RDF graph of the requested metadata.
        """

        request_methods = ('create', 'read', 'update', 'delete')

        if operation not in request_methods:
            raise ValueError(f'Invalid request method: {operation}')

        if operation in ('read', 'delete', 'update') and id is None:
            raise ValueError(f'Metadata "id" must be given for request method {operation}')

        if operation in ('create', 'update') and data is None:
            raise ValueError(f'Metadata "data" must be given for request method {operation}')

        if id is not None:
            url = '/'.join([self.host, type, id])
        else:
            url = '/'.join([self.host, type])
        url = url.rstrip('/')

        logger.debug(f'Request: {operation} metadata on {url}')
        request = getattr(operations, operation)
        if operation == 'delete':
            r = request(url=url, data=data, **kwargs)
        else:
            r = request(url=url, data=data, format=format, **kwargs)
        return r