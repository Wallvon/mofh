import pytest

from mofh.errors import APIError


def test_create(client):
    """
    Test that we can create a new user.
    """
    with pytest.raises(APIError) as exc_info:
        client.create(
            username="example",
            password="password",
            contactemail="example@example.com",
            domain="subdomain.example.com",
            plan="MyAwesomePlan",
        )

    exception_raised = exc_info.value
    assert "The API username you are using appears to be invalid" in str(
        exception_raised
    )


def test_suspend(client):
    """
    Test that we can suspend a user.
    """
    with pytest.raises(APIError) as exc_info:
        client.suspend(username="example", reason="Suspension unit test.")

    exception_raised = exc_info.value
    assert "The API username you are using appears to be invalid" in str(
        exception_raised
    )


def test_unsuspend(client):
    """
    Test that we can unsuspend a user.
    """
    with pytest.raises(APIError) as exc_info:
        client.unsuspend(username="example")

    exception_raised = exc_info.value
    assert "The API username you are using appears to be invalid" in str(
        exception_raised
    )


def test_change_password(client):
    """
    Test that we can change a user's password.
    """
    with pytest.raises(APIError) as exc_info:
        client.change_password(username="example", password="newpassword")

    exception_raised = exc_info.value
    assert "Invalid username provided." in str(exception_raised)


def test_domain_available(client):
    """
    Test that we can check if a domain is available.
    """
    with pytest.raises(APIError) as exc_info:
        client.domain_available(domain="subdomain.example.com")

    exception_raised = exc_info.value
    assert "The API username you are using appears to be invalid" in str(
        exception_raised
    )


def test_user_domains(client):
    """
    Test that we can get a user's domains.
    """
    with pytest.raises(APIError) as exc_info:
        client.user_domains(username="hname_12345678")

    exception_raised = exc_info.value
    assert "The API username you are using appears to be invalid" in str(
        exception_raised
    )


def test_user_by_domain(client):
    """
    Test that we can get a user by domain.
    """
    with pytest.raises(APIError) as exc_info:
        client.user_by_domain(domain="subdomain.example.com")

    exception_raised = exc_info.value
    assert "The API username you are using appears to be invalid" in str(
        exception_raised
    )
