#!/usr/bin/env python3.9
"""Unbound KeyControl Client API -> Models -> Roles
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
from pydantic import validator

ROLE_PERMISSION_OPERATIONS = {'ACTIVATE',
                              'ENABLE/DISABLE',
                              'REVOKE',
                              'ATTR-ADD',
                              'ATTR-CHANGE',
                              'ATTR-DELETE',
                              'LINK',
                              'RELINK',
                              'UNLINK',
                              'TOKENIZE',
                              'CHANGE-SECRET',
                              'DELETE',
                              'DESTROY',
                              'DERIVE-EXT',
                              'DERIVE',
                              'RE-KEYPAIR',
                              'RE-KEY',
                              'GENERATE-KEYPAIR',
                              'GENERATE-KEY',
                              'IMPORT',
                              'EXPORT-SECRET',
                              'EXPORT-KEY',
                              'MAC-VERIFY',
                              'MAC-CREATE',
                              'VERIFY',
                              'SIGN',
                              'DECRYPT',
                              'ENCRYPT'}


class RolesListAll(Record):
    """ Roles -> List All

    GET /api/v1/roles

    Return a list of all roles in a partition."""
    partition_id: Optional[str]
    limit: Optional[int]
    skip: Optional[int]
    detailed: Optional[bool] = True

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/roles'

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

    @property
    def headers(self) -> Optional[dict]:
        """Headers

        If you need to pass non-default headers

        Returns:
            (dict)"""
        return {'Accept': 'application/json'}


class RoleGetOne(Record):
    """Roles -> Get One

    GET /api/v1/roles/{roleId}

    Get details of an existing role."""
    role_id: str
    partition_id: Optional[str]
    detailed: Optional[bool] = True

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return f'/roles/{self.role_id}'

    @property
    def method(self) -> Optional[str]:
        """Method

        The HTTP verb to be used
         - Must be a valid HTTP verb as listed above in METHODS

        Returns:
            (str)"""
        return 'GET'

    @property
    def headers(self) -> Optional[dict]:
        """Headers

        If you need to pass non-default headers

        Returns:
            (dict)"""
        return {'Accept': 'application/json'}

    @property
    def parameters(self) -> Optional[str]:
        """URL Parameters

        If you need to pass parameters in the URL

        Returns:
            (dict)"""
        return self.json(exclude={'role_id'})


class RolePermission(Record):
    """Role -> Permission"""
    object_group: Optional[str]
    operations: Optional[List[str]]

    @validator('operations')
    def verify_operations(cls, value) -> list:
        """Verify Operations

        Checks if the operations specified are valid for the API

        Args:
            value (list):

        Returns:
            value (list):"""
        contains = list(map(lambda x: x in ROLE_PERMISSION_OPERATIONS, value))

        if False in contains:
            raise ValueError(f'Operations must be one of: {", ".join(ROLE_PERMISSION_OPERATIONS)}')

        return value


class NewRole(Record):
    """Role -> New"""
    name: str
    managed_objects_permissions: List[RolePermission]


class RoleCreateOne(Record):
    """Role -> Create One

    POST /api/v1/roles

    Create a new role in a given partition."""
    partition_id: Optional[str]
    body: NewRole

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/roles'

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


class UpdatedRole(Record):
    """Role -> Update"""
    managed_objects_permissions: List[RolePermission]


class RoleUpdateOne(Record):
    """Role -> Update One

    PUT /api/v1/roles/{roleId}

    Update a role."""
    role_id: str
    partition_id: Optional[str]
    body: UpdatedRole

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return f'/roles/{self.role_id}'

    @property
    def method(self) -> Optional[str]:
        """Method

        The HTTP verb to be used
         - Must be a valid HTTP verb as listed above in METHODS

        Returns:
            (str)"""
        return 'PUT'

    @property
    def headers(self) -> Optional[dict]:
        """Headers

        If you need to pass non-default headers

        Returns:
            (dict)"""
        return {'Accept': 'application/json', 'Content-Type': 'application/json'}
