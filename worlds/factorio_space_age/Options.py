from __future__ import annotations

from dataclasses import dataclass
import typing

from schema import Schema, Optional, And, Or, SchemaError

from Options import Choice, OptionDict, OptionSet, DefaultOnToggle, Range, DeathLink, Toggle, \
    StartInventoryPool, PerGameCommonOptions, OptionGroup, NamedRange


# schema helpers
class FloatRange:
    def __init__(self, low, high):
        self._low = low
        self._high = high

    def validate(self, value) -> float:
        if not isinstance(value, (float, int)):
            raise SchemaError(f"should be instance of float or int, but was {value!r}")
        if not self._low <= value <= self._high:
            raise SchemaError(f"{value} is not between {self._low} and {self._high}")
        return float(value)


LuaBool = Or(bool, And(int, lambda n: n in (0, 1)))

class Goal(Choice):
    """Goal required to complete the game."""
    display_name = "Goal"
    option_solar_system_edge = 0
    # TODO: add more goal options
    default = 0

class AllowImportedBlueprints(DefaultOnToggle):
    """Allow blueprints imported from outside the current game."""
    display_name = "Allow Imported Blueprints"

class StartingItems(OptionDict):
    """Mapping of Factorio internal item-name to amount granted on start."""
    display_name = "Starting Items"
    default = {"burner-mining-drill": 4, "stone-furnace": 4,  "raw-fish": 50}
    schema = Schema(
        {
            str: And(int, lambda n: n > 0,
                     error="amount of starting items has to be a positive integer"),
        }
        # TODO: move the additional validation from generate_early() into the schema
    )

class FactorioWorldGen(OptionDict):
    """World Generation settings. Overview of options at https://wiki.factorio.com/Map_generator,
    with in-depth documentation at https://lua-api.factorio.com/latest/concepts/MapGenSettings.html"""
    display_name = "World Generation"
    # FIXME: do we want default be a rando-optimized default or in-game DS?
    value: dict[str, dict[str, typing.Any]]
    default = {
        "autoplace_controls": {
            # terrain
            "water": {"frequency": 1, "size": 1, "richness": 1},
            "nauvis_cliff": {"frequency": 1, "size": 1, "richness": 1},
            "starting_area_moisture": {"frequency": 1, "size": 1, "richness": 1},
            # resources
            "coal": {"frequency": 1, "size": 3, "richness": 6},
            "copper-ore": {"frequency": 1, "size": 3, "richness": 6},
            "crude-oil": {"frequency": 1, "size": 3, "richness": 6},
            "iron-ore": {"frequency": 1, "size": 3, "richness": 6},
            "stone": {"frequency": 1, "size": 3, "richness": 6},
            "uranium-ore": {"frequency": 1, "size": 3, "richness": 6},
            # misc
            "trees": {"frequency": 1, "size": 1, "richness": 1},
            "enemy-base": {"frequency": 1, "size": 1, "richness": 1},
        },
        "seed": None,
        "starting_area": 1,
        "peaceful_mode": False,
        "no_enemies_mode": False,
        "cliff_settings": {
            "name": "cliff",
            "cliff_elevation_0": 10,
            "cliff_elevation_interval": 40,
            "richness": 1
        },
        "property_expression_names": {
            "control-setting:moisture:bias": 0,
            "control-setting:moisture:frequency:multiplier": 1,
            "control-setting:aux:bias": 0,
            "control-setting:aux:frequency:multiplier": 1
        },
        "pollution": {
            "enabled": True,
            "diffusion_ratio": 0.02,
            "ageing": 1,
            "enemy_attack_pollution_consumption_modifier": 1,
            "min_pollution_to_damage_trees": 60,
            "pollution_restored_per_tree_damage": 10
        },
        "enemy_evolution": {
            "enabled": True,
            "time_factor": 40.0e-7,
            "destroy_factor": 200.0e-5,
            "pollution_factor": 9.0e-7
        },
        "enemy_expansion": {
            "enabled": True,
            "max_expansion_distance": 7,
            "settler_group_min_size": 5,
            "settler_group_max_size": 20,
            "min_expansion_cooldown": 14400,
            "max_expansion_cooldown": 216000
        }
    }
    schema = Schema({
        "basic": {
            Optional("autoplace_controls"): {
                str: {
                    "frequency": FloatRange(0, 6),
                    "size": FloatRange(0, 6),
                    "richness": FloatRange(0.166, 6)
                }
            },
            Optional("seed"): Or(None, And(int, lambda n: n >= 0)),
            Optional("width"): And(int, lambda n: n >= 0),
            Optional("height"): And(int, lambda n: n >= 0),
            Optional("starting_area"): FloatRange(0.166, 6),
            Optional("peaceful_mode"): LuaBool,
            Optional("no_enemies_mode"): LuaBool,
            Optional("cliff_settings"): {
                "name": str, "cliff_elevation_0": FloatRange(0, 99),
                "cliff_elevation_interval": FloatRange(0.066, 241),  # 40/frequency
                "richness": FloatRange(0, 6)
            },
            Optional("property_expression_names"): Schema({
                Optional("control-setting:moisture:bias"): FloatRange(-0.5, 0.5),
                Optional("control-setting:moisture:frequency:multiplier"): FloatRange(0.166, 6),
                Optional("control-setting:aux:bias"): FloatRange(-0.5, 0.5),
                Optional("control-setting:aux:frequency:multiplier"): FloatRange(0.166, 6),
                Optional(str): object  # allow overriding all properties
            }),
        },
        "advanced": {
            Optional("pollution"): {
                Optional("enabled"): LuaBool,
                Optional("diffusion_ratio"): FloatRange(0, 0.25),
                Optional("ageing"): FloatRange(0.1, 4),
                Optional("enemy_attack_pollution_consumption_modifier"): FloatRange(0.1, 4),
                Optional("min_pollution_to_damage_trees"): FloatRange(0, 9999),
                Optional("pollution_restored_per_tree_damage"): FloatRange(0, 9999)
            },
            Optional("enemy_evolution"): {
                Optional("enabled"): LuaBool,
                Optional("time_factor"): FloatRange(0, 1000e-7),
                Optional("destroy_factor"): FloatRange(0, 1000e-5),
                Optional("pollution_factor"): FloatRange(0, 1000e-7),
            },
            Optional("enemy_expansion"): {
                Optional("enabled"): LuaBool,
                Optional("max_expansion_distance"): FloatRange(2, 20),
                Optional("settler_group_min_size"): FloatRange(1, 20),
                Optional("settler_group_max_size"): FloatRange(1, 50),
                Optional("min_expansion_cooldown"): FloatRange(3600, 216000),
                Optional("max_expansion_cooldown"): FloatRange(18000, 648000)
            }
        }
    })

    def __init__(self, value: dict[str, typing.Any]):
        advanced = {"pollution", "enemy_evolution", "enemy_expansion"}
        self.value = {
            "basic": {k: v for k, v in value.items() if k not in advanced},
            "advanced": {k: v for k, v in value.items() if k in advanced}
        }

        # verify min_values <= max_values
        def optional_min_lte_max(container, min_key, max_key):
            min_val = container.get(min_key, None)
            max_val = container.get(max_key, None)
            if min_val is not None and max_val is not None and min_val > max_val:
                raise ValueError(f"{min_key} can't be bigger than {max_key}")

        enemy_expansion = self.value["advanced"].get("enemy_expansion", {})
        optional_min_lte_max(enemy_expansion, "settler_group_min_size", "settler_group_max_size")
        optional_min_lte_max(enemy_expansion, "min_expansion_cooldown", "max_expansion_cooldown")

    @classmethod
    def from_any(cls, data: dict[str, typing.Any]) -> FactorioWorldGen:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

class TechnologyPrerequisites(Choice):
    """
    Researching a technology location requires researching the prerequisite locations first,
    the connections in the technology graph.
    vanilla: Imitate the vanilla tech tree connections.
    removed: No prerequisites. All technology locations can be researched simply by meeting the individual requirements.
    """
    display_name = "Technology Prerequisites"
    option_vanilla = 0
    option_removed = 1
    default = 0

class ProgressiveTechs(Choice):
    """
    Whether to group technologies that end with -1, -2, -3, etc. into a sequence of progressive items so that they are always received in sequential order.

    off: All technologies will be separate items, which means you might received inserter-capacity-bonus-7 before inserter-capacity-bonus-2.
    upgrades: Technologies that grant global bonuses will be grouped together and received in sequence, for example there will be 7 copies of progressive-inserter-capacity-bonus instead of the individual -1, -2, etc. items.
    all: In addition, technologies that unlock recipes will also be grouped, for example 3 copies of progressive-automation, 4 copies of progressive-military, 3 copies of progressive-speed-module, etc.
    """
    display_name = "Progressive Technologies"
    option_off = 0
    option_upgrades = 1
    option_all = 2
    default = 2

class InfiniteTechs(Choice):
    """
    How to handle infinitely researchable technologies, e.g. steel-plate-productivity.
    vanilla: They are not randomized, e.g. research productivity always requires promethium science packs.
    shuffled: The cost and prerequisites of each infinite tech is shuffled, e.g. research productivity mighty require only military, utility, and agricultural science packs (normally the health technology).
    removed: Infinite technologies are removed.
    """
    display_name = "Infinite Technologies"
    option_vanilla = 0
    option_shuffled = 1
    option_removed = 2
    default = 1

class TechTreeInformation(Choice):
    """
    How much information should be displayed in the tech tree.
    None: No indication of what a research unlocks.
    Advancement: Indicates if a research unlocks an item that is considered logical advancement, but not who it is for.
    Full: Labels with exact names and recipients of unlocked items; all researches are prefilled into the !hint command.
    """
    display_name = "Technology Tree Information"
    option_none = 0
    option_advancement = 1
    option_full = 2
    # TODO: option to reveal recipient
    default = 2

class FreeSamples(Choice):
    """
    Get free items with your recipe unlocks.
    These are not considered by logic.
    """
    display_name = "Free Samples"
    option_none = 0
    option_single_craft = 1
    option_half_stack = 2
    option_stack = 3
    default = 3

class FreeSamplesQuality(Choice):
    """If free samples are on, determine the quality of the granted items."""
    display_name = "Free Samples Quality"
    option_normal = 0
    option_uncommon = 1
    option_rare = 2
    option_epic = 3
    option_legendary = 4
    default = 0

class FreeSampleExcludes(OptionSet):
    """Recipes that when unlocked should never grant Free Samples of their products.
    Fluids, barreling/unbarreling, and biter eggs are always excluded.
    """
    display_name = "Free Sample Blacklist"
    default = {
        "automation-science-pack",
        "logistic-science-pack",
        "military-science-pack",
        "chemical-science-pack",
        "production-science-pack",
        "utility-science-pack",
        "space-science-pack",
        "metallurgic-science-pack",
        "agricultural-science-pack",
        "electromagnetic-science-pack",
        "cryogenic-science-pack",
        "promethium-science-pack",
    }
    # TODO: move the validation from generate_early() into a schema here.



class TrapCount(Range):
    range_end = 25


class AttackTrapCount(TrapCount):
    """Trap items that when received trigger an attack on your base."""
    display_name = "Attack Traps"


class TeleportTrapCount(TrapCount):
    """Trap items that when received trigger a random teleport.
    It is ensured the player can walk back to where they got teleported from."""
    display_name = "Teleport Traps"


class GrenadeTrapCount(TrapCount):
    """Trap items that when received trigger a grenade explosion on each player."""
    display_name = "Grenade Traps"


class ClusterGrenadeTrapCount(TrapCount):
    """Trap items that when received trigger a cluster grenade explosion on each player."""
    display_name = "Cluster Grenade Traps"


class ArtilleryTrapCount(TrapCount):
    """Trap items that when received trigger an artillery shell on each player."""
    display_name = "Artillery Traps"


class AtomicRocketTrapCount(TrapCount):
    """Trap items that when received trigger an atomic rocket explosion on each player.
    Warning: there is no warning. The launch is instantaneous."""
    display_name = "Atomic Rocket Traps"


class AtomicCliffRemoverTrapCount(TrapCount):
    """Trap items that when received trigger an atomic rocket explosion on a random cliff.
    Warning: there is no warning. The launch is instantaneous."""
    display_name = "Atomic Cliff Remover Traps"


class EvolutionTrapCount(TrapCount):
    """Trap items that when received increase the enemy evolution."""
    display_name = "Evolution Traps"
    range_end = 10


class EvolutionTrapIncrease(Range):
    """How much an Evolution Trap increases the enemy evolution.
    Increases scale down proportionally to the session's current evolution factor
    (40 increase at 0.50 will add 0.20... 40 increase at 0.75 will add 0.10...)"""
    display_name = "Evolution Trap % Effect"
    range_start = 1
    default = 10
    range_end = 100


class InventorySpillTrapCount(TrapCount):
    """Trap items that when received trigger dropping your main inventory and trash inventory onto the ground."""
    display_name = "Inventory Spill Traps"




class EnergyLink(Toggle):
    """Allow sending energy to other worlds. 25% of the energy is lost in the transfer."""
    display_name = "Energy Link"


@dataclass
class FactorioOptions(PerGameCommonOptions):
    goal: Goal
    allow_imported_blueprints: AllowImportedBlueprints
    starting_items: StartingItems
    world_gen: FactorioWorldGen

    technology_prerequisites: TechnologyPrerequisites
    progressive_technologies: ProgressiveTechs
    infinite_technologies: InfiniteTechs
    tech_tree_information: TechTreeInformation
    free_samples: FreeSamples
    free_samples_quality: FreeSamplesQuality
    free_sample_excludes: FreeSampleExcludes

    teleport_traps: TeleportTrapCount
    grenade_traps: GrenadeTrapCount
    cluster_grenade_traps: ClusterGrenadeTrapCount
    artillery_traps: ArtilleryTrapCount
    atomic_rocket_traps: AtomicRocketTrapCount
    atomic_cliff_remover_traps: AtomicCliffRemoverTrapCount
    inventory_spill_traps: InventorySpillTrapCount
    attack_traps: AttackTrapCount
    evolution_traps: EvolutionTrapCount
    evolution_trap_increase: EvolutionTrapIncrease

    death_link: DeathLink
    energy_link: EnergyLink
    start_inventory_from_pool: StartInventoryPool

option_groups: list[OptionGroup] = [
    OptionGroup(
        "Technologies",
        [
            TechnologyPrerequisites,
            ProgressiveTechs,
            InfiniteTechs,
            TechTreeInformation,
            FreeSamples,
            FreeSamplesQuality,
            FreeSampleExcludes,
        ]
    ),
    OptionGroup(
        "Traps",
        [
            AttackTrapCount,
            EvolutionTrapCount,
            EvolutionTrapIncrease,
            TeleportTrapCount,
            GrenadeTrapCount,
            ClusterGrenadeTrapCount,
            ArtilleryTrapCount,
            AtomicRocketTrapCount,
            AtomicCliffRemoverTrapCount,
            InventorySpillTrapCount,
        ],
        start_collapsed=True
    ),
]
