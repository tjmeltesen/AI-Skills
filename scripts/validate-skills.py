#!/usr/bin/env python3
"""
AI-Skills Repository Validator
Validates skill frontmatter, directory naming, and document structure
according to the Agent Skills / AI Hero specification.
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
    """Validate a single SKILL.md file. Returns list of errors."""
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
    
    # 2. Check required field: name
    name = data.get("name")
    if not name:
        errors.append("Missing required frontmatter field: 'name'")
    elif not isinstance(name, str):
        errors.append("Frontmatter field 'name' must be a string")
    else:
        if not NAME_PATTERN.match(name):
            errors.append(f"'name' ('{name}') must be lowercase kebab-case (letters, numbers, hyphens only).")
        parent_dir_name = skill_path.parent.name
        if name != parent_dir_name:
            errors.append(f"Skill name ('{name}') does not match directory name ('{parent_dir_name}').")
    
    # 3. Check required field: description
    desc = data.get("description")
    if not desc:
        errors.append("Missing required frontmatter field: 'description'")
    elif not isinstance(desc, str):
        errors.append("Frontmatter field 'description' must be a string")
    elif len(desc.strip()) < 10:
        errors.append("Frontmatter field 'description' is too short (must be at least 10 characters).")
    
    # 4. Optional metadata validation
    if "metadata" in data and not isinstance(data["metadata"], dict):
        errors.append("'metadata' field must be a key-value mapping if present.")
    
    # 5. Body Structure: H1 Title check
    h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if not h1_match:
        errors.append("Markdown body must contain at least one top-level H1 header ('# Title').")
    
    # 6. Balanced code fences
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
            print("  [PASS] Frontmatter & structure valid.")
    
    print("\n" + "=" * 50)
    if total_errors > 0:
        print(f"FAILED: {total_errors} error(s) found across {len(skill_files)} skill(s).")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(skill_files)} skill(s) passed validation!")
        sys.exit(0)


if __name__ == "__main__":
    main()
