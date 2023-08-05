#!/usr/bin/env python3.9
"""Unbound KeyControl Client API -> Models -> Users
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


class UsersListAll(Record):
    """Users -> List All

    GET /api/v1/users

    Return a list of all users in a partition."""
    partition_id: Optional[str]
    limit: Optional[int]
    skip: Optional[int]

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/users'

    @property
    def response_key(self) -> Optional[str]:
        """Data Key

        This is the key used in the return dict that holds the primary responses

        Returns:
            (str)"""
        return 'items' if self.limit or self.skip else None

    @property
    def method(self) -> Optional[str]:
        """Method

        The HTTP verb to be used
         - Must be a valid HTTP verb as listed above in METHODS

        Returns:
            (str)"""
        return 'GET'


# The API currently isn't accepting this (unknown field)
# class UserAliases(Record):
#     identity_provider_name: str
#     aliases: List[str]


class NewUser(Record):
    """New User"""
    password: Optional[str]  # todo: get complexity requirements
    name: str
    role: str
    # aliases: Optional[UserAliases]  # The API currently isn't accepting this (unknown field)
    auth_type: Optional[str]  # STANDARD, LDAP, OIDC


class UserCreateOne(Record):
    """User -> Create One

    POST /api/v1/users

    Create a new user in a given partition."""
    partition_id: Optional[str]
    body: NewUser

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/users'

    @property
    def method(self) -> Optional[str]:
        """Method

        The HTTP verb to be used
         - Must be a valid HTTP verb as listed above in METHODS

        Returns:
            (str)"""
        return 'POST'

    @property
    def headers(self) -> Optional[dict]:
        """Headers

        If you need to pass non-default headers

        Returns:
            (dict)"""
        return {'Accept': 'application/json', 'Content-Type': 'application/json'}
