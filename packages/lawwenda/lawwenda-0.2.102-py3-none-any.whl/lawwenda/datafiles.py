# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import os
import typing as t


LAWWENDADIR = os.path.abspath(f"{__file__}/..")

AUXDIR = os.path.abspath(f"{LAWWENDADIR}/_aux")

METADIR = os.path.abspath(f"{LAWWENDADIR}/../../_meta")
if not os.path.isdir(METADIR):
    METADIR = None


def find_data_file(fname: str, searchdirs: t.Optional[t.Iterable[str]] = None) -> t.Optional[str]:
    if searchdirs is None:
        searchdirs = [AUXDIR]
        if METADIR:
            searchdirs.append(f"{METADIR}/misc")
    for searchdir in searchdirs:
        ffname = f"{searchdir}/{fname}"
        if os.path.exists(ffname):
            return ffname
    return None
