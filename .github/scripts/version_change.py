#!/usr/bin/env python3
"""Classify a manifest version change as a release bump or a local-only change.

Used by .github/workflows/changelog-guard.yml, keeping version parsing out of
the YAML ``run: |`` block (column-0 Python inside that block breaks Actions).

Prints ``local`` when the change is confined to the PEP 440 local-version
segment and ``bump`` otherwise. A local segment carries no release meaning, so
``3.18.4`` and ``3.18.4+adam.1`` are the same release and a fork stamping or
restamping its local marker is not cutting one. Any change to the release
numbers, epoch, pre-release, post-release or dev segment is a bump.

One legacy shape needs care. A fork that stamped ``3.18.4-adam.1`` wrote an
invalid PEP 440 version: ``-`` is not the local separator and ``adam.1`` is not
a pre/post/dev marker. Correcting it to ``3.18.4+adam.1`` must not read as a
bump. The exemption is deliberately pairwise rather than a per-string
normalization, because ``adam.1`` and ``nightly.1`` are grammatically identical
local labels and no rule can tell a fork marker from a release qualifier by
looking at one string. What identifies the real legacy correction is that *only
the separator moved*: the public version and the label are the same on both
sides. So ``3.18.4-adam.1`` -> ``3.18.4+adam.1`` is local, while
``3.18.4-nightly.1`` -> ``3.18.4`` is a bump, since the label on the left has no
counterpart on the right.

Usage:
  python3 .github/scripts/version_change.py <base_version> <head_version>
"""

from __future__ import annotations

import re
import sys

# PEP 440 public version, accepting the non-normalized separators the spec
# permits. Anchored at both ends so a partial match cannot pass. Every quantifier
# applies to a bounded, non-overlapping alternation, so there is no ambiguity for
# a backtracking engine to explore.
_PUBLIC = re.compile(
    r"""
    ^
    v?
    (?:[0-9]+!)?                                                  # epoch
    [0-9]+(?:\.[0-9]+)*                                           # release
    (?:[-_.]?(?:a|b|c|rc|alpha|beta|pre|preview)[-_.]?[0-9]*)?    # pre
    (?:(?:-[0-9]+)|(?:[-_.]?(?:post|rev|r)[-_.]?[0-9]*))?         # post
    (?:[-_.]?dev[-_.]?[0-9]*)?                                    # dev
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)

# PEP 440 local version label: dot-separated alphanumeric segments.
_LOCAL_LABEL = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9]+)*$", re.IGNORECASE)


def _split(version: str) -> tuple[str, str] | None:
    """Split a valid version into (public, local_label). None if unparseable.

    ``local_label`` is "" when there is no local segment.
    """
    public, sep, local = version.strip().partition("+")
    if not _PUBLIC.match(public):
        return None
    if sep and not _LOCAL_LABEL.match(local):
        return None
    return public, local


def _split_legacy(version: str, expected_label: str) -> tuple[str, str] | None:
    """Split an invalid ``<public>-<label>`` only when the label is expected.

    Requiring the label to equal the one on the other side of the comparison is
    what keeps this narrow: it recognizes a separator correction and nothing
    else. Returns None when the shape does not match or the label differs.
    """
    if not expected_label:
        return None
    public, sep, local = version.strip().partition("-")
    if not sep or local != expected_label:
        return None
    if not _PUBLIC.match(public):
        return None
    return public, local


def classify(base: str, head: str) -> str:
    """Return "local" if the change is local-segment-only, else "bump"."""
    if base.strip() == head.strip():
        return "local"

    parsed_base = _split(base)
    parsed_head = _split(head)

    # Recover the one legacy shape, using the other side's label as the anchor.
    if parsed_base is None and parsed_head is not None:
        parsed_base = _split_legacy(base, parsed_head[1])
    elif parsed_head is None and parsed_base is not None:
        parsed_head = _split_legacy(head, parsed_base[1])

    # Anything still unparseable compares as a bump: an unrecognized version is
    # reported rather than silently exempted.
    if parsed_base is None or parsed_head is None:
        return "bump"

    return "local" if parsed_base[0] == parsed_head[0] else "bump"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: version_change.py <base_version> <head_version>")
    print(classify(sys.argv[1], sys.argv[2]))
