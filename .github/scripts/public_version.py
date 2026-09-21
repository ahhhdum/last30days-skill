#!/usr/bin/env python3
"""Print the PEP 440 public version, treating a local segment as insignificant.

Used by .github/workflows/changelog-guard.yml to tell a local-version restamp
apart from a real version bump, keeping version parsing out of the YAML
``run: |`` block (column-0 Python inside that block breaks Actions).

A PEP 440 local segment carries no release meaning: ``3.18.4`` and
``3.18.4+adam.1`` are the same release, so a fork stamping or restamping its
local marker is not cutting a release. Everything else is: a change to the
release numbers, epoch, pre-release, post-release or dev segment all change the
printed public version and so are still reported as bumps.

One legacy shape needs normalizing. A fork that stamped ``3.18.4-adam.1`` wrote
an invalid PEP 440 version, since ``adam.1`` is not a pre/post/dev marker and
``-`` is not the local separator. Such a trailing ``-<label>`` is treated as a
local segment so that correcting the separator is not a bump. Labels that *are*
recognized non-normalized markers are left alone: ``3.18.4-1`` stays a
post-release and ``3.18.4-rc1`` stays a pre-release, so both still count.

Usage:
  python3 .github/scripts/public_version.py "3.18.4+adam.1"   # -> 3.18.4
"""

from __future__ import annotations

import re
import sys

# PEP 440 public version, accepting the non-normalized separators the spec
# permits. Anchored at both ends so a partial match cannot pass.
_PUBLIC = re.compile(
    r"""
    ^
    v?
    (?:[0-9]+!)?                                             # epoch
    [0-9]+(?:\.[0-9]+)*                                      # release
    (?:[-_.]?(?:a|b|c|rc|alpha|beta|pre|preview)[-_.]?[0-9]*)?   # pre
    (?:(?:-[0-9]+)|(?:[-_.]?(?:post|rev|r)[-_.]?[0-9]*))?    # post
    (?:[-_.]?dev[-_.]?[0-9]*)?                               # dev
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)


def public_version(raw: str) -> str:
    """Return the public-version part of ``raw``, or ``raw`` if unparseable.

    Returning the input unchanged when nothing parses is deliberate: the caller
    compares two of these for equality, so an unrecognized string compares as
    itself and is reported as a bump rather than silently exempted.
    """
    candidate = raw.split("+", 1)[0].strip()
    if _PUBLIC.match(candidate):
        return candidate
    # Not a valid public version alone — it may carry a legacy '-<label>' local
    # segment. Split at the first '-' and accept only if the head is valid.
    head, sep, _tail = candidate.partition("-")
    if sep and _PUBLIC.match(head):
        return head
    return candidate


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: public_version.py <version>")
    print(public_version(sys.argv[1]))
