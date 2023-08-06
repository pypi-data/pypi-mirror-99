"""Utils imported from motionEye."""

# Copyright (c) 2013 Calin Crisan
# This file is snippet from motionEye.
#
# motionEye is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import hashlib
import re
from urllib.parse import (
    urlunsplit,
    urlsplit,
    parse_qsl,
    quote,
)

_SIGNATURE_REGEX = re.compile(r'[^a-zA-Z0-9/?_.=&{}\[\]":, -]')


def compute_signature_from_password(
    method: str,
    path: str,
    body: str | None,
    password: str | None = None,
) -> str:
    """Compute a request signature from a password."""
    key = hashlib.sha1((password or "").encode("UTF-8")).hexdigest()
    return compute_signature(method, path, body, key)


# ================================================================
# Below is a slightly adjusted version of the compute_signature function
# found here: https://github.com/ccrisan/motioneye/blob/dev/motioneye/utils.py
# ================================================================


def compute_signature(method: str, path: str, body: str | None, key: str) -> str:
    """Compute a request signature from a key."""
    parts: list[str] = list(urlsplit(path))
    query: list[tuple[str, str]] = [
        q for q in parse_qsl(parts[3], keep_blank_values=True) if (q[0] != "_signature")
    ]
    query.sort(key=lambda q: q[0])
    # "safe" characters here are set to match the encodeURIComponent JavaScript counterpart
    query_quoted = [(n, quote(v, safe="!'()*~")) for (n, v) in query]
    query_string = "&".join([(q[0] + "=" + q[1]) for q in query_quoted])
    parts[0] = parts[1] = ""
    parts[3] = query_string
    path = urlunsplit(parts)
    path = _SIGNATURE_REGEX.sub("-", path)
    key = _SIGNATURE_REGEX.sub("-", key)

    # File attachment.
    body = None if body and body.startswith("---") else body
    body = body and _SIGNATURE_REGEX.sub("-", body)

    return (
        hashlib.sha1(
            (
                "%s:%s:%s:%s"
                % (
                    method,
                    path,
                    body or "",
                    key,
                )
            ).encode("UTF-8")
        )
        .hexdigest()
        .lower()
    )
