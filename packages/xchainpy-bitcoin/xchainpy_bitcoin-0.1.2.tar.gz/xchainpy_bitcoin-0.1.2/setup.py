from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_bitcoin',
    packages=find_packages(),
    version='0.1.2',
    license='MIT',
    description='Bitcoin Module for XChainPy Clients',
    author='THORChain',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib',
    keywords=["THORChain", "XChainpy","XChainpy_bitcoin","BTC","Bitcoin"],
    install_requires=required,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python'
    ],
)