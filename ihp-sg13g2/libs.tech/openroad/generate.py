"""Generates the export.yml file which can be used OpenROAD-flow-scripts to update
IHP PDK files there."""
import pathlib
import hashlib
import yaml

API_VERSION = 1
PDK_ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()

SG13G2_IO = [
    {
        "destination": "gds",
        "files": [
            "gds/sg13g2_io.gds",
        ]
    },
    {
        "destination": "lef",
        "files": [
            "lef/sg13g2_io.lef",
        ]
    },
    {
        "destination": "lib",
        "files": [
            "lib/sg13g2_io_fast_1p32V_3p6V_m40C.lib",
            "lib/sg13g2_io_fast_1p65V_3p6V_m40C.lib",
            "lib/sg13g2_io_slow_1p08V_3p0V_125C.lib",
            "lib/sg13g2_io_slow_1p35V_3p0V_125C.lib",
            "lib/sg13g2_io_typ_1p2V_3p3V_25C.lib",
            "lib/sg13g2_io_typ_1p5V_3p3V_25C.lib",
        ]
    },
]

SG13G2_SRAMS = [
    "1P_1024x16_c2",
    "1P_1024x64_c2",
    "1P_1024x8_c2",
    "1P_2048x64_c2",
    "1P_256x48_c2",
    "1P_256x64_c2",
    "1P_4096x16_c3",
    "1P_4096x8_c3",
    "1P_512x64_c2",
    "1P_64x64_c2",
]

SG13G2_SRAM = [
    {
        "destination": "cdl",
        "file_formats": [
            "cdl/RM_IHPSG13_{}_bm_bist.cdl",
        ]
    },
    {
        "destination": "gds",
        "file_formats": [
            "gds/RM_IHPSG13_{}_bm_bist.gds",
        ]
    },
    {
        "destination": "lef",
        "file_formats": [
            "lef/RM_IHPSG13_{}_bm_bist.lef",
        ]
    },
    {
        "destination": "lib",
        "file_formats": [
            "lib/RM_IHPSG13_{}_bm_bist_fast_1p32V_m55C.lib",
            "lib/RM_IHPSG13_{}_bm_bist_slow_1p08V_125C.lib",
            "lib/RM_IHPSG13_{}_bm_bist_typ_1p20V_25C.lib",
        ]
    },
    {
        "destination": "verilog",
        "file_formats": [
            "verilog/RM_IHPSG13_{}_bm_bist.v",
        ]
    },
]

SG13G2_STDCELL = [
    {
        "destination": "cdl",
        "files": [
            "cdl/sg13g2_stdcell.cdl",
        ]
    },
    {
        "destination": "gds",
        "files": [
            "gds/sg13g2_stdcell.gds",
        ]
    },
    {
        "destination": "lef",
        "files": [
            "lef/sg13g2_stdcell.lef",
            "lef/sg13g2_tech.lef",
        ]
    },
    {
        "destination": "lib",
        "files": [
            "lib/sg13g2_stdcell_fast_1p32V_m40C.lib",
            "lib/sg13g2_stdcell_fast_1p65V_m40C.lib",
            "lib/sg13g2_stdcell_slow_1p08V_125C.lib",
            "lib/sg13g2_stdcell_slow_1p35V_125C.lib",
            "lib/sg13g2_stdcell_typ_1p20V_25C.lib",
            "lib/sg13g2_stdcell_typ_1p50V_25C.lib",
        ]
    },
    {
        "destination": "verilog",
        "files": [
            "verilog/sg13g2_stdcell.v",
        ]
    },
]


def write_file(content):
    """Saves the list of exportable files to the 'export.yml' file."""
    filename = PDK_ROOT / "libs.tech" / "openroad" / "export.yml"
    with open(filename, 'w', encoding="utf-8") as outfile:
        yaml.dump(content, outfile, default_flow_style=False)


def calc_file_md5(file):
    """Calculates a MD5 checksum of a file."""
    with open(file, 'rb') as file_content:
        return hashlib.md5(file_content.read()).hexdigest()


def get_entry(file, destination, cell_lib):
    """Creates an entry for a specific file."""
    entry = {
        "file": str(pathlib.Path("libs.ref") / cell_lib / file),
        "md5_checksum": calc_file_md5(PDK_ROOT / "libs.ref" / cell_lib / file),
        "destination": destination,
    }
    return entry


def main(): # pylint: disable=missing-function-docstring
    content = {
        "api_version": API_VERSION,
        "files": [],
    }
    for entry in SG13G2_IO:
        for file in entry.get('files', []):
            content['files'].append(get_entry(file, entry['destination'], "sg13g2_io"))
    for entry in SG13G2_SRAM:
        for file in entry.get('files', []):
            content['files'].append(get_entry(file, entry['destination'], "sg13g2_sram"))
        for file_format in entry.get('file_formats', []):
            for sram in SG13G2_SRAMS:
                file = file_format.format(sram)
                content['files'].append(get_entry(file, entry['destination'], "sg13g2_sram"))
    for entry in SG13G2_STDCELL:
        for file in entry.get('files', []):
            content['files'].append(get_entry(file, entry['destination'], "sg13g2_stdcell"))

    write_file(content)


if __name__ == "__main__":
    main()
