"""Outputs a Factorio Mod to facilitate integration with Archipelago"""

import dataclasses
import json
import os
import shutil
import threading
import zipfile
from typing import Optional, TYPE_CHECKING, Any, List, Callable, Tuple, Union

import jinja2

import Utils
import worlds.Files
from . import Options

if TYPE_CHECKING:
    from . import Factorio

data_template: Optional[jinja2.Template] = None
data_final_template: Optional[jinja2.Template] = None
locale_template: Optional[jinja2.Template] = None
control_template: Optional[jinja2.Template] = None
settings_template: Optional[jinja2.Template] = None

template_load_lock = threading.Lock()

base_info = {
    "version": Utils.__version__,
    "title": "Archipelago",
    "author": "Berserker",
    "homepage": "https://archipelago.gg",
    "description": "Integration client for the Archipelago Randomizer",
    "factorio_version": "2.0",
    "dependencies": [
        "base >= 2.0.28",
        "? quality >= 2.0.28",
        "! space-age",
        "? science-not-invited",
        "? factory-levels"
    ]
}


class FactorioModFile(worlds.Files.APPlayerContainer):
    game = "Factorio"
    compression_method = zipfile.ZIP_DEFLATED  # Factorio can't load LZMA archives
    writing_tasks: List[Callable[[], Tuple[str, Union[str, bytes]]]]
    patch_file_ending = ".zip"

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.writing_tasks = []

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        # directory containing Factorio mod has to come first, or Factorio won't recognize this file as a mod.
        mod_dir = self.path[:-4]  # cut off .zip
        for root, dirs, files in os.walk(mod_dir):
            for file in files:
                filename = os.path.join(root, file)
                opened_zipfile.write(filename,
                                     os.path.relpath(filename,
                                                     os.path.join(mod_dir, '..')))
        for task in self.writing_tasks:
            target, content = task()
            opened_zipfile.writestr(target, content)
        # now we can add extras.
        super().write_contents(opened_zipfile)

progressive_technology_table = {} # TODO

def generate_mod(
    player: int,
    seed_name: str,
    random,
    free_sample_excludes: set[str],
    output_directory: str,
):

    global data_final_template, locale_template, control_template, data_template, settings_template
    with template_load_lock:
        if not data_final_template:
            def load_template(name: str):
                import pkgutil
                data = pkgutil.get_data(__name__, "data/mod_template/" + name).decode()
                return data, name, lambda: False

            template_env = jinja2.Environment(
                loader=jinja2.FunctionLoader(load_template),
                undefined=jinja2.StrictUndefined,
            )

            data_template = template_env.get_template("data.lua")
            data_final_template = template_env.get_template("data-final-fixes.lua")
            locale_template = template_env.get_template(r"locale/en/locale.cfg")
            control_template = template_env.get_template("control.lua")
            settings_template = template_env.get_template("settings.lua")
    # get data for templates
    locations = [(location, location.item) for location in []] # TODO: deleted
    mod_name = f"AP-{seed_name}-P{player}-{multiworld.get_file_safe_player_name(player)}"
    versioned_mod_name = mod_name + "_" + Utils.__version__

    world_gen = world.options.world_gen.value
    world_gen_preset = {
        "default": False,
        "order": "a",
        "basic_settings": world_gen["basic"],
        "advanced_settings": world_gen["advanced"],
    }

    template_data = {
        "locations": locations,
        "player_names": multiworld.player_name,
        "mod_name": mod_name,
        "slot_name": world.player_name,
        "seed_name": seed_name,

        "default_death_link": "true" if world.options.death_link.value else "false",
        "deathlink_setting_name": "archipelago-death-link-{}-{}".format(player, seed_name),

        "free_samples": world.options.free_samples.value,
        "free_sample_excludes": {recipe: 1 for recipe in free_sample_excludes},
        "free_sample_quality_name": world.options.free_samples_quality.current_key,

        "progressive_technology_table": {tech.name: tech.progressive for tech in
                                         progressive_technology_table.values()},

        "goal": 0, # TODO
        "tech_tree_information": world.options.tech_tree_information.value,
        "starting_items": world.options.starting_items.value,
        "allow_imported_blueprints": "true" if world.options.imported_blueprints.value else "false",
        "world_gen_preset": world_gen_preset,
        "evolution_trap_increase": world.options.evolution_trap_increase.value,
        "energy_link": world.options.energy_link.value,
    }

    zf_path = os.path.join(output_directory, versioned_mod_name + ".zip")
    mod = FactorioModFile(zf_path, player=player, player_name=world.player_name)

    if world.zip_path:
        with zipfile.ZipFile(world.zip_path) as zf:
            for file in zf.infolist():
                if not file.is_dir() and "/data/mod/" in file.filename:
                    path_part = Utils.get_text_after(file.filename, "/data/mod/")
                    mod.writing_tasks.append(lambda arcpath=versioned_mod_name+"/"+path_part, content=zf.read(file):
                                             (arcpath, content))
    else:
        basepath = os.path.join(os.path.dirname(__file__), "data", "mod")
        for dirpath, dirnames, filenames in os.walk(basepath):
            base_arc_path = (versioned_mod_name+"/"+os.path.relpath(dirpath, basepath)).rstrip("/.\\")
            for filename in filenames:
                mod.writing_tasks.append(lambda arcpath=base_arc_path+"/"+filename,
                                                file_path=os.path.join(dirpath, filename):
                                         (arcpath, open(file_path, "rb").read()))

    mod.writing_tasks.append(lambda: (versioned_mod_name + "/data.lua",
                                      data_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/data-final-fixes.lua",
                                      data_final_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/control.lua",
                                      control_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/settings.lua",
                                      settings_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/locale/en/locale.cfg",
                                      locale_template.render(**template_data)))

    info = base_info.copy()
    info["name"] = mod_name
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/info.json",
                                      json.dumps(info, indent=4)))

    # write the mod file
    import pdb; pdb.set_trace()
    mod.write()
    return
