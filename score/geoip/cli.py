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

import click
from score.cli import config
from score.geoip import init


@click.group()
def main():
    """
    CLI for getting IP based location metadata.
    """


@main.command('lookup')
@click.argument('ip')
@click.option('-f', '--format', 'frmt', default='json',
              type=click.Choice(['json', 'xml']))
def lookup(ip, frmt):
    kvcache_conf = None
    try:
        import score.kvcache
    except ImportError:
        pass
    else:
        kvcache_conf = score.kvcache.init(dict(config()['score.kvcache']))
    module = init(dict(config()[__package__]), kvcache_conf)
    if frmt == 'json':
        from json import dumps as json_encode
        print(json_encode(module[ip], indent=4).strip())
        return
    from xml.dom.minidom import getDOMImplementation
    impl = getDOMImplementation()
    doc = impl.createDocument(None, 'location', None)
    root = doc.documentElement
    for k, v in module[ip].items():
        el = doc.createElement(str(k))
        el.appendChild(doc.createTextNode(str(v)))
        root.appendChild(el)
    doc.appendChild(root)
    print(doc.toprettyxml(indent=' '*4, newl='\n').strip())
