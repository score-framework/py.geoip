import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(
    name='score.geoip',
    version='0.1.1',
    description='IP Geolocalization for The SCORE Framework',
    long_description=README,
    author='strg.at',
    author_email='support@strg.at',
    url='http://strg.at',
    keywords='web wsgi bfg pylons pyramid',
    packages=['score.geoip'],
    namespace_packages=['score'],
    license='LGPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General '
            'Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
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
