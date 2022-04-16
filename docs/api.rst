API Reference
=============

This sections has reference to all of the available functions.

MyOwnFreeHost Client
--------------------

.. py:function:: mofh.Client.create(username='example', password='password', contactemail='example@example.com', domain='subdomain.example.com', plan='MyAwesomePlan')

    Creates a new vPanel account with the specified credentials.

|

.. py:function:: mofh.Client.suspend(username='example', reason='reason')

    Suspends a user's vPanel account. The username is the same username you set when you created the account.

|

.. py:function:: mofh.Client.unsuspend(username='example')

    Unsuspends a user's vPanel account. The username is the same username you set when you created the account.

|

.. py:function:: mofh.Client.chpassword(username='example', password='password')

    Changes a user's vPanel account password. The username is the same username you set when you created the account.

|

.. py:function:: mofh.Client.availability(domain='example.com')

    Checks if a domain is available for registration.

|

.. py:function:: mofh.Client.getuserdomains(username='hname_12345678')

    Gets the domains connected to a user's vPanel account. The username is the username the user uses to log into the vPanel.

|

.. py:function:: mofh.Client.getdomainuser(domain='example.com')

    Gets the user's vPanel account associated with the domain entered.
