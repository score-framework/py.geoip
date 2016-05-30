.. module:: score.geoip
.. role:: confkey
.. role:: confdefault

***********
score.geoip
***********

This module handles requests to a backend that is intended to get
location metadata for a given IP address. A backend is a configurable
implementation providing a lookup functionality returning metadata as
a dictionary.


Quickstart
==========

>>> from pprint import pprint
>>> pprint(score.geoip['8.8.8.8'])
{'as': 'AS15169 Google Inc.',
 'city': 'Mountain View',
 'country': 'United States',
 'countryCode': 'US',
 'isp': 'Google',
 'lat': 37.386,
 'lon': -122.0838,
 'org': 'Google',
 'query': '8.8.8.8',
 'region': 'CA',
 'regionName': 'California',
 'status': 'success',
 'timezone': 'America/Los_Angeles',
 'zip': '94035'}


Configuration
=============

.. autofunction:: init

Details
=======

Command-Line Interface
----------------------

Upon installation, this module registers a :mod:`score.cli` command that can be
used to lookup IP addresses. As a precondition the module
:ref:`configuration <geoip_configuration>` needs to be satisfied as
described in the :ref:`score.cli configuration management
<cli_configuration_management>`.

.. code-block:: console

    $ score geoip lookup 8.8.8.8
    $ score geoip lookup --format json 8.8.8.8
    {
        "metro_code": "807",
        "country_code_iso3166numeric": "840",
        "longitude": -122.0838,
        "isp": "Google",
        "country_code_iso3166alpha3": "USA",
        "postal_code": "94040",
        "continent_name": "North America",
        "area_code": "650",
        "organization": "Google",
        "country_name": "United States",
        "latitude": 37.386,
        "continent_code": "NA",
        "region_name": "California",
        "country_code_iso3166alpha2": "US",
        "region_code": "CA",
        "city": "Mountain View",
        "country_code_fips10-4": "US"
    }

.. code-block:: console

    $ score geoip lookup -f xml montypython.com
    <?xml version="1.0" ?>
    <location>
        <country_name>United States</country_name>
        <continent_code>NA</continent_code>
        <metro_code>807</metro_code>
        <region_name>California</region_name>
        <postal_code>94107</postal_code>
        <country_code_iso3166alpha3>USA</country_code_iso3166alpha3>
        <country_code_iso3166numeric>840</country_code_iso3166numeric>
        <isp>CloudFlare</isp>
        <city>San Francisco</city>
        <continent_name>North America</continent_name>
        <country_code_fips10-4>US</country_code_fips10-4>
        <longitude>-122.3933</longitude>
        <region_code>CA</region_code>
        <latitude>37.7697</latitude>
        <area_code>415</area_code>
        <organization>CloudFlare</organization>
        <country_code_iso3166alpha2>US</country_code_iso3166alpha2>
    </location>

Caching
-------

This module supports optional caching with :mod:`score.kvcache`. It registers a
cache container named *score.geoip*, that needs to be configured as
described in the :ref:`score.kvcache configuration <kvcache_configuration>`.

.. _geoip_configuration:

API
===

.. autofunction:: init

.. autoclass:: ConfiguredGeoipModule

    .. attribute:: backend

        The configured backend.

.. autoclass:: IPNotFound

.. autoclass:: score.geoip.backend.Backend

    .. automethod:: score.geoip.backend.Backend.__getitem__

Ready-to-use Backends
---------------------

.. autoclass:: score.geoip.backend.Dummy

.. autoclass:: score.geoip.backend.IpApi

.. autoclass:: score.geoip.backend.ApiGurus

    .. attribute:: uri

        The URI of the desired apigurus.com API.

    .. attribute:: key

        The key provided by the vendor for the client.

    .. attribute:: timeout

        The connect timeout while connecting to the API.
