#!/usr/bin/env python3
"""Install the manifest's skills using the cross-agent skills CLI."""

import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "config" / "skills.yaml"


def load_manifest(path=MANIFEST):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("Expected a version: 1 manifest mapping")
    agents = data.get("agents")
    if (not isinstance(agents, list) or not agents
            or not all(isinstance(a, str) and a for a in agents)):
        raise ValueError("agents must be a nonempty list of names")
    entries = data.get("installations")
    if not isinstance(entries, list) or not entries:
        raise ValueError("installations must be a nonempty list")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Each installation must be a mapping")
        for key in ("name", "source"):
            if not isinstance(entry.get(key), str) or not entry[key]:
                raise ValueError(f"Each installation needs a {key}")
        for key in ("skills", "agents"):
            values = entry.get(key)
            if (not isinstance(values, list) or not values
                    or not all(isinstance(v, str) and v for v in values)):
                raise ValueError(f"{entry['name']}: {key} must be a nonempty list")
        if not set(entry["agents"]) <= set(agents):
            raise ValueError(f"{entry['name']}: unknown agent")
    startup = data.get("startup")
    if not isinstance(startup, dict) or not isinstance(startup.get("skill"), str):
        raise ValueError("startup.skill must name a local skill")
    paths = startup.get("always_read")
    if not isinstance(paths, list) or not paths:
        raise ValueError("startup.always_read must list local skills")
    for relative in [startup["skill"], *paths]:
        if not isinstance(relative, str):
            raise ValueError("Startup paths must be strings")
        target = (ROOT / relative).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            raise ValueError(f"Missing or out-of-repository startup file: {relative}")
    return data


def install_commands(manifest, npx, selected, global_scope=False):
    commands = []
    for entry in manifest["installations"]:
        targets = [a for a in entry["agents"] if a in selected]
        if not targets:
            continue
        source = str(ROOT) if entry["source"] == "." else entry["source"]
        command = [npx, "--yes", "skills", "add", source,
                   "--skill", *entry["skills"], "--agent", *targets, "--copy", "--yes"]
        if global_scope:
            command.append("--global")
        commands.append(command)
    return commands


def normalize_local_lock(path=ROOT / "skills-lock.json"):
    """Keep this checkout's lock sources portable to other machines."""
    if not path.is_file():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for entry in data.get("skills", {}).values():
        if entry.get("sourceType") == "local" and entry.get("source") == str(ROOT):
            entry["source"] = "."
            changed = True
    if changed:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print commands without installing")
    parser.add_argument("--check", action="store_true", help="Validate the manifest offline")
    parser.add_argument("--global", dest="global_scope", action="store_true", help="Install user-wide")
    parser.add_argument("--agent", action="append", help="Limit agents; repeat for multiple")
    args = parser.parse_args()
    try:
        manifest = load_manifest()
        selected = args.agent or manifest["agents"]
        if not set(selected) <= set(manifest["agents"]):
            raise ValueError("Unknown agent; choose from " + ", ".join(manifest["agents"]))
        if args.check:
            print("Manifest and startup paths are valid.")
            return 0
        # Prefer .cmd on Windows to avoid PowerShell execution-policy restrictions.
        npx = shutil.which("npx.cmd" if sys.platform == "win32" else "npx")
        if not npx and not args.dry_run:
            raise ValueError("npx is missing; install Node.js 22.20+ and npm first")
        commands = install_commands(manifest, npx or "npx", selected, args.global_scope)
        for command in commands:
            print(shlex.join(command), flush=True)
            if not args.dry_run:
                subprocess.run(command, cwd=ROOT, check=True)
                if not args.global_scope:
                    normalize_local_lock()
        if "cursor" in selected:
            print("Cursor: pstack is enabled for this repo in .cursor/settings.json. "
                  "If unresolved, run /add-plugin pstack in Cursor, then /setup-pstack.")
        print("Load session-start in each new session. See docs/framework.md for host setup.")
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError, yaml.YAMLError) as error:
        print(f"Bootstrap failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
