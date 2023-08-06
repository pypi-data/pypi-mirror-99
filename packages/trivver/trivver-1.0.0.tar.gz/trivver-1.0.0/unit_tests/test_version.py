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
"""Test the version comparison routines."""

import unittest

import ddt  # type: ignore

import trivver

from . import data


def sign(value: int) -> int:
    """Return the sign of an integer."""
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


@ddt.ddt
class TestVersions(unittest.TestCase):
    """Test the version comparison routines."""

    # pylint: disable=no-self-use

    @ddt.data(*data.VERSIONS)
    @ddt.unpack
    def test_compare(self, left: str, right: str, expected: int) -> None:
        """Compare a single pair of versions."""
        assert sign(trivver.compare(left, right)) == sign(expected)
        assert sign(trivver.compare(right, left)) == sign(-expected)

    def test_sort(self) -> None:
        """Sort a list of versions."""
        assert sorted(data.UNSORTED, key=trivver.key_compare) == data.SORTED
