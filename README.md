# MOFH.py by Robert S.
An async API wrapper for [MyOwnFreeHost](https://myownfreehost.net).

## Installation

To install from PyPi run
```bash
pip install mofh
```

## Documentation

https://mofh.readthedocs.io

## Usage

### Basic usage (creating an account)
```python
import mofh

API_USERNAME = "USERNAME"
API_PASSWORD = "PASSWORD"

client = mofh.Client(API_USERNAME, API_PASSWORD)

response = await client.create(username='example', password='password', contactemail='example@example.com', domain='subdomain.example.com', plan='MyAwesomePlan')
print(response)

await client.close()
```

### Custom session

It is possible to use custom aiohttp session with configured timeouts and other settings.
```python
import mofh
from aiohttp import ClientSession, ClientTimeout

API_USERNAME = "USERNAME"
API_PASSWORD = "PASSWORD"

client = mofh.Client(API_USERNAME, API_PASSWORD, session=ClientSession(timeout=ClientTimeout))
```

### Custom API URL

In case URL gets changed for some reason  it is possible to overwrite the API URL:

```python
import mofh

API_USERNAME = "USERNAME"
API_PASSWORD = "PASSWORD"

client = mofh.Client(API_USERNAME, API_PASSWORD, api_url="https://panel.myownfreehost.net:2087/xml-api/")
```