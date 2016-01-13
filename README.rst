A decorator which enforces only some args may be passed positionally.

|Build Status|

|Documentation Status|

.. |Build Status| image:: https://travis-ci.org/morganfainberg/positional.svg?branch=master
   :target: https://travis-ci.org/morganfainberg/positional
.. |Documentation Status| image:: https://readthedocs.org/projects/positional/badge/?version=latest
   :target: http://positional.readthedocs.org/en/latest/?badge=latest

This idea and some of the code was taken from the oauth2 client of the
google-api client.

This decorator makes it easy to support Python 3 style key-word only
parameters. For example, in Python 3 it is possible to write::

    def fn(pos1, *, kwonly1, kwonly2=None):
        ...

All named parameters after * must be a keyword::

    fn(10, 'kw1', 'kw2')  # Raises exception.
    fn(10, kwonly1='kw1', kwonly2='kw2')  # Ok.

To replicate this behaviour with the positional decorator you simply
specify how many arguments may be passed positionally. To replicate the
example above::

    from positional import positional

    @positional(1)
    def fn(pos1, kwonly1=None, kwonly2=None):
        ...

If no default value is provided to a keyword argument, it becomes a
required keyword argument::

    @positional(0)
    def fn(required_kw):
        ...

This must be called with the keyword parameter::

    fn()  # Raises exception.
    fn(10)  # Raises exception.
    fn(required_kw=10)  # Ok.

When defining instance or class methods always remember that in python the
first positional argument passed is always the instance so you will need to
account for `self` and `cls`::

    class MyClass(object):

        @positional(2)
        def my_method(self, pos1, kwonly1=None):
            ...

        @classmethod
        @positional(2)
        def my_method(cls, pos1, kwonly1=None):
            ...

If you would prefer not to account for `self` and `cls` you can use the
`method` and `classmethod` helpers which do not consider the initial
positional argument. So the following class is exactly the same as the one
above::

    class MyClass(object):

        @positional.method(1)
        def my_method(self, pos1, kwonly1=None):
            ...

        @positional.classmethod(1)
        def my_method(cls, pos1, kwonly1=None):
            ...

If a value isn't provided to the decorator then it will enforce that
every variable without a default value will be required to be a kwarg::

    @positional()
    def fn(pos1, kwonly1=None):
        ...

    fn(10)  # Ok.
    fn(10, 20)  # Raises exception.
    fn(10, kwonly1=20)  # Ok.

This behaviour will work with the `positional.method` and
`positional.classmethod` helper functions as well::

    class MyClass(object):

        @positional.classmethod()
        def my_method(cls, pos1, kwonly1=None):
            ...

    MyClass.my_method(10)  # Ok.
    MyClass.my_method(10, 20)  # Raises exception.
    MyClass.my_method(10, kwonly1=20)  # Ok.

For compatibility reasons you may wish to not always raise an exception so
a WARN mode is available. Rather than raise an exception a warning message
will be logged::

    @positional(1, enforcement=positional.WARN):
    def fn(pos1, kwonly=1):
        ...

Available modes are:

- positional.EXCEPT - the default, raise an exception.
- positional.WARN - log a warning on mistake.
