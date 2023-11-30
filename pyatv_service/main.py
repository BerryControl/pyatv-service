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
from argparse import ArgumentParser
from bottle import run

from pyatv_service import pairing
from pyatv_service import scan
from pyatv_service import control
from pyatv_service.pyatv_storage import initialize_pyatv_storage


def main():
    parser = ArgumentParser(prog='pyatv-service', description='pyatv REST API for YUSR Remote')
    parser.add_argument('port', help='Port on which the service is listening', type=int)
    args = parser.parse_args()

    # TODO make the storage path configurable
    initialize_pyatv_storage("/Users/thomas/pyatv.conf")

    run(host='localhost', port=args.port)

if __name__ == '__main__':
    main()
