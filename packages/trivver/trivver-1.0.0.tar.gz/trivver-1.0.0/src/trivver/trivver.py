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
"""Implement the version comparison function."""

import functools
import re

from typing import List, Optional


RE_COMPONENT = re.compile(
    r""" ^
    (?P<num> [0-9]+ )? (?P<rest> .+ )?
$ """,
    re.X,
)


def cmp_strings(first: Optional[str], second: Optional[str]) -> int:
    """Compare two strings, possibly undefined."""
    if first is not None:
        if second is not None:
            if first == second:
                return 0
            if first > second:
                return 1
            return -1

        return 1

    if second is not None:
        return -1

    return 0


def cmp_components(first: str, second: str) -> int:
    """Compare a single pair of version components.

    - alpha4 < beta
    - alpha4 < 1
    - 1 < 1sp2
    - 1 < 2"""
    a_m = RE_COMPONENT.match(first)
    assert a_m
    a_num = a_m.group("num")
    a_rest = a_m.group("rest")

    b_m = RE_COMPONENT.match(second)
    assert b_m
    b_num = b_m.group("num")
    b_rest = b_m.group("rest")

    if a_num is not None:
        if b_num is not None:
            if a_num != b_num:
                return int(a_num) - int(b_num)
            return cmp_strings(a_rest, b_rest)

        return 1

    if b_num is not None:
        return -1

    return cmp_strings(a_rest, b_rest)


def cmp_examine_extra(a_first: str) -> int:
    """Does the version component start with a digit?

    In other words, is it an alpha/beta version or not?"""
    a_m = RE_COMPONENT.match(a_first)
    assert a_m
    if a_m.group("num") is not None:
        return 1
    return -1


def cmp_extra(first: List[str], second: List[str]) -> int:
    """Check for alpha versions in the longer list's additional components.

    Does one of the lists:
    - have more components than the other, and
    - the first extra component starts with a digit, not a letter?
    (if it starts with a letter, it's an alpha/beta/pre-release version)"""
    a_len = len(first)
    b_len = len(second)
    if a_len == b_len:
        return 0

    if a_len > b_len:
        a_first = first[b_len]
        return cmp_examine_extra(a_first)

    b_first = second[a_len]
    return -cmp_examine_extra(b_first)


def cmp_dot_components(first: str, second: str) -> int:
    """Split versions number no dots, compare them component by component."""
    a_dot = first.split(".")
    b_dot = second.split(".")
    for a_comp, b_comp in zip(a_dot, b_dot):
        res = cmp_components(a_comp, b_comp)
        if res != 0:
            return res

    # Does one of them have more dot-delimited components than the other?
    return cmp_extra(a_dot, b_dot)


# Split a version number on dashes, compare them component by component
def compare(first: str, second: str) -> int:
    """Compare two full versions strings."""
    a_dash = first.split("-")
    b_dash = second.split("-")
    for a_comp, b_comp in zip(a_dash, b_dash):
        res = cmp_dot_components(a_comp, b_comp)
        if res != 0:
            return res

    # Does one of them have more dash-delimited components than the other?
    # (don't check for beta versions in this case)
    return len(a_dash) - len(b_dash)


key_compare = functools.cmp_to_key(compare)  # pylint: disable=invalid-name

__all__ = ("compare", "key_compare")
