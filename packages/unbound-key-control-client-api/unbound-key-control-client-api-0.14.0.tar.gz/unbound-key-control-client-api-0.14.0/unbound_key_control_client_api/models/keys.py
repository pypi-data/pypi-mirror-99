#!/usr/bin/env python3.9
"""Unbound KeyControl Client API -> Models -> Keys
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

EXPORT_TYPES = ['IN_PLAIN', 'WRAPPED', 'WRAPPED_WITH_TRUSTED', 'NON_EXPORTABLE']
KEY_ID_ENCODING = ['PLAIN', 'BASE64', 'HEX']
KEY_MAP = {'RSA':     {'size':         ['2048', '3072', '4096'],
                       'usage':        ['SIGN', 'DECRYPT', 'UNWRAP'],
                       'export_types': EXPORT_TYPES},
           'ECC':     {'size':         ['P256', 'P384', 'P521', 'SECP_256K_1'],  # check on these for curve field
                       'usage':        ['SIGN', 'DERIVE', 'ENCRYPT', 'DECRYPT'],
                       'export_types': EXPORT_TYPES},
           'EDDSA':   {'size':         ['256'],
                       'usage':        ['SIGN', 'DERIVE'],
                       'export_types': EXPORT_TYPES},
           'AES':     {'size':         ['128', '192', '256'],
                       'usage':        ['ENCRYPT', 'DECRYPT', 'WRAP', 'UNWRAP', 'MAC'],
                       'export_types': EXPORT_TYPES},
           'AES-SIV': {'size':         ['256', '512'],
                       'usage':        ['WRAP', 'UNWRAP', 'DERIVE'],
                       'export_types': EXPORT_TYPES},
           'XTS':     {'size':         ['256', '512'],
                       'usage':        ['ENCRYPT', 'DECRYPT', 'DERIVE'],
                       'export_types': EXPORT_TYPES},
           'PWD':     {'size':         [],
                       'usage':        [],
                       'export_types': []},
           'PRF':     {'size':         [],
                       'usage':        [],
                       'export_types': []},
           '3DES':    {'size':         ['192'],
                       'usage':        ['ENCRYPT', 'DECRYPT', 'WRAP', 'UNWRAP', 'MAC', 'MAC_VERIFY', 'DERIVE'],
                       'export_types': EXPORT_TYPES},
           'LIMA':    {'size':         ['1024'],
                       'usage':        [],
                       'export_types': EXPORT_TYPES},
           'HAMC':    {'size':  ['8', '16', '24', '32', '40', '48', '56', '64', '72', '80', '88', '96', '104', '112', '120', '128',
                                 '136', '144', '152', '160', '168', '176', '184', '192', '200', '208', '216', '224', '232', '240',
                                 '248', '256', '264', '272', '280', '288', '296', '304', '312', '320', '328', '336', '344', '352',
                                 '360', '368', '376', '384', '392', '400', '408', '416', '424', '432', '440', '448', '456', '464',
                                 '472', '480', '488', '496', '504', '512', '520', '528', '536', '544', '552', '560', '568', '576',
                                 '584', '592', '600', '608', '616', '624', '632', '640', '648', '656', '664', '672', '680', '688',
                                 '696', '704', '712', '720', '728', '736', '744', '752', '760', '768', '776', '784', '792', '800',
                                 '808', '816', '824', '832', '840', '848', '856', '864', '872', '880', '888', '896', '904', '912',
                                 '920', '928', '936', '944', '952', '960', '968', '976', '984', '992', '1000', '1008', '1016',
                                 '1024', '1032', '1040', '1048', '1056', '1064', '1072', '1080', '1088', '1096', '1104', '1112',
                                 '1120', '1128', '1136', '1144', '1152', '1160', '1168', '1176', '1184', '1192', '1200', '1208',
                                 '1216', '1224', '1232', '1240', '1248', '1256', '1264', '1272', '1280', '1288', '1296', '1304',
                                 '1312', '1320', '1328', '1336', '1344', '1352', '1360', '1368', '1376', '1384', '1392', '1400',
                                 '1408', '1416', '1424', '1432', '1440', '1448', '1456', '1464', '1472', '1480', '1488', '1496',
                                 '1504', '1512', '1520', '1528', '1536', '1544', '1552', '1560', '1568', '1576', '1584', '1592',
                                 '1600', '1608', '1616', '1624', '1632', '1640', '1648', '1656', '1664', '1672', '1680', '1688',
                                 '1696', '1704', '1712', '1720', '1728', '1736', '1744', '1752', '1760', '1768', '1776', '1784',
                                 '1792', '1800', '1808', '1816', '1824', '1832', '1840', '1848', '1856', '1864', '1872', '1880',
                                 '1888', '1896', '1904', '1912', '1920', '1928', '1936', '1944', '1952', '1960', '1968', '1976',
                                 '1984', '1992', '2000', '2008', '2016', '2024', '2032', '2040'],
                       'usage': ['MAC', 'MAC_VERIFY', 'DERIVE']}}


class KeysListAll(Record):
    """Keys -> List All

    GET /api/v1/keys

    Return a list of keys."""
    # todo: add validator(s)

    partition_id: Optional[str]
    limit: Optional[int]
    skip: Optional[int]
    id: Optional[str]
    type: Optional[str]
    export_type: Optional[str]
    trusted: Optional[bool]
    groups: Optional[List[str]]
    state: Optional[str]
    is_enabled: Optional[bool]
    show_destroyed: Optional[bool]
    detailed: Optional[bool] = True

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/keys'

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


class OfflineKeyParams(Record):
    """Offline Key Parameters"""
    backup: Optional[str]
    paillier_key: str
    paillier_keys: List[str]


class KeyFormat(Record):
    """Key Format"""
    type: str
    size: Optional[str]
    curve: Optional[str]  # only required if type is curve
    offline_key_params: Optional[OfflineKeyParams]


class KeyStoreProperties(Record):
    """Key Store Properties"""
    key_store_name: str
    key_store_object_id: Optional[str]
    byok: Optional[bool]


class KeyProperties(Record):
    """Key Properties"""
    description: Optional[str]
    supported_operations: Optional[List[str]]
    trusted: Optional[bool]
    key_rotation_interval: Optional[int]  # 0-1095
    export_type: Optional[str]
    groups: Optional[List[str]]


class NewKey(Record):
    """New Key"""
    key_id: str
    key_id_encoding: Optional[str]  # todo: add validation
    key_properties: Optional[KeyProperties]
    key_store_properties: Optional[KeyStoreProperties]
    activate: Optional[bool]
    activation_date: Optional[int]  # int64
    deactivation_date: Optional[int]
    key_format: KeyFormat


class KeyGenerateOne(Record):
    """Key -> Generate

    PUT /api/v1/keys/generate

    Generate a new key."""
    user_id: str
    partition_id: Optional[str]
    body: NewKey

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return '/keys/generate'

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


class KeyDeleteOne(Record):
    """Key -> Delete

    DELETE /api/v1/keys/{keyId}

    Delete the specified key."""

    partition_id: Optional[str]
    key_id: str
    full_delete: Optional[bool]

    @property
    def endpoint(self) -> str:
        """Endpoint

        The suffix end of the URI

        Returns:
            (str)"""
        return f'/keys/{self.key_id}'

    @property
    def method(self) -> Optional[str]:
        """Method

        The HTTP verb to be used
         - Must be a valid HTTP verb as listed above in METHODS

        Returns:
            (str)"""
        return 'DELETE'

    @property
    def parameters(self) -> Optional[str]:
        """URL Parameters

        If you need to pass parameters in the URL

        Returns:
            (dict)"""
        return self.json(exclude={'key_id'})

    @property
    def headers(self) -> Optional[dict]:
        """Headers

        If you need to pass non-default headers

        Returns:
            (dict)"""
        return {'Accept': '*/*'}
