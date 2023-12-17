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
import uuid

from bottle import post, request, response
from cachetools import TTLCache

from async_utils import synchronized
from pyatv_service.pyatv_storage import get_pyatv_storage

pairing_requests_cache = TTLCache(maxsize=10, ttl=300)


@post('/start_pairing/<device_id>')
def start_pairing(device_id: str):
    loop = asyncio.get_event_loop()
    devices = synchronized(pyatv.scan(identifier=device_id, loop=loop))

    if not devices:
        response.status = 404
        return "Device not found"

    payload = json.load(request.body)
    remote_name: str = payload["remoteName"]

    apple_tv_device = devices[0]
    pairing_handler = synchronized(pyatv.pair(config=apple_tv_device, protocol=pyatv.Protocol.Companion, loop=loop,
                                              storage=get_pyatv_storage(), name=remote_name))
    synchronized(pairing_handler.begin())
    pairing_request = str(uuid.uuid4())
    pairing_requests_cache[pairing_request] = pairing_handler

    response.content_type = 'application/json'
    return json.dumps({
        "pairingRequest": pairing_request,
        "deviceProvidesPin": pairing_handler.device_provides_pin
    })


@post('/finalize_pairing/<pairing_request>')
def finalize_pairing(pairing_request: str):
    pairing_handler = pairing_requests_cache[pairing_request]

    if not pairing_handler:
        response.status = 404
        return "Pairing request not found"

    payload = json.load(request.body)
    pin: str = payload["pin"]
    device_provides_pin: bool = payload["deviceProvidesPin"]

    if device_provides_pin:
        pairing_handler.pin(pin)
        synchronized(pairing_handler.finish())
        device_has_paired = pairing_handler.has_paired
        pairing_handler.close()
        synchronized(get_pyatv_storage().save())
    else:
        response.status = 500
        return "Use case device_provides_pin = False not yet supported"

    response.content_type = 'application/json'
    return json.dumps({
        "deviceHasPaired": device_has_paired
    })