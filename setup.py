import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

setup(
    name='score.geoip',
    version='0.1',
    description='IP Geolocalization for The SCORE Framework',
    long_description=README,
    author='strg.at',
    author_email='support@strg.at',
    url='http://strg.at',
    keywords='web wsgi bfg pylons pyramid',
    packages=['score.geoip'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'score.cli': [
            'geoip = score.geoip.cli:main',
        ]
    },
    install_requires=[
        'score.init >= 0.1',
        'dnspython3',
    ],
    extras_require={
        'cli': [
            'score.kvcache >= 0.1',
            'score.cli >= 0.1',
        ]
    }
)
