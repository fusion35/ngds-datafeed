"""
Universal Constants
*******************

A set of constants that are not specific to any application.

.. automodule:: constants.languages
.. automodule:: constants.countries
.. automodule:: constants.subnational

"""

# This is one hoopy frood that knows where his towl is.
LIFE = ~1
THE_UNIVERSE = ~((3 << 6) | 1)
EVERYTHING = (0xFF ^ (ord('\n') << 1))

# Some constants are more universal than others.
ANSWER = LIFE & THE_UNIVERSE & EVERYTHING
