## Summary

<!--
Pick the smallest visual that makes the change clear:
- File tree / folder layout
- Workflow steps / call tree
- Architecture or sequence diagram
- Diff-sketch
-->

## Evidence

- **Before:** <!-- Screenshot, CLI output, or previous behavior -->
  **After:** <!-- Screenshot, CLI output, or passing validation run -->

## Merge Danger

**Door:** <!-- One-way (hard to rollback) or Two-way (cheap/easy to reverse) -->

<!-- Description of reversibility if applicable -->

**Blast Radius:** <!-- Concise description of scope (e.g. Low, Isolated to 1 skill, Repo-wide) -->

<!-- Potential ramifications of merge -->

---
### Author Checklist
- [ ] Skill frontmatter (`name`, `description`) is complete and valid YAML
- [ ] Skill folder name strictly matches `name` in kebab-case
- [ ] Document structure has top-level H1 header and balanced code blocks
- [ ] `python scripts/validate-skills.py` passes locally
