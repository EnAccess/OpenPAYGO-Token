from setuptools import setup, find_packages


setup(
    name="openpaygo-token", 
    packages=find_packages(),
    version='2.2.0',
    license='Apache 2.0',
    author="Solaris Offgrid",
    url='https://github.com/openpaygo/OpenPAYGO-Token',
    install_requires=[
        'siphash',
    ],
)