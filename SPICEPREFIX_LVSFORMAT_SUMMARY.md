# Summary: spiceprefix and lvsformat in IHP-Open-PDK Pull Requests

## Overview
This document summarizes all pull requests related to `spiceprefix` and `lvsformat` in the IHP-Open-PDK repository. These topics are critical for ensuring compatibility between schematic tools (like xschem), simulation tools (like ngspice), and LVS verification tools (like KLayout and magic/netgen).

## Key Issues and Concepts

### spiceprefix
- **Purpose**: Defines the prefix letter used in SPICE netlists (e.g., `M` for MOSFETs, `D` for diodes, `Q` for bipolar transistors, `C` for capacitors, `R` for resistors, `X` for subcircuits)
- **Problem**: IHP devices are defined as `.subckt` (subcircuits) in ngspice, requiring `X` prefix for simulation, but CDL-based LVS tools expect standard prefixes (`M`, `D`, `Q`, `C`, `R`)

### lvsformat (lvs_format)
- **Purpose**: Defines the netlist format specifically for LVS verification, separate from simulation netlists
- **Relationship to spiceprefix**: Works in conjunction with spiceprefix to generate proper netlists for different tools

## Pull Requests Review

### PR #132 - Symbols update (MERGED - June 2024)
**Status**: Closed/Merged  
**Author**: KrzysztofHerman  
**Date**: June 4-12, 2024  

**Key Changes**:
- Introduced use of `@spiceprefix` in MOSFET transistor and diode symbols for selective LVS netlisting
- Standardized parameters to lowercase letters
- Added symbols for RF high-voltage MOSFETs
- **Files Changed**: 43 files (604 additions, 260 deletions)

**Significance**: This was the foundational PR that introduced the spiceprefix mechanism to the PDK.

---

### PR #605 - Add prefix name for cmim & rfcmim (CLOSED - July 2025)
**Status**: Closed (not merged, superseded by #607)  
**Author**: H-Ojiro  
**Date**: July 17 - August 7, 2025  

**Key Changes**:
- Added `spiceprefix` to capacitor symbols (cap_cmim and cap_rfcmim)
- Changed symbol display from `@name` to `@spiceprefix@name`

**Discussion Highlights**:
- @d-m-bailey raised concerns about removing `spiceprefix` from `lvs_format` statements
- @sergeiandreyev questioned whether this approach should be aligned across all devices
- This PR was superseded by the more comprehensive PR #607

**Outcome**: Closed in favor of PR #607

---

### PR #607 - Xschem symbols unified to provide instance name without "spiceprefix" (OPEN)
**Status**: Open  
**Author**: KrzysztofHerman  
**Date**: July 18, 2025 - Present  

**Key Changes**:
- Unifies xschem symbols to NOT have `spiceprefix` in the displayed name
- Cleans up `lvs_format` entry to not have `spiceprefix`
- Cancels PR #605
- **Files Changed**: 21 files (23 additions, 23 deletions)

**Major Discussion Points**:

1. **Tool Compatibility Issues** (@d-m-bailey):
   - KLayout expects device names with standard SPICE prefixes (`M` for MOSFETs, etc.)
   - ngspice models are defined as subcircuits, requiring `X` prefix
   - Sky130 PDK uses magic extraction rules to extract as `X` devices
   - Question raised: Should IHP-sg13g2 use the `lvs` variant of tech file for consistency?

2. **3-Terminal Devices Problem** (@d-m-bailey, @RTimothyEdwards):
   - Magic extraction with `lvs` variant doesn't support 3-terminal capacitors/resistors and 4-terminal bipolar devices
   - CDL format for 3-terminal resistors/capacitors: `C0 TOP BOTTOM rfcmim $SUB=VSS`
   - This syntax violates standard SPICE and creates unsimulatable netlists
   - KLayout has special processing for these devices, but other tools may break

3. **Netlist Format Strategy** (@d-m-bailey):
   - Proposed two separate netlists:
     - Simulation netlist: devices as `X` subcircuits (ngspice compatible)
     - CDL netlist for LVS: devices with standard prefixes (M, D, Q, C, R)
   - Would require both `format` (simulation) and `lvs_format` (LVS) in symbols
   - May need both `spiceprefix` and `lvs_spiceprefix` variables

4. **Industry Standards Debate** (@RTimothyEdwards):
   - Strong criticism of "CDLisms" that create unsimulatable netlists
   - Industry practices that introduce incompatibilities with standard SPICE simulators

**Current Status**: Ongoing discussion, no resolution yet

---

### PR #669 - Fixing LVS problems (OPEN)
**Status**: Open  
**Author**: p-fath  
**Date**: September 2 - October 1, 2025  

**Key Changes**:
- Fixed LVS issues with (2+1)-terminal resistors (rppd, rsil, rhigh)
- Updated symbols with proper LVS_format for 2-terminal extraction
- Added LVS_format for spice extraction without spiceprefix for HBT (npn13g2) and cap_cmim devices
- **Files Changed**: 6 files (6 additions, 2 deletions)

**Problem Statement**:
- Current LVS implementation didn't work with (2+1)-terminal resistors due to `sub!` terminal
- Opted to update symbols rather than fix LVS script (considered more complicated)
- Ensured compatibility with existing LVS implementation

**Discussion**:
- @sergeiandreyev asked if devices should include LVS/CDL prefix in `lvs_format` attribute
- Waiting for guidance from @KrzysztofHerman on proper approach

**Significance**: Addresses practical LVS failures with specific device types

---

### PR #681 - Change spice netlist prefix for extracted circuits (OPEN)
**Status**: Open  
**Author**: FlinkbaumFAU  
**Date**: September 11 - October 1, 2025  

**Key Changes**:
- Changes prefix for extracted circuits from default to `X`
- Affects devices like sg13_lv_nmos
- **Files Changed**: 1 file (22 additions, 22 deletions)
- Fixes issue #680

**Rationale**:
- Devices are defined as `.subckt` not as models
- Prefix should be `X` so extracted netlists can be used for simulation

**Discussion**:
- @sergeiandreyev: Cannot be approved due to CDL-based KLayout LVS implementation
- @d-m-bailey: Reiterates need for two netlists (simulation and LVS)
  - Xschem should generate both ngspice-compatible simulation netlist (with `X` devices) and CDL netlist for LVS (with standard prefixes)
  - Most xschem device models may need 2 formats: `format` for simulation and `lvs_format` for LVS
  - May need both `spiceprefix` and `lvs_spiceprefix`

**Current Status**: Blocked pending resolution of dual-netlist strategy

---

## Key Stakeholders and Their Positions

### @KrzysztofHerman (IHP-GmbH)
- Initiated the spiceprefix mechanism in PR #132
- Driving the unified approach in PR #607
- Decision-maker on the proper approach for the PDK

### @d-m-bailey (Contributor)
- Advocates for dual-netlist approach (simulation vs. LVS)
- Concerned about tool compatibility across KLayout, magic/netgen, and Calibre
- Strong voice for practical solutions that work across the ecosystem

### @RTimothyEdwards (magic/netgen maintainer)
- Critical of CDL syntax that violates SPICE standards
- Advocates against unsimulatable netlists
- Willing to patch magic for CDL compatibility but disapproves of the approach

### @sergeiandreyev (IHP-GmbH)
- Reviewing PRs and coordinating discussions
- Seeking consistency across device implementations

### @FaragElsayed2 (IHP-GmbH)
- Involved in KLayout LVS implementation decisions

## Technical Challenges

### 1. Subcircuit vs. Primitive Devices
- **Issue**: IHP models use `.subckt` (require `X` prefix) but LVS tools expect primitives (M, D, Q, etc.)
- **Impact**: Single netlist cannot satisfy both simulation and LVS requirements

### 2. 3-Terminal Capacitors/Resistors
- **Issue**: SPICE doesn't support 3-terminal C/R; CDL uses comment syntax `$SUB=VSS`
- **Impact**: Creates unsimulatable netlists; different tools handle differently

### 3. Tool Ecosystem Compatibility
- **KLayout**: CDL-based LVS, expects standard prefixes, special handling for 3-terminal devices
- **magic/netgen**: Can be patched for CDL, but preference for standard SPICE
- **ngspice/Xyce**: Require subcircuit format for IHP models
- **Calibre**: Commercial CDL format
- **CVC-RV**: Requires consistent CDL format

### 4. Pin Order Issues
- Switching device pin orders (e.g., anode/cathode for diodes) breaks downstream tools

## Proposed Solutions

### Dual-Netlist Approach (Most Discussed)
**Concept**: Generate two separate netlists from xschem:
1. **Simulation netlist**: Uses `X` prefix, ngspice/Xyce compatible
2. **LVS netlist**: Uses standard prefixes (M, D, Q, C, R), CDL compatible

**Implementation Requirements**:
- `format` attribute for simulation
- `lvs_format` attribute for LVS
- Potentially `spiceprefix` and `lvs_spiceprefix`
- Scripts to convert between formats if needed

**Status**: Conceptual consensus but not yet implemented

### Magic LVS Variant
**Concept**: Use magic's `lvs` variant tech file to extract with standard prefixes
**Issues**: 
- Doesn't support 3-terminal devices
- May not match KLayout extraction

## Current State and Recommendations

### Open Issues
1. No consensus on unified approach across all PRs
2. Three PRs (#607, #669, #681) remain open and unmerged
3. Inconsistency in how different devices handle spiceprefix/lvs_format
4. Tool compatibility remains a blocking issue

### Recommended Next Steps
1. **Define PDK Strategy**: IHP should decide on official netlist generation strategy
   - Single netlist with workarounds, or
   - Dual netlists for simulation and LVS

2. **Document Standards**: Create clear guidelines for:
   - When to use `spiceprefix` vs. omit it
   - How to define `lvs_format`
   - Expected behavior for each device type

3. **Test Across Tools**: Validate chosen approach works with:
   - xschem netlist generation
   - ngspice simulation
   - KLayout LVS
   - magic/netgen LVS
   - Any other tools in the flow

4. **Resolve PR #607**: This is the most comprehensive change and needs resolution
   - Either merge with modifications, or
   - Close and define alternative approach

5. **Address 3-Terminal Devices**: Decide on official handling:
   - Accept CDL comment syntax and patch tools, or
   - Use subcircuit wrapper approach, or
   - Different approach for simulation vs. LVS

6. **Standardize All Symbols**: Once approach is decided, ensure consistency across all 43+ symbols

## Impact Assessment

### If Merged As-Is
- **PRs #607, #669, #681**: Would require users to manually add correct prefixes to device names
- LVS compatibility with KLayout may break
- Simulation compatibility with ngspice would improve
- Inconsistency across tools would persist

### If Dual-Netlist Approach Implemented
- More work required in xschem symbol definitions
- Better compatibility across entire tool ecosystem
- Clearer separation of concerns (simulation vs. verification)
- Follows patterns from successful PDKs like Sky130

## Timeline
- **June 2024**: PR #132 merged, introducing spiceprefix
- **July 2025**: PRs #605 and #607 opened, debate begins
- **September 2025**: PRs #669 and #681 opened, issues escalate
- **Present**: Three PRs remain open, no clear resolution path

## Conclusion

The spiceprefix and lvsformat issues in IHP-Open-PDK represent a fundamental challenge in balancing compatibility between simulation tools (which require subcircuit-based models) and LVS tools (which expect primitive device prefixes). The community has identified the problem and proposed solutions, but implementation requires:

1. A clear decision from IHP on the preferred approach
2. Consistent implementation across all device symbols
3. Comprehensive testing across the tool ecosystem
4. Clear documentation for users

The dual-netlist approach appears to have the most support among contributors as it provides the cleanest separation between simulation and verification requirements, though it requires more upfront work in the PDK development.

---

*Document generated: 2025-11-21*  
*Pull Requests reviewed: #132, #605, #607, #669, #681*  
*Status: 3 PRs open, 2 PRs closed*
