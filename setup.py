import re
from setuptools import setup, find_packages


with open('pm2_io_apm_python/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name="pm2_io_apm_python",
    version=version,
    author="Florian Hermouet-Joscht",
    author_email="florian@keymetrics.io",
    description="Python APM for PM2 Enterprise",
    long_description=open('README.md').read(),
    license="MIT",
    keywords="pm2 enterprise apm python metrics actions tracing",
    url='https://github.com/keymetrics/pm2-io-apm-python',
    entry_points={
        'console_scripts': [
            'dronedemo = dronedemo.scripts.dronedemo:cli_entry',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['tests']),
    tests_require=['nose'],
    test_suite='nose.collector',
)