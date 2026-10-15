#!/usr/bin/env python3

########################################################################
#
# Copyright 2026 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

# AI provenance: Generated with OpenAI Codex (GPT-5).

"""Validate the SRAM deliverables and their functional Verilog models."""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SRAM_REL = Path("ihp-sg13g2/libs.ref/sg13g2_sram")
MACRO_RE = re.compile(
    r"^RM_IHPSG13_(?P<ports>[12])P_(?P<depth>\d+)x(?P<width>\d+)_c\d+"
    r"(?P<bist>_bm_bist)?$"
)
TIMESCALE_RE = re.compile(r"(?m)^\s*`timescale\s+1ns/10ps\s*$")
DECL_RE = re.compile(
    r"(?m)^\s*(?:input|output)(?:\s+(?:wire|reg|logic))?\s*"
    r"(?:\[(\d+)\s*:\s*(\d+)\]\s*)?([^;]+);"
)
LIB_CORNER_RE = re.compile(
    r"^(?P<macro>RM_IHPSG13_.+)_"
    r"(?P<corner>fast_1p32V_m55C|slow_1p08V_125C|typ_1p20V_25C)\.lib$"
)
EXPECTED_CORNERS = {
    "fast_1p32V_m55C",
    "slow_1p08V_125C",
    "typ_1p20V_25C",
}
POWER_PINS = {"VDD!", "VDDARRAY!", "VSS!"}


class Validator:
    def __init__(self, root: Path, skip_gds: bool, skip_verilog: bool) -> None:
        self.root = root.resolve()
        self.sram = self.root / SRAM_REL
        self.skip_gds = skip_gds
        self.skip_verilog = skip_verilog
        self.errors: list[str] = []
        self.check_count = 0

    def check(self, condition: bool, message: str) -> None:
        self.check_count += 1
        if not condition:
            self.errors.append(message)

    @staticmethod
    def macro_names(directory: Path, suffix: str) -> set[str]:
        return {path.name[: -len(suffix)] for path in directory.glob(f"*{suffix}")}

    @staticmethod
    def declarations(text: str) -> dict[str, int]:
        ports: dict[str, int] = {}
        for match in DECL_RE.finditer(text):
            msb, lsb, names = match.groups()
            width = abs(int(msb) - int(lsb)) + 1 if msb is not None else 1
            names = names.split("//", 1)[0]
            for name in names.split(","):
                name = re.sub(r"\s*=.*$", "", name).strip()
                if re.fullmatch(r"[A-Za-z_]\w*", name):
                    ports[name] = width
        return ports

    @staticmethod
    def expanded_ports(ports: dict[str, int], bracket: str = "[]") -> set[str]:
        expanded: set[str] = set()
        left, right = bracket
        for name, width in ports.items():
            if width == 1:
                expanded.add(name)
            else:
                expanded.update(f"{name}{left}{index}{right}" for index in range(width))
        return expanded

    def validate_inventory(self) -> list[str]:
        verilog = self.macro_names(self.sram / "verilog", ".v")
        verilog = {name for name in verilog if "_core_behavioral" not in name}
        self.check(bool(verilog), "no SRAM macro Verilog models were found")

        for view, suffix in (
            ("cdl", ".cdl"),
            ("doc", ".txt"),
            ("gds", ".gds"),
            ("lef", ".lef"),
        ):
            names = self.macro_names(self.sram / view, suffix)
            missing = sorted(verilog - names)
            extra = sorted(names - verilog)
            self.check(not missing, f"{view}: missing macros: {', '.join(missing)}")
            self.check(not extra, f"{view}: macros without Verilog models: {', '.join(extra)}")

        liberty: dict[str, set[str]] = {}
        malformed: list[str] = []
        for path in (self.sram / "lib").glob("*.lib"):
            match = LIB_CORNER_RE.match(path.name)
            if match is None:
                malformed.append(path.name)
                continue
            liberty.setdefault(match["macro"], set()).add(match["corner"])
        self.check(not malformed, f"lib: unrecognized filenames: {', '.join(sorted(malformed))}")
        self.check(
            set(liberty) == verilog,
            "lib: macro inventory differs from Verilog: "
            f"missing={sorted(verilog - set(liberty))}, extra={sorted(set(liberty) - verilog)}",
        )
        for macro in sorted(verilog):
            self.check(
                liberty.get(macro) == EXPECTED_CORNERS,
                f"lib: {macro} corners are {sorted(liberty.get(macro, set()))}; "
                f"expected {sorted(EXPECTED_CORNERS)}",
            )
        return sorted(verilog)

    def validate_macro_text(self, macro: str) -> dict[str, int]:
        match = MACRO_RE.match(macro)
        self.check(match is not None, f"{macro}: filename does not encode a supported SRAM configuration")
        if match is None:
            return {}

        port_count = int(match["ports"])
        depth = int(match["depth"])
        data_width = int(match["width"])
        addr_width = int(math.log2(depth))
        self.check(2**addr_width == depth, f"{macro}: depth {depth} is not a power of two")

        verilog_path = self.sram / "verilog" / f"{macro}.v"
        text = verilog_path.read_text(encoding="utf-8")
        ports = self.declarations(text)

        self.check(
            len(TIMESCALE_RE.findall(text)) == 1,
            f"{verilog_path.relative_to(self.root)}: expected exactly one `timescale 1ns/10ps directive",
        )
        self.check(
            re.search(rf"\bmodule\s+{re.escape(macro)}\s*\(", text) is not None,
            f"{verilog_path.relative_to(self.root)}: module name does not match filename",
        )

        expected_widths: dict[str, int] = {}
        for prefix in ("A", "B")[:port_count]:
            expected_widths.update(
                {
                    f"{prefix}_CLK": 1,
                    f"{prefix}_MEN": 1,
                    f"{prefix}_WEN": 1,
                    f"{prefix}_REN": 1,
                    f"{prefix}_ADDR": addr_width,
                    f"{prefix}_DIN": data_width,
                    f"{prefix}_DLY": 1,
                    f"{prefix}_DOUT": data_width,
                }
            )
            if match["bist"]:
                expected_widths.update(
                    {
                        f"{prefix}_BM": data_width,
                        f"{prefix}_BIST_CLK": 1,
                        f"{prefix}_BIST_EN": 1,
                        f"{prefix}_BIST_MEN": 1,
                        f"{prefix}_BIST_WEN": 1,
                        f"{prefix}_BIST_REN": 1,
                        f"{prefix}_BIST_ADDR": addr_width,
                        f"{prefix}_BIST_DIN": data_width,
                        f"{prefix}_BIST_BM": data_width,
                    }
                )

        self.check(
            ports == expected_widths,
            f"{verilog_path.relative_to(self.root)}: port widths differ; "
            f"missing/wrong={sorted(set(expected_widths.items()) - set(ports.items()))}, "
            f"unexpected={sorted(set(ports.items()) - set(expected_widths.items()))}",
        )

        for prefix in ("A", "B")[:port_count]:
            dly = f"{prefix}_DLY"
            condition = re.compile(rf"if\s*\(\s*{dly}\s*!==\s*1'b1\s*\)")
            self.check(
                len(condition.findall(text)) == 2,
                f"{verilog_path.relative_to(self.root)}: {dly} needs initial and change-time high checks",
            )
            self.check(
                re.search(rf"\.{dly}\s*\(\s*{dly}\s*\)", text) is not None,
                f"{verilog_path.relative_to(self.root)}: {dly} is not passed through to the behavioral model",
            )
            self.check(
                re.search(rf"\.{dly}\s*\(\s*1'b[01]\s*\)", text) is None,
                f"{verilog_path.relative_to(self.root)}: {dly} must not be tied to a constant",
            )

        doc_path = self.sram / "doc" / f"{macro}.txt"
        doc = doc_path.read_text(encoding="utf-8", errors="replace")
        self.check(
            re.search(r"IMPORTANT:.*DLY must always be tied to ['\"]?1['\"]?", doc) is not None,
            f"{doc_path.relative_to(self.root)}: missing prominent DLY tie-high notice",
        )

        expected_expanded = self.expanded_ports(expected_widths)
        lef_path = self.sram / "lef" / f"{macro}.lef"
        lef = lef_path.read_text(encoding="utf-8", errors="replace")
        lef_pins = set(re.findall(r"(?m)^\s*PIN\s+(\S+)\s*$", lef))
        self.check(
            lef_pins == expected_expanded | POWER_PINS,
            f"{lef_path.relative_to(self.root)}: LEF pins differ from Verilog ports; "
            f"missing={sorted((expected_expanded | POWER_PINS) - lef_pins)}, "
            f"extra={sorted(lef_pins - (expected_expanded | POWER_PINS))}",
        )
        self.check(
            re.search(rf"(?m)^\s*MACRO\s+{re.escape(macro)}\s*$", lef) is not None,
            f"{lef_path.relative_to(self.root)}: MACRO name does not match filename",
        )

        cdl_path = self.sram / "cdl" / f"{macro}.cdl"
        cdl = cdl_path.read_text(encoding="utf-8", errors="replace")
        top = re.search(rf"(?m)^\.SUBCKT\s+{re.escape(macro)}\s+(.+)$", cdl)
        self.check(top is not None, f"{cdl_path.relative_to(self.root)}: missing top-level .SUBCKT {macro}")
        if top is not None:
            cdl_pins = {pin.replace("<", "[").replace(">", "]") for pin in top.group(1).split()}
            self.check(
                cdl_pins == expected_expanded | POWER_PINS,
                f"{cdl_path.relative_to(self.root)}: top-level pins differ from Verilog ports; "
                f"missing={sorted((expected_expanded | POWER_PINS) - cdl_pins)}, "
                f"extra={sorted(cdl_pins - (expected_expanded | POWER_PINS))}",
            )

        expected_groups = set(expected_widths)
        for lib_path in sorted((self.sram / "lib").glob(f"{macro}_*.lib")):
            liberty_text = lib_path.read_text(encoding="utf-8", errors="replace")
            self.check(
                re.search(rf"\bcell\s*\(\s*{re.escape(macro)}\s*\)", liberty_text) is not None,
                f"{lib_path.relative_to(self.root)}: cell name does not match macro",
            )
            groups = set(re.findall(r"\b(?:pin|bus)\s*\(\s*([A-Za-z_]\w*)\s*\)", liberty_text))
            self.check(
                groups == expected_groups,
                f"{lib_path.relative_to(self.root)}: Liberty port groups differ; "
                f"missing={sorted(expected_groups - groups)}, extra={sorted(groups - expected_groups)}",
            )

        return expected_widths

    def validate_gds(self, macro: str, expected_widths: dict[str, int]) -> None:
        if self.skip_gds:
            return
        try:
            import gdstk  # type: ignore[import-not-found]
        except ImportError:
            self.errors.append("gdstk is required for GDS validation; install it or pass --skip-gds")
            return

        path = self.sram / "gds" / f"{macro}.gds"
        try:
            library = gdstk.read_gds(path)
        except Exception as exc:  # gdstk raises format-specific exceptions
            self.errors.append(f"{path.relative_to(self.root)}: cannot read GDS: {exc}")
            return
        top_names = {cell.name for cell in library.top_level()}
        self.check(top_names == {macro}, f"{path.relative_to(self.root)}: top cells are {sorted(top_names)}")
        cells = [cell for cell in library.cells if cell.name == macro]
        self.check(len(cells) == 1, f"{path.relative_to(self.root)}: expected exactly one cell named {macro}")
        if len(cells) != 1:
            return
        labels = {label.text.replace("<", "[").replace(">", "]") for label in cells[0].labels}
        expected = self.expanded_ports(expected_widths) | POWER_PINS
        self.check(
            labels == expected,
            f"{path.relative_to(self.root)}: top-cell labels differ from Verilog ports; "
            f"missing={sorted(expected - labels)}, extra={sorted(labels - expected)}",
        )

    def compile_verilog(self, macro: str) -> None:
        if self.skip_verilog:
            return
        iverilog = shutil.which("iverilog")
        if iverilog is None:
            self.errors.append("iverilog is required for Verilog validation; install it or pass --skip-verilog")
            return

        one_port = "_1P_" in macro
        bist = macro.endswith("_bm_bist")
        if one_port:
            core = "RM_IHPSG13_1P_core_behavioral_bm_bist.v" if bist else "RM_IHPSG13_1P_core_behavioral.v"
        else:
            core = (
                "RM_IHPSG13_2P_core_behavioral_bm_bist_ideal.v"
                if bist
                else "RM_IHPSG13_2P_core_behavioral_ideal.v"
            )
        verilog_dir = self.sram / "verilog"
        sources = [verilog_dir / core, verilog_dir / f"{macro}.v"]
        for defines in (("FUNCTIONAL",), ("FUNCTIONAL", "SYNTHESIS")):
            command = [iverilog, "-g2012", "-t", "null", "-s", macro]
            command.extend(f"-D{define}" for define in defines)
            command.extend(str(source) for source in sources)
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.check(
                result.returncode == 0,
                f"{macro}: iverilog failed with {','.join(defines)}:\n{result.stderr.strip()}",
            )

    def validate_runtime_dly_check(self) -> None:
        if self.skip_verilog:
            return
        iverilog = shutil.which("iverilog")
        vvp = shutil.which("vvp")
        if iverilog is None or vvp is None:
            return

        macro = "RM_IHPSG13_2P_64x32_c2"
        verilog_dir = self.sram / "verilog"
        if not (verilog_dir / f"{macro}.v").exists():
            self.errors.append(f"{macro}: required runtime smoke-test model is missing")
            return
        testbench = r"""`timescale 1ns/10ps
module tb;
  reg A_CLK = 0, A_MEN = 0, A_WEN = 0, A_REN = 0, A_DLY = 1;
  reg B_CLK = 0, B_MEN = 0, B_WEN = 0, B_REN = 0, B_DLY = 1;
  reg [5:0] A_ADDR = 0, B_ADDR = 0;
  reg [31:0] A_DIN = 0, B_DIN = 0;
  wire [31:0] A_DOUT, B_DOUT;
  RM_IHPSG13_2P_64x32_c2 dut (
    .A_CLK(A_CLK), .A_MEN(A_MEN), .A_WEN(A_WEN), .A_REN(A_REN),
    .A_ADDR(A_ADDR), .A_DIN(A_DIN), .A_DLY(A_DLY), .A_DOUT(A_DOUT),
    .B_CLK(B_CLK), .B_MEN(B_MEN), .B_WEN(B_WEN), .B_REN(B_REN),
    .B_ADDR(B_ADDR), .B_DIN(B_DIN), .B_DLY(B_DLY), .B_DOUT(B_DOUT));
  initial begin
    #1 B_DLY = 0;
    #1 $fatal(1, "B_DLY violation was not stopped");
  end
endmodule
"""
        with tempfile.TemporaryDirectory(prefix="sram-dly-") as temporary:
            temporary_path = Path(temporary)
            tb_path = temporary_path / "tb.v"
            output_path = temporary_path / "sim.vvp"
            tb_path.write_text(testbench, encoding="utf-8")
            compile_result = subprocess.run(
                [
                    iverilog,
                    "-g2012",
                    "-DFUNCTIONAL",
                    "-s",
                    "tb",
                    "-o",
                    str(output_path),
                    str(verilog_dir / "RM_IHPSG13_2P_core_behavioral_ideal.v"),
                    str(verilog_dir / f"{macro}.v"),
                    str(tb_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.check(
                compile_result.returncode == 0,
                f"{macro}: runtime DLY testbench did not compile: {compile_result.stderr.strip()}",
            )
            if compile_result.returncode != 0:
                return
            run_result = subprocess.run(
                [vvp, "-N", str(output_path)], capture_output=True, text=True, check=False
            )
            output = run_result.stdout + run_result.stderr
            self.check(run_result.returncode != 0, f"{macro}: B_DLY violation did not fail simulation")
            self.check(
                "B_DLY must remain 1'b1" in output,
                f"{macro}: B_DLY violation did not emit the expected diagnostic",
            )

    def validate_new_macro_behavior(self) -> None:
        if self.skip_verilog:
            return
        iverilog = shutil.which("iverilog")
        vvp = shutil.which("vvp")
        if iverilog is None or vvp is None:
            return

        macro = "RM_IHPSG13_1P_64x16_c2"
        verilog_dir = self.sram / "verilog"
        if not (verilog_dir / f"{macro}.v").exists():
            self.errors.append(f"{macro}: newly delivered functional model is missing")
            return
        testbench = r"""`timescale 1ns/10ps
module tb;
  reg A_CLK = 0, A_MEN = 0, A_WEN = 0, A_REN = 0, A_DLY = 1;
  reg [5:0] A_ADDR = 0;
  reg [15:0] A_DIN = 0;
  wire [15:0] A_DOUT;
  RM_IHPSG13_1P_64x16_c2 dut (
    .A_CLK(A_CLK), .A_MEN(A_MEN), .A_WEN(A_WEN), .A_REN(A_REN),
    .A_ADDR(A_ADDR), .A_DIN(A_DIN), .A_DLY(A_DLY), .A_DOUT(A_DOUT));
  initial begin
    #1 A_MEN = 1; A_WEN = 1; A_ADDR = 6'h2a; A_DIN = 16'hcafe;
    #1 A_CLK = 1;
    #1 A_CLK = 0; A_WEN = 0; A_REN = 1; A_DIN = 0;
    #1 A_CLK = 1;
    #0.1;
    if (A_DOUT !== 16'hcafe)
      $fatal(1, "readback mismatch: expected cafe, got %h", A_DOUT);
    $display("64x16 functional read/write passed");
    $finish;
  end
endmodule
"""
        with tempfile.TemporaryDirectory(prefix="sram-functional-") as temporary:
            temporary_path = Path(temporary)
            tb_path = temporary_path / "tb.v"
            output_path = temporary_path / "sim.vvp"
            tb_path.write_text(testbench, encoding="utf-8")
            compile_result = subprocess.run(
                [
                    iverilog,
                    "-g2012",
                    "-DFUNCTIONAL",
                    "-s",
                    "tb",
                    "-o",
                    str(output_path),
                    str(verilog_dir / "RM_IHPSG13_1P_core_behavioral.v"),
                    str(verilog_dir / f"{macro}.v"),
                    str(tb_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.check(
                compile_result.returncode == 0,
                f"{macro}: functional testbench did not compile: {compile_result.stderr.strip()}",
            )
            if compile_result.returncode != 0:
                return
            run_result = subprocess.run(
                [vvp, "-N", str(output_path)], capture_output=True, text=True, check=False
            )
            output = run_result.stdout + run_result.stderr
            self.check(
                run_result.returncode == 0 and "functional read/write passed" in output,
                f"{macro}: functional read/write failed:\n{output.strip()}",
            )

    def run(self) -> int:
        self.check(self.sram.is_dir(), f"SRAM library not found under {self.root}")
        if not self.sram.is_dir():
            return self.report()
        macros = self.validate_inventory()
        for macro in macros:
            ports = self.validate_macro_text(macro)
            if ports:
                self.validate_gds(macro, ports)
            self.compile_verilog(macro)
        self.validate_runtime_dly_check()
        self.validate_new_macro_behavior()
        return self.report()

    def report(self) -> int:
        if self.errors:
            print(f"SRAM validation failed with {len(self.errors)} error(s):", file=sys.stderr)
            for error in self.errors:
                print(f"  - {error}", file=sys.stderr)
            return 1
        print(f"SRAM validation passed ({self.check_count} checks).")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[3],
        help="repository root (defaults to the root containing this script)",
    )
    parser.add_argument("--skip-gds", action="store_true", help="skip GDS parsing and label checks")
    parser.add_argument(
        "--skip-verilog", action="store_true", help="skip iverilog compile and runtime checks"
    )
    args = parser.parse_args()
    return Validator(args.root, args.skip_gds, args.skip_verilog).run()


if __name__ == "__main__":
    raise SystemExit(main())
