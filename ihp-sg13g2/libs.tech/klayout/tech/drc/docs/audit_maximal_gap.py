#!/usr/bin/env python3
"""
Audit script for DRC modular parity analysis.

Extracts rule IDs from maximal, modular, and auxiliary DRC files,
classifies each into target modular files, checks JSON parameter
coverage, and produces a Markdown inventory report.
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
DRC_BASE = SCRIPT_DIR.parent / "rule_decks"

MAXIMAL_DRC = DRC_BASE / "sg13g2_maximal.drc"
JSON_PARAMS = DRC_BASE / "sg13g2_tech_default.json"

FEOL_DIR = DRC_BASE / "feol"
BEOL_DIR = DRC_BASE / "beol"
OFFGRID_DIR = DRC_BASE / "offgrid"
PIN_DIR = DRC_BASE / "pin"

ANTENNA_DRC = DRC_BASE / "antenna.drc"
DENSITY_DRC = DRC_BASE / "density.drc"
FORBIDDEN_DRC = DRC_BASE / "forbidden" / "3_2_forbidden.drc"

OUTPUT_FILE = SCRIPT_DIR / "audit_inventory.md"

# ── Rule-to-file mapping ──────────────────────────────────────────────────
# Order matters: more specific prefixes first.

RULE_MAPPING = [
    # FEOL - existing files
    ("NW.",      "feol/5_1_nwell.drc"),
    ("PWB.",     "feol/5_2_pwellblock.drc"),
    ("NBLB.",    "feol/5_3_nbulay.drc"),
    ("NBL.",     "feol/5_3_nbulay.drc"),
    ("Act.",     "feol/5_5_activ.drc"),
    ("AFil.",    "feol/5_6_activfiller.drc"),
    ("TGO.",     "feol/5_7_thickgateox.drc"),
    ("Gat.",     "feol/5_8_gatpoly.drc"),
    ("GFil.",    "feol/5_9_gatpolyfiller.drc"),
    ("pSD.",     "feol/5_10_psd.drc"),
    ("nSDB.",    "feol/5_10_psd.drc"),
    # FEOL - new files needed
    ("nmosi.",   "feol/5_11_nmosi.drc"),
    ("Sal.",     "feol/5_12_salblock.drc"),
    ("EXTB.",    "feol/5_13_extblock.drc"),
    # FEOL - existing
    ("Cnt.",     "feol/5_14_cont.drc"),
    ("CntB.",    "feol/5_15_contbar.drc"),
    # FEOL - new files needed (resistors)
    ("Rsil.",    "feol/6_2_rsil.drc"),
    ("Rppd.",    "feol/6_3_rppd.drc"),
    ("Rpnd.",    "feol/6_3_rppd.drc"),  # Rpnd shares with Rppd
    ("Rhi.",     "feol/6_4_rhigh.drc"),
    # FEOL - existing
    ("npn13G2V.", "feol/6_1_npnsubstratetie.drc"),
    ("npn13G2L.", "feol/6_1_npnsubstratetie.drc"),
    ("npn13G2.",  "feol/6_1_npnsubstratetie.drc"),
    ("npnG2.",    "feol/6_1_npnsubstratetie.drc"),
    ("Sdiod.",    "feol/6_7_schottkydiode.drc"),
    ("LU.",       "feol/7_2_latchup.drc"),
    # BEOL - existing files
    ("M1Fil.",   "beol/5_18_metalnfiller.drc"),
    ("M2Fil.",   "beol/5_18_metalnfiller.drc"),
    ("M3Fil.",   "beol/5_18_metalnfiller.drc"),
    ("M4Fil.",   "beol/5_18_metalnfiller.drc"),
    ("M5Fil.",   "beol/5_18_metalnfiller.drc"),
    ("M1.",      "beol/5_16_metal1.drc"),
    ("M2.",      "beol/5_17_metaln.drc"),
    ("M3.",      "beol/5_17_metaln.drc"),
    ("M4.",      "beol/5_17_metaln.drc"),
    ("M5.",      "beol/5_17_metaln.drc"),
    ("V1.",      "beol/5_19_via1.drc"),
    ("V2.",      "beol/5_20_vian.drc"),
    ("V3.",      "beol/5_20_vian.drc"),
    ("V4.",      "beol/5_20_vian.drc"),
    ("TV1.",     "beol/5_21_topvia1.drc"),
    ("TM1Fil.",  "beol/5_23_topmetal1filler.drc"),
    ("TM1.",     "beol/5_22_topmetal1.drc"),
    ("TV2.",     "beol/5_24_topvia2.drc"),
    ("TM2Fil.",  "beol/5_26_topmetal2filler.drc"),
    ("TM2.",     "beol/5_25_topmetal2.drc"),
    ("Pas.",     "beol/5_27_passiv.drc"),
    ("BPas.",    "beol/5_27_passiv.drc"),
    ("Pad.",     "beol/6_9_pad.drc"),
    ("Padb.",    "beol/6_9_solderbump.drc"),
    ("padb.",    "beol/6_9_solderbump.drc"),
    ("Padc.",    "beol/6_9_copperpillar.drc"),
    ("padc.",    "beol/6_9_copperpillar.drc"),
    ("Seal.",    "beol/6_10_sealring.drc"),
    ("MIM.",     "beol/6_11_mim.drc"),
    ("Slt.",     "beol/7_3_metalslits.drc"),
    ("LBE.",     "beol/9_1_lbe.drc"),
    # Offgrid - new file
    ("OffGrid.", "offgrid/offgrid.drc"),
    # Antenna - existing standalone
    ("Ant.",     "antenna.drc"),
    # Density - existing standalone
    # (density rules like AFil.g, M1.j, etc. are in density.drc)
    # Pin
    ("Pin.",     "pin/7_4_pin.drc"),
    # Forbidden
    ("forbidden.", "forbidden/3_2_forbidden.drc"),
]


def classify_rule(rule_id):
    """Map a rule ID to its target modular file."""
    for prefix, target in RULE_MAPPING:
        if rule_id.startswith(prefix):
            return target
    return "UNMAPPED"


# ── Extraction functions ──────────────────────────────────────────────────

# Patterns for rule output in DRC files
# Maximal uses: .output("RuleID", "description")
# Modular uses: .output('RuleID', "description") or .output("RuleID", ...)
OUTPUT_PATTERN = re.compile(
    r"""\.output\(\s*['"]([^'"]+)['"]\s*,""",
    re.IGNORECASE,
)


def extract_rules_from_file(filepath):
    """Extract all rule IDs from .output() calls in a DRC file.

    Returns a dict {rule_id: line_number}.
    """
    rules = {}
    if not filepath.exists():
        return rules
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            for match in OUTPUT_PATTERN.finditer(line):
                rule_id = match.group(1)
                if rule_id not in rules:
                    rules[rule_id] = lineno
    return rules


def extract_maximal_rules():
    """Extract all rules from the maximal deck."""
    return extract_rules_from_file(MAXIMAL_DRC)


def extract_modular_rules():
    """Extract rules from all modular files (feol/, beol/, antenna, density, pin, forbidden)."""
    all_rules = {}  # rule_id -> (file, lineno)
    search_dirs = [FEOL_DIR, BEOL_DIR, OFFGRID_DIR, PIN_DIR]

    for d in search_dirs:
        if not d.exists():
            continue
        for drc_file in sorted(d.glob("*.drc")):
            rules = extract_rules_from_file(drc_file)
            relpath = drc_file.relative_to(DRC_BASE)
            for rule_id, lineno in rules.items():
                # Skip Ruby interpolation templates (e.g., "Slt.a.#{met_abbrev}")
                if "#{" in rule_id:
                    continue
                all_rules[rule_id] = (str(relpath), lineno)

    # Standalone modular files
    for standalone in [ANTENNA_DRC, DENSITY_DRC, FORBIDDEN_DRC]:
        if standalone.exists():
            rules = extract_rules_from_file(standalone)
            relpath = standalone.relative_to(DRC_BASE)
            for rule_id, lineno in rules.items():
                if "#{" in rule_id:
                    continue
                all_rules[rule_id] = (str(relpath), lineno)

    return all_rules


def load_json_params():
    """Load the JSON parameter keys."""
    with open(JSON_PARAMS, "r") as f:
        data = json.load(f)
    return set(data.get("drc_rules", {}).keys())


def json_key_for_rule(rule_id):
    """Convert a rule ID to its JSON key(s) and check if any match.

    Many rules use shared/base parameters rather than per-instance keys:
    - Slt.a.M1 -> Slt_a (shared across metals)
    - M2.c -> Mn_c (metals 2-5 use Mn_* params)
    - M3Fil.b -> MFil_b (all metal fillers share MFil_* params)
    - OffGrid.* -> grid (single grid value)
    - Seal.a_Activ -> Seal_a (shared across layers)
    - Seal.c1.Via1 -> Seal_c1 (shared across vias)
    - V2.b1 -> Vn_b1 (vias 2-4 use Vn_* params)

    Returns a list of candidate JSON keys to check.
    """
    candidates = []

    # Direct literal conversion (NW.a -> NW_a)
    candidates.append(rule_id.replace(".", "_"))

    # OffGrid rules use the single "grid" parameter
    if rule_id.startswith("OffGrid."):
        candidates.append("grid")
        return candidates

    # Slt rules: Slt.a.M1 -> base key Slt_a, also Slt_h1, Slt_h2, etc.
    if rule_id.startswith("Slt."):
        parts = rule_id.split(".")
        if len(parts) >= 3:
            # Slt.a.M1 -> Slt_a
            candidates.append(f"Slt_{parts[1]}")
        if len(parts) == 2:
            candidates.append(f"Slt_{parts[1]}")

    # Seal rules: Seal.a_Activ -> Seal_a, Seal.c1.Via1 -> Seal_c1
    if rule_id.startswith("Seal."):
        parts = rule_id.split(".")
        if len(parts) >= 2:
            # Seal.a_Metal1 -> Seal_a (strip layer suffix after _)
            base = parts[1].split("_")[0]
            candidates.append(f"Seal_{base}")
        if len(parts) >= 3:
            # Seal.c1.Via1 -> Seal_c1
            candidates.append(f"Seal_{parts[1]}")
            # Seal.d.Cont -> Seal_d
            candidates.append(f"Seal_{parts[1]}")

    # Metal 2-5 rules use Mn_* params: M2.c -> Mn_c, M3.d -> Mn_d
    import re as _re
    mn_match = _re.match(r"^M([2-5])\.(\w+)$", rule_id)
    if mn_match:
        suffix = mn_match.group(2)
        candidates.append(f"Mn_{suffix}")

    # Metal filler rules: M1Fil.a1 -> MFil_a1, M2Fil.b -> MFil_b
    mfil_match = _re.match(r"^M([1-5])Fil\.(\w+)$", rule_id)
    if mfil_match:
        suffix = mfil_match.group(2)
        candidates.append(f"MFil_{suffix}")

    # Via 2-4 rules use Vn_* params: V2.b1 -> Vn_b1
    vn_match = _re.match(r"^V([2-4])\.(\w+)$", rule_id)
    if vn_match:
        suffix = vn_match.group(2)
        candidates.append(f"Vn_{suffix}")

    # MIM rules: JSON uses Mim_* (lowercase) but rule IDs use MIM.*
    if rule_id.startswith("MIM."):
        suffix = rule_id[4:]
        candidates.append(f"Mim_{suffix}")

    # NPN rules with layer suffixes: npnG2.d.NWell -> npn_ring (uses hardcoded)
    if rule_id.startswith("npnG2.d.") or rule_id.startswith("npnG2.d1") or rule_id.startswith("npnG2.d2"):
        candidates.append("npn_ring")

    # Pad.fR_* rules: Pad.fR_M1 -> Pad_fR
    if rule_id.startswith("Pad.fR_"):
        candidates.append("Pad_fR")

    # LBE.e.dfPad/Passiv -> LBE_e
    if rule_id.startswith("LBE.e."):
        candidates.append("LBE_e")

    return candidates


def rule_has_json(rule_id, json_keys):
    """Check if any candidate JSON key exists for a rule."""
    candidates = json_key_for_rule(rule_id)
    return any(k in json_keys for k in candidates)


# ── Density rules: special handling ───────────────────────────────────────
# Some rules in density.drc are for the same logical rule but applied to
# different layers (e.g. M1.j, M2.j, etc.). These expand from templates.
# We extract them directly.


def get_density_rule_ids():
    """Get the rule IDs that the density.drc file produces.

    Some are template-expanded at runtime. We extract what we can statically,
    and augment with known expansions.
    """
    static = extract_rules_from_file(DENSITY_DRC)
    # Template expansions we know about:
    expanded = {}
    # M#{met_no}.j and M#{met_no}.k for met_no in 2..5
    for met in range(2, 6):
        for suffix in ["j", "k"]:
            rid = f"M{met}.{suffix}"
            expanded[rid] = 0
    # M#{metalfiller_no}Fil.h and M#{metalfiller_no}Fil.k for 1..5
    for mf in range(1, 6):
        for suffix in ["h", "k"]:
            rid = f"M{mf}Fil.{suffix}"
            expanded[rid] = 0
    # Slt.i_#{met_abbrev} for each metal
    for met_abbrev in ["M1", "M2", "M3", "M4", "M5", "TM1", "TM2"]:
        rid = f"Slt.i_{met_abbrev}"
        expanded[rid] = 0

    all_density = {**expanded, **static}
    return all_density


# ── Antenna rules: template expansion ─────────────────────────────────────

def get_antenna_rule_ids():
    """Get the rule IDs that antenna.drc produces including template expansions."""
    static = extract_rules_from_file(ANTENNA_DRC)
    expanded = {}
    metals = ["Metal1", "Metal2", "Metal3", "Metal4", "Metal5",
              "TopMetal1", "TopMetal2"]
    vias = ["Cont", "Via1", "Via2", "Via3", "Via4", "TopVia1", "TopVia2"]

    for met in metals:
        expanded[f"Ant.b_{met}"] = 0
        expanded[f"Ant.e_{met}"] = 0
    for via in vias:
        expanded[f"Ant.d_{via}"] = 0
        expanded[f"Ant.f_{via}"] = 0

    all_ant = {**expanded, **static}
    return all_ant


# ── Modular template expansion ────────────────────────────────────────────
# Many modular files use Ruby loops to generate per-layer/per-metal rule IDs
# at runtime. The static regex extraction can't resolve these, so we expand
# them explicitly based on the known loop patterns.


def expand_modular_templates():
    """Expand all template-loop-generated rule IDs from modular files.

    Returns a dict {rule_id: (source_file, 0)} for all dynamically
    generated rule IDs.
    """
    expanded = {}

    # ── beol/5_17_metaln.drc: M{2-5}.{a,b,c,c1,d,e,f,g,i} ──
    for met in range(2, 6):
        for suffix in ['a', 'b', 'c', 'c1', 'd', 'e', 'f', 'g', 'i']:
            expanded[f"M{met}.{suffix}"] = ("beol/5_17_metaln.drc", 0)

    # ── beol/5_20_vian.drc: V{2-4}.{a,b,b1,c,c1} ──
    for via in range(2, 5):
        for suffix in ['a', 'b', 'b1', 'c', 'c1']:
            expanded[f"V{via}.{suffix}"] = ("beol/5_20_vian.drc", 0)

    # ── beol/5_18_metalnfiller.drc: M{1-5}Fil.{c,a1,a2,b,d} ──
    for met in range(1, 6):
        for suffix in ['c', 'a1', 'a2', 'b', 'd']:
            expanded[f"M{met}Fil.{suffix}"] = ("beol/5_18_metalnfiller.drc", 0)

    # ── beol/7_3_metalslits.drc ──
    metals_abbrev = ['M1', 'M2', 'M3', 'M4', 'M5', 'TM1', 'TM2']
    # Per-metal rules: Slt.{a,b,c,e,f}
    for met in metals_abbrev:
        for rule in ['a', 'b', 'c', 'e', 'f']:
            expanded[f"Slt.{rule}.{met}"] = ("beol/7_3_metalslits.drc", 0)
    # Slt.g: only M5 and TM1
    for met in ['M5', 'TM1']:
        expanded[f"Slt.g.{met}"] = ("beol/7_3_metalslits.drc", 0)
    # Slt.h*: M1->h1, M2-M5->h2.Mx, TM1->h3, TM2->h4
    expanded["Slt.h1"] = ("beol/7_3_metalslits.drc", 0)
    for met in ['M2', 'M3', 'M4', 'M5']:
        expanded[f"Slt.h2.{met}"] = ("beol/7_3_metalslits.drc", 0)
    expanded["Slt.h3"] = ("beol/7_3_metalslits.drc", 0)
    expanded["Slt.h4"] = ("beol/7_3_metalslits.drc", 0)
    # Slt.e1_* per metal
    for met in metals_abbrev:
        expanded[f"Slt.e1_{met}"] = ("beol/7_3_metalslits.drc", 0)

    # ── beol/6_10_sealring.drc ──
    seal_a_names = ['Activ', 'pSD', 'Metal1', 'Metal2', 'Metal3',
                    'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']
    for name in seal_a_names:
        expanded[f"Seal.a_{name}"] = ("beol/6_10_sealring.drc", 0)
    seal_b_names = ['metal1', 'metal2', 'metal3', 'metal4', 'metal5',
                    'topmetal1', 'topmetal2', 'activ', 'psd']
    for name in seal_b_names:
        expanded[f"Seal.b_{name}"] = ("beol/6_10_sealring.drc", 0)
    for via in ['Via1', 'Via2', 'Via3', 'Via4']:
        expanded[f"Seal.c1.{via}"] = ("beol/6_10_sealring.drc", 0)
    seal_cv = ['Cont', 'Via1', 'Via2', 'Via3', 'Via4', 'TopVia1', 'TopVia2']
    for name in seal_cv:
        expanded[f"Seal.d.{name}"] = ("beol/6_10_sealring.drc", 0)
    for name in seal_a_names:
        expanded[f"Seal.f.{name}"] = ("beol/6_10_sealring.drc", 0)

    # ── beol/6_9_pad.drc: Pad.fR_{M1-TM2} ──
    for met in metals_abbrev:
        expanded[f"Pad.fR_{met}"] = ("beol/6_9_pad.drc", 0)

    # ── pin/7_4_pin.drc: Pin.{rule} ──
    for rule in ['a', 'b', 'e', 'f_M2', 'f_M3', 'f_M4', 'f_M5', 'g', 'h']:
        expanded[f"Pin.{rule}"] = ("pin/7_4_pin.drc", 0)

    return expanded


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("DRC Modular Parity Audit")
    print("=" * 60)

    # 1. Extract rules from all sources
    print("\n[1/5] Extracting maximal rules...")
    maximal_rules = extract_maximal_rules()
    print(f"  Found {len(maximal_rules)} rules in maximal deck")

    print("\n[2/5] Extracting modular rules...")
    modular_rules = extract_modular_rules()
    print(f"  Found {len(modular_rules)} rules across modular files")

    print("\n[3/6] Expanding template rules (density, antenna, modular loops)...")
    density_rules = get_density_rule_ids()
    antenna_rules = get_antenna_rule_ids()
    modular_templates = expand_modular_templates()
    print(f"  Density rules: {len(density_rules)}")
    print(f"  Antenna rules: {len(antenna_rules)}")
    print(f"  Modular template rules: {len(modular_templates)}")

    print("\n[4/6] Loading JSON parameters...")
    json_keys = load_json_params()
    print(f"  Found {len(json_keys)} parameter keys")

    # 2. Build unified rule inventory
    # All unique rule IDs across all sources
    all_rule_ids = set()
    all_rule_ids.update(maximal_rules.keys())
    all_rule_ids.update(modular_rules.keys())

    # Merge density, antenna, and modular templates into modular_rules
    for rid in density_rules:
        if rid not in modular_rules:
            modular_rules[rid] = ("density.drc", density_rules[rid])
    for rid in antenna_rules:
        if rid not in modular_rules:
            modular_rules[rid] = ("antenna.drc", antenna_rules[rid])
    for rid, (src, lineno) in modular_templates.items():
        if rid not in modular_rules:
            modular_rules[rid] = (src, lineno)

    all_rule_ids.update(density_rules.keys())
    all_rule_ids.update(antenna_rules.keys())
    all_rule_ids.update(modular_templates.keys())

    # 3. Classify each rule
    print("\n[5/6] Classifying rules and generating inventory...")

    # Group by target file
    by_target = defaultdict(list)
    unmapped = []

    for rule_id in sorted(all_rule_ids):
        target = classify_rule(rule_id)
        in_maximal = rule_id in maximal_rules
        in_modular = rule_id in modular_rules
        modular_file = modular_rules.get(rule_id, (None, None))[0]
        json_key = json_key_for_rule(rule_id)
        has_json = rule_has_json(rule_id, json_keys)

        entry = {
            "rule_id": rule_id,
            "in_maximal": in_maximal,
            "maximal_line": maximal_rules.get(rule_id, None),
            "in_modular": in_modular,
            "modular_file": modular_file,
            "target_file": target,
            "has_json": has_json,
            "json_key": json_key,
        }

        if target == "UNMAPPED":
            unmapped.append(entry)
        else:
            by_target[target].append(entry)

    # 4. Compute statistics
    total_unique = len(all_rule_ids)
    maximal_only = {r for r in maximal_rules if r not in modular_rules}
    modular_only = {r for r in modular_rules if r not in maximal_rules}
    in_both = set(maximal_rules.keys()) & set(modular_rules.keys())

    missing_json_ready = {r for r in maximal_only
                          if rule_has_json(r, json_keys)}
    missing_no_json = maximal_only - missing_json_ready

    existing_files = set()
    new_files_needed = set()
    for target in by_target:
        target_path = DRC_BASE / target
        if target_path.exists():
            existing_files.add(target)
        else:
            new_files_needed.add(target)

    # 5. Generate Markdown report
    lines = []
    lines.append("# DRC Modular Parity Audit Inventory")
    lines.append("")
    lines.append(f"Generated by `audit_maximal_gap.py`")
    lines.append("")
    lines.append("## Summary Statistics")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total unique rules across all decks | {total_unique} |")
    lines.append(f"| Rules in maximal deck | {len(maximal_rules)} |")
    lines.append(f"| Rules in modular deck (all files) | {len(modular_rules)} |")
    lines.append(f"| Rules in both (overlap) | {len(in_both)} |")
    lines.append(f"| Maximal-only (need porting) | {len(maximal_only)} |")
    lines.append(f"| Modular-only (not in maximal) | {len(modular_only)} |")
    lines.append(f"| Maximal-only with JSON params | {len(missing_json_ready)} |")
    lines.append(f"| Maximal-only without JSON params | {len(missing_no_json)} |")
    lines.append(f"| Target files that exist | {len(existing_files)} |")
    lines.append(f"| New modular files needed | {len(new_files_needed)} |")
    lines.append("")

    # New files needed
    if new_files_needed:
        lines.append("## New Modular Files Needed")
        lines.append("")
        for nf in sorted(new_files_needed):
            rules_for_file = by_target.get(nf, [])
            missing_count = sum(1 for r in rules_for_file
                                if r["in_maximal"] and not r["in_modular"])
            lines.append(f"- `{nf}` ({missing_count} rules to port)")
        lines.append("")

    # Maximal-only rules needing JSON keys
    if missing_no_json:
        lines.append("## Rules Needing New JSON Keys")
        lines.append("")
        lines.append("These maximal-only rules have no matching parameter "
                      "in `sg13g2_tech_default.json`:")
        lines.append("")
        lines.append("| Rule ID | Target File | Missing JSON Key |")
        lines.append("|---------|-------------|------------------|")
        for r in sorted(missing_no_json):
            target = classify_rule(r)
            jk = ", ".join(json_key_for_rule(r))
            lines.append(f"| {r} | `{target}` | `{jk}` |")
        lines.append("")

    # Detailed inventory by target file
    lines.append("## Detailed Inventory by Target File")
    lines.append("")

    for target in sorted(by_target.keys()):
        entries = by_target[target]
        target_path = DRC_BASE / target
        file_exists = target_path.exists()
        status = "EXISTS" if file_exists else "NEW"

        # Counts for this file
        n_in_maximal = sum(1 for e in entries if e["in_maximal"])
        n_in_modular = sum(1 for e in entries if e["in_modular"])
        n_missing = sum(1 for e in entries
                        if e["in_maximal"] and not e["in_modular"])
        n_modular_only = sum(1 for e in entries
                             if e["in_modular"] and not e["in_maximal"])

        lines.append(f"### `{target}` [{status}]")
        lines.append("")
        lines.append(f"- In maximal: {n_in_maximal}")
        lines.append(f"- In modular: {n_in_modular}")
        lines.append(f"- Missing from modular: **{n_missing}**")
        lines.append(f"- Modular-only: {n_modular_only}")
        lines.append("")

        lines.append("| Rule ID | Maximal | Modular | JSON | Status |")
        lines.append("|---------|---------|---------|------|--------|")

        for e in entries:
            max_mark = f"L{e['maximal_line']}" if e["in_maximal"] else "-"
            mod_mark = e["modular_file"] if e["in_modular"] else "-"
            json_mark = "Y" if e["has_json"] else "N"

            if e["in_maximal"] and e["in_modular"]:
                status = "COVERED"
            elif e["in_maximal"] and not e["in_modular"]:
                status = "**MISSING**"
            elif not e["in_maximal"] and e["in_modular"]:
                status = "modular-only"
            else:
                status = "?"

            lines.append(
                f"| {e['rule_id']} | {max_mark} | {mod_mark} | "
                f"{json_mark} | {status} |"
            )

        lines.append("")

    # Unmapped rules
    if unmapped:
        lines.append("## Unmapped Rules")
        lines.append("")
        lines.append("These rules could not be mapped to any target file:")
        lines.append("")
        lines.append("| Rule ID | In Maximal | In Modular | JSON |")
        lines.append("|---------|-----------|-----------|------|")
        for e in unmapped:
            max_mark = "Y" if e["in_maximal"] else "N"
            mod_mark = "Y" if e["in_modular"] else "N"
            json_mark = "Y" if e["has_json"] else "N"
            lines.append(f"| {e['rule_id']} | {max_mark} | {mod_mark} | "
                          f"{json_mark} |")
        lines.append("")

    # Maximal-only rules summary (flat list)
    lines.append("## Maximal-Only Rules (Need Porting)")
    lines.append("")
    lines.append(f"Total: {len(maximal_only)} rules")
    lines.append("")
    lines.append("| Rule ID | Target File | JSON Ready | Maximal Line |")
    lines.append("|---------|-------------|------------|--------------|")
    for r in sorted(maximal_only):
        target = classify_rule(r)
        has_json = "Y" if rule_has_json(r, json_keys) else "N"
        mline = maximal_rules.get(r, "?")
        lines.append(f"| {r} | `{target}` | {has_json} | L{mline} |")
    lines.append("")

    # Modular-only rules summary
    lines.append("## Modular-Only Rules (Not in Maximal)")
    lines.append("")
    lines.append(f"Total: {len(modular_only)} rules")
    lines.append("")
    lines.append("| Rule ID | Source File |")
    lines.append("|---------|------------|")
    for r in sorted(modular_only):
        src = modular_rules.get(r, ("?", 0))[0]
        lines.append(f"| {r} | `{src}` |")
    lines.append("")

    # Priority breakdown
    lines.append("## Porting Priority Breakdown")
    lines.append("")

    priority_groups = {
        "P0 - Core FEOL": [
            "feol/5_1_nwell.drc", "feol/5_5_activ.drc",
            "feol/5_8_gatpoly.drc", "feol/5_10_psd.drc",
            "feol/5_7_thickgateox.drc", "feol/5_12_salblock.drc",
            "feol/5_13_extblock.drc",
        ],
        "P1 - BEOL + Sealring + Pad + Slit": [
            "beol/5_16_metal1.drc", "beol/5_17_metaln.drc",
            "beol/5_19_via1.drc", "beol/5_20_vian.drc",
            "beol/5_21_topvia1.drc", "beol/5_22_topmetal1.drc",
            "beol/5_24_topvia2.drc", "beol/5_25_topmetal2.drc",
            "beol/5_27_passiv.drc", "beol/6_10_sealring.drc",
            "beol/6_9_pad.drc", "beol/6_9_solderbump.drc",
            "beol/6_9_copperpillar.drc", "beol/7_3_metalslits.drc",
            "beol/9_1_lbe.drc",
        ],
        "P2 - Cont/CntB + Resistors + Latchup + nmosi": [
            "feol/5_14_cont.drc", "feol/5_15_contbar.drc",
            "feol/6_2_rsil.drc", "feol/6_3_rppd.drc",
            "feol/6_4_rhigh.drc", "feol/7_2_latchup.drc",
            "feol/5_11_nmosi.drc",
        ],
        "P3 - OffGrid + Filler + Density": [
            "offgrid/offgrid.drc",
            "feol/5_6_activfiller.drc", "feol/5_9_gatpolyfiller.drc",
            "beol/5_18_metalnfiller.drc",
            "beol/5_23_topmetal1filler.drc",
            "beol/5_26_topmetal2filler.drc",
            "density.drc",
            "feol/5_2_pwellblock.drc", "feol/5_3_nbulay.drc",
        ],
        "P4 - HBT/Schottky + MIM + Antenna": [
            "feol/6_1_npnsubstratetie.drc", "feol/6_7_schottkydiode.drc",
            "beol/6_11_mim.drc", "antenna.drc",
        ],
    }

    for prio, files in priority_groups.items():
        total_missing = 0
        total_covered = 0
        for f in files:
            entries = by_target.get(f, [])
            total_missing += sum(
                1 for e in entries
                if e["in_maximal"] and not e["in_modular"]
            )
            total_covered += sum(
                1 for e in entries
                if e["in_maximal"] and e["in_modular"]
            )

        lines.append(f"### {prio}")
        lines.append(f"- Missing: **{total_missing}** | "
                      f"Covered: {total_covered}")
        lines.append(f"- Files: {', '.join(f'`{f}`' for f in files)}")
        lines.append("")

    # Write report
    report_text = "\n".join(lines)
    with open(OUTPUT_FILE, "w") as f:
        f.write(report_text)

    print(f"\nReport written to: {OUTPUT_FILE}")
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total unique rules:        {total_unique}")
    print(f"  In maximal:              {len(maximal_rules)}")
    print(f"  In modular (all files):  {len(modular_rules)}")
    print(f"  Overlap:                 {len(in_both)}")
    print(f"  Maximal-only:            {len(maximal_only)}")
    print(f"    JSON-ready:            {len(missing_json_ready)}")
    print(f"    Needs JSON key:        {len(missing_no_json)}")
    print(f"  Modular-only:            {len(modular_only)}")
    print(f"  New files needed:        {len(new_files_needed)}")
    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
