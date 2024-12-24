import worlds.LauncherComponents as LauncherComponents

from .world import KeymastersKeepWorld


def launch_client() -> None:
    from .client import main
    LauncherComponents.launch_subprocess(main, name="KeymastersKeepClient")


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Keymaster's Keep Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT
    )
)