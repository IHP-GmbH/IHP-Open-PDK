#!/usr/bin/env python3
"""
Layer Editor Server for IHP SG13CMOS5L PDK

A lightweight local server that provides:
- Static file serving for layer_editor.html
- REST API for reading/writing layer JSON files
- Execution of generation scripts for KLayout files

Usage:
    python layer_editor_server.py [--port PORT]

The server will open the browser automatically.
All paths are relative to the layer_tracking directory.
"""

import argparse
import http.server
import json
import os
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Directory structure (relative to this script)
SCRIPT_DIR = Path(__file__).parent.resolve()
SCRIPTS_DIR = SCRIPT_DIR.parent / "scripts"
KLAYOUT_TECH_DIR = SCRIPT_DIR.parent / "libs.tech" / "klayout" / "tech"

# JSON files in this directory
FULL_PDK_JSON = SCRIPT_DIR / "ihp-sg13g2_layers.json"
SG13CMOS5L_PDK_JSON = SCRIPT_DIR / "ihp-sg13cmos5l_layers.json"

# Generation script
GENERATE_SCRIPT = SCRIPTS_DIR / "generate_layer_files.py"


class LayerEditorHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with REST API endpoints."""

    def __init__(self, *args, **kwargs):
        # Serve files from the layer_tracking directory
        super().__init__(*args, directory=str(SCRIPT_DIR), **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        # API endpoints
        if path == "/api/full-pdk":
            self._send_json_file(FULL_PDK_JSON)
        elif path == "/api/sg13cmos5l-pdk":
            self._send_json_file(SG13CMOS5L_PDK_JSON)
        elif path == "/api/status":
            self._send_status()
        elif path == "/" or path == "/index.html":
            # Serve the layer editor HTML
            self.path = "/layer_editor.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/sg13cmos5l-pdk":
            self._save_sg13cmos5l_pdk()
        elif path == "/api/generate":
            self._run_generation()
        else:
            self.send_error(404, "Not Found")

    def _send_json_file(self, filepath):
        """Send a JSON file as response."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, f"File not found: {filepath.name}")
        except Exception as e:
            self.send_error(500, str(e))

    def _send_status(self):
        """Send server status and file information."""
        status = {
            "server": "Layer Editor Server",
            "version": "1.0",
            "files": {
                "full_pdk": {
                    "path": str(FULL_PDK_JSON.relative_to(SCRIPT_DIR)),
                    "exists": FULL_PDK_JSON.exists()
                },
                "sg13cmos5l_pdk": {
                    "path": str(SG13CMOS5L_PDK_JSON.relative_to(SCRIPT_DIR)),
                    "exists": SG13CMOS5L_PDK_JSON.exists()
                }
            },
            "scripts": {
                "generate": {
                    "path": str(GENERATE_SCRIPT.relative_to(SCRIPT_DIR.parent)),
                    "exists": GENERATE_SCRIPT.exists()
                }
            },
            "output_dir": {
                "path": str(KLAYOUT_TECH_DIR.relative_to(SCRIPT_DIR.parent)),
                "exists": KLAYOUT_TECH_DIR.exists()
            }
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(status, indent=2).encode('utf-8'))

    def _save_sg13cmos5l_pdk(self):
        """Save the SG13CMOS5L PDK JSON file."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Update timestamp
            from datetime import datetime
            data['generated_at'] = datetime.now().isoformat()

            # Write to file
            with open(SG13CMOS5L_PDK_JSON, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            response = {
                "success": True,
                "message": f"Saved {len(data.get('layers', {}))} layers to {SG13CMOS5L_PDK_JSON.name}",
                "file": str(SG13CMOS5L_PDK_JSON.name)
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError as e:
            self.send_error(400, f"Invalid JSON: {e}")
        except Exception as e:
            self.send_error(500, f"Error saving file: {e}")

    def _run_generation(self):
        """Run the layer file generation script."""
        try:
            if not GENERATE_SCRIPT.exists():
                self.send_error(404, f"Generation script not found: {GENERATE_SCRIPT}")
                return

            # Run the generation script
            result = subprocess.run(
                [sys.executable, str(GENERATE_SCRIPT)],
                capture_output=True,
                text=True,
                cwd=str(SCRIPT_DIR.parent)  # Run from ihp-sg13cmos5l directory
            )

            # Check for generated files
            generated_files = []
            for ext in ['.lyp', '.lyt', '.map']:
                filepath = KLAYOUT_TECH_DIR / f"sg13cmos5l{ext}"
                if filepath.exists():
                    generated_files.append({
                        "name": filepath.name,
                        "size": filepath.stat().st_size
                    })

            response = {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "generated_files": generated_files,
                "output_dir": str(KLAYOUT_TECH_DIR.relative_to(SCRIPT_DIR.parent))
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Error running generation: {e}")

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def run_server(port=5000):
    """Start the HTTP server."""
    # Verify required files exist
    if not FULL_PDK_JSON.exists():
        print(f"Warning: Full PDK JSON not found: {FULL_PDK_JSON}")
        print("Run parse_lyp_to_json.py first to generate it.")

    if not SG13CMOS5L_PDK_JSON.exists():
        print(f"Warning: SG13CMOS5L PDK JSON not found: {SG13CMOS5L_PDK_JSON}")

    # Start server
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, LayerEditorHandler)

    url = f"http://localhost:{port}"
    print(f"\n{'='*60}")
    print(f"  IHP SG13CMOS5L Layer Editor")
    print(f"{'='*60}")
    print(f"\n  Server running at: {url}")
    print(f"  Working directory: {SCRIPT_DIR}")
    print(f"\n  Press Ctrl+C to stop\n")

    # Open browser after a short delay
    def open_browser():
        webbrowser.open(url)
    threading.Timer(0.5, open_browser).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        httpd.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Layer Editor Server for IHP SG13CMOS5L")
    parser.add_argument("--port", "-p", type=int, default=5000,
                        help="Port to run the server on (default: 5000)")
    args = parser.parse_args()

    run_server(args.port)


if __name__ == "__main__":
    main()
