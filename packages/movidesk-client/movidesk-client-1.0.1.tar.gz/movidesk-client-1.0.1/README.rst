===============
movedesk-client
===============

.. image:: https://travis-ci.org/daniellbastos/movidesk-client.svg?branch=master
    :target: https://travis-ci.org/daniellbastos/movidesk-client

Requirements
~~~~~~~~~~~~

    * Python >= 3.x


How to install
~~~~~~~~~~~~~~

    pip install movedesk-client


How to use
~~~~~~~~~~

>>> from move_client import MovedeskClient
>>> client = MovedeskClient('super-token')
>>>
>>> client.person_create({'foo': 'bar'})
>>> ...
>>> client.ticket_create({'foo': 'bar'})


TODO
~~~~

Add access to all resource.
