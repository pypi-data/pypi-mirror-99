"""
Swarm bus
"""
from setuptools import find_packages
from setuptools import setup

__version__ = '5.11'
__license__ = 'GPL License'

__author__ = 'The Swarm Team'
__email__ = 'dev@hiventy.com'

__url__ = 'https://bitbucket.org/monalgroup/swarm-bus'


install_requires = [
    'boto3==1.14.20',
]


setup(
    name='swarm-bus',
    version=__version__,
    license=__license__,

    description='ESB SQS based',
    long_description=open('README.rst').read(),
    keywords='ESB, tools, swarm, bus',

    packages=find_packages(exclude=('tests', 'tests.*')),

    author=__author__,
    author_email=__email__,
    url=__url__,

    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],

    install_requires=install_requires,

    zip_safe=False,
    include_package_data=True,
)
