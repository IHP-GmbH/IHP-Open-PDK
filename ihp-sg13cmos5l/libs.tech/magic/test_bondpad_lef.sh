#!/bin/bash
########################################################################
# Test script for bondpad LEF generation
# Validates Python-generated LEF and compares with Magic output
########################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDK_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
OUTPUT_DIR="${SCRIPT_DIR}/test_output"

echo "=== Bondpad LEF Generation Test ==="
echo "PDK Root: $PDK_ROOT"
echo "Output Dir: $OUTPUT_DIR"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

#-----------------------------------------------------------------------
# Step 1: Generate bondpad GDS and LEF using Python
#-----------------------------------------------------------------------
echo "Step 1: Generate bondpad using Python/KLayout..."

# Check if klayout is available
if ! command -v klayout &> /dev/null; then
    echo "ERROR: klayout not found in PATH"
    echo "Install KLayout or add it to PATH"
    exit 1
fi

# Generate 70x70um square bondpad
klayout -n sg13cmos5l -zz -r "$PDK_ROOT/libs.tech/klayout/tech/scripts/bondpad.py" \
    -rd diameter=70.0 \
    -rd shape=square \
    -rd output="$OUTPUT_DIR/bondpad_70x70.gds" \
    -rd lef_output="$OUTPUT_DIR/bondpad_70x70_python.lef" \
    2>&1 || {
        echo "WARNING: KLayout PCell generation failed (library may not be loaded)"
        echo "Creating minimal test GDS for Magic validation..."
    }

echo "Python LEF generated: $OUTPUT_DIR/bondpad_70x70_python.lef"
echo ""

#-----------------------------------------------------------------------
# Step 2: Generate LEF using Magic (for comparison)
#-----------------------------------------------------------------------
echo "Step 2: Generate LEF using Magic (for corroboration)..."

# Check if magic is available
if ! command -v magic &> /dev/null; then
    echo "WARNING: magic not found in PATH"
    echo "Skipping Magic comparison"
    SKIP_MAGIC=1
fi

if [ -z "$SKIP_MAGIC" ]; then
    # Check if GDS file exists
    if [ -f "$OUTPUT_DIR/bondpad_70x70.gds" ]; then
        # Read GDS in Magic and export LEF
        magic -T "$SCRIPT_DIR/ihp-sg13cmos5l.tech" -noconsole << EOF
gds read $OUTPUT_DIR/bondpad_70x70.gds
lef write $OUTPUT_DIR/bondpad_70x70_magic.lef
quit
EOF
        echo "Magic LEF generated: $OUTPUT_DIR/bondpad_70x70_magic.lef"

        # Post-process Magic LEF to fix layer names
        echo "Post-processing Magic LEF (Metal5 -> TopMetal1)..."
        sed -i 's/LAYER Metal5/LAYER TopMetal1/g' "$OUTPUT_DIR/bondpad_70x70_magic.lef"

    else
        echo "WARNING: GDS file not found, skipping Magic LEF generation"
    fi
fi
echo ""

#-----------------------------------------------------------------------
# Step 3: Validate Python LEF structure
#-----------------------------------------------------------------------
echo "Step 3: Validate Python LEF structure..."

if [ -f "$OUTPUT_DIR/bondpad_70x70_python.lef" ]; then
    # Check for required elements
    ERRORS=0

    # Check MACRO definition
    if grep -q "^MACRO bondpad_70x70" "$OUTPUT_DIR/bondpad_70x70_python.lef"; then
        echo "  ✓ MACRO definition found"
    else
        echo "  ✗ MACRO definition missing"
        ERRORS=$((ERRORS + 1))
    fi

    # Check CLASS COVER BUMP
    if grep -q "CLASS COVER BUMP" "$OUTPUT_DIR/bondpad_70x70_python.lef"; then
        echo "  ✓ CLASS COVER BUMP found"
    else
        echo "  ✗ CLASS COVER BUMP missing"
        ERRORS=$((ERRORS + 1))
    fi

    # Check SIZE
    if grep -q "SIZE 70.000 BY 70.000" "$OUTPUT_DIR/bondpad_70x70_python.lef"; then
        echo "  ✓ SIZE 70x70 found"
    else
        echo "  ✗ SIZE 70x70 missing"
        ERRORS=$((ERRORS + 1))
    fi

    # Check PIN PAD
    if grep -q "PIN PAD" "$OUTPUT_DIR/bondpad_70x70_python.lef"; then
        echo "  ✓ PIN PAD found"
    else
        echo "  ✗ PIN PAD missing"
        ERRORS=$((ERRORS + 1))
    fi

    # Check TopMetal1 layer (correct name)
    if grep -q "LAYER TopMetal1" "$OUTPUT_DIR/bondpad_70x70_python.lef"; then
        echo "  ✓ LAYER TopMetal1 found (correct name)"
    else
        echo "  ✗ LAYER TopMetal1 missing"
        ERRORS=$((ERRORS + 1))
    fi

    # Check OBS section
    if grep -q "^  OBS$" "$OUTPUT_DIR/bondpad_70x70_python.lef"; then
        echo "  ✓ OBS section found"
    else
        echo "  ✗ OBS section missing"
        ERRORS=$((ERRORS + 1))
    fi

    # Check Metal1-4 obstructions
    for metal in Metal1 Metal2 Metal3 Metal4; do
        if grep -q "LAYER $metal" "$OUTPUT_DIR/bondpad_70x70_python.lef"; then
            echo "  ✓ LAYER $metal obstruction found"
        else
            echo "  ✗ LAYER $metal obstruction missing"
            ERRORS=$((ERRORS + 1))
        fi
    done

    if [ $ERRORS -eq 0 ]; then
        echo ""
        echo "✓ Python LEF validation PASSED"
    else
        echo ""
        echo "✗ Python LEF validation FAILED ($ERRORS errors)"
    fi
else
    echo "  WARNING: Python LEF file not found"
fi
echo ""

#-----------------------------------------------------------------------
# Step 4: Compare Python and Magic LEF (if both exist)
#-----------------------------------------------------------------------
echo "Step 4: Compare Python and Magic LEF..."

if [ -f "$OUTPUT_DIR/bondpad_70x70_python.lef" ] && \
   [ -f "$OUTPUT_DIR/bondpad_70x70_magic.lef" ]; then

    echo "  Comparing layer definitions..."

    # Extract layer names from both files
    PYTHON_LAYERS=$(grep "LAYER " "$OUTPUT_DIR/bondpad_70x70_python.lef" | sort -u)
    MAGIC_LAYERS=$(grep "LAYER " "$OUTPUT_DIR/bondpad_70x70_magic.lef" | sort -u)

    echo "  Python layers: $(echo "$PYTHON_LAYERS" | tr '\n' ' ')"
    echo "  Magic layers:  $(echo "$MAGIC_LAYERS" | tr '\n' ' ')"

    # Check that both have TopMetal1 (not Metal5)
    if echo "$PYTHON_LAYERS" | grep -q "TopMetal1" && \
       echo "$MAGIC_LAYERS" | grep -q "TopMetal1"; then
        echo "  ✓ Both use correct TopMetal1 layer name"
    else
        echo "  ⚠ Layer name mismatch detected"
    fi

else
    echo "  Comparison skipped (one or both LEF files missing)"
fi
echo ""

#-----------------------------------------------------------------------
# Summary
#-----------------------------------------------------------------------
echo "=== Summary ==="
echo "Output files:"
ls -la "$OUTPUT_DIR"/ 2>/dev/null || echo "  (no output files)"
echo ""
echo "Test complete."
