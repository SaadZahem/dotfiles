#!/usr/bin/env python3
import argparse
import json
import os
import string
import subprocess
import sys
import time
from urllib.parse import urlparse

DATA_FILE = os.path.expanduser("~/.pcurl.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"profiles": {}, "zones": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def handle_profile(args, data):
    if args.action == "add":
        variables = dict(v.split("=", 1) for v in args.vars) if args.vars else {}
        data["profiles"][args.name] = variables
        save_data(data)
        print(f"Profile '{args.name}' added/updated.")
    elif args.action == "delete":
        if data["profiles"].pop(args.name, None) is not None:
            save_data(data)
            print(f"Profile '{args.name}' deleted.")
        else:
            print(f"Profile '{args.name}' not found.")
    elif args.action == "list":
        for name, vars in data["profiles"].items():
            print(f"- {name}: {vars}")

def handle_zone(args, data):
    if args.action == "add":
        zone = {"url": args.url, "method": args.method}
        if args.data: zone["data"] = args.data
        if args.headers: zone["headers"] = args.headers
        data["zones"][args.name] = zone
        save_data(data)
        print(f"Template '{args.name}' added/updated.")
    elif args.action == "delete":
        if data["zones"].pop(args.name, None) is not None:
            save_data(data)
            print(f"Template '{args.name}' deleted.")
        else:
            print(f"Template '{args.name}' not found.")
    elif args.action == "list":
        for name, zone in data["zones"].items():
            print(f"- {name}: {zone}")

def override_url_port(url, port):
    parsed = urlparse(url)
    netloc = parsed.netloc.split(":")[0] + f":{port}"
    return parsed._replace(netloc=netloc).geturl()

def format_payload(data_template, profile):
    return string.Template(data_template).safe_substitute(**profile)

def execute_request(profile, zone, overrides, silent, verbose):
    # Apply Profile Variables to Template
    url = zone["url"].format(**profile)
    data = zone.get("data", "")
    data_payload = format_payload(data, profile)
    redacted_profile = {**profile, "password": "********"}
    redacted_payload = format_payload(data, redacted_profile)
    
    # Apply Overrides
    if overrides.port:
        url = override_url_port(url, overrides.port)
        
    # Build curl command
    cmd = ["curl", "-X", zone["method"], url]
    
    if data_payload:
        cmd.extend(["-d", data_payload])
        
    for header in zone.get("headers", []):
        cmd.extend(["-H", header.format(**profile)])
        
    if silent:
        cmd.append("-s")
    if verbose:
        cmd.append("-v")

    # Run
    if not silent:
        cut_index = cmd.index("-d") + 1
        redacted_cmd = [*cmd[:cut_index], redacted_payload, *cmd[cut_index + 1:]]
        print(f"Executing: {' '.join(redacted_cmd)}")
        del cut_index, redacted_cmd
    subprocess.run(cmd)
    print()

def handle_run(args, data):
    if args.profile not in data["profiles"]:
        sys.exit(f"Error: Profile '{args.profile}' not found.")
    if args.zone not in data["zones"]:
        sys.exit(f"Error: Template '{args.zone}' not found.")

    profile = data["profiles"][args.profile]
    zone = data["zones"][args.zone]

    try:
        while True:
            execute_request(profile, zone, args, args.silent, args.verbose)
            if args.loop and args.loop > 0:
                if not args.silent:
                    print(f"Waiting {args.loop} seconds...")
                time.sleep(args.loop)
            else:
                break
    except KeyboardInterrupt:
        print("\nExecution stopped by user.")

def main():
    parser = argparse.ArgumentParser(description="pcurl: A profile-driven wrapper for curl.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Profile Commands ---
    parser_profile = subparsers.add_parser("profile", help="Manage profiles")
    parser_profile.add_argument("action", choices=["add", "delete", "list"])
    parser_profile.add_argument("name", nargs="?", help="Profile name")
    parser_profile.add_argument("--var", dest="vars", action="append", help="Variables in key=value format (e.g., --var username=admin)")

    # --- Template Commands ---
    parser_zone = subparsers.add_parser("zone", help="Manage request zones")
    parser_zone.add_argument("action", choices=["add", "delete", "list"])
    parser_zone.add_argument("name", nargs="?", help="Template name")
    parser_zone.add_argument("--url", help="Target URL (can include {variables})")
    parser_zone.add_argument("--method", default="POST", help="HTTP Method (default: POST)")
    parser_zone.add_argument("--data", help="Request body data (can include {variables})")
    parser_zone.add_argument("--header", dest="headers", action="append", help="HTTP Headers (can include {variables})")

    # --- Run Commands ---
    parser_run = subparsers.add_parser("run", help="Run a profile against a zone")
    parser_run.add_argument("profile", help="Name of the profile to use")
    parser_run.add_argument("zone", help="Name of the zone to use")
    parser_run.add_argument("--port", help="Override the port in the zone URL")
    parser_run.add_argument("--silent", action="store_true", help="Run curl silently (-s)")
    parser_run.add_argument("--verbose", action="store_true", help="Run curl verbosely (-v)")
    parser_run.add_argument("--loop", type=float, help="Run in a loop with a delay in seconds")

    args = parser.parse_args()
    data = load_data()

    if args.command == "profile":
        if args.action in ["add", "delete"] and not args.name:
            sys.exit("Error: Profile name is required for this action.")
        handle_profile(args, data)
    elif args.command == "zone":
        if args.action in ["add", "delete"] and not args.name:
            sys.exit("Error: Template name is required for this action.")
        handle_zone(args, data)
    elif args.command == "run":
        handle_run(args, data)

if __name__ == "__main__":
    main()
