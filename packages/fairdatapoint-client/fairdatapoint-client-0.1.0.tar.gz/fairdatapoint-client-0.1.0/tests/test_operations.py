import pytest
import rdflib
import requests

from fdpclient import operations

base_url = 'http://example.org/catalog'
data_url = base_url + '/catalog01'

# datadir fixture provided via pytest-datadir-ng
@pytest.fixture()
def data(datadir):
    with open(datadir['catalog01.ttl']) as f:
        return f.read()

@pytest.fixture()
def data_update(datadir):
    with open(datadir['catalog01_update.ttl']) as f:
        return f.read()

@pytest.fixture()
def graph_data(datadir):
    with open(datadir['catalog01.ttl']) as f:
        g = rdflib.Graph()
        g.parse(data=f.read(), format='turtle')
        return g

@pytest.fixture()
def graph_data_update(datadir):
    with open(datadir['catalog01_update.ttl']) as f:
        g = rdflib.Graph()
        g.parse(data=f.read(), format='turtle')
        return g

class TestDefault:
    """Test fdpclient.operations functions"""

    # requests_mock fixture provided via requests-mock
    def test_create(self, data, requests_mock):
        """Test create function"""
        requests_mock.post(base_url)
        r = operations.create(base_url, data=data)
        assert r is None

    def test_read(self, data, requests_mock):
        """Test read function"""
        requests_mock.get(data_url, text=data)
        r = operations.read(data_url)
        assert isinstance(r, rdflib.Graph)
        assert  b'hasVersion "1.0"' in r.serialize(format='turtle')

    def test_update(self, data_update, requests_mock):
        """Test update function"""
        requests_mock.put(data_url)
        r = operations.update(data_url, data=data_update)
        assert r is None

    def test_delete(self, requests_mock):
        """Test read function"""
        requests_mock.delete(data_url)
        r = operations.delete(data_url)
        assert r is None

    # test 'format' parameter
    def test_create_format(self, data, requests_mock):
        """Test create function parameter `format` overwriting `content-type`"""
        requests_mock.post(base_url, request_headers={'content-type': 'text/turtle'})
        r = operations.create(base_url, data=data, format='turtle',
            headers={'content-type': 'application/ld+json'})
        assert r is None

    def test_read_format(self, data, requests_mock):
        """Test read function parameter `format` overwriting `accept`"""
        requests_mock.get(data_url, text=data,
            request_headers={'content-type': 'text/turtle'})
        r = operations.read(data_url, format='turtle',
            headers={'content-type': 'application/ld+json'})
        assert isinstance(r, rdflib.Graph)
        assert  b'hasVersion "1.0"' in r.serialize(format='turtle')

    def test_update_format(self, data_update, requests_mock):
        """Test update function parameter `format` overwriting `content-type`"""
        requests_mock.put(data_url, request_headers={'content-type': 'text/turtle'})
        r = operations.update(data_url, data=data_update, format='turtle',
            headers={'content-type': 'application/ld+json'})
        assert r is None


class TestGraphData:
    """Test graph data as input of fdpclient.operations functions"""

    def test_create(self, graph_data, requests_mock):
        """Test create function"""
        requests_mock.post(base_url)
        r = operations.create(base_url, data=graph_data)
        assert r is None

    def test_update(self, graph_data_update, requests_mock):
        """Test update function"""
        requests_mock.put(data_url)
        r = operations.update(data_url, data=graph_data_update)
        assert r is None

class TestException:
    """Test exceptions and errors for fdpclient.operations functions"""

    # test unexpected errors
    def test_create_unexpected_error(self, data, requests_mock, capsys):
        """Test create function unexpected error"""
        requests_mock.post(base_url, exc=ConnectionError)
        with pytest.raises(ConnectionError):
            r = operations.create(base_url, data=data)
        assert 'Unexpected error when connecting to' in capsys.readouterr().out

    def test_read_unexpected_error(self, data, requests_mock, capsys):
        """Test read function unexpected error"""
        requests_mock.get(data_url, exc=ConnectionError)
        with pytest.raises(ConnectionError):
            r = operations.read(data_url)
        assert 'Unexpected error when connecting to' in capsys.readouterr().out

    def test_update_unexpected_error(self, data_update, requests_mock, capsys):
        """Test update function unexpected error"""
        requests_mock.put(data_url, exc=ConnectionError)
        with pytest.raises(ConnectionError):
            r = operations.update(data_url, data=data_update)
        assert 'Unexpected error when connecting to' in capsys.readouterr().out

    def test_delete_unexpected_error(self, requests_mock, capsys):
        """Test read function unexpected error"""
        requests_mock.delete(data_url, exc=ConnectionError)
        with pytest.raises(ConnectionError):
            r = operations.delete(data_url)
        assert 'Unexpected error when connecting to' in capsys.readouterr().out

    # test HTTP errors
    def test_create_http_error(self, data, requests_mock, capsys):
        """Test create function HTTP error"""
        requests_mock.post(base_url, status_code=300)
        with pytest.raises(RuntimeError):
            r = operations.create(base_url, data=data)
        assert 'HTTP error: 300' in capsys.readouterr().out

    def test_read_http_error(self, data, requests_mock, capsys):
        """Test read function HTTP error"""
        requests_mock.get(data_url, status_code=300)
        with pytest.raises(RuntimeError):
            r = operations.read(data_url)
        assert 'HTTP error: 300' in capsys.readouterr().out

    def test_update_http_error(self, data_update, requests_mock, capsys):
        """Test update function HTTP error"""
        requests_mock.put(data_url, status_code=300)
        with pytest.raises(RuntimeError):
            r = operations.update(data_url, data=data_update)
        assert 'HTTP error: 300' in capsys.readouterr().out

    def test_delete_http_error(self, requests_mock, capsys):
        """Test read function HTTP error"""
        requests_mock.delete(data_url, status_code=300)
        with pytest.raises(RuntimeError):
            r = operations.delete(data_url)
        assert 'HTTP error: 300' in capsys.readouterr().out