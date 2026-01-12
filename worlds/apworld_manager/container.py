from __future__ import annotations

import zipfile
from typing import Any

from worlds.Files import APWorldContainer

LITERAL_KEYS = ("github", "authors", "world_version_full", "tracker", "flags", "repo_url")

class RepoWorldContainer(APWorldContainer):
    """A zipfile containing a world implementation."""
    github: str | None = None

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        if "poptracker" in manifest:
            manifest["tracker"] = manifest.pop("poptracker")
            del manifest["poptracker"]
        for lit_key in LITERAL_KEYS:
            if lit_key in manifest:
                setattr(self, lit_key, manifest[lit_key])
        return manifest

    def get_manifest(self) -> dict[str, Any]:
        manifest = super().get_manifest()
        for lit_key in LITERAL_KEYS:
            value = getattr(self, lit_key, None)
            if value is not None:
                manifest[lit_key] = value
        return manifest
