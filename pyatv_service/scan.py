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
import json
import pyatv

from pyatv.interface import BaseConfig
from typing import List

from bottle import get, response

from async_utils import synchronized

def __is_apple_tv(device: BaseConfig):
    return device.device_info.raw_model.startswith('AppleTV')


def __to_devices_list(devices: List[BaseConfig]) -> List:
    apple_tv_devices = list(filter(__is_apple_tv, devices))
    result = list(map(lambda device: {
        "address": str(device.address),
        "name": device.name,
        "identifier": device.identifier,
        "services": list(map(lambda service: {
            "identifier": service.identifier,
            "protocol": service.protocol.name,
            "enabled": service.enabled,
            "requires_password": service.requires_password,
            "pairing": service.pairing.name
        }, device.services)),
        "device_info": {
            "operating_system": device.device_info.operating_system.name,
            "version": device.device_info.version,
            "model": device.device_info.model.name,
            "raw_model": device.device_info.raw_model,
            "mac": device.device_info.mac
        }
    }, apple_tv_devices))

    return result


@get('/scan', method='GET')
def scan():
    result = __to_devices_list(devices=synchronized(pyatv.scan(loop=asyncio.get_event_loop())))

    response.content_type = 'application/json'
    return json.dumps(result)
