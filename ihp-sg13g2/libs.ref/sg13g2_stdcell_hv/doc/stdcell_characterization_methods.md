---
title: "Standard-Cell Characterization Methods for sg13g2_stdcell_hv"
subtitle: "fo4.py (reference) · CharLib 2.1.0 · lctime 0.0.26 — the measurement physics behind the Liberty file, and the cells no characterizer reaches"
author:
  - "Koen Van Caekenberghe, Ph.D."
  - "ChipDesign B.V."
  - "[info@chipdesign.be](mailto:info@chipdesign.be)"
date: "2026-08-20 (rev. 4: all three PVT corners characterized; howto and corner-flow failure modes)"
logo: "ChipDesign_logo.png"
---

# Scope and headline result

Three tools touched the `sg13g2_stdcell_hv` Liberty file, in three different
roles:

* **`work/fo4.py`** — the *reference anchor*: a 96-line ngspice deck that
  measures the FO4 delay and the input capacitance of the thick-oxide
  `inv_1` against the thin-oxide original. Its two ratios (2.66× delay,
  2.20× capacitance) set the slew and load grids of the shipped library,
  and its rail-biased AC capacitance (5.87 fF) is the reference every other
  capacitance number in this report is judged against.
* **CharLib 2.1.0** (commit `6859faf`, driven through the `infinitymdm`
  PySpice 1.6 fork) — the *production characterizer* that generated the
  shipped NLDM tables, configured with the `charge_integration` input-
  capacitance procedure and, for the sequential cells, the project's own
  `seq_delay_procedure.py` registered through CharLib's procedure registry.
* **lctime 0.0.26** (LibreCell) — the *independent cross-check*:
  `work/lctime_compare.py` re-characterized eight combinational cells on
  identical grids and models and aligned 3 132 table points against the
  shipped library.

Every method claim below was verified in the installed source of the three
tools (file and line references throughout; a provenance appendix closes the
report). The comparison in one table, before the derivations:

| quantity | fo4.py (reference) | CharLib 2.1.0 as configured | lctime 0.0.26 |
|---|---|---|---|
| delay / slew load | four real inverter gates | lumped capacitor | lumped capacitor |
| stimulus ramp | shaped by a driver stage | PWL, stretched by 1/0.6 (Liberty-correct) | PWL equal to the raw slew number (**convention error**) |
| extraction | ngspice `.meas trig/targ` | ngspice `.meas trig/targ` | numpy interpolation of waveforms |
| input capacitance | AC at 1 MHz, rail-biased, mean of both rails | charge integration, worst edge | constant-current slope 10 µA, 20–80 % window |
| `inv_1` C~in~ result | 5.87 fF | 6.44 fF (+9.7 %) | 8.92 fF (+52 %) |
| internal power | not measured | **not implemented in CharLib 2.1.0** | rectangle-rule energy integration (load energy not subtracted) |
| leakage | not measured | DC operating point per input state, all 2^N^ states | **unimplemented stub** |
| setup / hold | — | pass/fail bisection, 1.5× C2Q degradation (local procedure) | Brent root-finding, 10 ps absolute pushout |
| clock→Q | — | local procedure (upstream is a stub) | implemented; constraint search at zero output load |
| simulator coupling | `ngspice -b` batch | libngspice in-process (shared) | ngspice subprocess, ASCII `wrdata` |

**Answer to the standing question — can lctime use CharLib's
charge-integration method?** Not as shipped: lctime 0.0.26 contains no code
path that integrates a current anywhere (no `trapz`, no `cumsum`, no ngspice
`integ` in any generated `.control` block). Its input capacitance is a
constant-current secant slope, which is where its +52 % error comes from.
However, lctime's simulator coupling *already* returns branch currents with
the time vector — it integrates supply and gate current for its
internal-power tables — so a charge-integration capacitance is a localized,
three-part patch to one function. Section 8 gives the exact changes.

# What the Liberty NLDM asks for

All three tools ultimately serve the same data model, so the definitions
come first. The library header fixes eight trip points; the shipped file
uses the industry-standard set

$$V_{th,in} = V_{th,out} = 0.5\,V_{DD}, \qquad V_{slew,lo} = 0.2\,V_{DD}, \qquad V_{slew,hi} = 0.8\,V_{DD}$$

and defines, per timing arc, the propagation delay and the output transition
time as threshold-crossing intervals of the simulated waveforms:

$$t_{pd} = t\left(v_{out} = 0.5\,V_{DD}\right) - t\left(v_{in} = 0.5\,V_{DD}\right)$$

$$t_{tran} = t\left(v_{out} = 0.8\,V_{DD}\right) - t\left(v_{out} = 0.2\,V_{DD}\right)$$

(rising conventions shown; falling edges mirror the thresholds). The NLDM
`cell_rise` / `rise_transition` groups tabulate these two quantities as
functions of two independent variables,

$$t_{pd} = f\left(s_{in},\, C_L\right), \qquad t_{tran} = g\left(s_{in},\, C_L\right),$$

where $s_{in}$ is the *input* transition time measured between the same
20 %/80 % slew thresholds, and $C_L$ the lumped load. The shipped library
uses 7×7 grids per arc; the grid values are the thin-oxide library's grids
scaled by the fo4.py ratios so the tables span the same electrical
territory. Everything a characterizer does for a combinational arc reduces
to filling $f$ and $g$ point by point from transient simulations, and every
methodological difference between the three tools is a difference in
*stimulus construction*, *load modelling*, or *waveform extraction* for
those same two equations.

A physical scale for the delays themselves comes from logical effort: with
$\tau = R_{inv} C_{in}$ the technology time constant, a stage driving an
electrical effort $h = C_{out}/C_{in}$ has normalized delay

$$d = g\,h + p,$$

and the fanout-of-4 inverter delay ($g = 1$, $h = 4$) is the canonical
technology speed metric fo4.py measures directly: $t_{FO4} = \tau\,(4 + p)$.
It is a *ratio-preserving* metric — sizing every cell by the same factors
leaves $g$ and $p$ nearly unchanged — which is exactly why one FO4 number
per library (142.4 ps HV vs 53.6 ps LV) legitimately rescales an entire
grid set.

# Input capacitance: three answers to one question

## The physics being sampled

The input pin of a CMOS gate is not a capacitor; it is a nonlinear,
*transcapacitive* charge reservoir. The gate charge is a function of the
gate voltage **and** of every other terminal voltage, so the differential
capacitance seen while the input traverses its switching trajectory is

$$C_{in}(v) = \frac{dQ_G}{dv_{in}} = C_{gs}(v) + C_{gb}(v) + C_{gd}(v)\left(1 - \frac{dv_{out}}{dv_{in}}\right).$$

The last term is the Miller effect: while the cell switches, the output
moves *against* the input with the incremental gain $A_v = dv_{out}/dv_{in} < 0$,
so $C_{gd}$ contributes $C_{gd}(1 + |A_v|)$ — a sharp peak centred on the
switching threshold $V_M$, where $|A_v|$ is largest. Away from $V_M$, with
the output pinned at a rail, $A_v \approx 0$ and $C_{in}$ relaxes to its
small end-point values.

Every "input capacitance" is therefore a *functional* of $C_{in}(v)$ — a
weighted average over some window of the input swing — and the three tools
choose three different windows. That single observation explains all three
numbers.

## fo4.py: small-signal AC at the rails

fo4.py drives an isolated inverter input with a 1 V AC source at 1 MHz,
once biased at $v = 0$ and once at $v = V_{DD}$
([fo4.py:38–55](../../work/fo4.py)). For a linear one-port
$Y(j\omega) = G + j\omega C$, the measured current at unit drive gives

$$C_{AC} = \frac{\mathrm{Im}\,\{I\}}{2\pi f\,|\hat V|} \qquad \mathrm{(evaluated\ at}\ f = 1\ \mathrm{MHz).}$$

The frequency is chosen so that gate leakage is invisible
($G \ll \omega C$: at 1 MHz, $\omega C \approx 3.7\times10^{-8}$ S for 5.9 fF,
orders above any gate conductance) yet low enough that non-quasi-static
channel effects play no role. The deck comments state the bias rationale
explicitly: at either rail the inverter sits in a zero-gain region, so
$A_v \approx 0$ and the Miller term vanishes —

$$C_{AC} = \frac{1}{2}\left[\,C_{in}(0) + C_{in}(V_{DD})\,\right] \quad \mathrm{(endpoint\ sample,\ no\ Miller).}$$

A mid-rail bias would instead sample the peak of $C_{in}(v)$ and
Miller-multiply $C_{gd}$ into the answer. Result: **5.87 fF** for
`sg13g2_hv_inv_1`.

## CharLib: charge integration

The configured procedure
(`charlib/characterizer/procedures/pin_capacitance/charge_integration.py`)
drives the pin with a PWL *voltage* ramp — VSS up to VDD, wait, back down —
and lets ngspice integrate the stimulus-source branch current over each
edge window:

```spice
.meas TRAN q_rise integ i(vstim) from=... to=...
.meas TRAN q_fall integ i(vstim) from=... to=...
```

then applies the defining relation of effective capacitance
(charge_integration.py:100–135):

$$C_{int} = \frac{|\Delta Q|}{\Delta V} = \frac{1}{V_{DD}}\int_{edge} i_{in}(t)\,dt = \frac{1}{V_{DD}}\int_0^{V_{DD}} C_{in}(v)\,dv.$$

This is the *full-swing mean* of $C_{in}(v)$ along the real switching
trajectory: the Miller charge $Q_M \approx C_{gd}\,(\Delta v_{in} + \Delta v_{out})$
is included in $\Delta Q$, but it is spread over the full denominator
$V_{DD}$. Non-driven pins are isolated with 10 GΩ ∥ 1 pF; the ramp time
defaults to the fastest grid slew and the wait time to 1000× that, so each
edge integrates to completion. The reported `capacitance` is the worst
(larger) of the two edges. Result: **6.44 fF** (+9.7 % vs the AC
reference — that surplus *is* the Miller and nonlinearity charge, not an
error; it is the charge a driving cell genuinely must deliver across a full
transition).

Worth recording: CharLib's *upstream default* is a different procedure,
`ac_sweep`, which fits capacitance as the slope of the admittance
*magnitude* versus frequency, $C = d|Y|/df$. Since $|Y| = 2\pi f C$ for a
capacitor, the correct estimator is $C = \frac{1}{2\pi}\,d|Y|/df$; the
missing $1/2\pi$ makes the default overestimate by ≈ 6.28×, and the
observed 6.8–7.5× (inv_1: 43.8 fF) is exactly $2\pi$ compounded with the
Miller contribution of its mid-transition drive. This is why the project
configuration selects `charge_integration`.

## lctime: constant-current secant slope

lctime does something else entirely
(`lctime/characterization/input_capacitance.py`, docstring: *"Measurement
of the input capacitance by driving the input pin with a constant
current"*). A fixed source $I = 10\ \mu\mathrm{A}$ (hard-coded,
util.py:162) charges the pin; the pin *voltage* alone is recorded; and the
capacitance is the secant slope between the two slew trip points
(input_capacitance.py:273–297):

$$C_{slope} = \frac{I}{\Delta V / \Delta t} = \frac{I\,\left[t(0.8 V_{DD}) - t(0.2 V_{DD})\right]}{0.6\,V_{DD}}.$$

From first principles this is again a windowed mean of the same
$C_{in}(v)$: with $C_{in}(v)\,dv/dt = I$,

$$\Delta t = \frac{1}{I}\int_{0.2 V_{DD}}^{0.8 V_{DD}} C_{in}(v)\,dv \;\;\Rightarrow\;\; C_{slope} = \frac{1}{0.6\,V_{DD}}\int_{0.2 V_{DD}}^{0.8 V_{DD}} C_{in}(v)\,dv.$$

The window $[0.2, 0.8]\,V_{DD}$ *contains* the Miller peak at $V_M$ and
*excludes* the low-capacitance tails near the rails; the Miller charge is
divided by $0.6\,V_{DD}$ instead of $V_{DD}$. Both effects push the same
direction, which orders the three estimators from first principles alone —
the Miller-free endpoint sample below the full-swing mean below the
peak-window mean:

$$C_{AC} \;<\; C_{int} \;<\; C_{slope}$$

— and the measurements land in exactly that order: 5.87 < 6.44 < 8.92 fF,
the slope method **+52 %** above the reference. lctime averages the result
over all 2^n^ static states of the other inputs and over both edge
directions (reduction per calc-mode: mean for `typical`), and carries a
genuine bug while doing so: the returned dictionary swaps the labels,
assigning the falling measurement to `rise_capacitance` and vice versa
(input_capacitance.py:318–321). The default `capacitance` attribute, being
the mean of both, hides the swap.

# Delay and output slew

## Stimulus: the slew convention is where the tools diverge

Liberty defines $s_{in}$ between the 20 %/80 % thresholds. A characterizer
that drives the pin with a single linear ramp of total duration $T$
(0→100 %) realizes a Liberty slew of

$$s = (0.8 - 0.2)\,T = 0.6\,T \qquad\Longleftrightarrow\qquad T = \frac{s}{0.6}.$$

**CharLib gets this right.** Its `slew_pwl` helper (utils.py:49–65,
explicitly citing the Liberty User Guide) stretches the requested slew to
the full ramp, $T = s/(V_{hi}-V_{lo}) = s/0.6$, before building the PWL
source.

**lctime does not.** Its `StepWave` for combinational stimulus is built
with `rise_threshold=0, fall_threshold=1`
(timing_combinatorial.py:186–191), i.e. the table's slew number is used
directly as the 0→100 % ramp time. The circuit therefore sees an edge whose
*Liberty* slew is only $0.6\,s$ — every lctime table point at index $s$ is
actually a measurement at $0.6\,s$. Since $\partial t_{pd}/\partial s_{in} > 0$,
lctime under-reads delays, negligibly at fast edges and severely at slow
ones. The cross-check quantifies it: over the STA-relevant region the two
tools agree to a median 2.9 % on delays and 0.0 % on output transitions
(3 132 points, 8 cells), but at the 3.36 ns slew point of `inv_1`
(0.396 pF) a direct ngspice measurement gives 2.3605 ns where CharLib's
table says 2.3571 ns (**+0.15 %**) and lctime says 1.9158 ns (**−19 %**);
re-interpolating the CharLib table at $0.6\,s$ reproduces lctime to 0.25 %,
nailing the mechanism. Ironically lctime *reads* all eight trip points from
the Liberty template header (util.py:377–398) and measures with them
correctly — only the stimulus construction ignores them.

fo4.py sidesteps the question: its device under test is driven by a real
inverter stage (`Xdrv`), so the edge shape is whatever the technology
produces, and the measured 50 % crossings use ngspice `.meas` with
`rise=2`/`fall=2` — the *second* edge, past the initial-condition
transient, so the measurement is taken in periodic steady state.

## Load modelling

Both characterizers drive a lumped capacitor: $C_L$ to ground on the output
(CharLib delay.py:83; lctime deck `Cload` elements). fo4.py loads the DUT
with **four actual inverter inputs** — nonlinear $C_{in}(v)$ loads that
also kick Miller charge back into the driving node. A lumped capacitor
equal to $4\,C_{in}$ is the NLDM abstraction of that load; the FO4 deck is
the ground truth the abstraction is checked against. This is precisely why
the library's load grid is anchored to a *measured* $C_{in}$ ratio rather
than a nominal one.

Side-input handling differs in a way that shows up in multi-input cells:
CharLib simulates every non-masking static state of the other inputs and
records the **worst case**, `criterion = max` (delay.py:16, 188–190);
lctime enumerates the unateness-consistent states and reduces with the
calc-mode function — `np.mean` under the default `typical` mode
(timing_combinatorial.py:77–81). Two tables built from identical
simulations can therefore legitimately differ on any cell where the arc
delay depends on the side-input state (stack position effects).

## Extraction

fo4.py and CharLib let ngspice do the measurement — `.meas tran ... trig
v(in) val=... targ v(out) val=...` — which interpolates crossings inside
the simulator on the adaptive time grid. lctime post-processes: it
normalizes the stored waveforms to $[0,1]$, mirrors falling edges, and
linearly interpolates the bracketing samples of each threshold crossing in
numpy (util.py:251–374). Both are first-order interpolations of the same
transient; the difference is not accuracy but *plumbing* — and the plumbing
matters, as §7 shows: PySpice's subprocess backend silently drops `.meas`
results, which is why CharLib must run in shared-library mode, while lctime
never uses `.meas` at all and is immune.

# Energy, power, leakage

## The energy bookkeeping a Liberty file expects

Per rising output transition the supply delivers charge
$Q = \int i_{VDD}\,dt$, hence energy

$$E_{supply} = V_{DD}\int i_{VDD}(t)\,dt = V_{DD}\,\Delta Q.$$

Of this, $C_L V_{DD}^2$ is associated with the external load (half stored
on $C_L$, half dissipated in the pull-up network), and the remainder is
*internal*: parasitic-node charging plus the short-circuit (crowbar) charge
that flows while both networks conduct near $V_M$. Liberty's
`internal_power` tables are meant to carry only that remainder, because the
STA tool separately computes the switching energy of the external net from
its own capacitance:

$$E_{int} = V_{DD}\int i_{VDD}\,dt - C_L V_{DD}^2 \quad (\mathrm{rising\ edge}).$$

**CharLib 2.1.0 does not measure internal power at all.** The package
contains no procedure writing `internal_power`, `rise_power` or
`fall_power` — energy appears only as a unit definition — and
`Characterizer.analyse_cell` schedules exactly: pin capacitance, then
delay + leakage (combinational) or the constraint procedures (sequential).
The shipped Liberty consequently has no internal-power groups; any
power-aware flow consuming it sees switching and leakage power only.

**lctime is the only tool of the three that writes power tables**, inside
the same transient as the delay measurement
(timing_combinatorial.py:263–274):

```python
gate_energy   = np.mean(gate_current  * input_voltage) * dt
supply_energy = np.mean(supply_current * vdd) * dt
switching_energy = gate_energy + supply_energy
```

Two defects are visible from first principles. First, the quadrature:
$\mathrm{mean}(f)\cdot(t_N - t_0)$ equals $\int f\,dt$ **only on a uniform
time grid**; ngspice's adaptive stepping clusters points around the edges,
where $i\,v$ is largest, so the sample mean over-weights the transition
region. The unbiased estimator on the same data is the trapezoidal sum
$\int f\,dt \approx \sum_k \frac{1}{2}(f_k + f_{k+1})(t_{k+1}-t_k)$, i.e.
`np.trapz(f, time)` — available but unused. Second, the accounting: no
$C_L V_{DD}^2$ subtraction is performed, so the tabulated "internal" energy
includes the full load-charging energy and grows linearly with $C_L$; an
STA tool then counts that energy a second time as switching power.
Sequential cells get no power tables even from lctime (the supply current
is retrieved in the FF harness but never integrated).

## Leakage

Static power is a per-state quantity because subthreshold leakage depends
exponentially on the bias of every device in a stack,

$$I_{leak} \propto e^{\left(V_{GS}-V_{th}\right)/n V_T}\left(1 - e^{-V_{DS}/V_T}\right),$$

so a NAND2 leaks differently in each of its four input states (stack
effect). CharLib does the canonical thing: one DC operating point per input
combination, all $2^N$ of them, with

$$P_{leak}(\mathrm{state}) = V_{DD}\,\left|I_{VDD}(\mathrm{state})\right|$$

read from the supply branch (leakage_power.py:67, 86–91), emitting one
conditioned `leakage_power { when : ... }` group per state. lctime's
`characterize_leakage_power` is an empty stub, never called — no leakage
data at all. For the sequential cells (which CharLib's combinational-branch
leakage never reaches, and which have no unique DC operating point anyway),
the project's `seq_leakage.py` measures a *transient average* instead: a
reset pulse forces a known state, then
$P = V_{DD}\,|\overline{i_{VDD}}|$ with the mean taken by `.meas tran AVG`
over the settled window 40–60 ns — a documented single-state
approximation.

# Sequential constraints

## The physics: pushout

As the data edge approaches the clock edge, a flip-flop's internal
regeneration starts from an ever-smaller initial imbalance and the
clock-to-Q delay diverges logarithmically (regeneration time constant
$\tau_m$ of the cross-coupled pair):

$$t_{C2Q}(t_{su}) \approx t_{C2Q,\infty} + \tau_m \ln\frac{t_0}{t_{su}-t_{su}^{*}}.$$

A setup (hold) constraint is therefore not a hard edge but a chosen point
on this curve, and every characterizer must pick a *criterion*: how much
delay pushout $\Delta d = t_{C2Q} - t_{C2Q,\infty}$ is tolerable. Inverting
the curve shows how the criterion maps to the constraint:

$$t_{su}(\Delta d) = t_{su}^{*} + t_0\,e^{-\Delta d/\tau_m},$$

so a tighter (smaller) $\Delta d$ yields a larger, more conservative setup
time — but only logarithmically slowly, which is why differing criteria
still produce comparable libraries.

## CharLib: what is stock and what is local

Stock CharLib 2.1.0 is largely unimplemented here: the sequential *delay*
procedure returns immediately (`delay.py:14–15`, a `# TODO` stub), as do
recovery, removal, min-pulse-width and the metastability binary search. Its
one working constraint procedure is the C2Q *contour* method (per the
setup/hold-interdependence literature): reference C2Q at a relaxed corner,
validity criterion $t_{C2Q} \leq 1.2 \times t_{C2Q,ref}$, exponential
bracketing plus binary search for the window edges, then an N×N sweep of
the (setup, hold) rectangle and knee-point selection on the pass contour.
On these HV cells the contour harness built transients that exhausted
memory, so the shipped library uses the project's procedures
(`seq_delay_procedure.py`, registered through CharLib's own registry):

* **clock→Q**: preload pulse, data switch mid-period, measured clock edge
  at the grid slew; ngspice `.meas` from the clock's 50 % crossing
  (second rise) to the output's 50 % crossing, 20–80 % output transition;
  tables indexed clock-slew × load.
* **setup/hold**: pass/fail **bisection** on a two-pulse harness, search
  range −2…+8 ns, tolerance 10 ps. The pass criterion is deliberately
  two-part: the output must reach the target final state **and** its first
  half-rail crossing must occur within $1.5 \times$ the nominal C2Q
  ($\Delta d = 0.5\,t_{C2Q,\infty}$, a *relative* degradation criterion) —
  final-state-only acceptance would silently ride through metastability.
  Latches are constrained against the closing enable edge; non-convergence
  counts as fail.

## lctime

lctime's sequential path is genuinely implemented and more mathematically
polished: it measures the pushout curve itself. `find_min_data_delay`
doubles the setup/hold window until $t_{C2Q}$ converges to
$t_{C2Q,\infty}$ (abstol 1 ps); the constraint is then the root of

$$t_{C2Q}(t_{su}) - \left(t_{C2Q,\infty} + \Delta d\right) = 0,$$

with $\Delta d = 10$ ps (the default `max_pushout_time`), found with
Brent's method (`optimize.brentq`, xtol = 1 fs) after exponential
bracketing — an *absolute* pushout criterion, in contrast to
CharLib-local's relative one. It then re-solves setup with hold fixed at
its unconditional minimum plus a 10 ps margin (and vice versa), which is
what populates the constraint tables. Min-pulse-width uses the same
root-finding on a two-pulse harness. Caveats visible in the source: the
constraint search runs at **zero output load** (flagged `# TODO` in
flipflop.py:196), clk→Q tables are taken at a fixed generous
setup = hold = 1 ns rather than the measured constraints, and **latches are
not supported at all** (main_lctime.py aborts) — where the shipped library
needed en→Q and closing-edge constraints for its five latches.

For this library's C2Q of a few hundred ps, CharLib-local's
$\Delta d = 0.5\,t_{C2Q,\infty}$ (∼100+ ps) versus lctime's 10 ps sit far
apart on the pushout curve, yet by the logarithmic inversion above the
extracted constraints differ only by $\tau_m \ln(\Delta d_1/\Delta d_2)$ —
a few regeneration time constants, i.e. tens of ps. The bigger structural
difference is coverage: only the local CharLib procedures produced latch
data at realistic loads.

# Numerics and simulator coupling

All three tools run the same engine — ngspice with the IHP OSDI-compiled
PSP103 Verilog-A MOS models — through three different couplings, and two of
the project's hardest-won findings are couplings, not physics:

| | fo4.py | CharLib | lctime |
|---|---|---|---|
| coupling | `ngspice -b` batch | libngspice in-process (PySpice fork) | subprocess, ASCII `wrdata` |
| `.meas` support | native | fork-added; **lost in subprocess mode** | not used |
| integration method | trapezoidal (default) | trapezoidal, `trtol = 1` | trapezoidal (no options set) |
| timestep | 20 ps fixed print step | slew/8 (delay), slew/10 (cap) | 10 ps default, `stop when` breakpoints |
| stop condition | fixed 3 periods | `autostop` on `.meas` completion | breakpoint at 1 %/99 % V~DD~ |
| OSDI model loading | `.spiceinit` (batch honors it) | `.spiceinit` copied into run dir | `.spiceinit` copied by compare script |
| temperature | deck value | 25 °C | **hard-coded 25 °C** (liberty header ignored) |

The trapezoidal rule's local truncation error per step,
$\varepsilon \approx \frac{h^3}{12}\,\left|d^3v/dt^3\right|$, is what ngspice's
timestep control bounds; `trtol` scales the tolerance it is compared
against, so CharLib's `trtol = 1` (versus the default 7) forces
$\approx 7^{1/3} \approx 1.9\times$ finer steps through the transitions —
a deliberate accuracy/runtime trade in the delay decks.

The two coupling landmines, both documented in `run_charlib.sh` and the
config generator because both produce *silently* wrong libraries: (1) with
the `ngspice-subprocess` backend PySpice parses only the rawfile and never
reads measurement results back, so every delay table comes back empty while
leakage and capacitance still populate — the file looks plausible until a
timing tool finds no arcs; shared mode is mandatory. (2) ngspice reads
`.spiceinit` in batch and interactive mode but *not* in server mode
(`ngspice -s`), so PySpice-driven runs never load the OSDI PSP103 models
without the project's `pre_osdi` shim. lctime's file-based batch backend is
immune to both by construction — its weakness is instead that it sets no
simulator options at all and inherits whatever `.spiceinit` the working
directory supplies, and that it stamps `.option TEMP=25` regardless of the
library header (the `nom_temperature` it parses is never propagated;
characterizing a non-25 °C corner silently produces 25 °C data).

# Can lctime use the charge-integration method?

**As shipped in 0.0.26 — no.** The verdict rests on three code facts:

1. The input-capacitance procedure is irreducibly the constant-current
   slope method: it drives the pin from a current source, records *only*
   the pin voltage (`output_currents=[]`,
   input_capacitance.py:253–257), and computes
   $C = I\,\Delta t / \Delta V$ from two threshold crossings
   (lines 273–297). There is no charge in sight.
2. No code path in the package integrates a current: a search over the
   installed tree finds no `trapz`/`cumsum` and no ngspice `integ` in any
   generated control block.
3. The 10 µA source magnitude is a hard-coded constant (util.py:162), not
   reachable from the CLI — so even the existing method cannot be tuned,
   let alone replaced, by configuration.

**But the port is small, because the data path already exists.** For its
power tables lctime already requests branch currents through named voltage
sources and gets them back aligned with the time vector — both backends
implement it (`wrdata ... i(vpin)` file-based; `print i(vpin)`
interactive) — and the combinational routine already retrieves the *gate*
current `-currents["V<pin>"]` for its energy term. Charge-integration
capacitance is the same measurement pointed at a different source. The
patch, confined to `characterize_input_capacitances()`:

1. **Drive voltage, not current**: declare the active pin as a voltage
   input and replace the `I<pin>` PWL current source with the `StepWave`
   ramp the delay code already uses (using the Liberty-correct
   $T = s/0.6$ stretch while at it).
2. **Ask for the current**: `output_currents=["V<pin>"]` instead of the
   empty list.
3. **Integrate**: replace the secant-slope block with

$$Q = \int_{edge} i_{pin}(t)\,dt \;\approx\; \mathtt{np.trapz}(-i_{V pin},\,t), \qquad C = \frac{|Q|}{V_{DD}},$$

   using the trapezoidal sum (not the rectangle rule the power code uses)
   since the time grid is adaptive.

Nothing else in the harness changes — grids, state enumeration, reduction,
and Liberty emission all operate on the returned scalar. On the evidence of
this library, the payoff is the difference between +52 % and +9.7 % on
`inv_1`'s pin capacitance, i.e. between a wire-load estimate that is wrong
by half and one within the Miller-charge ambiguity that any single-number
capacitance carries. (lctime is AGPL-3.0-or-later; a modified copy used
in-house carries no distribution obligation, and an upstream contribution
would resolve the license question entirely while fixing the rise/fall
label swap noted in §3.)

# Provenance of the shipped Liberty: no lctime data

A natural question given three tools: which of them actually populated
`lib/sg13g2_stdcell_hv_typ_3p30V_25C.lib`? The answer is that every number
in the shipped file traces to the CharLib flow, and **none to lctime**:

| Liberty content | produced by |
|---|---|
| combinational `cell_rise/fall`, `rise/fall_transition` tables | CharLib 2.1.0 (`run_charlib.sh`), post-processed by `fix_lib.py` |
| pin `capacitance` / `rise_capacitance` / `fall_capacitance` | CharLib `charge_integration` procedure |
| per-state `leakage_power` groups (combinational) | CharLib all-states DC enumeration |
| clk→Q and en→Q arcs, setup/hold constraint tables | local `seq_delay_procedure.py` inside CharLib's registry, merged by `merge_lib.py`, fixed by `fix_lib_seq.py` |
| sequential and tie-cell `cell_leakage_power` | local `seq_leakage.py` / `tie_leakage.py` (transient average) |
| slew and load index grids | thin-oxide grids × the fo4.py ratios (2.66 delay, 2.20 capacitance) |
| functions, pin directions, `ff`/`latch` groups | lifted from the thin-oxide Liberty (logic unchanged by the transform) |

lctime's role was strictly read-only verification: `lctime_compare.py`
re-characterizes eight combinational cells on the same grids and models and
compares its output *against* the shipped tables — the 2.9 % median delay
agreement, the −19 % slew-convention band and the +52 % pin-capacitance
finding of the preceding sections are all products of that comparison, and
none of its data flows back. Given what the comparison revealed about the
slope-method capacitance (§3) and the slew convention (§4), that
separation is the correct engineering outcome, not an accident of history.
A text search of the shipped file confirms it carries no lctime or
LibreCell traces.

# Cells outside every characterizer's model

Nine of the 84 cells are drawn but could not be characterized by either
tool, and in every case the obstacle is the characterizer's data model
rather than anything about the cell. Seven of the nine — `sighold` and the
6 tri-states — are measured directly instead and do ship Liberty data
(sections 10.1 and 10.2); the 2 clock gates are still in progress
(section 10.3). The three mechanisms are worth separating, because only one of them
announces itself.

**No high-impedance state (the 6 tri-states).** CharLib's cell schema
(`charlib/config/syntax.py:30-120`) has keys for `inputs`, `outputs`,
`functions`, `clock`, `enable`, `set`, `reset`, `state` — and nothing for
`three_state` or a Hi-Z output value. A search of the entire installed
package for `high.?impedance|high-?z|hiz|three.?state` returns exactly one
hit, a comment on `Port.Role.ENABLE`. So a tri-state cell cannot be
expressed. What makes this the dangerous case is that
`gen_charlib_config.py` does *not* skip these cells: `Z` has a `function`
(`A` or `!(A)`), `TE_B` is collected as an ordinary input, and the cell is
configured as a two-input combinational gate whose output ignores one
input. CharLib then emits an empty result, `omit_on_failure` swallows it,
and **the run log never mentions the cell**. This is the same silent-failure
class that once hid all 14 sequential cells.

**No statetable (the 2 clock gates).** `lgcp_1` and `slgcp_1` hold state in
a `statetable` with an `internal` pin, not in an `ff`/`latch` group.
CharLib has no input form for that, so `gen_charlib_config.py:136-142`
skips them explicitly, with a stated reason — the honest failure mode.

**No output pin (`sighold`).** The bus holder's only signal pin is an
`inout`, so the configurator's "no output pin" branch drops it, together
with the genuinely arc-less fill/decap/antenna cells.

**lctime does not rescue any of them.** It *is* tri-state aware — it reads
`three_state` into `CombinationalOutput(high_impedance=...)` and writes the
attribute back out — but its characterization deliberately pins the enable
to its active value (`constant_input_pins`, "Skip measuring the tri-state
enable input") and characterizes only the data arc. The enable arcs, which
are most of what a tri-state Liberty group contains, are exactly what it
omits. For clock gates it has nothing: no `clock_gating_integrated_cell`,
no statetable, and its sequential recogniser bails on tri-state outputs
outright.

The answer is the one the tie cells and the sequential constraints already
use: measure directly against the shipped netlist with ngspice, and emit
the Liberty groups from the measurements.

## A fourth answer to the capacitance question: the bus holder

Section 3 compared three ways of averaging $C_{in}(v)$. `sighold` adds a
case where one of them is not merely different but **invalid**.

Charge integration — the production method for gate pins, and the
defensible one there because it measures the charge a driver actually
delivers — assumes the integrated current is the charge that ends up on
the pin capacitance. On a bus holder it is not: the keeper actively fights
the driver until the internal inverter flips, and that crowbar charge
lands in the same integral. It is therefore not a property of the cell.
Measured on the shipped netlist, integrating the driven edge:

| driving edge | 0.2 ns | 0.5 ns | 1 ns | 2 ns | 5 ns |
|---|---|---|---|---|---|
| rise charge | 30.5 fC | 38.1 fC | 46.3 fC | 58.4 fC | 86.4 fC |

A monotone 2.8× spread across a plausible range of driver strengths. Any
single point reported as `capacitance` would silently encode an arbitrary
assumption about whatever drives the net.

The rail-biased AC method of section 3.2 has no such coupling, because it
never asks the keeper to lose: at a fixed bias the keeper is in a defined
state and the small signal sees only the physical capacitance.
Four bias points near the rails give 0.00377 / 0.00378 / 0.00353 /
0.00361 pF — a 7 % spread, and consistent with the ~2.1 fF of gate area
plus junction contributions. Mid-rail is excluded on purpose: the
cross-coupled pair has gain there and the small-signal result is
meaningless.

This also explains the thin-oxide library's `sighold`, which reports
0.0268 pF rising against 0.0096 pF falling — a 2.8× asymmetry with no
structural cause, since the physical capacitance of a node has no
direction. It is a fight-charge artifact of whatever transient method
produced it. The thick-oxide cell therefore ships equal rise and fall
values, with the keeper fight-back charge documented separately as the
driver-dependent quantity it is.

The leakage numbers land where the rest of the library's do: 0.0118 nW
holding high and 0.0224 nW holding low, roughly $10^4$ below the
thin-oxide cell, the same ratio the tie cells show and for the same reason
— 0.45–0.70 µm channels under a thick oxide.

## Tri-states: three arcs, and one that cannot be measured as specified

A tri-state cell needs three arc classes rather than one: the
`combinational` data arc — which either tool could produce, and which is
measured here exactly as for any other gate — plus `three_state_enable`
and `three_state_disable`, which are distinguished from ordinary delays by
measuring *into* and *out of* a floating state. `ebufn` carries four
tables per enable arc; `einvn` uses the `_rise` variants and carries two.
All six cells are characterized by `work/char_tristate/char_tristate.py`;
the harness is
calibrated by re-measuring a shipped cell's pin capacitance
(`sg13g2_hv_buf_4` pin A) through the same code path and requiring
agreement with the shipped library — it lands at **0.46 %**.

The **enable** arc is straightforward once the floating node is defined:
the output starts in Hi-Z held by the 1 GΩ mid-rail keeper the functional
suite already uses for its 12 Hi-Z checks, `TE_B` switches, and the
measurement is the usual 50 %-to-50 % delay and 20/80 transition into the
specified load.

The **disable** arc is where the specification breaks down. The obvious
recipe — wait for the output to leave its driven level through the slew
threshold — is not physically measurable on a capacitively loaded Hi-Z
node. Once the driver releases, nothing but the keeper moves the node, so
the answer is $0.2\,RC \approx 0.5$ ms and is *exactly proportional to the
load*. No keeper value repairs this: to make the decay comparable with the
turn-off time it would have to approach the cell's on-resistance (~1 kΩ),
at which point the keeper fights the enabled driver and the cell can no
longer hold its own output.

The thin-oxide library cannot have measured it that way either, and its
own tables say so: its disable entries are *exactly* load-independent,
the seven values along the load axis differing only by a 1 fs increment —
a monotonicity epsilon, not a measurement.

What is measured instead is the quantity that actually goes away: the
drive current. `Z` is held by an ideal source at the slew threshold it
would cross on leaving the driven level (0.66 V driving low, 2.64 V
driving high), the on-state drive current $I_{on}$ is recorded (0.56 /
0.60 mA for `ebufn_4`), and the arc is the time from `TE_B` crossing 50 %
to $|I_Z|$ falling through $I_{on}/2$ — the same 50 % convention used
everywhere else in this library, applied to current rather than voltage.
This is load-independent by construction, so the seven rows are identical
with **no synthetic epsilon**, and the transition tables repeat the delay
because nothing traverses a slew after release (as the thin-oxide library
also does).

### What the ratios say

| cell | comb. c~r~/c~f~ | enable c~r~/c~f~ | disable c~r~/c~f~ |
|---|---|---|---|
| `ebufn_2` | 2.22 / 3.01 | 2.02 / 1.92 | 1.48 / 2.10 |
| `ebufn_4` | 2.21 / 2.93 | 2.01 / 1.87 | 1.46 / 2.03 |
| `ebufn_8` | 2.20 / 2.93 | 2.00 / 1.80 | 1.52 / 1.87 |
| `einvn_2` | 2.11 / 2.74 | 2.00 / – | 1.47 / – |
| `einvn_4` | 2.11 / 2.74 | 2.00 / – | 1.49 / – |
| `einvn_8` | 2.09 / 2.73 | 1.98 / – | 1.53 / – |

Median over load points 2–7 against the thin-oxide library; the expected
band is the library's 2.66× delay ratio ±20 %. Load point 1 is excluded
because the thin-oxide tri-states offset their load axis by the `Z` pin
capacitance (0.0098 pF rather than 0.001), so at that point the HV cell
carries a 10× lighter load than its reference.

The **combinational** arcs are in band. The **enable** delays sit at
1.8–2.0, just under it — but the denominator is the problem, not the
measurement: the thin-oxide enable tables are *clamped* at their fast end
(`ebufn_4` repeats 0.074755, 0.074756, 0.074757, 0.074758 — a 1 fs floor
rather than four measurements). The enable *transitions*, which are the
same physical quantity as the combinational transitions that do agree,
come out at 2.25–2.28, in band.

The **disable** ratios (1.46–1.53) are out of band **by construction**,
because the criterion differs from whatever produced the thin-oxide
numbers. They are reported rather than tuned. Their tight clustering
across two footprints and three drive strengths is what a consistent
criterion offset looks like; noise would not cluster.

### Two infrastructure defects found on the way

Worth recording because both would have produced plausible numbers:

* The mid-rail keeper used to define the floating node was left attached
  during **leakage** measurement, where it sourced its own 1.65 nA into
  the supply reading — a fictitious 5.48 nW on `ebufn_2` in the
  `A & !TE_B` state, **150× the true value**. The keeper now exists only
  where the node actually floats. A leakage number that is 150× wrong is
  still a perfectly plausible-looking leakage number.
* ngspice must run with `OMP_NUM_THREADS=1` here. Its spinning OpenMP
  barriers burned 130+ CPU-seconds without completing on a contended
  machine, against ~4 CPU-seconds to completion single-threaded.

## Clock gates

The clock gates need a `CLK`→`GCLK` propagation arc (which the thin-oxide
library writes with *no* `timing_type` at all, i.e. combinational),
`setup_rising`/`hold_rising` on the enable pins against the clock — the
form the local bisection procedure of section 6.2 already emits — and a
`min_pulse_width` constraint on the clock pin, obtained by bisecting the
clock pulse until the gated output fails to produce a full-swing pulse.
CharLib has a config slot for `min_pulse_width_constraint_procedure` but
never calls it; its dispatch is a `# TODO`.

Both cells are now measured, by `char_clockgate/char_clockgate.py`.
`sg13g2_hv_lgcp_1` ships as `latch_posedge` with 4 timing groups and 3
leakage states; `sg13g2_hv_slgcp_1` as `latch_posedge_precontrol` with 6 of
each, the extra pair being setup/hold on `SCE`. Two results are worth
recording because neither is an artifact of the method:

* **The two cells are indistinguishable on the clock path.** Their
  `min_pulse_width` vectors are identical point for point (0.462561,
  0.625607, 0.792817, 0.974794 ns) and their CLK→GCLK delays differ only in
  the 4th–6th digit (0.152337 vs 0.152298 ns at the first grid point). This
  is physically right — the scan leg loads the *enable* path, not the clock
  path — and the difference is far below the 0.01 ns bisection tolerance,
  so both land on the same value. It is documented rather than hidden,
  because a user comparing the two cells in an STA report will see it.
* **The min-pulse-width search must be forced to bracket.** An early run
  emitted the bisection's own 48 ns upper bound as if it were measured
  data: the search never bracketed, and returning the bound produced a
  number that was plausible, wrong by two orders of magnitude, and silent.
  The emit path now asserts that every point bracketed before it will write
  anything.

### Why the min_pulse_width shape differs from the thin-oxide library

The HV/LV cross-check (`char_clockgate.py … ratio`) reports `min_pulse_width`
ratios running from 5.47 at the fastest slew down to 0.24 at the slowest.
That is not a measurement error in either library: **the two tables answer
different questions**, and the answers cross over.

| CLK slew HV (LV) | HV | LV | HV/LV |
|---|---|---|---|
| 0.04948 (0.0186) | 0.4626 | 0.2304 | 2.01 |
| 1.37352 (0.5164) | 0.6256 | 0.8521 | 0.73 |
| 3.35958 (1.2630) | 0.7928 | 2.0850 | 0.38 |
| 6.66968 (2.5074) | 0.9748 | 4.1382 | 0.24 |

The thin-oxide numbers give the game away. With 20/80 slew thresholds a full
0→100 % input transition takes $s/0.6$, and for the three larger slews the
thin-oxide table is

$$\text{mpw}_{LV} = 0.990 \times \frac{s}{0.6}$$

to three decimals at every point — 0.8521/0.8607, 2.0850/2.1050,
4.1382/4.1790. A constant of that precision across a 5× range of $s$ is not
something a bisection produces; it is a **waveform-geometry limit**: the
narrowest pulse for which the clock still completes one full transition.
Below it the input never reaches the rail. At the fastest slew the same table
gives 0.2304 and 0.1022 ns against a geometric value of 0.031 ns, so there
the number is circuit-limited instead. The thin-oxide table is therefore the
*envelope* of the two limits, and for most of its range the geometric one is
in control.

This project's number is the **circuit limit alone**, obtained by shrinking
the clock pulse until the gated output stops producing a full-swing pulse
(§ *Clock gates*). It grows only weakly with slew — 0.46 → 0.97 ns while the
slew grows 135× — because what sets it is internal gate delay, not the shape
of the input edge.

The two therefore cross: at fast slews the thick-oxide devices are slow
enough that the circuit limit dominates and HV is the larger number
(ratio 2.01, 5.47); at slow slews the thin-oxide geometric term grows
linearly, overtakes, and HV becomes the smaller one (0.38, 0.24).

**What the circuit limit means physically, checked directly.** At the slowest
slew the stimulus generator degenerates the pulse to a triangle once its
width falls below one ramp time, preserving the edge *rate* and losing
amplitude. At the reported 0.9748 ns width the clock peaks at **1.79 V, 54 %
of VDD** — and GCLK still reaches **2.999 V**, above the 2.97 V full-swing
criterion; at 0.8× that width GCLK reaches only 1.92 V and the trial fails.
So the ICG responds to a half-amplitude clock blip. That is correct for a
latch-based clock gate: the internal latch is a threshold device, and once
CLK crosses its trip point the output gate drives GCLK to the rail
irrespective of what the clock does afterwards.

**Consequence for users.** The shipped value is what the cell does, not what
a clock of that slew can be expected to look like. A flow that wants the
conservative thin-oxide convention should take

$$\max\left(\text{mpw}_{\text{shipped}},\; s/0.6\right)$$

i.e. never allow a clock pulse narrower than one full transition of its own
edge rate. This library reports the measured limit because that is the
quantity it can defend by simulation; the geometric limit is arithmetic the
consuming tool can apply itself, and folding it in silently would hide a real
device measurement behind a rule of thumb.

# Drive limits: the attribute whose absence fails twice

CharLib emits no `max_capacitance` and no `max_transition`, on any pin, in
any cell — and no library-level `default_max_*` either. The shipped
library inherited that gap for three revisions, and it fails in two very
different ways.

**Silently.** OpenSTA answers "no limit" for every pin, so a flow's
max-capacitance and max-transition checks report zero violations. They are
not passing; there is nothing for them to compare against. A green
signoff report is the worst possible presentation of an absent constraint.

**Loudly, and much later.** OpenROAD's TritonCTS consults the same data
when it sizes the clock tree, gets an empty buffer selection back, and
dereferences it: `clock_tree_synthesis` terminates with SIGSEGV inside
`cts::TritonCTS::getBufferFanoutLimit`. The failure surfaces in a
different tool, several flow stages after the actual defect, with a stack
trace that says nothing about liberty. Reduced to a two-flip-flop test
case it reproduces deterministically, and it disappears the moment the
limits are present — reported upstream as OpenROAD issue #11165, on the
argument that a liberty without limits deserves a diagnosable error rather
than a signal 11.

The limits are derived from the characterization rather than borrowed:
a pin may not be asked to drive more load than its tables cover, nor to
accept a slower edge than was characterized. So per output pin
`max_capacitance` is the top of that pin's load axis, per pin
`max_transition` the top of the slew axis it was characterized against,
and the library defaults follow the thin-oxide convention of
weakest-drive / slowest-edge. These bound the characterized range; real
slew targets belong in the flow constraints, not here.

# How to characterize this library, step by step

Everything above describes *what* is measured and why. This section is the
operational counterpart: the exact commands that turn the shipped netlists
into a signed-off Liberty file, in the order they must run, with the checks
that tell you each step actually did something. It is written to be followed
by someone who has never run the flow.

## 0. Prerequisites

| what | where | notes |
|---|---|---|
| IHP SG13G2 PDK | `$PDK_ROOT/$PDK`, default `/foss/pdks/ihp-sg13g2` | supplies `cornerMOShv.lib` and the PSP103 OSDI modules |
| CharLib 2.1.0 | venv `/foss/tools/charlib` | driven through `charlib_patched.py`, never invoked directly |
| ngspice ≥ 42 with OSDI | `libngspice.so` on the loader path | see the note on the shim below |
| Python 3.12 | system | `merge_lib.py`, `finalize_lib.py`, `verify_lib.py` and the direct-measurement decks are stock Python |

Two environment details are not optional and are the cause of most
first-run failures:

* **The OSDI shim.** The PSP103 models are Verilog-A compiled to `.osdi`
  and must be `pre_osdi`-loaded before the netlist is read. `run_corner.sh`
  prepends `work/ngspice-osdi-shim` to `PATH` for exactly this reason. Run
  CharLib without it and every device falls back to an intrinsic model —
  the run *succeeds* and the numbers are silently wrong.
* **`.spiceinit` thread count.** `work/.spiceinit` sets `num_threads=1` and
  is copied into the scratch directory at stage 3. This is deliberate:
  ngspice's `.spiceinit` **overrides** `OMP_NUM_THREADS`, so setting the
  environment variable alone does nothing. With per-simulation threading
  left on, the outer job-level parallelism oversubscribes the machine and
  the run slows down by more than an order of magnitude.

## 1. The short version

One corner, end to end:

```sh
cd work
./run_corner.sh typ            # or fast, or slow
```

That is the whole flow. It takes hours — the combinational stage alone is
~28 800 ngspice invocations — and it is resumable, so read the rest of this
section before starting a long run.

`run_corner.sh` takes an optional second argument naming the stage to start
from, which is how you recover from a failure without repeating work:

```sh
./run_corner.sh fast direct    # skip straight to the direct measurements
```

Valid stages, in order: `config`, `charlib`, `seq`, `direct`, `finalize`,
`verify`.

## 2. The six stages

### Stage 1 — configuration

```sh
python3 gen_charlib_config.py --corner fast
```

Writes `charlib_sg13g2_stdcell_hv_fast_3p60V_m40C.yml`: every cell, its
pins, its logic, the slew and load grids, and the PVT triplet taken from
`corners.py`. Nothing is hardcoded here — the corner supplies the model
section (`mos_ff`), the supply (3.6 V) and the temperature (−40 °C)
together.

**Check it landed.** Three greps, because a corner that is only *partly*
applied produces a plausible library rather than an error:

```sh
CFG=charlib_sg13g2_stdcell_hv_fast_3p60V_m40C.yml
grep -E 'voltage: 3.6|temperature: -40|mos_ff' $CFG | head
```

### Stage 2 — CharLib, combinational

```sh
./run_charlib.sh fast
```

The production characterizer, run over everything it can express: the
combinational cells, their NLDM delay and transition tables, input
capacitance by charge integration, and all-state DC leakage. This is the
long pole. Parallelism defaults to `nproc - 2`; override with
`CHARLIB_JOBS`.

**What "done" looks like:** a progress bar reaching `28801/28801` and a
`.lib` appearing at `lib/sg13g2_stdcell_hv_fast_3p60V_m40C.lib`.

**What a healthy log still contains:** thousands of lines of
`ImportError: A module that was compiled using NumPy 1.x…` and a PySpice
traceback ending in `_hspice_read`. Both are benign — PySpice probes for an
HSpice backend, fails, and falls through to ngspice. Do not go hunting
them. To count *real* problems, filter them out:

```sh
grep -hiE 'error|assert|fail' log \
  | grep -viE 'numpy|hspice|pybind11|ImportError' | wc -l
```

**Where the simulations are.** They will not appear in `ps` as `ngspice`.
CharLib drives ngspice through PySpice's *shared-library* interface: each
worker `dlopen`s `libngspice.so` and calls into it in-process. The Python
workers pinning the CPU **are** the simulations. Confirm with:

```sh
grep -o '.*libngspice.*' /proc/<worker-pid>/maps
```

### Stage 3 — CharLib, sequential

```sh
charlib_patched.py run charlib_<libname>.yml \
    -f 'sg13g2_hv_(sdf|dfr|dlh|dll)' -o seq_fast.lib -j <jobs>
python3 merge_lib.py <lib> seq_fast.lib
```

The flops and latches, re-run through the project's own procedures
(`seq_delay_procedure.py`) because upstream CharLib's sequential delay is a
stub. Produces clk→Q, setup and hold by the relative-1.5×-C2Q bisection
described earlier in this report.

Note this stage does **not** go through `run_charlib.sh`, even though that
script accepts a filter. `run_charlib.sh` writes directly to the corner's
Liberty; reusing it here would overwrite stage 2's combinational results
rather than add to them. The sequential run therefore writes its own
`seq_<corner>.lib` and is folded in with `merge_lib.py`.

### Stage 4 — the cells no characterizer reaches

```sh
python3 seq_leakage.py  --corner fast
python3 tie_leakage.py  --corner fast
python3 char_sighold.py --corner fast
python3 char_tristate/char_tristate.py --corner fast
python3 merge_lib.py <lib> char_tristate/tristate_fast.lib
python3 char_clockgate/char_clockgate.py --corner fast all
python3 merge_lib.py <lib> char_clockgate/clockgate_fast.lib
```

Nine cells — six tri-states, two clock gates, one bus holder — plus the tie
cells and sequential single-state leakage. Each is a direct ngspice
measurement against the shipped netlist, for the reasons given in *Cells
outside every characterizer's model*.

`char_clockgate.py` accepts individual task names instead of `all`
(`leakage`, `cap`, `delay`, `mpw`, `suh`, `emit`, `ratio`) and resumes from
whatever it has already measured, which matters because the min-pulse-width
bisection is the slowest single measurement in the flow. `CG_JOBS` and
`TIMEOUT` tune it.

### Stage 5 — drive limits, stubs, areas

```sh
python3 finalize_lib.py --corner fast
python3 update_lib_area.py
```

`finalize_lib.py` derives `max_capacitance` and `max_transition` from the
table axes of whatever is present, adds the physical-cell stubs with
measured leakage, and stamps the corner-suffixed library name.
`update_lib_area.py` replaces every `area` with the drawn LEF footprint.

> **This step must run after every merge, not before.** It reads the
> axes that exist at the moment it runs. Run it before stage 4 and the
> tri-states and clock gates ship with no drive limits — which is the exact
> gap that crashed OpenROAD's TritonCTS on the first revision of this
> library. `run_corner.sh` enforces the order; if you are driving the
> stages by hand, this is the one that bites.

### Stage 6 — the gate

```sh
python3 verify_lib.py --corner fast
```

Refuses to pass on: missing leakage groups, empty timing tables, pin sets
that disagree with the CDL, areas that disagree with the LEF,
non-monotonic load axes, missing drive limits, and incomplete
special-class constructs (a `three_state` output without both enable and
disable arcs, an ICG without statetable + internal pin + GCLK propagation +
enable setup/hold + `min_pulse_width`, a bus holder without
`driver_type : bus_hold`). Expect:

```
cells in lib: 84
timing tables: 668, empty: 0
sequential cells checked: 14, clean: 14
RESULT: PASS
```

## 3. Adding a corner

Corners are data, not code. All three shipped corners are one line each in
`CORNERS` in `work/corners.py`:

```python
"typ":  Corner("typ",  "mos_tt", 3.30,   25.0, 1.00),
"fast": Corner("fast", "mos_ff", 3.60,  -40.0, 1.00),
"slow": Corner("slow", "mos_ss", 3.00,  125.0, 1.00),
```

A fourth is added the same way, then run `./run_corner.sh <name>`. The
filename, the Liberty library name,
the ngspice `.lib` section, the supply and the temperature all follow from
that one line. The PDK-level LibreLane config registers whichever corners
are actually present, so no downstream file needs editing.

The slew and load grids are deliberately **not** corner-dependent: the
tables must span the same electrical territory at every corner or an STA
tool cannot interpolate across them.

> **Three failure modes to watch for when adding corners**, all of which
> this flow shipped at least once. Every one was invisible while `typ` was
> the only corner that existed.
>
> 1. **A constant derived from `VDD` at module import time.** Rebinding
>    `VDD` from `--corner` does not update anything computed from it, so a
>    threshold keeps the *previous* corner's volts while the run looks
>    perfectly healthy. Six instances so far: `.option temp`, the SPICE
>    header, the ICG trip points, the keeper bias, the tri-state hold
>    tolerance, and the calibration reference. Recompute derived constants
>    in the same block that rebinds `VDD`, or derive them at the point of
>    use.
> 2. **A measurement cache not keyed by corner.** `char_tristate`
>    memoises each simulation to disk under `<cell>_<slew>_<direction>`.
>    With no PVT in the key, the fast run replayed the typ run's results
>    and would have shipped typical tri-state timing in the fast Liberty.
>    It was caught only because an independent check — the keeper-hold
>    assertion — saw a floating node at 3.3 V when the rail was 3.6 V. A
>    cache is a correctness surface, not just a speed one.
> 3. **A step that patches what it assumes already exists.**
>    `tie_leakage.py` inserted leakage into tie-cell entries that nothing
>    in the flow ever created — they had come from the initial bulk
>    import. That held for exactly as long as no corner was built from
>    scratch. Anything that edits the Liberty should be able to create
>    what it edits, or say plainly that it cannot.
> 4. **A deck that converges is not a deck that is well posed.** The
>    antenna-diode leakage deck left its signal pin dangling, with no DC
>    path. At typ and fast ngspice converged on *some* operating point and
>    returned a number; at slow (125 °C) gmin stepping, source stepping and
>    the transient op all failed. The failure is what exposed it, but the
>    successes were the real damage: typ's floating answer was **6.6× the
>    well-defined one**, and it shipped. Every signal pin now gets a 1 GΩ
>    tie to ground — 3 nA, three orders below the currents being measured.
>    Convergence is not evidence of a meaningful question.
>
> The common root is that `typ` was built up incrementally over many
> sessions and never once from an empty directory. **A flow is only
> reproducible if it has actually been run that way**; until then it is
> merely a flow that has not yet been contradicted.

## 4. Installing into the PDK

```sh
python3 make_pdk_pr.py --pdk /path/to/IHP-Open-PDK
```

Copies the eight view directories, the tech LEF, the LibreLane SCL, and the
reports; patches the PDK-level `librelane/config.tcl` corner block; then
runs two checks that exist because both have failed silently before:

* the installed netlist is cross-checked cell-for-cell against the SPICE
  view (`84/84 cells match`);
* **every installed file is confirmed `git`-trackable.** The `spice/` views
  were once dropped entirely by a root `.gitignore` rule — `*.spice` with a
  `!spice/` re-include only un-ignores the *directory*, not the files in
  it. `git check-ignore --stdin --no-index` is what catches this; without
  `--no-index` it is silent on already-staged paths and the guard is
  vacuous.

## 5. Traps, in descending order of time lost

1. **A clean log does not mean a correct run.** CharLib has no Hi-Z
   concept, so the tri-states were *configured*, produced nothing,
   swallowed the empty result, and logged not one word. The same lesson
   arrived a second way when a corner-blind cache silently served typical
   numbers to a fast-corner run (§3). Compare the emitted cell list against
   the intended one, and keep at least one check that looks at the physics
   rather than the bookkeeping — the cache bug was caught by a keeper-hold
   assertion, not by anything counting cells.
2. **Never ship an unbracketed bisection.** A search that hits its bounds
   without bracketing must raise, not return the bound. The clock-gate
   min-pulse-width search once emitted its 48 ns upper bound as measured
   data; it now asserts.
3. **HV table axes are reversed relative to the thin-oxide library.**
   `variable_1 : total_output_net_capacitance`, so `index_1` is loads and
   `index_2` is slews. Every structure ported from the LV Liberty must swap
   axes.
4. **`pkill -f <pattern>` matches your own command line.** It cost three
   self-terminated shells here. Use the bracket trick: `pkill -f
   '[c]har_clockgate'`.
5. **`import` at the top of a one-line multi-import** can silently no-op a
   scripted edit. Assert on every automated source replacement; the one
   substitution not checked was the one that did nothing.
6. **A report must not be able to break a build.** The HV/LV ratio
   cross-check sits in the clock-gate driver's task list, so when its
   Liberty parser failed, `set -e` killed `run_corner.sh` before the merge
   and the final two stages. It had in fact *never* worked — its pattern
   required `") ;"` where the thin-oxide library writes `");"` — so no
   corner had ever completed a scripted end-to-end run; the tail was
   finished by hand each time without anyone noticing. Both are fixed, and
   the parser now asserts rather than returning `None`.

# Conclusions

1. **All three input-capacitance methods are averages of the same
   $C_{in}(v)$ over different windows**, and their results order exactly as
   the windows predict: rail end-points 5.87 fF < full-swing charge mean
   6.44 fF < Miller-peak window mean 8.92 fF. Charge integration is the
   defensible production choice — it measures the charge a driver actually
   delivers — with the rail-biased AC value as the clean lower anchor.
2. **CharLib is Liberty-correct on the slew convention; lctime is not.**
   The $T = s/0.6$ ramp stretch is the single largest systematic between
   the two characterizers (−19 % at multi-ns slews, mechanism confirmed by
   re-interpolation at $0.6\,s$ to 0.25 %); where the convention doesn't
   bite, the tools agree to a median 2.9 % on delays and 0.0 % on
   transitions.
3. **Neither tool covers the full Liberty power model.** CharLib 2.1.0 has
   no internal-power procedure at all; lctime writes power tables but with
   a biased quadrature and without subtracting the $C_L V_{DD}^2$ load
   term, so they double-count against STA switching power. Leakage is
   CharLib-only (all-states DC enumeration; the project adds transient
   single-state leakage for sequential cells).
4. **Sequential characterization shipped only because of local code**:
   upstream CharLib's sequential delay is a stub and its contour method was
   unusable here; the local bisection (relative 1.5× C2Q criterion) and
   lctime's Brent-on-pushout (absolute 10 ps) are both principled points on
   the same metastability curve, differing mainly in coverage — lctime
   cannot do latches and constrains at zero load.
5. **lctime can adopt CharLib's charge-integration method with a
   three-part, single-function patch** — the branch-current infrastructure
   it needs is already exercised by its own power measurement. Until then,
   its pin capacitances should not be used for anything load-sensitive.
6. **Neither characterizer models tri-states, clock gates or bus holders**,
   and the tri-state case fails *silently* — the cell is configured, no
   simulation runs, an empty result is swallowed, and the log says nothing.
   Any characterization flow needs a coverage check that compares the
   emitted cell list against the intended one; a clean run log does not
   mean the run was complete. These nine cells are measured directly
   against the shipped netlists instead.
7. **A method can be correct for one cell class and invalid for another.**
   Charge integration is the right production choice for gate pins and the
   wrong one for a bus holder, where the integral is dominated by keeper
   fight-back and varies 2.8× with the driver's edge rate. The bias-swept
   AC method, which is only the *anchor* for gate pins, is the *production*
   method there. The thin-oxide library's unexplained 2.8× rise/fall
   asymmetry on the same cell is the same artifact, visible in shipped
   data.
8. **`max_capacitance` and `max_transition` are not optional.** Absent,
   they make STA limit checks pass vacuously and crash OpenROAD's CTS in a
   different tool several stages downstream. Deriving them from the
   characterized table axes costs nothing and is self-consistent by
   construction: a cell is never asked to operate outside the range it was
   measured over.

---

# Appendix: provenance

| item | identity |
|---|---|
| reference deck | `work/fo4.py`, 96 lines, ngspice batch |
| CharLib | 2.1.0, git `stineje/CharLib` commit `6859faf`, venv `/foss/tools/charlib`, install hash-verified unmodified |
| PySpice | 1.6 fork, git `infinitymdm/PySpice` commit `da81c4d` (adds `.meas` readback) |
| lctime | 0.0.26, `/usr/local/lib/python3.12/dist-packages/lctime` |
| models | IHP SG13G2 PSP103 Verilog-A via OSDI, `cornerMOShv.lib`, one section per corner: `mos_tt` 3.30 V/25 °C, `mos_ff` 3.60 V/−40 °C, `mos_ss` 3.00 V/125 °C |
| shipped libraries | `lib/sg13g2_stdcell_hv_{typ_3p30V_25C, fast_3p60V_m40C, slow_3p00V_125C}.lib` — 84 cells and 668 delay/transition tables each, thresholds 20/80/50, 7×7 NLDM grids on identical axes at every corner |
| cross-check | `work/lctime_compare.py`: 8 cells, 3 132 aligned points |
| local CharLib adaptations | `charlib_patched.py` (case-insensitive branch lookup, procedure registration), `seq_delay_procedure.py` (clk→Q, setup/hold bisection), `seq_leakage.py`, `gen_charlib_config.py` (grids ×2.66/×2.20, charge integration selected), `fix_lib.py` / `fix_lib_seq.py` (header and sequential emission repairs) |
| direct measurement, outside both characterizers | `tie_leakage.py` (tie cells), `char_sighold.py` (bus holder: settled-tail leakage, bias-swept AC capacitance, fight-charge sweep), `char_tristate/char_tristate.py` (data + enable/disable arcs), `char_clockgate/char_clockgate.py` (CLK→GCLK propagation, enable setup/hold, CLK min-pulse-width, per-state leakage for the two statetable ICGs) |
| Liberty post-processing | `finalize_lib.py` (drive limits from the table axes, physical-cell stubs with measured leakage and a defined DC path on every signal pin, corner-suffixed library name) |
| Liberty gate | `verify_lib.py`: structure, cross-view, areas vs layout, load-axis monotonicity, C~in~ vs reference, sequential arcs, drive limits, and complete-construct checks for the tri-state / clock-gate / bus-hold classes |

Key source locations cited: CharLib `procedures/combinational/delay.py`
(stimulus 75–83, measurements 101–112, worst-case 188–190),
`pin_capacitance/charge_integration.py` (integration 100–104, formula
124–135), `combinational/leakage_power.py` (67, 86–91); lctime
`characterization/timing_combinatorial.py` (StepWave 186–191, energy
263–274), `characterization/input_capacitance.py` (current source 235–243,
slope 273–297, label swap 318–321), `characterization/timing_sequential.py`
(pushout root-finding 1018–1228), `ngspice_subprocess.py` (deck 122–187,
temperature 83).
