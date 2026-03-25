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
from .FactorioData import parse_level_from_technology_prototype_name
from .data.ap_data import (
    energy_link_bridge_recipes,
)
from .data.json_dumps_but_smaller import json_dumps
from .data.ap_data import (
    never_give_free_samples_from_recipes,
)
from .data import generated_names as names

if TYPE_CHECKING:
    from . import Factorio

template_parameters_template: Optional[jinja2.Template] = None
locale_template: Optional[jinja2.Template] = None

template_load_lock = threading.Lock()

__version__ = "1.1.2"


buffed_resources_basic = {
    "autoplace_controls": {
        # Resources
        ## Nauvis
        "iron-ore":             { "frequency": 6, "size": 6, "richness": 6 },
        "copper-ore":           { "frequency": 6, "size": 6, "richness": 6 },
        "stone":                { "frequency": 6, "size": 6, "richness": 6 },
        "coal":                 { "frequency": 6, "size": 6, "richness": 6 },
        "crude-oil":            { "frequency": 6, "size": 6, "richness": 6 },
        "uranium-ore":          { "frequency": 6, "size": 6, "richness": 6 },
        ## Vulcanus
        "vulcanus_coal":        { "frequency": 6, "size": 6, "richness": 6 },
        "calcite":              { "frequency": 6, "size": 6, "richness": 6 },
        "sulfuric_acid_geyser": { "frequency": 6, "size": 6, "richness": 6 },
        "tungsten_ore":         { "frequency": 6, "size": 6, "richness": 6 },
        ## Gleba
        "gleba_stone":          { "frequency": 6, "size": 6, "richness": 6 },
        ## Fulgora
        "scrap":                { "frequency": 6, "size": 6, "richness": 6 },
        ## Aquilo
        "aquilo_crude_oil":     { "frequency": 6, "size": 6, "richness": 6 },
        "lithium_brine":        { "frequency": 6, "size": 6, "richness": 6 },
        "fluorine_vent":        { "frequency": 6, "size": 6, "richness": 6 },

        # Terrain
        ## Nauvis
        "water":                  { "frequency": 1, "size": 0.5, "richness": 1 },
        "trees":                  { "frequency": 1, "size": 1, "richness": 1 },
        "rocks":                  { "frequency": 1, "size": 1, "richness": 1 },
        "starting_area_moisture": { "frequency": 1, "size": 1, "richness": 1 },
        ## Vulcanus
        "vulcanus_volcanism": { "frequency": 0.1666666716337204, "size": 6, "richness": 1 },
        ## Gleba
        "gleba_water":        { "frequency": 0.1666666716337204, "size": 0.1666666716337204, "richness": 1 },
        "gleba_plants":       { "frequency": 0.1666666716337204, "size": 6, "richness": 1 },
        ## Fulgora
        "fulgora_islands":    { "frequency": 0.1666666716337204, "size": 6, "richness": 1 },
        ## Cliffs
        "nauvis_cliff":       { "frequency": 1, "size": 0, "richness": 1 },
        "gleba_cliff":        { "frequency": 1, "size": 0, "richness": 1 },
        "fulgora_cliff":      { "frequency": 1, "size": 0, "richness": 1 },

        # Enemy
        "enemy-base":         { "frequency": 0.25, "size": 1.5, "richness": 1 },
        "gleba_enemy_base":   { "frequency": 1, "size": 0.25, "richness": 1 },
    },
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

def read_local_path(name: str) -> bytes:
    import pkgutil
    return pkgutil.get_data(__name__, name)

def generate_mod(
    player: int,
    player_name: str,
    world_locations: "list[FactorioLocation]",
    options: Options,
    multiworld: "Multiworld",
    logic_events: dict,
    progressive_technology_stacks: dict[str, dict[str, str]],
    technology_name_to_progressive_group_name: dict[str, str],
    infinite_technology_names: set[str],
    infinite_technology_shuffle: dict[str, str] | None,
    technology_props_lua: dict[str, dict],
    recipe_changes: dict[str, dict[str, object]],
    rocket_parts_per_rocket: int,
    asteroid_hp_changes: dict[str, float],
    technology_effect_additions: dict[str, dict],
    starting_planet: str,
    vulcanus_rock_multiplier: float,
    enable_alternate_explosives: bool,
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
    versioned_mod_name = f"{mod_name}_{__version__}"

    death_link_setting_name = "archipelago-death-link-{}-{}".format(player, multiworld.seed_name)

    free_sample_excludes = options.free_sample_excludes.value | never_give_free_samples_from_recipes

    @dataclass
    class LocaleLocation:
        name: str
        display_name: str
        description: str
    locale_locations: list[LocaleLocation] = []
    new_technology_data: dict[str, dict] = {}
    infinite_technology_name_corrections: dict[str, str] = {}
    for location in world_locations:
        technology_name = location.name.replace("_other_location", "_location").replace("_location", "")
        if technology_name in infinite_technology_names:
            # At runtime, infinite technology names include the level at the end of the name.
            # e.g. "electric-weapons-damage-4_location" is at force.technologies["electric-weapons-damage-4_location-4"]
            infinite_technology_name_corrections[location.name] = "{}-{}".format(
                location.name,
                parse_level_from_technology_prototype_name(technology_name)
            )
            if options.infinite_technologies.current_key == "removed":
                continue
            elif options.infinite_technologies.current_key == "vanilla":
                item_name = technology_name
            elif options.infinite_technologies.current_key == "shuffled":
                item_name = infinite_technology_shuffle[technology_name]
            else: assert False
            target_props_item_name = item_name
            item_name = technology_name_to_progressive_group_name[item_name]
            target_player = player
            is_goal = False
            is_advancement = False
            is_useful = True
            is_trap = False
        else:
            item = location.item
            item_name = item.name
            target_player = item.player
            is_goal = item_name == names.victory
            is_advancement = item.advancement
            is_useful = item.useful
            is_trap = item.trap

        display_name = location.name
        helpfulness_clause = ""
        icon = "/ap_unimportant.png"
        display_item_name = "something"
        receiver_name = "someone"
        if location.revealed or options.tech_tree_information.current_key == "full":
            # Full information
            receiver_name = multiworld.player_name[target_player]
            display_name = f"{receiver_name}'s {item_name} ({location.name})"
            display_item_name = item_name
            if is_goal:
                helpfulness_clause = ", which completes your goal"
                icon = "/trophy.png"
            elif is_advancement:
                helpfulness_clause = ", which is considered a logical advancement"
                icon = "/ap.png"
            elif is_useful:
                helpfulness_clause = ", which is considered useful"
                icon = "/ap_unimportant.png"
            elif is_trap:
                helpfulness_clause = ", which is considered fun"
                icon = "/ap_unimportant.png"
            if item_name in technology_props_lua:
                # This is an item for Factorio (probably). Use the built in icon.
                icon = item_name
            elif item_name in progressive_technology_stacks:
                # This is a progressive item for Factorio (probably). Use one of the icons in the stack.
                icon = {
                    # Override a few of the large group icons, because the first item in the list isn't always a good representative.
                    names.progressive_oil: names.oil_processing,
                    names.progressive_circuit: names.advanced_circuit,
                    names.progressive_robotics: names.construction_robotics,
                    names.progressive_uranium: names.uranium_processing,
                    names.progressive_space: names.space_platform_thruster,
                    names.progressive_gleba: names.planet_discovery_gleba,
                    names.progressive_fulgora: names.planet_discovery_fulgora,
                    names.progressive_promethium: names.promethium_science_pack,
                }.get(item_name, progressive_technology_stacks[item_name][0])
            elif item_name == names.ap_energy_link_bridge:
                # Handled specially in data-updates.lua.
                icon = item_name
        else:
            # Partial or no information.
            if options.tech_tree_information.current_key in ("advancement", "recipient_advancement"):
                # Reveal flags.
                if is_advancement or is_trap:
                    helpfulness_clause = ", which is considered a logical advancement"
                    icon = "/ap.png"
                elif is_useful:
                    helpfulness_clause = ", which is considered useful"
                    icon = "/ap_unimportant.png"
            if options.tech_tree_information.current_key in ("recipient", "recipient_advancement"):
                # Reveal recipient.
                receiver_name = multiworld.player_name[target_player]
        description = f"Researching this technology sends {display_item_name} to {receiver_name}{helpfulness_clause}."
        locale_location = LocaleLocation(location.name, display_name, description)

        technology_props = technology_props_lua[technology_name]
        if options.technology_prerequisites.current_key == "vanilla":
            # Translate preprequisite tech names to the AP names.
            prerequisites = [name + "_location" for name in technology_props["prerequisites"]]
        elif options.technology_prerequisites.current_key == "removed":
            prerequisites = []
        else: assert False, options.technology_prerequisites.current_key
        # https://lua-api.factorio.com/latest/prototypes/TechnologyPrototype.html
        tech_data = {
            "icon": icon,
            "prerequisites": prerequisites,
        }
        if "unit" in technology_props:
            tech_data["unit"] = {
                **technology_props["unit"],
            }
            if "count" in technology_props["unit"]:
                # Adjust finite tech cost according to settings.
                tech_data["unit"]["count"] = max(1, technology_props["unit"]["count"] // options.tech_cost_divisor)
            else:
                # Infinite.
                tech_data["level"] = technology_props["level"]
                tech_data["max_level"] = technology_props["max_level"]
                target_props = technology_props_lua[target_props_item_name]
                tech_data["effects"] = target_props["effects"]
        else:
            tech_data["research_trigger"] = technology_props["research_trigger"]

        new_technology_data[location.name] = tech_data
        locale_locations.append(locale_location)

    world_gen_preset = {
        "default": False,
        "order": "a",
        "basic_settings": {},
        "advanced_settings": {},
    }
    if options.world_gen.current_key == "custom":
        world_gen_preset["basic_settings"] = options.world_gen_custom.value["basic"]
        world_gen_preset["advanced_settings"] = options.world_gen_custom.value["advanced"]
    else:
        if options.world_gen.current_key == "vanilla":
            pass # No modifications.
        elif options.world_gen.current_key == "buffed_resources":
            world_gen_preset["basic_settings"] = buffed_resources_basic
        else: assert False
        # Additional adjustments when not custom.
        if options.world_gen_enemies.value == False:
            world_gen_preset["basic_settings"]["no_enemies_mode"] = True
            world_gen_preset["advanced_settings"]["pollution"] = {"enabled": False}
        # These next two don't go into the preset for some reason??
        # In order to implement these, we'd need to give world gen settings directly to the --create invocation
        # using one of the json file interfaces, not through a preset created by a mod.
        if options.world_gen_asteroid_spawn_rate.value != 100:
            raise NotImplementedError("TODO: world_gen_asteroid_spawn_rate must be 100")
        if options.world_gen_spoil_rate.value != 100:
            raise NotImplementedError("TODO: world_gen_spoil_rate must be 100")

    def set_to_1(s: set):
        return {x: 1 for x in s}

    mod_params = {
        "mod_name": mod_name,
        "seed_name": multiworld.seed_name,
        "slot_name": player_name,
        "goal": options.goal.current_key,

        "default_death_link": bool(options.death_link.value),
        "death_link_setting": death_link_setting_name,
        "trap_evo_factor": options.evolution_trap_increase.value / 100,
        "energy_link_increment": 10_000_000 if options.energy_link.value else 0,
        "energy_link_bridge_ingredients": energy_link_bridge_recipes[options.energy_link_recipe.current_key],
        "energy_link_bridge_starts_unlocked": not options.energy_link_technology.value,

        "starting_items": options.starting_items.value,
        "free_sample_amount": options.free_samples.current_key,
        "free_sample_quality": options.free_samples_quality.current_key,
        "free_sample_excludes": set_to_1(free_sample_excludes),
        "recipe_changes": recipe_changes,
        "rocket_parts_per_rocket": rocket_parts_per_rocket,
        "asteroid_hp_changes": asteroid_hp_changes,
        "technology_effect_additions": technology_effect_additions,

        "starting_planet": starting_planet,
        "vulcanus_rock_multiplier": vulcanus_rock_multiplier,
        "enable_alternate_explosives": enable_alternate_explosives,

        "hide_base_technologies": sorted(technology_props_lua.keys()),
        "new_technology_data": new_technology_data,
        "progressive_technology_stacks": progressive_technology_stacks,
        "infinite_technology_name_corrections": infinite_technology_name_corrections,

        "allow_imported_blueprints": bool(options.allow_imported_blueprints.value),
        "world_gen_preset": world_gen_preset,
    }
    template_parameters_contents = template_parameters_template.render(mod_params=render_lua_value(mod_params))

    locale_contents = locale_template.render(
        locations=locale_locations,
        death_link_setting=death_link_setting_name,
    )

    zf_path = os.path.join(output_directory, versioned_mod_name + ".zip")
    mod = FactorioModFile(zf_path, player=player, player_name=player_name)

    for path in [
        "LICENSE.md",
        "thumbnail.png",
        "settings.lua",
        "settings-updates.lua",
        "data-updates.lua",
        "control.lua",
        "lib.lua",
        "graphics/icons/ap.png",
        "graphics/icons/ap_unimportant.png",
        "graphics/icons/trophy.png",
    ]:
        def f(
            arcpath=versioned_mod_name+"/"+path,
            file_path="data/mod/" + path,
        ):
            return arcpath, read_local_path(file_path)
        mod.writing_tasks.append(f)

    mod.writing_tasks.append(lambda: (versioned_mod_name + "/template_parameters.lua",
                                      template_parameters_contents))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/locale/en/locale.cfg",
                                      locale_contents))

    info = {
        "name": mod_name,
        "version": __version__,
        "title": "Archipelago",
        "author": "Berserker, Josh Wolfe",
        "homepage": "https://archipelago.gg",
        "description": "Integration client for the Archipelago Randomizer",
        "factorio_version": "2.0",
        "dependencies": [
            "base >= 2.0.73",
            "space-age >= 2.0.73",
            "? respawn-to-any-planet",
        ]
    }
    if starting_planet != names.nauvis:
        info["dependencies"].append("any-planet-start >= 1.1.28"),
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/info.json",
                                      json.dumps(info, indent=4) + "\n"))
    mod.writing_tasks.append(lambda: ("logic.json",
                                      json_dumps(logic_events) + "\n"))

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
