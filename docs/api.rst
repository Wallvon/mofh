API Reference
=============

This sections has reference to all of the available functions.

MyOwnFreeHost Client
--------------------

.. py:function:: mofh.Client.create(username='example', password='password', contactemail='example@example.com', domain='subdomain.example.com', plan='MyAwesomePlan')

    Create a user account with the specified credentials on the vPanel.

|

.. py:function:: mofh.Client.suspend(username='example', reason='reason')

    Suspends the user account with the specified credentials. The username is the same username you set when you created the account.

|

.. py:function:: mofh.Client.unsuspend(username='example')

    Unsuspends the user account with the specified credentials. The username is the same username you set when you created the account.

|

.. py:function:: mofh.Client.chpassword(username='example', password='password')

    Changes the password of the user account with the specified credentials. The username is the same username you set when you created the account.

|

.. py:function:: mofh.Client.availability(domain='example.com')

    Checks if the specified domain is still available.

|

.. py:function:: mofh.Client.getuserdomains(username='hname_12345678')

    Gets the connected domains of the user account with the specified credentials. The username is the username the user uses to log into the vPanel.

|

.. py:function:: mofh.Client.getdomainuser(domain='example.com')

    Gets the user associated with the domain entered.
