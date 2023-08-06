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
"""Command-line version comparison tool."""

import argparse
import sys

from typing import Callable, Dict, NamedTuple, Tuple

from . import trivver


V_HANDLERS: Dict[str, Callable[[int], bool]] = {
    "<": lambda res: res < 0,
    "=": lambda res: res == 0,
    ">": lambda res: res > 0,
    "<=": lambda res: res <= 0,
    ">=": lambda res: res >= 0,
    "!=": lambda res: res != 0,
}
V_ALIASES = {
    "lt": "<",
    "eq": "=",
    "gt": ">",
    "le": "<=",
    "ge": ">=",
    "ne": "!=",
}
V_CHOICES = sorted(V_HANDLERS) + sorted(V_ALIASES)


class Config(NamedTuple):
    """Runtime configuration for the version comparison tool."""

    left: str
    right: str
    rel: str


def cmd_compare(cfg: Config) -> None:
    """Compare the two versions specified."""
    res = trivver.compare(cfg.left, cfg.right)
    if res < 0:
        print("<")
    elif res > 0:
        print(">")
    else:
        print("=")


def cmd_verify(cfg: Config) -> None:
    """Verify that a relation holds true for the specified versions."""

    rel = V_ALIASES.get(cfg.rel, cfg.rel)
    handler = V_HANDLERS.get(rel)
    if handler is None:
        sys.exit(
            (
                "Invalid relation '{rel}' specified, "
                "must be one of {choices}"
            ).format(rel=cfg.rel, choices=" ".join(V_CHOICES))
        )

    res = trivver.compare(cfg.left, cfg.right)
    sys.exit(0 if handler(res) else 1)


def cmd_sort(_cfg: Config) -> None:
    """Sort a list of versions supplied on the standard input stream."""
    lines = [line.strip() for line in sys.stdin.readlines()]
    print("\n".join(sorted(lines, key=trivver.key_compare)))


def parse_args() -> Tuple[Config, Callable[[Config], None]]:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(prog="trivver")

    subp = parser.add_subparsers(help="trivver subcommands")

    cmd_p = subp.add_parser("compare", help="compare the specified versions")
    cmd_p.add_argument("left", type=str, help="the first version string")
    cmd_p.add_argument("right", type=str, help="the second version string")
    cmd_p.set_defaults(func=cmd_compare)

    cmd_p = subp.add_parser("verify", help="verify that a relation holds true")
    cmd_p.add_argument("left", type=str, help="the first version string")
    cmd_p.add_argument(
        "rel", type=str, choices=V_CHOICES, help="the relation to verify"
    )
    cmd_p.add_argument("right", type=str, help="the second version string")
    cmd_p.set_defaults(func=cmd_verify)

    cmd_p = subp.add_parser(
        "sort", help="sort a list of versions from stdin to stdout"
    )
    cmd_p.set_defaults(func=cmd_sort)

    args = parser.parse_args()

    func = getattr(args, "func", None)
    if func is None:
        sys.exit("No command specified")

    return (
        Config(
            left=getattr(args, "left", ""),
            right=getattr(args, "right", ""),
            rel=getattr(args, "rel", ""),
        ),
        func,
    )


def main() -> None:
    """Parse the command-line arguments, perform the required actions."""
    cfg, func = parse_args()
    func(cfg)


if __name__ == "__main__":
    main()
