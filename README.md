![Tests](https://github.com/Wallvon/mofh/actions/workflows/tests.yml/badge.svg)
# mofh by Robert S.
An API wrapper for [MyOwnFreeHost](https://myownfreehost.net).

## Installation
To install from PyPi run
```bash
pip install mofh
```

## Documentation
https://mofh.readthedocs.io

## Versioning
mofh uses the following versioning pattern:

**major.minor.patch**
- **Major**: Breaking changes, the bot is no longer compatible with previous versions.
- **Minor**: New features, no breaking changes.
- **Patch**: Bug fixes and small improvements.

## Usage

### Basic usage (creating an account)
Sync:

```python
import mofh

# With a context manager
with mofh.Client(username="example", password="password") as client:
    response = client.create(username='example', password='password', contactemail='example@example.com',
                         domain='subdomain.example.com', plan='MyAwesomePlan')
    print(response)

# ---

# Without a context manager
client = mofh.Client(username="example", password="password")

response = client.create(username='example', password='password', contactemail='example@example.com',
                         domain='subdomain.example.com', plan='MyAwesomePlan')
print(response)

client.close()
```

Async:

```python
import mofh

# With a context manager
async with mofh.AsyncClient(username="example", password="password") as client:
    response = await client.create(username='example', password='password', contactemail='example@example.com',
                         domain='subdomain.example.com', plan='MyAwesomePlan')
    print(response)

# ---

# Without a context manager
client = mofh.AsyncClient(username="example", password="password")

response = await client.create(username='example', password='password', contactemail='example@example.com',
                         domain='subdomain.example.com', plan='MyAwesomePlan')
print(response)

await client.close()
```

### Custom session
It is possible to use custom requests or aiohttp session with configured timeouts and other settings.

Sync:

```python
import mofh
from requests import Session

client = mofh.Client(username="example", password="password", session=Session())
```

Async:

```python
import mofh
from aiohttp import ClientSession, ClientTimeout

client = mofh.AsyncClient(username="example", password="password", session=ClientSession(timeout=ClientTimeout))
```

### Custom API URL
In case URL gets changed for some reason it is possible to overwrite the API URL:

```python
import mofh

client = mofh.Client(username="example", password="password", api_url="https://panel.myownfreehost.net/xml-api/")
```