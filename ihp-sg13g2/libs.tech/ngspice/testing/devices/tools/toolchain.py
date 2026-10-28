#!/usr/bin/env python3
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
Simulator toolchains for the device tests: install them, register local builds, compile the
Verilog-A models, and print paths for the Makefile.

A toolchain ID names one ngspice release and one OpenVAF-Reloaded build, for example
    ng47-ovr-b4517ad    ngspice-47 + OpenVAF-Reloaded commit b4517ad
Versions, download URLs, checksums and build options are pinned in toolchain.lock, next to
the Makefile. Models built into ngspice (e.g. VBIC) only depend on the ngspice part.

Install layout under $TOOLCHAIN_ROOT (default ~/.local/toolchains):
    ngspice-<ver>/bin/ngspice        built from the pinned tarball, or a registered local build
    openvaf-r-<sha7>/bin/openvaf-r   built from the pinned commit, or a registered local build
The Verilog-A models of this repo, compiled per OpenVAF build, go to osdi_build/ovr-<sha7>/
next to the Makefile (not in git).

Commands (run from the folder of the Makefile):
    list                              the toolchain IDs of the lock file, and what is installed
    build ngspice <ver> [--jobs N]    download, check sha256, configure, make, make install
    build openvaf <sha7> [--offline]  download the source, check its commit, cargo build
    register ngspice <ver> <binary>   use an existing build instead (symlink + `ngspice -v`)
    register openvaf <sha7> <binary>
    osdi <toolchain>                  compile the Verilog-A models with that OpenVAF build
    path ngspice|openvaf|osdi-dir <toolchain>   print one path (used by the Makefile)
    ids <toolchain>                   print "ngspice=<ver>" and "openvaf=<sha7>" (CI step outputs)
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent          # the folder of the Makefile and toolchain.lock
LOCK = yaml.safe_load((HERE / "toolchain.lock").read_text())
ROOT = Path(os.environ.get("TOOLCHAIN_ROOT", Path.home() / ".local" / "toolchains"))


# -------------------------------------------------------------------------------------------
# Toolchain IDs and install paths
# -------------------------------------------------------------------------------------------

def split_id(toolchain: str) -> tuple[str, str]:
    """"ng47-ovr-b4517ad" -> ("47", "b4517ad"). Both parts must be pinned in the lock file."""
    try:
        ng, ovr = toolchain.split("-ovr-")
        version = ng.removeprefix("ng")
    except ValueError:
        sys.exit(f"bad toolchain ID '{toolchain}' (expected ng<ver>-ovr-<sha7>, e.g. ng47-ovr-b4517ad)")
    if version not in LOCK["ngspice"] or ovr not in LOCK["openvaf"]:
        sys.exit(f"toolchain '{toolchain}' is not pinned in {HERE / 'toolchain.lock'}")
    return version, ovr


def ngspice_path(version: str) -> Path:
    """Installed ngspice binary of a version."""
    return ROOT / f"ngspice-{version}" / "bin" / "ngspice"


def openvaf_path(sha7: str) -> Path:
    """Installed OpenVAF-Reloaded binary of a commit."""
    return ROOT / f"openvaf-r-{sha7}" / "bin" / "openvaf-r"


def osdi_dir(sha7: str) -> Path:
    """Folder of the Verilog-A models compiled with an OpenVAF build (next to the Makefile)."""
    return HERE / "osdi_build" / f"ovr-{sha7}"


# -------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------

def run(cmd: list, cwd: Path | None = None, env: dict | None = None) -> None:
    """Run a command, echo it, stop on failure."""
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], cwd=cwd, env=env, check=True)


def download(url: str, dest: Path) -> Path:
    """Download `url` to `dest`."""
    print(f"downloading {url}", flush=True)
    with urllib.request.urlopen(url, timeout=300) as response, open(dest, "wb") as out:
        shutil.copyfileobj(response, out)
    return dest


def sha256(path: Path) -> str:
    """sha256 of a file's content."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_info(prefix: Path, lines: list[str]) -> None:
    """Record how a tool was installed: <prefix>/TOOLCHAIN_INFO.txt."""
    prefix.mkdir(parents=True, exist_ok=True)
    (prefix / "TOOLCHAIN_INFO.txt").write_text("\n".join(lines) + "\n")


def version_output(cmd: list) -> str:
    """Combined stdout/stderr of a version command."""
    out = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    return (out.stdout + out.stderr).strip()


# -------------------------------------------------------------------------------------------
# Commands
# -------------------------------------------------------------------------------------------

def build_ngspice(version: str, jobs: int) -> None:
    """Download the pinned tarball, check its sha256, configure with the pinned flags, install."""
    pin = LOCK["ngspice"][version]
    prefix = ROOT / f"ngspice-{version}"
    with tempfile.TemporaryDirectory(prefix=f"ngspice-{version}-") as tmp:
        tarball = download(pin["url"], Path(tmp) / "ngspice.tar.gz")
        if sha256(tarball) != pin["sha256"]:
            sys.exit(f"sha256 mismatch for {pin['url']}")
        with tarfile.open(tarball) as tar:
            tar.extractall(tmp, filter="data")
        src = Path(tmp) / f"ngspice-{version}"
        build = src / "release"
        build.mkdir()
        run([src / "configure", f"--prefix={prefix}", *LOCK["ngspice_configure"]], cwd=build)
        run(["make", f"-j{jobs}"], cwd=build)
        run(["make", "install"], cwd=build)
    write_info(prefix, [f"built from {pin['url']} (sha256 {pin['sha256']})",
                        "configure: " + " ".join(LOCK["ngspice_configure"]),
                        version_output([ngspice_path(version), "-v"])])


def build_openvaf(sha7: str, offline: bool) -> None:
    """Download the pinned commit, check it, build `openvaf-r` with cargo, install it."""
    pin = LOCK["openvaf"][sha7]
    build = LOCK["openvaf_build"]
    prefix = ROOT / f"openvaf-r-{sha7}"
    src_root = ROOT / "src" / f"openvaf-r-{sha7}"
    shutil.rmtree(src_root, ignore_errors=True)
    src_root.mkdir(parents=True)
    tarball = download(pin["url"], src_root / "source.tar.gz")
    # GitHub writes the commit into the tar header; `git get-tar-commit-id` reads it back.
    tar_bytes = subprocess.run(["gzip", "-dc", str(tarball)], capture_output=True, check=True).stdout
    commit = subprocess.run(["git", "get-tar-commit-id"], input=tar_bytes, capture_output=True).stdout.decode().strip()
    if commit != pin["commit"]:
        sys.exit(f"{pin['url']} holds commit {commit}, expected {pin['commit']}")
    with tarfile.open(tarball) as tar:
        tar.extractall(src_root, filter="data")
    src = next(p for p in src_root.iterdir() if p.is_dir())

    env = dict(os.environ)
    env[build["llvm_prefix_env"]] = build["llvm_prefix"]
    env["PATH"] = f"{build['llvm_prefix']}/bin:{env['PATH']}"
    cmd = ["cargo", "build", "--release", "--locked", "--features", build["cargo_features"], "--bin", "openvaf-r"]
    run(cmd + (["--offline"] if offline else []), cwd=src, env=env)

    (prefix / "bin").mkdir(parents=True, exist_ok=True)
    shutil.copy2(src / "target" / "release" / "openvaf-r", openvaf_path(sha7))
    write_info(prefix, [f"built from {pin['url']} (commit {pin['commit']})",
                        "cargo: " + " ".join(cmd), f"{build['llvm_prefix_env']}={build['llvm_prefix']}",
                        version_output(["cargo", "--version"]), version_output(["rustc", "--version"])])
    shutil.rmtree(src_root, ignore_errors=True)


def register(tool: str, key: str, binary: Path) -> None:
    """Use an existing local build: symlink it into the install layout and record its version."""
    binary = binary.expanduser().resolve()
    if not os.access(binary, os.X_OK):
        sys.exit(f"{binary} is not an executable")
    if tool == "ngspice" and f"ngspice-{key}" not in version_output([binary, "-v"]):
        sys.exit(f"{binary} is not ngspice-{key}: {version_output([binary, '-v']).splitlines()[:3]}")
    target = ngspice_path(key) if tool == "ngspice" else openvaf_path(key)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.unlink(missing_ok=True)
    target.symlink_to(binary)
    version = version_output([target, "-v" if tool == "ngspice" else "--version"])
    write_info(target.parent.parent, [f"registered local build {binary}", version])
    print(f"{target} -> {binary}")


def compile_osdi(build: str) -> None:
    """Compile every Verilog-A model of toolchain.lock `osdi.models` with one OpenVAF build, named
    by a toolchain ID ("ng47-ovr-b4517ad") or by the OpenVAF commit alone ("b4517ad").

    STAMP.txt next to the objects records what they were built from: the sha256 of every file
    of each model's source folder (the .va file and its includes), the flags and the compiler.
    Nothing is compiled when the objects exist and the stamp matches. Without an installed
    compiler (e.g. a CI job that restored the objects from its cache) the objects are used when
    the sources and flags match, and the run stops when they do not.
    """
    sha7 = build if build in LOCK["openvaf"] else split_id(build)[1]
    compiler = openvaf_path(sha7)
    out_dir = osdi_dir(sha7)
    models = LOCK["osdi"]["models"]
    stamp = out_dir / "STAMP.txt"

    def source_lines() -> list[str]:
        lines = []
        for model in models:
            folder = (HERE / model["source"]).resolve().parent
            digest = hashlib.sha256(b"".join(sha256(f).encode() for f in sorted(folder.iterdir()) if f.is_file()))
            lines.append(f"sources {model['output']} {digest.hexdigest()}")
        return lines + [f"flags {' '.join(LOCK['osdi']['flags'])}"]

    expected = source_lines()
    built = all((out_dir / m["output"]).exists() for m in models) and stamp.exists()
    recorded = stamp.read_text().splitlines() if built else []
    if built and recorded[:-1] == expected:
        if not compiler.exists() or recorded[-1] == f"compiler {sha256(compiler.resolve())}":
            print(f"up to date: {out_dir}")
            return
    if not compiler.exists():
        sys.exit(f"OpenVAF {sha7} is not installed and {out_dir} does not match the current sources: "
                 f"python3 tools/toolchain.py build openvaf {sha7}")
    out_dir.mkdir(parents=True, exist_ok=True)
    for model in models:
        source = (HERE / model["source"]).resolve()
        run([compiler, *LOCK["osdi"]["flags"], "-o", out_dir / model["output"], source.name], cwd=source.parent)
    stamp.write_text("\n".join(expected + [f"compiler {sha256(compiler.resolve())}"]) + "\n")


def list_toolchains() -> None:
    """Print every pinned toolchain and whether its parts are installed."""
    for toolchain in LOCK["toolchains"]:
        version, sha7 = split_id(toolchain)
        state = [f"ngspice-{version} {'ok' if ngspice_path(version).exists() else 'missing'}",
                 f"openvaf-r-{sha7} {'ok' if openvaf_path(sha7).exists() else 'missing'}",
                 f"osdi {'ok' if osdi_dir(sha7).is_dir() else 'missing'}"]
        print(f"{toolchain:24s} " + ", ".join(state))


def main() -> int:
    """Command-line entry point (see the module docstring)."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    b = sub.add_parser("build")
    b.add_argument("tool", choices=["ngspice", "openvaf"])
    b.add_argument("key", help="ngspice version (47) or OpenVAF commit (b4517ad)")
    b.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    b.add_argument("--offline", action="store_true", help="cargo --offline (crates already cached)")
    r = sub.add_parser("register")
    r.add_argument("tool", choices=["ngspice", "openvaf"])
    r.add_argument("key")
    r.add_argument("binary", type=Path)
    o = sub.add_parser("osdi")
    o.add_argument("build", help="toolchain ID or OpenVAF commit (7 hex)")
    p = sub.add_parser("path")
    p.add_argument("what", choices=["ngspice", "openvaf", "osdi-dir"])
    p.add_argument("toolchain")
    i = sub.add_parser("ids")
    i.add_argument("toolchain")
    args = parser.parse_args()

    if args.command == "list":
        list_toolchains()
    elif args.command == "build" and args.tool == "ngspice":
        build_ngspice(args.key, args.jobs)
    elif args.command == "build":
        build_openvaf(args.key, args.offline)
    elif args.command == "register":
        register(args.tool, args.key, args.binary)
    elif args.command == "osdi":
        compile_osdi(args.build)
    elif args.command == "ids":
        version, sha7 = split_id(args.toolchain)
        print(f"ngspice={version}\nopenvaf={sha7}")
    elif args.command == "path":
        version, sha7 = split_id(args.toolchain)
        print({"ngspice": ngspice_path(version), "openvaf": openvaf_path(sha7), "osdi-dir": osdi_dir(sha7)}[args.what])
    return 0


if __name__ == "__main__":
    sys.exit(main())
