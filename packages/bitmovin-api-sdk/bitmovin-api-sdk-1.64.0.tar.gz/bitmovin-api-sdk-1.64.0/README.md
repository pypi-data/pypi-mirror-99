<p align="center">
  <a href="https://www.bitmovin.com">
    <img alt="Bitmovin Python API SDK Header" src="https://cdn.bitmovin.com/frontend/encoding/openapi-clients/readme-headers/ReadmeHeader_Python.png" >
  </a>

  <h4 align="center">
    Python API SDK which enables you to seamlessly integrate the Bitmovin API into your projects.
  </h4>

  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></img></a>
  </p>
</p>

Using this API client requires an active account.

> Don't have an account yet? [Sign up for a free Bitmovin trial plan](https://dashboard.bitmovin.com/signup)!

For full documentation of all available API endpoints, see the [Bitmovin API reference](https://bitmovin.com/docs).

## Installation
### pip install

#### Python 2.7
```sh
pip install git+https://github.com/bitmovin/bitmovin-api-sdk-python.git
```

#### Python 3.4+
```sh
pip3 install git+https://github.com/bitmovin/bitmovin-api-sdk-python.git
```

### Setuptools

#### Python 2.7
```sh
python setup.py install
```

#### Python 3.4+
```sh
python3 setup.py install
```

## Initialization

```python
from bitmovin_api_sdk import BitmovinApi


bitmovinApi = BitmovinApi(api_key='<YOUR_API_KEY>')
```

## Examples
You can find sample workflow scripts in the [Bitmovin API SDK examples](https://github.com/bitmovin/bitmovin-api-sdk-examples) repository.

# Previous API Client (Legacy)

`bitmovin-api-sdk-python` is the latest Bitmovin API client for Python 2 and 3. It guarantees 100% specification conformity at any given time and access to all features of the API as soon as they are released. 

However, if you need to use the previous version for legacy reasons, you can still find it at [bitmovin-python](https://github.com/bitmovin/bitmovin-python). 
