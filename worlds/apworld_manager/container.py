from __future__ import annotations

import json
import zipfile

from typing import Dict, Any

from Utils import tuplize_version, Version

try:
    from worlds.Files import APWorldContainer
except ImportError:
    from ._vendor.world_container import APWorldContainer

class RepoWorldContainer(APWorldContainer):
    """A zipfile containing a world implementation."""
    github: str | None = None
    author: str | None = None
    description: str | None = None

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        try:
            manifest = super().read_contents(opened_zipfile)
        except KeyError:
            manifest = self.read_incorrect_contents(opened_zipfile)
        for string_key in ("github", "author", "description", "world_version_full"):
            if string_key in manifest:
                setattr(self, string_key, manifest[string_key])
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        for string_key in ("github", "author", "description", "world_version_full"):
            string = getattr(self, string_key, None)
            if string:
                manifest[string_key] = string
        return manifest

    def read_incorrect_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        """Read contents of the zipfile from an archipelago.json file in the subdirectory."""
        manifest = {}
        for file in opened_zipfile.namelist():
            if file.endswith("archipelago.json"):
                with opened_zipfile.open(file) as f:
                    contents = f.read()
                manifest = json.loads(contents)
        for string_key in ("game",):
            if string_key in manifest:
                setattr(self, string_key, manifest[string_key])

        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            if version_key in manifest:
                setattr(self, version_key, Version(*tuplize_version(manifest[version_key])))

        return manifest
