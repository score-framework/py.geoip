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

from score.init import init_object, ConfiguredModule
import dns.resolver


def init(confdict, kvcache_conf=None):
    """
    Initializes this module acoording to :ref:`our module initialization
    guidelines <module_initialization>` with the following configuration keys:

    :confkey:`backend`
        The backend object configuration that will be passed to
        :func:`score.init.init_object`. Have a look at the configurable
        backend's constructor parameters for further information about
        the backend's configurable keys.

    """
    backend = init_object(confdict, 'backend')
    cache_container = None
    if kvcache_conf is not None:
        kvcache_conf.register_generator('score.geoip', backend.__getitem__)
        cache_container = kvcache_conf['score.geoip']
    return ConfiguredGeoipModule(backend, cache_container)


class ConfiguredGeoipModule(ConfiguredModule):
    """
    This module's :class:`configuration object
    <score.init.ConfiguredModule>`.
    """

    def __init__(self, backend, cache_container=None):
        super().__init__(__package__)
        self.backend = backend
        self.cache_container = cache_container

    def __getitem__(self, ip):
        try:
            ip = str(dns.resolver.query(ip)[0])
        except dns.resolver.NXDOMAIN:
            raise IPNotFound(ip, 'Domain not resolvable.')
        if self.cache_container is None:
            return self.backend[ip]
        return self.cache_container[ip]


class IPNotFound(Exception):
    """
    Thrown if IP lookup failed.
    """

    def __init__(self, ip, cause=None):
        self.ip = ip
        self.cause = cause
