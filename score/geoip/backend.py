# Copyright © 2015 STRG.AT GmbH, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

from abc import ABCMeta, abstractmethod
from score.geoip import IPNotFound
from score.init import parse_time_interval


class Backend(metaclass=ABCMeta):

    @abstractmethod
    def __getitem__(self, ip):
        """
        Retrieves location metadata for given IP address and returns backend
        dependent metadata (usually latitude, longitude and location specific
        ISO data) as a dictionary.
        """
        return {}


class Dummy(Backend):
    """
    This backend implementation provides a hardcoded mapping of some IP
    addresses for test purposes. Do not use in production.
    """

    def __getitem__(self, ip):
        mapping = {
            '127.0.0.1': {},  # localhost
            '91.114.15.85': {
                'latitude': 48.190652,
                'longitude': 16.340476,
            }  # strg.at
        }
        if ip in mapping:
            return mapping[ip]
        raise IPNotFound(ip)


class ApiGurus(Backend):
    """
    This backend implementation connects to the API of apigurus.com. It
    retrieves a very detailed set of metadata dependent on the paid licence. For
    detailed information about metadata and licencing visit
    http://apigurus.com/.
    """

    def __init__(self, uri, key, timeout):
        super().__init__()
        self.uri = uri
        self.key = key
        self.timeout = parse_time_interval(timeout)

    def __getitem__(self, ip):
        from http.client import HTTPConnection, HTTPException
        from urllib.parse import urlparse, urlencode
        import json
        parsed_url = urlparse(self.uri)
        connection = HTTPConnection(parsed_url.netloc, timeout=self.timeout)
        params = urlencode({
            'key': self.key,
            'format': 'JSON',
            'compact': 'Y',
            'ip': ip,
        })
        try:
            connection.request('GET', '%s?%s' % (parsed_url.path, params))
            response = connection.getresponse()
            if response.status is not 200:
                raise IPNotFound(ip, response.reason)
            response_body = response.read().decode('UTF-8')
        except HTTPException as e:
            raise IPNotFound(ip, e)
        finally:
            connection.close()
        response_obj = json.loads(response_body)
        if 'geolocation_data' in response_obj:
            return response_obj['geolocation_data']
        if 'query_status' in response_obj and 'query_status_description' \
                in response_obj['query_status']:
            cause = response_obj['query_status']['query_status_description']
        else:
            cause = 'API returned a not parsable response.'
        raise IPNotFound(ip, cause)
