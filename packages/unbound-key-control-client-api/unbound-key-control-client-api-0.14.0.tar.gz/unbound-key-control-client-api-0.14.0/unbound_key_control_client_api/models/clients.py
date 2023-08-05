#!/usr/bin/env python3.9
"""Unbound KeyControl Client API -> Models -> Clients
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
from typing import Optional

from base_client_api.models.record import Record
from pydantic import validator


class ClientCreateOne(Record):
    """Client -> Create One

    POST /api/v1/clients

    Creates a new client and returns the activation code."""
    name: str
    partition_id: Optional[str]
    check_ip: Optional[bool]
    allow_nat: Optional[bool]
    expiration: Optional[int]  # minutes
    activation_code_validity: Optional[int]  # minutes
    is_template: Optional[bool]
    activation_code_length: Optional[int]  # digits
    ip_range: Optional[str]  # CIDR 0.0.0.0/0
    certificate_expiration: Optional[int]  # minutes

    @validator('expiration', 'activation_code_validity', 'activation_code_length', 'certificate_expiration')
    def check_int_length(cls, value) -> int:
        """Check Integer Length

        Ensures the integer provided does not exceed the 32bit limit (2,147,483,647) as set by the API

        Args:
            value (int):

        Returns:
            value (int):"""
        if value > 2147483647:
            raise ValueError('This field must be <= 2,147,483,647')

        return value

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/clients'

    @property
    def method(self) -> str:
        """Method

        The HTTP verb to be used

        Returns:
            (str)"""
        return 'POST'

    @property
    def parameters(self) -> Optional[str]:
        """URL Parameters

        If you need to pass parameters in the URL

        Returns:
            (dict)"""
        return self.json(include={'partition_id'})

    @property
    def headers(self) -> Optional[dict]:
        """Headers

        If you need to pass non-default headers

        Returns:
            (dict)"""
        return {'Accept': 'application/json', 'Content-Type': 'application/json'}

    @property
    def json_body(self) -> Optional[dict]:
        """Request Body"""
        return self.dict(exclude={'partition_id'})


class ClientsListAll(Record):
    """Clients -> List All

    GET /api/v1/clients

    Return a list of all clients."""

    partition_id: Optional[str]
    limit: Optional[int]
    skip: Optional[int]
    detailed: Optional[bool] = True
    template: Optional[str]

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/clients'

    @property
    def response_key(self) -> str:
        """Data Key

        This is the key used in the return dict that holds the primary responses

        Returns:
            (str)"""
        return 'items' if self.limit or self.skip else None

    @property
    def method(self) -> str:
        """Method

        The HTTP verb to be used
         - Must be a valid HTTP verb as listed above in METHODS

        Returns:
            (str)"""
        return 'GET'

    @property
    def headers(self) -> dict:
        """Headers

        If you need to pass non-default headers

        Returns:
            (dict)"""
        return {'Accept': 'application/json'}


class RefreshedCertificateClient(Record):
    """Refreshed Certificate Client"""
    certificate_expiration: Optional[int]
    activation_code_validity: Optional[int]
    activation_code_length: Optional[int]
    ip_range: Optional[str]  # cidr


class ClientRefreshActivationCode(Record):
    """Client -> Refresh Activation Code

    PUT /api/v1/clients/{clientId}/activation-code

    Refresh the client's activation code."""
    client_id: str
    partition_id: Optional[str]
    body: Optional[RefreshedCertificateClient]

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return f'/clients/{self.client_id}/activation-code'

    @property
    def method(self) -> str:
        """Method

        The HTTP verb to be used

        Returns:
            (str)"""
        return 'PUT'

    @property
    def parameters(self) -> Optional[str]:
        """URL Parameters

        If you need to pass parameters in the URL

        Returns:
            (Union[dict, None])"""
        return self.json(include={'partition_id'})

    @property
    def headers(self) -> Optional[dict]:
        """Headers

        If you need to pass non-default headers

        Returns:
            (Union[dict, None])"""
        return {'Accept': 'application/json', 'Content-Type': 'application/json'}
