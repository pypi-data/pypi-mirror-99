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

import re
import attr

from ..block_uid import BlockUID
from ..document import MalformedDocumentError
from ...constants import (
    WS2P_PUBLIC_PREFIX_REGEX,
    WS2P_PRIVATE_PREFIX_REGEX,
    WS2P_HEAD_REGEX,
    PUBKEY_REGEX,
    SIGNATURE_REGEX,
    WS2PID_REGEX,
    BLOCK_UID_REGEX,
)


@attr.s()
class API:
    private = attr.ib(type=str)
    public = attr.ib(type=str)

    re_inline = re.compile(
        "WS2P({ws2p_private})?({ws2p_public})?".format(
            ws2p_private=WS2P_PRIVATE_PREFIX_REGEX, ws2p_public=WS2P_PUBLIC_PREFIX_REGEX
        )
    )

    @classmethod
    def from_inline(cls, inline: str):
        data = API.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("WS2P API Document")
        private = "" if data.group(1) is None else data.group(1)
        public = "" if data.group(2) is None else data.group(2)
        return cls(private, public)

    def __str__(self) -> str:
        return "WS2P" + self.private + self.public


@attr.s()
class Head:
    version = attr.ib(type=int)

    re_inline = re.compile(WS2P_HEAD_REGEX)

    @classmethod
    def from_inline(cls, inline: str, signature: str):
        try:
            data = Head.re_inline.match(inline)
            if data is None:
                raise MalformedDocumentError("Head")
            head = data.group(0).split(":")
            version = int(head[1]) if len(head) == 2 else 0
            return cls(version)
        except AttributeError:
            raise MalformedDocumentError("Head") from AttributeError

    def __str__(self) -> str:
        return "HEAD" if self.version == 0 else "HEAD:{}".format(str(self.version))


@attr.s()
class HeadV0(Head):
    signature = attr.ib(type=str)
    api = attr.ib(type=API)
    head = attr.ib(type=Head)
    pubkey = attr.ib(type=str)
    blockstamp = attr.ib(type=BlockUID)

    re_inline = re.compile(
        "^(WS2P(?:{ws2p_private})?(?:{ws2p_public})?):({head}):({pubkey}):({blockstamp})(?::)?(.*)".format(
            ws2p_private=WS2P_PRIVATE_PREFIX_REGEX,
            ws2p_public=WS2P_PUBLIC_PREFIX_REGEX,
            head=WS2P_HEAD_REGEX,
            pubkey=PUBKEY_REGEX,
            blockstamp=BLOCK_UID_REGEX,
        )
    )

    re_signature = re.compile(SIGNATURE_REGEX)

    @classmethod
    def from_inline(cls, inline: str, signature: str):
        try:
            data = HeadV0.re_inline.match(inline)
            if data is None:
                raise MalformedDocumentError("HeadV0")
            api = API.from_inline(data.group(1))
            head = Head.from_inline(data.group(2), "")
            pubkey = data.group(3)
            blockstamp = BlockUID.from_str(data.group(4))
            offload = data.group(5)
            return cls(head.version, signature, api, head, pubkey, blockstamp), offload
        except AttributeError:
            raise MalformedDocumentError("HeadV0") from AttributeError

    def inline(self) -> str:
        values = (
            str(v)
            for v in attr.astuple(
                self,
                recurse=False,
                filter=attr.filters.exclude(
                    attr.fields(HeadV0).version,
                    attr.fields(HeadV0).signature,
                    attr.fields(HeadV0).api,
                ),
            )
        )
        return "{0}:{1}".format(str(self.api), ":".join(values))


@attr.s()
class HeadV1(HeadV0):
    ws2pid = attr.ib(type=str)
    software = attr.ib(type=str)
    software_version = attr.ib(type=str)
    pow_prefix = attr.ib(type=int)

    re_inline = re.compile(
        "({ws2pid}):({software}):({software_version}):({pow_prefix})(?::)?(.*)".format(
            ws2pid=WS2PID_REGEX,
            software="[A-Za-z-_]+",
            software_version="[0-9]+[.][0-9]+[.][0-9]+[-\\w]*",
            pow_prefix="[0-9]+",
        )
    )

    @classmethod
    def from_inline(cls, inline: str, signature: str):
        try:
            v0, offload = HeadV0.from_inline(inline, signature)
            data = HeadV1.re_inline.match(offload)
            if data is None:
                raise MalformedDocumentError("HeadV1")
            ws2pid = data.group(1)
            software = data.group(2)
            software_version = data.group(3)
            pow_prefix = int(data.group(4))
            offload = data.group(5)
            return (
                cls(
                    v0.version,
                    v0.signature,
                    v0.api,
                    v0.head,
                    v0.pubkey,
                    v0.blockstamp,
                    ws2pid,
                    software,
                    software_version,
                    pow_prefix,
                ),
                offload,
            )
        except AttributeError:
            raise MalformedDocumentError("HeadV1") from AttributeError


@attr.s
class HeadV2(HeadV1):
    free_member_room = attr.ib(type=int)
    free_mirror_room = attr.ib(type=int)

    re_inline = re.compile(
        "({free_member_room}):({free_mirror_room})(?::)?(.*)".format(
            free_member_room="[0-9]+", free_mirror_room="[0-9]+"
        )
    )

    @classmethod
    def from_inline(cls, inline: str, signature: str):
        try:
            v1, offload = HeadV1.from_inline(inline, signature)
            data = HeadV2.re_inline.match(offload)
            if data is None:
                raise MalformedDocumentError("HeadV2")
            free_member_room = int(data.group(1))
            free_mirror_room = int(data.group(2))
            return (
                cls(
                    v1.version,
                    v1.signature,
                    v1.api,
                    v1.head,
                    v1.pubkey,
                    v1.blockstamp,
                    v1.ws2pid,
                    v1.software,
                    v1.software_version,
                    v1.pow_prefix,
                    free_member_room,
                    free_mirror_room,
                ),
                "",
            )
        except AttributeError:
            raise MalformedDocumentError("HeadV2") from AttributeError
