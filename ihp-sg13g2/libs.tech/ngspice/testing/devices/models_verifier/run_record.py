# =========================================================================================
# Copyright 2025 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================================

"""
Which simulator toolchain produced a run, written to `<output_dir>/toolchain.txt`.

The Makefile selects a toolchain with `TOOLCHAIN=<id>` (see tools/toolchain.py) and exports:
    TOOLCHAIN     e.g. "ng47-ovr-b4517ad" = ngspice-47 + OpenVAF-Reloaded commit b4517ad
    NGSPICE_BIN   the ngspice executable of that toolchain
    OSDI_DIR      the Verilog-A models compiled with that OpenVAF build
    RESULTS_ROOT  e.g. "models_results/ng47-ovr-b4517ad"

Exceptions (waivers/waiver.py) are stored per toolchain. A device whose models are built into
ngspice (no `osdi_path` in its config, e.g. the VBIC bipolar models) does not depend on
OpenVAF, so its exceptions use only the ngspice part of the ID ("ng47").

toolchain.txt is a plain "key: value" file, read back by the waiver generator.
"""

from __future__ import annotations

import hashlib
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

UNREGISTERED = "unregistered"


def toolchain_id() -> str:
    """The toolchain of this run ($TOOLCHAIN, set by the Makefile)."""
    return os.environ.get("TOOLCHAIN") or UNREGISTERED


def exception_toolchain(toolchain: str, uses_osdi: bool) -> str:
    """Toolchain key of the exceptions: the full ID with OSDI models, else only "ng<ver>"."""
    return toolchain if uses_osdi else toolchain.split("-")[0]


def toolchain_mismatch(toolchain: str, ngspice_version_text: str, osdi_path: Optional[str]) -> Optional[str]:
    """
    Why the binaries of a run do not belong to its toolchain ID, or None when they do: the
    ngspice banner must name the ID's version ("ng47" -> "ngspice-47") and an OSDI model must
    come from the ID's OpenVAF folder ("ovr-b4517ad"). An unregistered run is not checked.
    """
    if toolchain == UNREGISTERED:
        return None
    ng, _, ovr = toolchain.partition("-")
    if f"ngspice-{ng.removeprefix('ng')}" not in ngspice_version_text:
        return f"toolchain {toolchain} but the ngspice binary reports '{ngspice_version_text}'"
    if osdi_path and ovr and ovr not in str(osdi_path):
        return f"toolchain {toolchain} but the OSDI model is {osdi_path}"
    return None


def ngspice_version(binary: str) -> str:
    """First line of `ngspice -v` that names the version, e.g. "ngspice-47 : Circuit level ..."."""
    try:
        out = subprocess.run([binary, "-v"], capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError) as e:
        return f"unavailable ({e})"
    lines = [ln.strip("* ").strip() for ln in out.splitlines() if "ngspice-" in ln]
    return lines[0] if lines else "unknown"


def sha256_of(path: Path) -> str:
    """Short sha256 of a file (16 hex digits), or "missing"."""
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
    except OSError:
        return "missing"


def write_toolchain_txt(output_dir: Path, device_name: str, toolchain: str, exception_key: str,
                        ngspice_bin: str, ngspice_version_text: str, osdi_files: Iterable[Path] = ()) -> Path:
    """Write `<output_dir>/toolchain.txt` and return its path."""
    lines = [
        f"toolchain: {toolchain}",
        f"exception_key: {exception_key}",
        f"device: {device_name}",
        f"ngspice_bin: {ngspice_bin}",
        f"ngspice_version: {ngspice_version_text}",
    ]
    lines += [f"osdi: {p} sha256={sha256_of(p)}" for p in osdi_files]
    lines += [
        f"python: {platform.python_version()}",
        f"date_utc: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
    ]
    path = Path(output_dir) / "toolchain.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")
    return path


def read_toolchain_txt(results_dir: Path) -> Dict[str, str]:
    """Read `<results_dir>/toolchain.txt` into a dict (repeated keys such as "osdi" keep the last)."""
    record: Dict[str, str] = {}
    for line in (Path(results_dir) / "toolchain.txt").read_text().splitlines():
        key, _, value = line.partition(":")
        record[key.strip()] = value.strip()
    return record


def osdi_files_in(directory: Optional[str]) -> List[Path]:
    """The *.osdi files of a directory (sorted), for the run record."""
    if not directory or not Path(directory).is_dir():
        return []
    return sorted(Path(directory).glob("*.osdi"))
