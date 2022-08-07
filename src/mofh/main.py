import ast
import asyncio
from defusedxml import ElementTree
from typing import Optional, Any, Union

import uvloop
from aiohttp import ClientSession, BasicAuth, TCPConnector
from requests import Session
from requests.auth import HTTPBasicAuth

from .errors import APIError


class Client:
    """
    MyOwnFreeHost API client.

    :param username: MyOwnFreeHost API username
    :param password: MyOwnFreeHost API password
    :param api_url: MyOwnFreeHost API url
    :param session: AIOHTTP session

    Usage:
        >>> client = Client(username='username', password='password')
    """

    def __init__(
        self,
        username,
        password,
        api_url: str = "https://panel.myownfreehost.net/xml-api/",
        *,
        session: Optional[Session] = None,
    ):
        self.username = username
        self.password = password
        self.api_url = api_url
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _ensure_session(self) -> Session:
        """
        Ensure that the session is created.
        """
        if self._session is None:
            # Create new session and return it.
            self._session = Session()

        return self._session

    @staticmethod
    def _parse_xml(response: str) -> Any:
        """
        Parses the XML response and returns a dictionary.

        :param response: XML response.
        """
        # Parse the response and get the root element.
        root = ElementTree.fromstring(response)

        return root

    def create(
        self, username: str, password: str, contactemail: str, domain: str, plan: str
    ) -> Any:
        """
        Creates a new vPanel user account.

        :param username: user's internal username, has a limit of 8 characters.
        :param password: user's password on the vPanel.
        :param contactemail: user's email on the vPanel.
        :param domain: user's domain on the vPanel.
        :param plan: user's plan on the vPanel.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.create(
            >>>     username="username",
            >>>     password="password",
            >>>     contactemail="example@example.com",
            >>>     domain="subdomain.example.com",
            >>>     plan="MyAwesomePlan",
            >>> )
        """
        # Get the session, set the params, and make a post request.
        session = self._ensure_session()

        params = {
            "username": username,
            "password": password,
            "contactemail": contactemail,
            "domain": domain,
            "plan": plan,
        }

        with session.post(
            f"{self.api_url}/createacct.php",
            params=params,
            auth=HTTPBasicAuth(self.username, self.password),
        ) as r:
            response = r.text

            # Parse the response and get the root element.
            root = self._parse_xml(response)

            status = root[0][2].text
            if status == "1":
                # Return the vPanel username.
                return root[0][0][1].text
            # Raise exception with error.
            error = root[0][3].text
            raise APIError(error, 0)

    def suspend(self, username: str, reason: str) -> Optional[int]:
        """
        Suspends a user's vPanel account.

        :param username: user's internal username, has a limit of 8 characters.
        :param reason: reason of suspension.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.suspend(username='username', reason='reason')
        """
        # Get the session, set the params, and make a post request.
        session = self._ensure_session()

        params = {"user": username, "reason": reason}

        with session.post(
            f"{self.api_url}/suspendacct.php",
            params=params,
            auth=HTTPBasicAuth(self.username, self.password),
        ) as r:
            response = r.text

            try:
                # Parse the response and get the root element.
                root = self._parse_xml(response)

                status = root[0][0].text
                try:
                    return int(status)
                except ValueError:
                    raise APIError(response, 0)
            except ElementTree.ParseError:
                # Raise exception with error.
                raise APIError(response, 0)

    def unsuspend(self, username: str) -> Optional[int]:
        """
        Unsuspends a user's vPanel account.

        :param username: user's internal username, has a limit of 8 characters.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.unsuspend(username='username')
        """
        # Get the session, set the params, and make a post request.
        session = self._ensure_session()

        params = {"user": username}

        with session.post(
            f"{self.api_url}/unsuspendacct.php",
            params=params,
            auth=HTTPBasicAuth(self.username, self.password),
        ) as r:
            response = r.text

            try:
                # Parse the response and get the root element.
                root = self._parse_xml(response)

                status = root[0][0].text
                try:
                    return int(status)
                except ValueError:
                    raise APIError(response, 0)
            except ElementTree.ParseError:
                # Raise exception with error.
                raise APIError(response, 0)

    def change_password(self, username: str, password: str) -> Optional[int]:
        """
        Changes a user's vPanel account password.

        :param username: user's internal username, has a limit of 8 characters.
        :param password: user's new password.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.change_password(username='username', password='password')
        """
        # Get the session, set the params, and make a post request.
        session = self._ensure_session()

        params = {"user": username, "pass": password}

        with session.post(
            f"{self.api_url}/passwd.php",
            params=params,
            auth=HTTPBasicAuth(self.username, self.password),
        ) as r:
            response = r.text

            try:
                # Parse the response and get the root element.
                root = self._parse_xml(response)

                status = root[0][5].text
                try:
                    return int(status)
                except ValueError:
                    raise APIError(response, 0)
            except ElementTree.ParseError:
                # Raise exception with error.
                raise APIError("Invalid username provided.", 0)

    def domain_available(self, domain: str) -> int:
        """
        Checks if a domain is available for registration.

        :param domain: domain you want to check.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.domain_available(domain='example.com')
        """
        # Get the session, set the params, and make a post request.
        session = self._ensure_session()

        params = {"api_user": self.username, "api_key": self.password, "domain": domain}

        with session.post(
            f"{self.api_url}/checkavailable.php",
            params=params,
            auth=HTTPBasicAuth(self.username, self.password),
        ) as r:
            # Get the response and return it.
            response = r.text

            try:
                return int(response)
            except ValueError:
                raise APIError(response, 0)

    def user_domains(self, username: str) -> Any:
        """
        Gets the domains connected to a user's vPanel account.

        :param username: user's vPanel username, e.g. hname_12345678.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.user_domains(username='hname_12345678')
        """
        # Get the session, set the params, and make a post request.
        session = self._ensure_session()

        params = {
            "api_user": self.username,
            "api_key": self.password,
            "username": username,
        }

        with session.post(
            f"{self.api_url}/getuserdomains.php",
            params=params,
            auth=HTTPBasicAuth(self.username, self.password),
        ) as r:
            response = r.text

            if response == "null":
                return 0

            try:
                # Evaluate the response and return it.
                return ast.literal_eval(response)
            except (ValueError, SyntaxError):
                raise APIError(response, 0)

    def user_by_domain(self, domain: str) -> Any:
        """
        Gets the user's vPanel account associated with the domain entered.

        :param domain: domain of the user you want to check.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.user_by_domain(domain='example.com')
        """
        # Get the session, set the params, and make a post request.
        session = self._ensure_session()

        params = {"api_user": self.username, "api_key": self.password, "domain": domain}

        with session.post(
            f"{self.api_url}/getdomainuser.php",
            params=params,
            auth=HTTPBasicAuth(self.username, self.password),
        ) as r:
            response = r.text

            if response == "null":
                return 0

            try:
                # Evaluate the response and return it.
                return ast.literal_eval(response)
            except (ValueError, SyntaxError):
                raise APIError(response, 0)

    def close(self) -> None:
        """
        Closes the internal session.

        Note: This closes the custom session if you used one.

        Usage:
            >>> client = Client(username='username', password='password')
            >>> client.close()
        """
        # Close the session.
        if self._session is not None:
            self._session.close()


class AsyncClient:
    """
    MyOwnFreeHost async API client.

    :param username: MyOwnFreeHost API username
    :param password: MyOwnFreeHost API password
    :param api_url: MyOwnFreeHost API url
    :param session: AIOHTTP session

    Usage:
        >>> client = AsyncClient(username='username', password='password')
    """

    def __init__(
        self,
        username,
        password,
        api_url: str = "https://panel.myownfreehost.net/xml-api/",
        *,
        session: Union[ClientSession, None] = None,
    ):
        self.username = username
        self.password = password
        self.api_url = api_url
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def _ensure_session(self) -> Any:
        """
        Ensure that the session is created.
        """
        if self._session is None:
            # Create new uvloop event loop,
            # set it as the default,
            # and return the ClientSession.
            loop = uvloop.new_event_loop()
            asyncio.set_event_loop(loop)

            self._session = ClientSession(connector=TCPConnector(), loop=loop)

        return self._session

    @staticmethod
    def _parse_xml(response: str) -> Any:
        """
        Parses the XML response and returns a dictionary.

        :param response: XML response.
        """
        # Parse the response and get the root element.
        root = ElementTree.fromstring(response)

        return root

    async def create(
        self, username: str, password: str, contactemail: str, domain: str, plan: str
    ) -> Any:
        """
        Creates a new vPanel user account.

        :param username: user's internal username, has a limit of 8 characters.
        :param password: user's password on the vPanel.
        :param contactemail: user's email on the vPanel.
        :param domain: user's domain on the vPanel.
        :param plan: user's plan on the vPanel.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.create(
            >>>     username="username",
            >>>     password="password",
            >>>     contactemail="example@example.com",
            >>>     domain="subdomain.example.com",
            >>>     plan="MyAwesomePlan",
            >>> )
        """
        # Get the session, set the params, and make a post request.
        session = await self._ensure_session()

        params = {
            "username": username,
            "password": password,
            "contactemail": contactemail,
            "domain": domain,
            "plan": plan,
        }

        async with session.post(
            f"{self.api_url}/createacct.php",
            params=params,
            auth=BasicAuth(self.username, self.password),
        ) as r:
            response = await r.text()

            # Parse the response and get the root element.
            root = self._parse_xml(response)

            status = root[0][2].text
            if status == "1":
                # Return the vPanel username.
                return root[0][0][1].text
            # Raise exception with error.
            error = root[0][3].text
            raise APIError(error, 0)

    async def suspend(self, username: str, reason: str) -> Optional[int]:
        """
        Suspends a user's vPanel account.

        :param username: user's internal username, has a limit of 8 characters.
        :param reason: reason of suspension.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.suspend(username='username', reason='reason')
        """
        # Get the session, set the params, and make a post request.
        session = await self._ensure_session()

        params = {"user": username, "reason": reason}

        async with session.post(
            f"{self.api_url}/suspendacct.php",
            params=params,
            auth=BasicAuth(self.username, self.password),
        ) as r:
            response = await r.text()

            try:
                # Parse the response and get the root element.
                root = self._parse_xml(response)

                status = root[0][0].text
                try:
                    return int(status)
                except ValueError:
                    raise APIError(response, 0)
            except ElementTree.ParseError:
                # Raise exception with error.
                raise APIError(response, 0)

    async def unsuspend(self, username: str) -> Optional[int]:
        """
        Unsuspends a user's vPanel account.

        :param username: user's internal username, has a limit of 8 characters.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.unsuspend(username='username')
        """
        # Get the session, set the params, and make a post request.
        session = await self._ensure_session()

        params = {"user": username}

        async with session.post(
            f"{self.api_url}/unsuspendacct.php",
            params=params,
            auth=BasicAuth(self.username, self.password),
        ) as r:
            response = await r.text()

            try:
                # Parse the response and get the root element.
                root = self._parse_xml(response)

                status = root[0][0].text
                try:
                    return int(status)
                except ValueError:
                    raise APIError(response, 0)
            except ElementTree.ParseError:
                # Raise exception with error.
                raise APIError(response, 0)

    async def change_password(self, username: str, password: str) -> Optional[int]:
        """
        Changes a user's vPanel account password.

        :param username: user's internal username, has a limit of 8 characters.
        :param password: user's new password.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.change_password(username='username', password='password')
        """
        # Get the session, set the params, and make a post request.
        session = await self._ensure_session()

        params = {"user": username, "pass": password}

        async with session.post(
            f"{self.api_url}/passwd.php",
            params=params,
            auth=BasicAuth(self.username, self.password),
        ) as r:
            response = await r.text()

            try:
                # Parse the response and get the root element.
                root = self._parse_xml(response)

                status = root[0][0].text
                try:
                    return int(status)
                except ValueError:
                    raise APIError(response, 0)
            except ElementTree.ParseError:
                # Raise exception with error.
                raise APIError("Invalid username provided.", 0)

    async def domain_available(self, domain: str) -> int:
        """
        Checks if a domain is available for registration.

        :param domain: domain you want to check.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.domain_available(domain='example.com')
        """
        # Get the session, set the params, and make a post request.
        session = await self._ensure_session()

        params = {"api_user": self.username, "api_key": self.password, "domain": domain}

        async with session.post(
            f"{self.api_url}/checkavailable.php",
            params=params,
            auth=BasicAuth(self.username, self.password),
        ) as r:
            # Get the response and return it.
            response = await r.text()

            try:
                return int(response)
            except ValueError:
                raise APIError(response, 0)

    async def user_domains(self, username: str) -> Any:
        """
        Gets the domains connected to a user's vPanel account.

        :param username: user's vPanel username, e.g. hname_12345678.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.user_domains(username='hname_12345678')
        """
        # Get the session, set the params, and make a post request.
        session = await self._ensure_session()

        params = {
            "api_user": self.username,
            "api_key": self.password,
            "username": username,
        }

        async with session.post(
            f"{self.api_url}/getuserdomains.php",
            params=params,
            auth=BasicAuth(self.username, self.password),
        ) as r:
            response = await r.text()

            if response == "null":
                return 0

            try:
                return ast.literal_eval(response)
            except (ValueError, SyntaxError):
                raise APIError(response, 0)

    async def user_by_domain(self, domain: str) -> Any:
        """
        Gets the user's vPanel account associated with the domain entered.

        :param domain: domain of the user you want to check.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.user_by_domain(domain='example.com')
        """
        # Get the session, set the params, and make a post request.
        session = await self._ensure_session()

        params = {"api_user": self.username, "api_key": self.password, "domain": domain}

        async with session.post(
            f"{self.api_url}/getdomainuser.php",
            params=params,
            auth=BasicAuth(self.username, self.password),
        ) as r:
            response = await r.text()

            if response == "null":
                return 0

            try:
                # Evaluate the response and return it.
                return ast.literal_eval(response)
            except (ValueError, SyntaxError):
                raise APIError(response, 0)

    async def close(self) -> None:
        """
        Closes the internal session.

        Note: This closes the custom session if you used one.

        Usage:
            >>> client = AsyncClient(username='username', password='password')
            >>> await client.close()
        """
        # Close the session.
        if self._session is not None:
            await self._session.close()
