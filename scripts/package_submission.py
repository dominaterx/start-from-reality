#!/usr/bin/env python3
"""Build the skills-only ZIP expected by the OpenAI plugin submission portal."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "start-from-reality"
DIST = ROOT / "dist"


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_repo.py")], check=True)

    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    output = DIST / f"start-from-reality-v{manifest['version']}-submission.zip"
    DIST.mkdir(exist_ok=True)

    files = sorted(path for path in PLUGIN.rglob("*") if path.is_file())
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(PLUGIN)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

    print(output)


if __name__ == "__main__":
    main()
