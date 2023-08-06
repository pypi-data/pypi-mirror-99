"""Setup script for maestro-launcher"""
import os

from setuptools import find_packages
from setuptools import setup

__version__ = '1.0.10'
__license__ = 'BSD License'

__author__ = 'Fantomas42'
__email__ = 'julien.fache@hiventy.com'

__url__ = 'https://bitbucket.org/monalgroup/maestro-cli/'


install_requires = [
    'requests',
    'ruamel.yaml',
]


setup(
    name='maestro-cli',
    version=__version__,
    zip_safe=False,

    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    author=__author__,
    author_email=__email__,
    url=__url__,

    license=__license__,
    platforms='any',
    description='Launch and monitor Maestro JobRequest in few lines of code.',
    long_description=open(os.path.join('README.rst')).read(),
    keywords='maestro, jobrequest',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=install_requires,
)
