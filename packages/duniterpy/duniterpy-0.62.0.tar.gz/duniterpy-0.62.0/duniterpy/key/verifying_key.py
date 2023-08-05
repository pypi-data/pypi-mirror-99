"""
Copyright  2014-2021 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import base64
from typing import Any

import libnacl.sign
import libnacl.encode

from duniterpy.documents import Document
from duniterpy.documents.block import Block
from .base58 import Base58Encoder


class VerifyingKey(libnacl.sign.Verifier):
    """
    Class to verify documents
    """

    def __init__(self, pubkey: str) -> None:
        """
        Creates a Verify class from base58 pubkey
        :param pubkey:
        """
        key = libnacl.encode.hex_encode(Base58Encoder.decode(pubkey))
        super().__init__(key)

    def verify_document(self, document: Document) -> bool:
        """
        Check specified document
        :param duniterpy.documents.Document document:
        :return:
        """
        signature = base64.b64decode(document.signatures[0])
        if isinstance(document, Block):
            content_to_verify = "InnerHash: {0}\nNonce: {1}\n".format(
                document.inner_hash, document.nonce
            )
        else:
            content_to_verify = document.raw()
        prepended = signature + bytes(content_to_verify, "ascii")

        try:
            self.verify(prepended)
            return True
        except ValueError:
            return False

    def verify_ws2p_head(self, head: Any) -> bool:
        """
        Check specified document
        :param Any head:
        :return:
        """
        signature = base64.b64decode(head.signature)
        inline = head.inline()
        prepended = signature + bytes(inline, "ascii")

        try:
            self.verify(prepended)
            return True
        except ValueError:
            return False

    def get_verified_data(self, data: bytes) -> bytes:
        """
        Check specified signed data signature and return data

        Raise exception if signature is not valid

        :param data: Data + signature
        :return:
        """
        return self.verify(data)
