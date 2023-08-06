[![PyPI](https://img.shields.io/pypi/v/fairdatapoint-client)](https://pypi.org/project/fairdatapoint-client/)
[![Documentation Status](https://readthedocs.org/projects/fairdatapoint-client/badge/?version=latest)](https://fairdatapoint-client.readthedocs.io/en/latest/?badge=latest)
[![Build_Test](https://github.com/fair-data/fairdatapoint-client/actions/workflows/build_test.yml/badge.svg)](https://github.com/fair-data/fairdatapoint-client/actions/workflows/build_test.yml)
[![Coverage Status](https://coveralls.io/repos/github/fair-data/fairdatapoint-client/badge.svg?branch=master)](https://coveralls.io/github/fair-data/fairdatapoint-client?branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fair-data_fairdatapoint-client&metric=alert_status)](https://sonarcloud.io/dashboard?id=fair-data_fairdatapoint-client)


# fairdatapoint-client

### Contents

-   [Overview](#overview)
-   [Installation](#installation)
-   [Quick Tutorial](#Tutorial)
-   [Issues & Contributing](#Issues-and-Contributing)
-   [License](./LICENSE)

## Overview

fairdatapoint-client is a simple and elegant library to interact with
[FAIR Data Point](https://github.com/fair-data/fairdatapoint) resources from
Python, e.g. read and write catalogs, datasets and distributions in an FDP server.

The supported APIs are listed below:

| FDP Layers   | Path Endpoint               | Specific Resource Endpoint              |
|--------------|-----------------------------|-----------------------------------------|
| fdp          | [baseURL] or [baseURL]/fdp  |                                         |
| catalog      | [baseURL]/catalog           | [baseURL]/catalog/[catalogID]           |
| dataset      | [baseURL]/dataset           | [baseURL]/dataset/[datasetID]           |
| distribution | [baseURL]/distribution      | [baseURL]/distribution/[distributionID] |

## Installation

It requires a Python version of 3.7, 3.8 or 3.9.

#### Stable Release

The fairdatapoint-client is available on [PyPI](https://pypi.org/project/fairdatapoint-client/),
you can install it using:

`pip install fairdatapoint-client`

#### Development Version

You can also install from the latest source code, but note that the
in-development version might be unstable:

```{.sourceCode .console}
git clone https://github.com/fair-data/fairdatapoint-client.git
cd fairdatapoint-client
pip install .
```

To run tests (including coverage):

```{.sourceCode .console}
pip install '.[tests]'
pytest
```


## Tutorial

### Using Client
```python
from fdpclient.client import Client

# create a client with base URL
client = Client('http://example.org')

# create metadata
with open('catalog01.ttl') as f:
    data = f.read()
client.create_catalog(data)

# let's assume the catalogID was assigned as 'catalog01'
# read metadata, return a RDF graph
r = client.read_catalog('catalog01')
print(r.serialize(format="turtle").decode("utf-8"))

# update metadata
with open('catalog01_update.ttl') as f:
    data_update = f.read()
client.update_catalog('catalog01', data_update)

# delete metadata
client.delete_catalog('catalog01')
```

### Using operation functions
```python
from fdpclient import operations

# create metadata
with open('catalog01.ttl') as f:
    data = f.read()
operations.create('http://example.org/catalog', data)

# read metadata, return a RDF graph
r = operations.read('http://example.org/catalog/catalog01')
print(r.serialize(format="turtle").decode("utf-8"))

# update metadata
with open('catalog01_update.ttl') as f:
    data_update = f.read()
operations.update('http://example.org/catalog/catalog01', data_update)

# delete metadata
operations.delete('http://example.org/catalog/catalog01')
```

## Issues and Contributing
If you have questions or find a bug, please report the issue in the
[Github issue channel](https://github.com/fair-data/fairdatapoint-client/issues).

If you want to contribute to the development of fairdatapoint-client, have a
look at the [contribution guidelines](CONTRIBUTING.rst).