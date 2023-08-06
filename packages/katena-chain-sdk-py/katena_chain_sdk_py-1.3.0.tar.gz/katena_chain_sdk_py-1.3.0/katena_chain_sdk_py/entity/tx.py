"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from marshmallow import fields
from katena_chain_sdk_py.serializer.bytes_field import BytesField
from katena_chain_sdk_py.entity.tx_data import TxDataSchema
from katena_chain_sdk_py.serializer.base_schema import BaseSchema
from katena_chain_sdk_py.serializer.utc_datetime_field import UTCDatetimeField
from datetime import datetime
from katena_chain_sdk_py.entity.tx_data_interface import TxData


class Tx:
    # Tx wraps a tx data with its signature information and a nonce time to avoid replay attacks.

    def __init__(self, nonce_time: datetime, data: TxData, signer_fqid: str, signature: bytes):
        self.nonce_time = nonce_time
        self.data = data
        self.signer_fqid = signer_fqid
        self.signature = signature

    def get_nonce_time(self) -> datetime:
        return self.nonce_time

    def get_data(self) -> TxData:
        return self.data

    def get_signer_fqid(self) -> str:
        return self.signer_fqid

    def get_signature(self) -> bytes:
        return self.signature


class TxSchema(BaseSchema):
    # TxSchema allows to serialize and deserialize Tx.

    __model__ = Tx
    signer_fqid = fields.Str()
    signature = BytesField()
    data = fields.Nested(TxDataSchema)
    nonce_time = UTCDatetimeField()
