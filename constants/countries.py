# -*- coding: utf8 -*-
"""
:mod:`constants.countries` -- A list of countries
=================================================

`ISO 3166-1`_ country codes and associated data.

Alpha-2 country codes
---------------------

.. autodata:: US
.. autodata:: CA

Extra country information
-------------------------

.. autodata:: INFO

.. _ISO 3166-1: http://en.wikipedia.org/wiki/ISO_3166-1

"""

#: Country code for US
US = u'US'

#: Country code for Canada
CA = u'CA'


#: use like:
#:
#: .. code-block:: python
#:
#:    from constants import countries
#:
#:    countries.INFO[countries.US]

INFO = {
    US: {
        'long': u'USA',  # Alpha-3 country code
        'numeric': 840,  # Numeric country code
        'name': u'United States'  # Official name
    },
    CA: {
        'long': u'CAN',
        'numeric': 124,
        'name': u'Canada'
    }
}
