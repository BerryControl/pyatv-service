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
import asyncio

from pyatv.storage.file_storage import FileStorage

from pyatv_service.async_utils import synchronized


__pyatv_storage: FileStorage = None


def get_pyatv_storage() -> FileStorage:
    global __pyatv_storage
    return __pyatv_storage


def initialize_pyatv_storage(filename: str):
    global __pyatv_storage
    __pyatv_storage = FileStorage(filename=filename, loop=asyncio.get_event_loop())
    synchronized(__pyatv_storage.load())