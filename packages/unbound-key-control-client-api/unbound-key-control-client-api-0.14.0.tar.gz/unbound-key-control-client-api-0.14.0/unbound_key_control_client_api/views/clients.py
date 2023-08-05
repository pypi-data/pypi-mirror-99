#!/usr/bin/env python3.9
"""Unbound KeyControl Client API -> Views -> Clients
Copyright (C) 2021 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>."""

from typing import List, Optional

from base_client_api.models.record import Record


class Client(Record):
    """Client"""
    name: Optional[str]
    partition: Optional[str]
    created_at: Optional[str]


class ClientListRespons(Record):
    """Client List Response"""
    total_items: Optional[int]
    limit: Optional[int]
    skip: Optional[int]
    items: Optional[List[Client]]
