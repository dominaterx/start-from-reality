#!/usr/bin/env python3
"""Dependency-free structural checks for the public plugin repository."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "start-from-reality"
SKILL = PLUGIN / "skills" / "start-from-reality"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


required = [
    ROOT / ".agents" / "plugins" / "marketplace.json",
    PLUGIN / ".codex-plugin" / "plugin.json",
    SKILL / "SKILL.md",
    SKILL / "agents" / "openai.yaml",
    ROOT / "evals" / "cases.yaml",
]
for path in required:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")

manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
if manifest.get("name") != "start-from-reality":
    fail("plugin name mismatch")
version = manifest.get("version", "")
if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
    fail("plugin version is not semver-like")
if manifest.get("skills") != "./skills/":
    fail("skills path must be ./skills/")
if not manifest.get("description") or not manifest.get("author", {}).get("name"):
    fail("plugin description and author.name are required")

interface = manifest.get("interface", {})
for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
    if not interface.get(field):
        fail(f"plugin interface.{field} is required")
if len(interface["displayName"]) > 30:
    fail("plugin interface.displayName exceeds the directory limit of 30 characters")
if "\n" in interface["shortDescription"] or len(interface["shortDescription"]) > 30:
    fail("plugin interface.shortDescription must be one line and at most 30 characters")
if len(interface["longDescription"]) > 4000:
    fail("plugin interface.longDescription exceeds the directory limit of 4000 characters")
if len(interface["developerName"]) > 80:
    fail("plugin interface.developerName exceeds the directory limit of 80 characters")
if manifest.get("author", {}).get("name") != interface["developerName"]:
    fail("plugin author.name and interface.developerName must match")
allowed_categories = {
    "Productivity",
    "Creativity",
    "Developer Tools",
    "Business & Operations",
    "Data & Analytics",
    "Communication",
    "Education & Research",
    "Security",
    "Finance",
    "Healthcare",
    "Travel",
    "Entertainment",
    "Other",
}
if interface["category"] not in allowed_categories:
    fail("plugin interface.category is not supported by the public directory")
capabilities = interface.get("capabilities", [])
if not isinstance(capabilities, list) or len(capabilities) > 20:
    fail("plugin interface.capabilities must be a list of at most 20 strings")
if any(not isinstance(item, str) or not item.strip() or "\n" in item or len(item) > 120 for item in capabilities):
    fail("each capability must be one non-empty line of at most 120 characters")
prompts = interface.get("defaultPrompt")
if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
    fail("plugin interface.defaultPrompt must contain one to three prompts")
if any(not isinstance(prompt, str) or not prompt.strip() or "\n" in prompt or len(prompt) > 128 for prompt in prompts):
    fail("each default prompt must be one non-empty line of at most 128 characters")
if len({" ".join(prompt.split()) for prompt in prompts}) != len(prompts):
    fail("plugin interface.defaultPrompt entries must be unique")
if any("@" in prompt for prompt in prompts):
    fail("plugin interface.defaultPrompt entries must not contain MCP mentions")

for field in ("websiteURL", "privacyPolicyURL"):
    value = interface.get(field)
    if value and (not isinstance(value, str) or not value.startswith("https://") or len(value) > 1024):
        fail(f"plugin interface.{field} must be an HTTPS URL of at most 1024 characters")

for field in ("logo", "composerIcon"):
    value = interface.get(field)
    if not isinstance(value, str) or not value.startswith("./"):
        fail(f"plugin interface.{field} must be a relative asset path beginning with ./")
    asset = PLUGIN / value[2:]
    if not asset.is_file():
        fail(f"plugin interface.{field} points to a missing file")
    if asset.suffix.lower() == ".svg":
        try:
            svg = ET.parse(asset).getroot()
        except ET.ParseError as exc:
            fail(f"plugin interface.{field} SVG is malformed: {exc}")
        if svg.tag.rsplit("}", 1)[-1] != "svg":
            fail(f"plugin interface.{field} SVG root element is not <svg>")
        view_box = svg.attrib.get("viewBox", "").split()
        if len(view_box) != 4:
            fail(f"plugin interface.{field} SVG must have a numeric viewBox")
        try:
            width, height = float(view_box[2]), float(view_box[3])
        except ValueError:
            fail(f"plugin interface.{field} SVG viewBox is not numeric")
        if width != height or width < 48:
            fail(f"plugin interface.{field} SVG must be square and at least 48 by 48")

changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
if f"## {version} " not in changelog:
    fail("plugin version is missing from CHANGELOG.md")

market = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
entries = [p for p in market.get("plugins", []) if p.get("name") == "start-from-reality"]
if len(entries) != 1:
    fail("marketplace must contain exactly one start-from-reality entry")
if entries[0].get("source", {}).get("path") != "./plugins/start-from-reality":
    fail("marketplace source path mismatch")
policy = entries[0].get("policy", {})
if policy.get("installation") not in {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}:
    fail("marketplace installation policy is invalid")
if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
    fail("marketplace authentication policy is invalid")
if not entries[0].get("category"):
    fail("marketplace category is required")

skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
if "[TODO:" in skill_text or "TODO" in skill_text:
    fail("SKILL.md contains a TODO placeholder")
if len(skill_text) > 20000:
    fail("SKILL.md exceeds the progressive-disclosure size budget")
if not skill_text.startswith("---\nname: start-from-reality\n"):
    fail("SKILL.md frontmatter is malformed")

for target in re.findall(r"\]\((references/[^)]+)\)", skill_text):
    if not (SKILL / target).is_file():
        fail(f"broken reference from SKILL.md: {target}")

agent_text = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
short_match = re.search(r'^\s*short_description:\s*"([^"]+)"\s*$', agent_text, re.MULTILINE)
if not short_match or not 25 <= len(short_match.group(1)) <= 64:
    fail("openai.yaml short_description must contain 25–64 characters")
prompt_match = re.search(r'^\s*default_prompt:\s*"([^"]+)"\s*$', agent_text, re.MULTILINE)
if not prompt_match or "$start-from-reality" not in prompt_match.group(1):
    fail("openai.yaml default_prompt must mention $start-from-reality")

case_text = (ROOT / "evals" / "cases.yaml").read_text(encoding="utf-8")
if case_text.count("  - id:") < 12:
    fail("expected at least twelve behavior cases")

for suffix in ("*.epub", "*.pdf", "*.docx", "*.mobi", "*.azw*"):
    if list(ROOT.rglob(suffix)):
        fail(f"source-book file found in repository: {suffix}")

print("OK: repository structure, links, manifest, and eval inventory are valid")
