# Compare package versions in all their varied glory.

## Description

This module provides the `compare()` function which compares two
version strings and returns a negative value, zero, or a positive
value depending on whether the first string represents a version
number lower than, equal to, or higher than the second one, and
the `key_compare()` function which may be used as a key for e.g.
`sorted()`.

This module does not strive for completeness in the formats of
version strings that it supports. Some version strings sorted by
its rules are:

- 0.1.0
- 0.2.alpha
- 0.2
- 0.2.1
- 0.2a
- 0.2a.1
- 0.2p3
- 1.0.beta
- 1.0.beta.2
- 1.0

## Contact

This module is [developed in a Gitlab repository][gitlab].
The author is [Peter Pentchev][roam].

## Version history

### 1.0.0

- reformat the source code using black 20
- drop Python 2.x compatibility:
  - use types and modules from the Python 3 standard library
  - use type annotations, not type hints
  - subclass NamedTuple, using Python 3.6 variable type annotations
- switch to a declarative setup.cfg file
- install the module into the `unit_tests` tox environment
- add a PEP 517 buildsystem definition to the pyproject.toml file
- add the py.typed marker
- push the source down into a src/ subdirectory
- add a command-line utility exposing some of the functionality
- add a shell tool for testing the command-line utility
- add a manual page generated from an scdoc source file

### 0.1.0

- first public release

[gitlab]: https://gitlab.com/ppentchev/python-trivver
[git]: https://gitlab.com/ppentchev/python-trivver.git
[roam]: mailto:roam@ringlet.net
