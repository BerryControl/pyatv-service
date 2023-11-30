#
#    Copyright 2023 Thomas Bonk <thomas@meandmymac.de>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

from setuptools import setup
from pyatv_service import __version__

setup(
    name='pyatv-service',
    version=__version__,
    description='pyatv REST API for YUSR Remote',
    url='https://github.com/yusr-project/pyatv-service',
    author='Thomas Bonk',
    author_email='thomas@meandmymac.de',
    license='Apache-2.0',
    packages=[
        'pyatv_service'
    ],
    install_requires=[
        'pyatv>=0.14.4',
        'bottle>=0.12.25',
        'cachetools>=5.3.2'
    ],
    entry_points={
        'console_scripts': ['pyatv-service=pyatv_service.main:main'],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)