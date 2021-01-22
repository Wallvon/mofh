import ast
from typing import Any, Optional, Sequence
from aiohttp import ClientSession, BasicAuth, TCPConnector
import xml.etree.ElementTree
from .errors import APIError

class Client(object):
    """Main wrapper class"""

    def __init__(self, username, password, api_url: str = "https://panel.myownfreehost.net:2087/xml-api/", *, session: Optional[ClientSession] = None):
        self.username = username
        self.password = password
        self.api_url = api_url
        self._session = session

    async def _ensure_session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession(connector=TCPConnector(verify_ssl=False))

        return self._session

    async def create(self, username : str, password: str, contactemail: str, domain: str, plan: str):
        """
        Send query and get response.
        Prameters:
            username: user's internal username, has a limit of 8 characters.
            password: user's password on the vPanel.
            contactemail: user's email on the vPanel.
            domain: user's domain on the vPanel.
            plan: user's plan on the vPanel.
        """

        session = await self._ensure_session()

        params = {
            'username': username,
            'password': password,
            'contactemail': contactemail,
            'domain': domain,
            'plan': plan
        }

        async with session.post(f"{self.api_url}/createacct.php", params=params, auth=BasicAuth(self.username, self.password)) as r:
            response = await r.text()
            tree = xml.etree.ElementTree.ElementTree(
                xml.etree.ElementTree.fromstring(response))
            root = tree.getroot()
            for child in root:
                status = child[2].text
                if status == "1":
                    return child[0][1].text # Return the vPanel username.
                else:
                    error = child[3].text
                    raise APIError(error, status) # Raise exception with error.

    async def suspend(self, username : str, reason: str):
        """
        Send query and get response.
        Prameters:
            username: user's internal username, has a limit of 8 characters.
            reason: reason of suspension.
        """

        session = await self._ensure_session()

        params = {
            'user': username,
            'reason': reason
        }

        async with session.post(f"{self.api_url}/suspendacct.php", params=params, auth=BasicAuth(self.username, self.password)) as r:
            response = await r.text()
            try:
                tree = xml.etree.ElementTree.ElementTree(
                    xml.etree.ElementTree.fromstring(response))
                root = tree.getroot()
                for child in root:
                    status = child[0].text
                    return status
            except xml.etree.ElementTree.ParseError:
                raise APIError(response, "0")  # Raise exception with error.

    async def unsuspend(self, username: str):
        """
        Send query and get response.
        Prameters:
            username: user's internal username, has a limit of 8 characters.
        """

        session = await self._ensure_session()

        params = {
            'user': username
        }

        async with session.post(f"{self.api_url}/unsuspendacct.php", params=params, auth=BasicAuth(self.username, self.password)) as r:
            response = await r.text()
            try:
                tree = xml.etree.ElementTree.ElementTree(
                    xml.etree.ElementTree.fromstring(response))
                root = tree.getroot()
                for child in root:
                    status = child[0].text
                    return status
            except xml.etree.ElementTree.ParseError:
                raise APIError(response, "0")  # Raise exception with error.
    
    async def chpassword(self, username: str, password: str):
        """
        Send query and get response.
        Prameters:
            username: user's internal username, has a limit of 8 characters.
            password: user's new password.
        """

        session = await self._ensure_session()

        params = {
            'user': username,
            'pass': password
        }

        async with session.post(f"{self.api_url}/passwd.php", params=params, auth=BasicAuth(self.username, self.password)) as r:
            response = await r.text()
            try:
                tree = xml.etree.ElementTree.ElementTree(
                    xml.etree.ElementTree.fromstring(response))
                root = tree.getroot()
                for child in root:
                    status = child[0].text
                    return status
            except xml.etree.ElementTree.ParseError:
                raise APIError("Invalid username provided.", "0")  # Raise exception with error.

    async def availability(self, domain: str):
        """
        Send query and get response.
        Prameters:
            domain: domain you want to check.
        """

        session = await self._ensure_session()

        params = {
            'api_user': self.username,
            'api_key': self.password,
            'domain': domain
        }

        async with session.post(f"{self.api_url}/checkavailable.php", params=params, auth=BasicAuth(self.username, self.password)) as r:
            response = await r.text()
            return response
    
    async def getuserdomains(self, username: str):
        """
        Send query and get response.
        Prameters:
            username: user's vPanel username, e.g. hname_12345678.
        """

        session = await self._ensure_session()

        params = {
            'api_user': self.username,
            'api_key': self.password,
            'username': username
        }

        async with session.post(f"{self.api_url}/getuserdomains.php", params=params, auth=BasicAuth(self.username, self.password)) as r:
            response = await r.text()
            try:
                return ast.literal_eval(response)
            except ValueError:
                return response
    
    async def getdomainuser(self, domain: str):
        """
        Send query and get response.
        Prameters:
            domain: domain of the user you want to check.
        """

        session = await self._ensure_session()

        params = {
            'api_user': self.username,
            'api_key': self.password,
            'domain': domain
        }

        async with session.post(f"{self.api_url}/getdomainuser.php", params=params, auth=BasicAuth(self.username, self.password)) as r:
            response = await r.text()
            try:
                return ast.literal_eval(response)
            except ValueError:
                return response

    async def close(self) -> None:
        """
        Close internal session.
        Note that it closes custom session if you used one.
        """

        if self._session is not None:
            await self._session.close()
