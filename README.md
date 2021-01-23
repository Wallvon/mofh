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
from aiohttp import ClientSession, ClientTimeout
import mofh

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

## License

![License Badge](https://mirrors.creativecommons.org/presskit/buttons/80x15/svg/by-sa.svg)

The aforementioned code is protected and released to the public under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License which can be viewed on the Creative Commons website (https://creativecommons.org/licenses/by-sa/4.0/). Any failure to comply with the terms designated in the license will be met with swift judicial action by the author.