"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import asyncio
import uuid

import pytest

from .helpers import PalgateAPI


@pytest.mark.asyncio
async def test_generate_token(derived_token_generator):
    check_token_response = await PalgateAPI.check_token(derived_token_generator())
    assert check_token_response['msg'] == 'token valid', 'Unexpected message from server'


@pytest.mark.asyncio
async def test_device_linking(derived_token_generator):
    unique_id = str(uuid.uuid4())
    start_device_linking_task = asyncio.create_task(PalgateAPI.start_device_linking(unique_id))

    link_device_response = await PalgateAPI.link_device(derived_token_generator(), unique_id)
    assert link_device_response['msg'] == 'link success', 'Unexpected message from server'

    linked_device_response = await start_device_linking_task
    assert linked_device_response['msg'] == 'success', 'Unexpected message from server'


@pytest.mark.asyncio
async def test_list_all_gates(derived_token_generator):
    response = await PalgateAPI.get_all_devices(derived_token_generator())
    assert response['msg'] == 'all my devices', 'Unexpected message from server'


@pytest.mark.asyncio
async def test_gate_open(derived_token_generator):
    response = await PalgateAPI.get_all_devices(derived_token_generator())
    assert response['msg'] == 'all my devices', 'Unexpected message from server'

    for gate in response['devices']:
        if not gate['localOnly']:
            open_gate_response = await PalgateAPI.open_gate(derived_token_generator(), gate['id'])
            assert open_gate_response['msg'] == 'Gate opened: true', 'Unexpected message from server'
            break
    else:
        pytest.skip("Didn't find any suitable gates to open")
