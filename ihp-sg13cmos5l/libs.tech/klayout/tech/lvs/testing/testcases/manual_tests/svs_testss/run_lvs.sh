#!/bin/bash
# ==============================================================
# Run manual SVS regression (1 PASS + 2 FAIL expected)
# ==============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_LVS="${SCRIPT_DIR}/../../../../run_lvs.py"
MASTER_NETLIST="${SCRIPT_DIR}/svs_master_inv.cdl"
RUN_ROOT="${TMPDIR:-/tmp}/sg13cmos5l_svs_testss_$(date +%Y_%m_%d_%H_%M_%S)"

FAILED=0

run_case() {
  local case_name="$1"
  local layout_netlist="$2"
  local expected="$3"
  local case_dir="${RUN_ROOT}/${case_name}"
  local case_log="${case_dir}/${case_name}.log"

  mkdir -p "${case_dir}"

  echo "Running ${case_name} (expected: ${expected})"
  python3 "${RUN_LVS}" \
    --topcell=svs_inv \
    --netlist="${MASTER_NETLIST}" \
    --layout_netlist="${layout_netlist}" \
    --run_mode=deep \
    --run_dir="${case_dir}" > "${case_log}" 2>&1

  local actual="UNKNOWN"
  if grep -q "Congratulations! Netlists match." "${case_log}"; then
    actual="PASS"
  elif grep -q "ERROR : Netlists don't match" "${case_log}"; then
    actual="FAIL"
  fi

  if [[ "${actual}" == "${expected}" ]]; then
    echo "  -> ${case_name}: PASSED (actual=${actual})"
  else
    echo "  -> ${case_name}: FAILED (actual=${actual}, expected=${expected})"
    FAILED=$((FAILED + 1))
  fi
}

run_case "1_pass_match" "${SCRIPT_DIR}/svs_layout_match.cdl" "PASS"
run_case "2_fail_connection" "${SCRIPT_DIR}/svs_layout_conn_fail.cdl" "FAIL"
run_case "3_fail_parameter" "${SCRIPT_DIR}/svs_layout_param_fail.cdl" "FAIL"

if [[ "${FAILED}" -ne 0 ]]; then
  echo "SVS regression FAILED (${FAILED} case(s) mismatched expected outcome)."
  echo "Logs: ${RUN_ROOT}"
  exit 1
fi

echo "SVS regression PASSED (1 PASS + 2 FAIL as expected)."
echo "Logs: ${RUN_ROOT}"
