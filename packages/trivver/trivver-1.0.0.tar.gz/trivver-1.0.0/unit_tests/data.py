#
# Copyright (c) 2020, 2021  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
"""Definitions and data for the trivver unit tests."""

from typing import NamedTuple


class VersionSet(NamedTuple):
    """A basic test case for comparing versions."""

    left: str
    right: str
    expected: int


VERSIONS = [
    VersionSet(left="1.0", right="2.0", expected=-1),
    VersionSet(left="1.0", right="1.0.1", expected=-1),
    VersionSet(left="1.0", right="1.0a", expected=-1),
    VersionSet(left="1.0", right="1.0", expected=0),
    VersionSet(left="1.0a", right="1.0a", expected=0),
    VersionSet(left="0.1.0.b", right="0.1.0", expected=-1),
    VersionSet(
        left="3.10.0-1062.1.1.el7.x86_64",
        right="3.10.0-983.13.1.el7.x86_64",
        expected=1,
    ),
    VersionSet(
        left="3.10.0-1062.1.1.el7.x86_64",
        right="3.10.0-1062.1.1.el6.x86_64",
        expected=1,
    ),
]

EXPECTED_TO_STR = {
    -1: "<",
    0: "=",
    1: ">",
}

EXPECTED_TO_REL = {
    -1: {
        False: ["=", ">", ">=", "eq", "gt", "ge"],
        True: ["<", "<=", "!=", "lt", "le", "ne"],
    },
    0: {
        False: ["<", ">", "!=", "lt", "gt", "ne"],
        True: ["=", "<=", ">=", "eq", "le", "ge"],
    },
    1: {
        False: ["<", "=", "<=", "lt", "eq", "le"],
        True: [">", ">=", "!=", "gt", "ge", "ne"],
    },
}

UNSORTED = [
    "3.10.0-1062.1.1.el7.x86_64",
    "1.0a",
    "0.1.0.b",
    "1.0",
    "3.10.0-983.13.1.el7.x86_64",
    "0.1.0",
    "1.0.1",
    "2.0",
    "3.10.0-1062.1.1.el6.x86_64",
]
SORTED = [
    "0.1.0.b",
    "0.1.0",
    "1.0",
    "1.0.1",
    "1.0a",
    "2.0",
    "3.10.0-983.13.1.el7.x86_64",
    "3.10.0-1062.1.1.el6.x86_64",
    "3.10.0-1062.1.1.el7.x86_64",
]
