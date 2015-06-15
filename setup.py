from distutils.core import setup
from setuptools import find_packages

setup(
    name='D-Link DDNS IP-Updater',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/philip-raschke/D-Link-DDNS-IP-Updater',
    license='MIT',
    author='Philip Raschke',
    author_email='philip@raschke.cc',
    description='A small script to update the public IP address to the D-Link DDNS web service.',
    install_requires=['requests[security]', 'BeautifulSoup']
)
