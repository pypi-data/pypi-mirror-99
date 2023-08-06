#
# Copyright (c) 2021  Peter Pentchev <roam@ringlet.net>
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
"""Test the command-line invocation routines."""

import sys
import unittest

from typing import List

import ddt  # type: ignore
import mock

from trivver import __main__ as tmain

from . import data


@ddt.ddt
class TestMain(unittest.TestCase):
    """Test the functions implementing the commands."""

    # pylint: disable=no-self-use

    @ddt.data(*data.VERSIONS)
    def test_compare(self, case: data.VersionSet) -> None:
        """Test the 'trivver compare left right' subcommand."""
        res: List[str] = []
        with mock.patch("builtins.print", new=res.append):
            tmain.cmd_compare(
                tmain.Config(left=case.left, right=case.right, rel="")
            )

        assert res == [data.EXPECTED_TO_STR[case.expected]]

    @ddt.data(*data.VERSIONS)
    def test_main_compare(self, case: data.VersionSet) -> None:
        """Test the 'trivver compare left right' invocation."""
        res: List[str] = []
        with mock.patch.object(
            sys, "argv", new=["trivver", "compare", case.left, case.right]
        ), mock.patch("builtins.print", new=res.append):
            tmain.main()

        assert res == [data.EXPECTED_TO_STR[case.expected]]

    @ddt.data(*data.VERSIONS)
    def test_verify(self, case: data.VersionSet) -> None:
        """Test the 'trivver verify left op right' subcommand."""
        rels = data.EXPECTED_TO_REL[case.expected]
        res: List[int] = []

        assert len(rels[False]) == 6
        for rel in rels[False]:
            with mock.patch("sys.exit", new=res.append):
                tmain.cmd_verify(
                    tmain.Config(left=case.left, right=case.right, rel=rel)
                )

        assert len(rels[True]) == 6
        for rel in rels[True]:
            with mock.patch("sys.exit", new=res.append):
                tmain.cmd_verify(
                    tmain.Config(left=case.left, right=case.right, rel=rel)
                )

        assert res == ([1] * 6) + ([0] * 6)

    @ddt.data(*data.VERSIONS)
    def test_main_verify(self, case: data.VersionSet) -> None:
        """Test the 'trivver verify left op right' subcommand."""
        rels = data.EXPECTED_TO_REL[case.expected]
        res: List[int] = []

        assert len(rels[False]) == 6
        for rel in rels[False]:
            with mock.patch.object(
                sys,
                "argv",
                new=["trivver", "verify", case.left, rel, case.right],
            ), mock.patch("sys.exit", new=res.append):
                tmain.main()

        assert len(rels[True]) == 6
        for rel in rels[True]:
            with mock.patch.object(
                sys,
                "argv",
                new=["trivver", "verify", case.left, rel, case.right],
            ), mock.patch("sys.exit", new=res.append):
                tmain.main()

        assert res == ([1] * 6) + ([0] * 6)

    def test_sort(self) -> None:
        """Test the 'trivver sort' functionality."""
        res: List[str] = []
        with mock.patch.object(
            sys.stdin,
            "readlines",
            new=lambda: [item + "\n" for item in data.UNSORTED],
        ), mock.patch("builtins.print", new=res.append):
            tmain.cmd_sort(tmain.Config(left="", right="", rel=""))

        assert res == ["\n".join(data.SORTED)]

    def test_main_sort(self) -> None:
        """Test the 'trivver sort' functionality."""
        res: List[str] = []
        with mock.patch.object(
            sys, "argv", new=["trivver", "sort"]
        ), mock.patch.object(
            sys.stdin,
            "readlines",
            new=lambda: [item + "\n" for item in data.UNSORTED],
        ), mock.patch(
            "builtins.print", new=res.append
        ):
            tmain.main()

        assert res == ["\n".join(data.SORTED)]
