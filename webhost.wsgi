import logging
import os
import ModuleUpdate
ModuleUpdate.requirements_files.add(os.path.join("WebHostLib", "requirements.txt"))
ModuleUpdate.update(yes=True)

import WebHost

application = WebHost.get_app()

from worlds import AutoWorldRegister, network_data_package
# Update to only valid WebHost worlds
invalid_worlds = {name for name, world in AutoWorldRegister.world_types.items()
                    if not hasattr(world.web, "tutorials")}
if invalid_worlds:
    logging.error(f"Following worlds not loaded as they are invalid for WebHost: {invalid_worlds}")
AutoWorldRegister.world_types = {k: v for k, v in AutoWorldRegister.world_types.items() if k not in invalid_worlds}
network_data_package["games"] = {k: v for k, v in network_data_package["games"].items() if k not in invalid_worlds}

from WebHostLib.options import create as create_options_files
create_options_files()
WebHost.copy_tutorials_files_to_static()
