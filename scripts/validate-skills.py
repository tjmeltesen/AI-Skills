#!/usr/bin/env python3
"""
AI-Skills Repository Validator
Validates skill frontmatter according to the comprehensive YAML frontmatter specification
(agentskills.io standard, Anthropic Claude Code, Google Antigravity, Cursor, and Windsurf),
directory naming conventions, and document structure.
"""

import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not found. Installing pyyaml...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    import yaml


NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
IS_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"

VALID_CONTEXT_MODES = {"inherit", "fresh", "fork"}
VALID_WORKSPACE_MODES = {"inherit", "branch", "share"}


def log_error(file_path: Path, message: str, line: int = 1):
    if IS_GITHUB_ACTIONS:
        print(f"::error file={file_path.as_posix()},line={line}::{message}")
    print(f"  [FAIL] Line {line}: {message}")


def extract_frontmatter(content: str):
    """Extract YAML frontmatter and remaining markdown body."""
    if not content.startswith("---"):
        return None, content, "File does not start with '---' YAML frontmatter delimiter."
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content, "Unterminated frontmatter; missing closing '---'."
    
    frontmatter_raw = parts[1]
    body = parts[2]
    return frontmatter_raw, body, None


def validate_skill_file(skill_path: Path) -> list:
    """Validate a single SKILL.md file against the master frontmatter specification. Returns list of errors."""
    errors = []
    
    try:
        content = skill_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Unable to read file: {e}"]
    
    # 1. Frontmatter existence and parsing
    fm_raw, body, err = extract_frontmatter(content)
    if err:
        errors.append(err)
        return errors
    
    try:
        data = yaml.safe_load(fm_raw)
    except Exception as e:
        errors.append(f"Invalid YAML in frontmatter: {e}")
        return errors
    
    if not isinstance(data, dict):
        errors.append("Frontmatter must be a YAML dictionary/mapping.")
        return errors
    
    # ── Tier 1: Core Specification (Required) ──
    name = data.get("name")
    if not name:
        errors.append("Missing required frontmatter field: 'name'")
    elif not isinstance(name, str):
        errors.append("Frontmatter field 'name' must be a string")
    else:
        if len(name) > 64:
            errors.append(f"'name' is too long ({len(name)} chars; max 64).")
        if not NAME_PATTERN.match(name):
            errors.append(f"'name' ('{name}') must be lowercase kebab-case (letters, numbers, hyphens only).")
        parent_dir_name = skill_path.parent.name
        if name != parent_dir_name:
            errors.append(f"Skill name ('{name}') does not match directory name ('{parent_dir_name}').")
    
    desc = data.get("description")
    if not desc:
        errors.append("Missing required frontmatter field: 'description'")
    elif not isinstance(desc, str):
        errors.append("Frontmatter field 'description' must be a string")
    elif len(desc.strip()) < 10:
        errors.append("Frontmatter field 'description' is too short (must be at least 10 characters).")
    elif len(desc) > 1024:
        errors.append(f"Frontmatter field 'description' exceeds 1024 character limit ({len(desc)} chars).")

    # ── agentskills.io compatibility & license ──
    if "compatibility" in data:
        if not isinstance(data["compatibility"], str):
            errors.append("Field 'compatibility' must be a string.")
        elif len(data["compatibility"]) > 500:
            errors.append("Field 'compatibility' exceeds 500 character limit.")

    # ── Tier 2: Invocation & Interaction Controls ──
    for bool_field in ["disable-model-invocation", "user-invoked", "always-on", "alwaysApply"]:
        if bool_field in data and not isinstance(data[bool_field], bool):
            errors.append(f"Field '{bool_field}' must be a boolean (true/false).")
    
    if "argument-hint" in data and not isinstance(data["argument-hint"], str):
        errors.append("Field 'argument-hint' must be a string.")
    
    if "trigger" in data and not isinstance(data["trigger"], str):
        errors.append("Field 'trigger' must be a string.")
    
    if "triggers" in data and not isinstance(data["triggers"], (list, str)):
        errors.append("Field 'triggers' must be a string or list of strings.")

    # ── Tier 3: Execution Context & Subagent Dispatch ──
    if "model" in data and not isinstance(data["model"], str):
        errors.append("Field 'model' must be a string.")
    
    if "context" in data:
        if data["context"] not in VALID_CONTEXT_MODES:
            errors.append(f"Field 'context' must be one of {sorted(VALID_CONTEXT_MODES)}, got '{data['context']}'.")
            
    if "workspace" in data:
        if data["workspace"] not in VALID_WORKSPACE_MODES:
            errors.append(f"Field 'workspace' must be one of {sorted(VALID_WORKSPACE_MODES)}, got '{data['workspace']}'.")
            
    if "role" in data and not isinstance(data["role"], str):
        errors.append("Field 'role' must be a string.")
        
    for timeout_field in ["timeout", "timeout-seconds"]:
        if timeout_field in data and not isinstance(data[timeout_field], int):
            errors.append(f"Field '{timeout_field}' must be an integer.")
            
    if "is-daemon" in data and not isinstance(data["is-daemon"], bool):
        errors.append("Field 'is-daemon' must be a boolean.")

    # ── Tier 4: Tool Access & Permissions ──
    for tool_field in ["tools", "allowed-tools"]:
        if tool_field in data:
            if isinstance(data[tool_field], list):
                if not all(isinstance(t, str) for t in data[tool_field]):
                    errors.append(f"Field '{tool_field}' list must contain strings only.")
            elif isinstance(data[tool_field], str):
                pass  # Space-delimited string per agentskills.io
            else:
                errors.append(f"Field '{tool_field}' must be a list of strings or space-delimited string.")

    for blacklist_field in ["disallowed-tools", "disable-tools"]:
        if blacklist_field in data:
            if not isinstance(data[blacklist_field], list) or not all(isinstance(t, str) for t in data[blacklist_field]):
                errors.append(f"Field '{blacklist_field}' must be a list of tool name strings.")
                
    for bool_tool_field in ["enable-write-tools", "enable-mcp-tools", "enable-subagent-tools"]:
        if bool_tool_field in data and not isinstance(data[bool_tool_field], bool):
            errors.append(f"Field '{bool_tool_field}' must be a boolean.")

    # ── Tier 5: Filepath Matching & Scoping ──
    for path_list_field in ["paths", "file-types"]:
        if path_list_field in data:
            if not isinstance(data[path_list_field], list) or not all(isinstance(p, str) for p in data[path_list_field]):
                errors.append(f"Field '{path_list_field}' must be a list of strings.")
                
    if "globs" in data:
        if not isinstance(data["globs"], (list, str)):
            errors.append("Field 'globs' must be a string or list of strings.")

    # ── Tier 6: Dependencies & Prerequisites ──
    for dep_field in ["requires", "dependencies"]:
        if dep_field in data and not isinstance(data[dep_field], (dict, list)):
            errors.append(f"Field '{dep_field}' must be a mapping or list.")
            
    if "env" in data and not isinstance(data["env"], dict):
        errors.append("Field 'env' must be a key-value dictionary.")

    # ── Tier 7: Metadata & Catalog Discovery ──
    for str_meta in ["version", "author", "maintainer", "license", "homepage", "repository", "category"]:
        if str_meta in data and not isinstance(data[str_meta], str):
            errors.append(f"Field '{str_meta}' must be a string.")
            
    for list_meta in ["tags", "keywords"]:
        if list_meta in data:
            if not isinstance(data[list_meta], list) or not all(isinstance(t, str) for t in data[list_meta]):
                errors.append(f"Field '{list_meta}' must be a list of strings.")
                
    if "metadata" in data and not isinstance(data["metadata"], dict):
        errors.append("Field 'metadata' must be a key-value dictionary.")

    # ── Body Structure Checks ──
    h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if not h1_match:
        errors.append("Markdown body must contain at least one top-level H1 header ('# Title').")
    
    fences = re.findall(r"^```", body, re.MULTILINE)
    if len(fences) % 2 != 0:
        errors.append(f"Unbalanced code block fences (found {len(fences)} occurrences of ```).")
    
    return errors


def main():
    repo_root = Path(__file__).resolve().parent.parent
    print(f"Scanning for SKILL.md files in: {repo_root}")
    
    ignore_dirs = {".git", ".github", "node_modules", ".venv", "venv", "__pycache__", "scripts"}
    
    skill_files = []
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if f.lower() == "skill.md":
                skill_files.append(Path(root) / f)
    
    if not skill_files:
        print("No SKILL.md files found in repository!")
        sys.exit(1)
    
    print(f"Found {len(skill_files)} skill(s) to validate.\n")
    
    total_errors = 0
    for skill_path in sorted(skill_files):
        rel_path = skill_path.relative_to(repo_root)
        print(f"Validating {rel_path}...")
        errors = validate_skill_file(skill_path)
        
        if errors:
            total_errors += len(errors)
            for err in errors:
                log_error(rel_path, err)
        else:
            print("  [PASS] Master frontmatter & structure valid.")
    
    print("\n" + "=" * 50)
    if total_errors > 0:
        print(f"FAILED: {total_errors} error(s) found across {len(skill_files)} skill(s).")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(skill_files)} skill(s) passed validation!")
        sys.exit(0)


if __name__ == "__main__":
    main()
