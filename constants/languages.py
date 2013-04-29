# -*- coding: utf8 -*-
"""
:mod:`constants.languages` -- A list of languages
=================================================

`ISO 639-1`_ language codes and associated data.

.. autodata:: EN
.. autodata:: ENGLISH
.. autodata:: FR
.. autodata:: FRENCH
.. autodata:: ES
.. autodata:: SPANISH

Extra language information
--------------------------

.. autodata:: INFO

.. _ISO 639-1: http://en.wikipedia.org/wiki/ISO_639-1

"""

#: Language code for english
EN = u'en'
#: Alias english
ENGLISH = EN

#: Language code for french
FR = u'fr'
#: Alias french
FRENCH = FR

#: Language code for spanish
ES = u'es'
#: Alias spanish
SPANISH = ES


#: use like:
#:
#: .. code-block:: python
#:
#:    from constants import languages
#:
#:    languages.INFO[languages.EN]

INFO = {
    EN: {
        'lang': ENGLISH,  # A self reference
        'direction': 'ltr',  # text direction, ltr (left to right) or 'rtl'
        'name': u'English',  # Name of the language as known to its speakers.
        'local_names': {}  # Name of the language localized to given lang.
    },
    ES: {
        'lang': SPANISH,
        'direction': 'ltr',
        'name': u'Español',
        'local_names': {
            'en': u'Spanish'
        }
    },
    FR: {
        'lang': FRENCH,
        'direction': 'ltr',
        'name': u'français',
        'local_names': {
            'en': u'French'
        }
    }
}
