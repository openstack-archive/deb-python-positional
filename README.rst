==========
positional
==========

|PyPi|

|Build Status|

|Documentation Status|

Intro
=====

`positional` provides a decorator which enforces only some args may be passed
positionally. The idea and some of the code was taken from the oauth2 client
of the google-api client.

The Basics
==========

The decorator makes it easy to support Python 3 style key-word only
parameters. For example, in Python 3 it is possible to write:

.. code:: python

    >>> def fn(pos1, *, kwonly1 kwonly=None):
    ...     ...

All named parameters after `*` must be a keyword:

.. code:: python

    >>> fn(10, 'kw1', 'kw2')  # Raises exception.
    >>> fn(10, kwonly1='kw1', kwonly2='kw2')  # Ok.

To replicate this behaviour with the positional decorator you simply specify
how many arguments may be passed positionally.

Replicating the Example above:

.. code:: python

    >>> @positional(1)
    ... fn(pos1, kwonly1=None, kwonly2=None):
    ...     ...

If no default value is provided to a keyword argument, it becomes a required
keyword argument:

.. code:: python

    >>> @positional(0)
    ... def fn(required_kw):
    ...     ...

This must be called with the keyword parameter:

.. code:: python

    >>> fn() # Raises exception
    >>> fn(10) # Raises Exception
    >>> fn(required_kw=10) # OK

When defining instance or class methods always remember that in python the
first positional argument passed is the instance; you will need to account for
`self` and `cls`:

.. code:: python

    >>> class MyClass(object):
    ...
    ...     @positional(2)
    ...     def my_method(self, pos1, kwonly1=None):
    ...         ...
    ...
    ...     @classmethod
    ...     @positional(2)
    ...     def my_method(cls, pos1, kwonly1=None):
    ...         ...



If you would prefer not to account for `self` and `cls` you can use the
`method` and `classmethod` helpers which do not consider the initial
positional argument. So the following class is exactly the same as the one
above:

.. code:: python

    >>> class MyClass(object):
    ...
    ...     @positional.method(1)
    ...     def my_method(self, pos1, kwonly1=None):
    ...         ...
    ...
    ...     @positional.classmethod(1)
    ...     def my_method(cls, pos1, kwonly1=None):
    ...         ...


If a value isn't provided to the decorator then it will enforce that
every variable without a default value will be required to be a kwarg:

.. code:: python

    >>> @positional()
    ... def fn(pos1, kwonly1=None):
    ...     ...
    ...
    >>> fn(10)  # Ok.
    >>> fn(10, 20)  # Raises exception.
    >>> fn(10, kwonly1=20)  # Ok.

This behaviour will work with the `positional.method` and
`positional.classmethod` helper functions as well:

.. code:: python

    >>> class MyClass(object):
    ...
    ...    @positional.classmethod()
    ...    def my_method(cls, pos1, kwonly1=None):
    ...        ...
    ...
    >>> MyClass.my_method(10)  # Ok.
    >>> MyClass.my_method(10, 20)  # Raises exception.
    >>> MyClass.my_method(10, kwonly1=20)  # Ok.

For compatibility reasons you may wish to not always raise an exception so
a WARN mode is available. Rather than raise an exception a warning message
will be logged:

.. code:: python

    >>> @positional(1, enforcement=positional.WARN):
    ... def fn(pos1, kwonly=1):
    ...    ...


.. |Build Status| image:: https://travis-ci.org/morganfainberg/positional.svg?branch=master
   :target: https://travis-ci.org/morganfainberg/positional
.. |Documentation Status| image:: https://readthedocs.org/projects/positional/badge/?version=latest
   :target: http://positional.readthedocs.org/en/latest/?badge=latest
.. |PyPi| image:: https://badge.fury.io/py/positional.png
   :target: http://badge.fury.io/py/positional
