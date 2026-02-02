"""Outputs a Factorio Mod to facilitate integration with Archipelago"""

import json
import os
import shutil
import threading
import zipfile
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Any, List, Callable, Tuple, Union

import jinja2

import Utils
import worlds.Files
from . import Options
from .Technologies import (
    never_give_free_samples_from_recipes,
    progressive_technology_stacks,
    technologies,
    technology_name_to_location_name, location_name_to_technology_name,

    ResearchRequirement,
    CraftRequirement,
    MineRequirement,
    BuildRequirement,
    CaptureSpawnerRequirement,
    CreateSpacePlatformRequirement,
)

if TYPE_CHECKING:
    from . import Factorio

template_parameters_template: Optional[jinja2.Template] = None
locale_template: Optional[jinja2.Template] = None

template_load_lock = threading.Lock()

base_info = {
    "version": Utils.__version__,
    "title": "Archipelago",
    "author": "Berserker",
    "homepage": "https://archipelago.gg",
    "description": "Integration client for the Archipelago Randomizer",
    "factorio_version": "2.0",
    "dependencies": [
        "base >= 2.0.73",
        "space-age >= 2.0.73",
    ]
}


class FactorioModFile(worlds.Files.APPlayerContainer):
    game = "Factorio: Space Age"
    writing_tasks: List[Callable[[], Tuple[str, Union[str, bytes]]]]
    patch_file_ending = ".zip"

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.writing_tasks = []

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        # directory containing Factorio mod has to come first, or Factorio won't recognize this file as a mod.
        mod_dir = self.path[:-len(".zip")]
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

def generate_mod(
    player: int,
    player_name: str,
    world_zip_path: str | None,
    world_locations: "list[FactorioLocation]",
    options: Options,
    multiworld: "Multiworld",
    output_directory: str,
):

    global template_parameters_template, locale_template
    with template_load_lock:
        if not template_parameters_template:
            def load_template(name: str):
                import pkgutil
                data = pkgutil.get_data(__name__, "data/mod_template/" + name).decode()
                return data, name, lambda: False

            template_env = jinja2.Environment(
                loader=jinja2.FunctionLoader(load_template),
                undefined=jinja2.StrictUndefined,
            )

            template_parameters_template = template_env.get_template("template_parameters.lua")
            locale_template = template_env.get_template("locale/en/locale.cfg")

    # get data for templates
    mod_name = f"AP-{multiworld.seed_name}-P{player}-{multiworld.get_file_safe_player_name(player)}"
    versioned_mod_name = f"{mod_name}_{Utils.__version__}"

    death_link_setting_name = "archipelago-death-link-{}-{}".format(player, multiworld.seed_name)

    free_sample_excludes = set()
    free_sample_excludes.update(options.free_sample_blacklist.value)
    for item in options.free_sample_whitelist.value:
        del free_sample_excludes[item]
    free_sample_excludes.update(never_give_free_samples_from_recipes)

    @dataclass
    class LocaleLocation:
        name: str
        display_name: str
        description: str
    locale_locations: list[LocaleLocation] = []
    new_technology_data: dict[str, dict] = {}
    for location in world_locations:
        if location.revealed:
            item = location.item
            receiver_name = multiworld.player_name[item.player]
            display_name = f"{receiver_name}'s {item.name} ({location.name})"
            if item.advancement:
                helpfulness_clause = ", which is considered a logical advancement"
                icon = "/ap.png"
            elif item.useful:
                helpfulness_clause = ", which is considered useful"
                icon = "/ap_unimportant.png"
            elif item.trap:
                helpfulness_clause = ", which is considered fun"
                icon = "/ap_unimportant.png"
            else:
                helpfulness_clause = ""
                icon = "/ap_unimportant.png"
            description = f"Researching this technology sends {item.name} to {receiver_name}{helpfulness_clause}."
            # TODO: set icon = "automation" or such if it's a Factorio item.
        else:
            display_name = location.name
            description = "Researching this technology sends something to someone."
            icon = "/ap_unimportant.png"
        locale_locations.append(LocaleLocation(location.name, display_name, description))

        technology = technologies[location_name_to_technology_name[location.name]]
        # https://lua-api.factorio.com/latest/prototypes/TechnologyPrototype.html
        tech_data = {
            "icon": icon,
            # Mimic the same prerequisit map.
            "prerequisites": [technology_name_to_location_name[name] for name in sorted(technology.prerequisites)],
        }
        if type(technology.requirement) == ResearchRequirement:
            # https://lua-api.factorio.com/latest/types/TechnologyUnit.html
            unit = {
                "time": technology.requirement.energy,
                "ingredients": [[ingredient_name, amount] for ingredient_name, amount in technology.requirement.ingredients.items()],
            }
            if type(technology.requirement.units) == str:
                # Infinite
                unit["count_formula"] = technology.requirement.units
            else:
                unit["count"] = technology.requirement.units
            tech_data["unit"] = unit
        elif type(technology.requirement) == CraftRequirement:
            tech_data["research_trigger"] = {
                "type": "craft-item",
                "item": {"name": technology.requirement.item},
                "count": technology.requirement.count,
            }
        elif type(technology.requirement) == MineRequirement:
            tech_data["research_trigger"] = {
                "type": "mine-entity",
                "entity": technology.requirement.entity,
            }
        elif type(technology.requirement) == BuildRequirement:
            tech_data["research_trigger"] = {
                "type": "build-entity",
                "entity": technology.requirement.entity,
            }
        elif type(technology.requirement) == CaptureSpawnerRequirement:
            tech_data["research_trigger"] = {
                "type": "capture-spawner",
            }
        elif type(technology.requirement) == CreateSpacePlatformRequirement:
            tech_data["research_trigger"] = {
                "type": "create-space-platform",
            }
        else: assert False, str(type(technology.requirement))
        new_technology_data[location.name] = tech_data

    def set_to_1(s):
        return {x: 1 for x in s}

    mod_params = {
        "mod_name": mod_name,
        "seed_name": multiworld.seed_name,
        "slot_name": player_name,

        "default_death_link": bool(options.death_link.value),
        "death_link_setting": death_link_setting_name,
        "energy_link_increment": 10_000_000 if options.energy_link.value else 0,
        "trap_evo_factor": options.evolution_trap_increase.value / 100,

        "free_sample_amount": options.free_samples.current_key,
        "free_sample_quality": options.free_samples_quality.current_key,
        "free_sample_excludes": set_to_1(free_sample_excludes),

        "hide_base_technologies": sorted(technologies.keys()),
        "new_technology_data": new_technology_data,
        "progressive_technology_stacks": progressive_technology_stacks,

        "allow_imported_blueprints": bool(options.imported_blueprints.value),
        "starting_items": options.starting_items.value,
        "world_gen_preset": {
            "default": False,
            "order": "a",
            "basic_settings": options.world_gen.value["basic"],
            "advanced_settings": options.world_gen.value["advanced"],
        },
    }
    template_parameters_contents = template_parameters_template.render(mod_params=render_lua_value(mod_params))

    locale_contents = locale_template.render(
        locations=locale_locations,
        death_link_setting=death_link_setting_name,
    )

    zf_path = os.path.join(output_directory, versioned_mod_name + ".zip")
    mod = FactorioModFile(zf_path, player=player, player_name=player_name)

    if world_zip_path:
        with zipfile.ZipFile(world_zip_path) as zf:
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

    mod.writing_tasks.append(lambda: (versioned_mod_name + "/template_parameters.lua",
                                      template_parameters_contents))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/locale/en/locale.cfg",
                                      locale_contents))

    info = base_info.copy()
    info["name"] = mod_name
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/info.json",
                                      json.dumps(info, indent=4) + "\n"))

    # write the mod file
    mod.write()
    return

def render_lua_value(x):
    from io import StringIO
    import re
    out = StringIO()
    def recurse(x, indentation):
        # Numbers and strings repr correctly from python to lua.
        if type(x) in (int, float, str): return out.write(repr(x))
        # Booleans are slightly different.
        if type(x) == bool: return out.write("true" if x else "false")
        if type(x) == list:
            if len(x) == 0: return out.write("{}")
            if len(x) <= 2 and all(type(child) in (int, float, str) for child in x):
                # This is perhaps a tuple like {"automation-science-pack", 1}
                out.write("{")
                out.write(repr(x[0]))
                if len(x) == 2:
                    out.write(", ")
                    out.write(repr(x[1]))
                out.write("}")
                return
            out.write("{\n")
            new_indentation = indentation + "  "
            for child in x:
                out.write(new_indentation)
                recurse(child, new_indentation)
                out.write(",\n")
            out.write(indentation)
            out.write("}")
            return
        if type(x) == dict:
            if len(x) == 0: return out.write("{}")
            out.write("{\n")
            new_indentation = indentation + "  "
            for name, child in x.items():
                out.write(new_indentation)
                if re.match(r'^\w+$', name):
                    # Simple identifier
                    out.write(name)
                else:
                    # Needs quotes.
                    out.write("[" + repr(name) + "]")
                out.write(" = ")
                recurse(child, new_indentation)
                out.write(",\n")
            out.write(indentation)
            out.write("}")
            return
        assert False, f"cannot render type to Lua: {type(x)}: {repr(x)}"

    recurse(x, "")
    return out.getvalue()
