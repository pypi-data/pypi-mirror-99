from setuptools import setup, find_packages, Extension

import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if os.environ.get("CI_SYNTROPY_VERSION"):
    version = os.environ["CI_SYNTROPY_VERSION"]
else:
    # Development version of the package
    version = "devel"

setup(
    name="syntropy-agent",
    version=version,
    py_modules=['platform-agent'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests==2.24.0',
        'urllib3<1.26',
        'pyroute2==0.5.12',
        'websocket-client==0.57.0',
        'PyNaCl==1.3.0',
        'docker-py==1.10.6',
        'icmplibv2==1.0.6',
        'PyYAML==5.3.1',
        'dnspython==1.16.0',
        'iperf3==0.1.11',
        'prometheus-client==0.8.0',
        'psutil==5.7.2',
        'kubernetes==11.0.0',
    ],
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'syntropy_agent = platform_agent.__main__:main'
        ]
    },
)
