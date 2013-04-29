import os

from setuptools import setup


requires = [
    'mongokit',  # Fork of MongoKit by same author is MongoLite
    'pymongo'
]

message_extractors = {
}

setup(
    name='dataimport',
    version='0.0',
    description='Data Pump utility',
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    message_extractors=message_extractors,
    tests_require=requires,        
)
