#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import time
import json
import string
from urllib.parse import urlparse

try:
    import tomllib
except ImportError:
    sys.exit("Error: Python 3.11+ is required for the standard 'tomllib' module.")

PROFILES_FILE = os.path.expanduser("~/.pcurl_profiles.toml")
ZONES_FILE = os.path.expanduser("~/.pcurl_zones.toml")

def load_toml(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "rb") as f:
        return tomllib.load(f)

def save_toml(filepath, data):
    """Minimal TOML writer."""
    with open(filepath, "w") as f:
        for section, contents in data.items():
            f.write(f"[{section}]\n")
            for k, v in contents.items():
                if isinstance(v, str):
                    f.write(f"{k} = {json.dumps(v)}\n")
                elif isinstance(v, list):
                    list_str = "[" + ", ".join(json.dumps(i) for i in v) + "]"
                    f.write(f"{k} = {list_str}\n")
                else:
                    f.write(f"{k} = {v}\n")
            f.write("\n")

def load_profiles():
    data = load_toml(PROFILES_FILE)
    if "default" not in data:
        data["default"] = {}
    return data

def load_zones():
    return load_toml(ZONES_FILE)

def handle_profile(args):
    profiles = load_profiles()
    if args.action == "add":
        variables = dict(v.split("=", 1) for v in args.vars) if args.vars else {}
        if args.name in profiles:
            profiles[args.name].update(variables)
        else:
            profiles[args.name] = variables
        save_toml(PROFILES_FILE, profiles)
        print(f"Profile '{args.name}' added/updated.")
    elif args.action == "delete":
        if args.name == "default":
            print("Error: Cannot delete the 'default' profile.")
        elif profiles.pop(args.name, None) is not None:
            save_toml(PROFILES_FILE, profiles)
            print(f"Profile '{args.name}' deleted.")
        else:
            print(f"Profile '{args.name}' not found.")
    elif args.action == "list":
        for name, vars in profiles.items():
            safe_vars = {k: ("***" if any(s in k.lower() for s in ['pass', 'token', 'secret', 'key']) else v) for k, v in vars.items()}
            print(f"- {name}: {safe_vars}")

def handle_zone(args):
    zones = load_zones()
    if args.action == "add":
        # Comment 2: URL is required when adding a zone
        if not args.url:
            sys.exit("Error: URL (-u/--url) is required when adding a zone.")
            
        zone = {"url": args.url, "method": args.method}
        if args.data: zone["data"] = args.data
        if args.headers: zone["headers"] = args.headers
        zones[args.name] = zone
        save_toml(ZONES_FILE, zones)
        print(f"Zone '{args.name}' added/updated.")
    elif args.action == "delete":
        if zones.pop(args.name, None) is not None:
            save_toml(ZONES_FILE, zones)
            print(f"Zone '{args.name}' deleted.")
        else:
            print(f"Zone '{args.name}' not found.")
    elif args.action == "list":
        for name, zone in zones.items():
            print(f"- {name}: {zone}")

def override_url_port(url, port):
    parsed = urlparse(url)
    netloc = parsed.netloc.split(":")[0] + f":{port}"
    return parsed._replace(netloc=netloc).geturl()

def execute_request(profile, zone, overrides, silent, verbose, force_method=None):
    url = string.Template(zone["url"]).safe_substitute(**profile)
    data_payload = string.Template(zone.get("data", "")).safe_substitute(**profile)
    
    if overrides.port:
        url = override_url_port(url, overrides.port)
        
    method = force_method if force_method else zone.get("method", "GET")
    cmd = ["curl", "-X", method, url]
    
    if data_payload:
        cmd.extend(["-d", data_payload])
        
    for header in zone.get("headers", []):
        cmd.extend(["-H", string.Template(header).safe_substitute(**profile)])
        
    if silent:
        cmd.append("-s")
    if verbose:
        cmd.append("-v")

    if not silent:
        cmd_str = f"Executing: {' '.join(cmd)}"
        sensitive_keys = ['pass', 'secret', 'token', 'key']
        
        for k, v in profile.items():
            if any(s in k.lower() for s in sensitive_keys) and v:
                cmd_str = cmd_str.replace(str(v), "***")
                
        print(cmd_str)
        
    subprocess.run(cmd)
    print() # Comment 1: Added blank line print after curl executes

def handle_run(args, force_method=None):
    profiles = load_profiles()
    zones = load_zones()

    # Comment 3: Positional argument logic for [profile] zone
    if len(args.targets) == 1:
        profile_name = "default"
        zone_name = args.targets[0]
    elif len(args.targets) == 2:
        profile_name = args.targets[0]
        zone_name = args.targets[1]
    else:
        sys.exit("Error: Too many arguments. Use: run [--options] [profile] zone")

    if profile_name not in profiles:
        sys.exit(f"Error: Profile '{profile_name}' not found.")
    if zone_name not in zones:
        sys.exit(f"Error: Zone '{zone_name}' not found.")

    profile = profiles[profile_name]
    zone = zones[zone_name]

    try:
        while True:
            execute_request(profile, zone, args, args.silent, args.verbose, force_method=force_method)
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
    parser_profile = subparsers.add_parser("profile", help="manage profiles")
    parser_profile.add_argument("action", choices=["add", "delete", "list"])
    parser_profile.add_argument("name", nargs="?", help="profile name")
    # Comment 4: Changed to -v for var
    parser_profile.add_argument("-v", "--var", dest="vars", action="append", help="variables in key=value format")

    # --- Zone Commands ---
    parser_zone = subparsers.add_parser("zone", help="manage request zones")
    parser_zone.add_argument("action", choices=["add", "delete", "list"])
    parser_zone.add_argument("name", nargs="?", help="zone name")
    parser_zone.add_argument("-u", "--url", help="target URL (use $var or ${var})")
    parser_zone.add_argument("-X", "--method", default="GET", help="HTTP Method (default: GET)")
    parser_zone.add_argument("-d", "--data", help="request body data (use $var or ${var})")
    parser_zone.add_argument("-H", "--header", dest="headers", action="append", help="HTTP Headers")

    # --- Reusable Execution Arguments ---
    def add_exec_args(exec_parser):
        # Comment 3: targets handles both [profile] and zone
        exec_parser.add_argument("targets", nargs="+", help="[profile] zone (if one argument is provided, profile defaults to 'default')")
        exec_parser.add_argument("-p", "--port", help="override the port")
        exec_parser.add_argument("-s", "--silent", action="store_true", help="run silently")
        # Comment 4: Changed to -V for verbose
        exec_parser.add_argument("-V", "--verbose", action="store_true", help="run verbosely")
        exec_parser.add_argument("-l", "--loop", type=float, help="run in a loop with delay in seconds")

    # --- Run & Post Commands ---
    parser_run = subparsers.add_parser("run", help="run a zone")
    add_exec_args(parser_run)

    parser_post = subparsers.add_parser("post", help="run a zone but override method to POST")
    add_exec_args(parser_post)

    args = parser.parse_args()

    if args.command == "profile":
        if args.action in ["add", "delete"] and not args.name:
            sys.exit("Error: Profile name is required for this action.")
        handle_profile(args)
    elif args.command == "zone":
        if args.action in ["add", "delete"] and not args.name:
            sys.exit("Error: Zone name is required for this action.")
        handle_zone(args)
    elif args.command == "run":
        handle_run(args)
    elif args.command == "post":
        handle_run(args, force_method="POST")

if __name__ == "__main__":
    main()

