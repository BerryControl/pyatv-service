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
import pyatv

from bottle import post, request, response

from async_utils import synchronized
from pyatv_service.pyatv_storage import get_pyatv_storage


def __execute_while_connected(device_id: str, operation):
    loop = asyncio.get_event_loop()
    devices = synchronized(pyatv.scan(identifier=device_id, loop=loop))

    if not devices:
        response.status = 404
        return "Device not found"

    apple_tv_device = devices[0]
    atv = synchronized(pyatv.connect(apple_tv_device, loop=loop, storage=get_pyatv_storage()))

    operation(atv)

    synchronized(asyncio.gather(*atv.close()))


@post("/control/turn_off/<device_id>")
def turn_off(device_id: str):
    def __turn_off(atv):
        synchronized(atv.power.turn_off())

    __execute_while_connected(device_id, __turn_off)


@post("/control/turn_on/<device_id>")
def turn_on(device_id: str):
    def __turn_on(atv):
        synchronized(atv.power.turn_on())

    __execute_while_connected(device_id, __turn_on)


@post("/control/up/<device_id>")
def up(device_id: str):
    def __up(atv):
        synchronized(atv.remote_control.up())

    __execute_while_connected(device_id, __up)


@post("/control/right/<device_id>")
def right(device_id: str):
    def __right(atv):
        synchronized(atv.remote_control.right())

    __execute_while_connected(device_id, __right)


@post("/control/down/<device_id>")
def down(device_id: str):
    def __down(atv):
        synchronized(atv.remote_control.down())

    __execute_while_connected(device_id, __down)


@post("/control/left/<device_id>")
def left(device_id: str):
    def __left(atv):
        synchronized(atv.remote_control.left())

    __execute_while_connected(device_id, __left)


@post("/control/select/<device_id>")
def select(device_id: str):
    def __select(atv):
        synchronized(atv.remote_control.select())

    __execute_while_connected(device_id, __select)


@post('/control/play_pause/<device_id>')
def play_pause(device_id: str):
    def __play_pause(atv):
        synchronized(atv.remote_control.play_pause())

    __execute_while_connected(device_id, __play_pause)


@post('/control/back/<device_id>')
def back(device_id: str):
    def __back(atv):
        synchronized(atv.remote_control.menu())

    __execute_while_connected(device_id, __back)


@post('/control/volume_up/<device_id>')
def back(device_id: str):
    def __volume_up(atv):
        synchronized(atv.audio.volume_up())

    __execute_while_connected(device_id, __volume_up)


@post('/control/volume_down/<device_id>')
def back(device_id: str):
    def __volume_down(atv):
        synchronized(atv.audio.volume_down())

    __execute_while_connected(device_id, __volume_down)


@post('/control/home/<device_id>')
def back(device_id: str):
    def __home(atv):
        synchronized(atv.remote_control.home())

    __execute_while_connected(device_id, __home)
