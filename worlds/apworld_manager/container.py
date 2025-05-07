from __future__ import annotations

import zipfile

from typing import (Dict, Any, TYPE_CHECKING)

if TYPE_CHECKING:
    from Utils import Version

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
        manifest = super().read_contents(opened_zipfile)
        for string_key in ("github", "author", "description"):
            if string_key in manifest:
                setattr(self, string_key, manifest[string_key])
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        for string_key in ("github", "author", "description"):
            string = getattr(self, string_key)
            if string:
                manifest[string_key] = string
        return manifest
