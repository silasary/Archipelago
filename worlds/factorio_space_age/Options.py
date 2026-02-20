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

option_groups: list[OptionGroup] = []
def auto_group(cls):
    option_groups[-1].options.append(cls)
    return cls


class Goal(Choice):
    """
    Goal required to complete the game.
    space platform: Build a space platform.
    any other planet science: Research anything with metallurgic, agricultural, or electromagnetic science (TODO: unimplemented).
    aquilo orbit: Reach aquilo orbit with a space platform.
    solar system edge: (default) The victory condition in the normal game.
    """
    display_name = "Goal"
    option_space_platform = 0
    option_any_other_planet_science = 1
    option_aquilo_orbit = 2
    option_solar_system_edge = 3
    default = 3

class AllowImportedBlueprints(DefaultOnToggle):
    """Allow blueprints imported from outside the current game."""
    display_name = "Allow Imported Blueprints"


option_groups.append(OptionGroup("World Gen", []))

@auto_group
class WorldGen(Choice):
    """
    vanilla: The vanilla Default settings.
    buffed resources: All resource patches cranked to the max, cliffs disabled, oceans reduced, Fulgoran islands max size.
    custom: use the world_gen_custom property.
    """
    option_vanilla = 0
    option_buffed_resources = 1
    option_custom = 2
    default = 1

@auto_group
class WorldGenEnemies(DefaultOnToggle):
    """
    Enable enemies. Turning this off checks the 'No enemies' mode during world gen and disables pollution.
    Ignored when world_gen is set to 'custom'.
    """

@auto_group
class WorldGenAsteroids(Range):
    """
    Percentage modifier for spawning asteroids.
    Ignored when world_gen is set to 'custom'.
    TODO: unimplemented.
    """
    range_start = 10
    range_end = 400
    default = 100

@auto_group
class WorldGenSpoilage(Range):
    """
    Percentage modifier for spoiling rate. Higher rate is faster spoiling.
    Ignored when world_gen is set to 'custom'.
    TODO: unimplemented.
    """
    range_start = 10
    range_end = 1000
    default = 100

@auto_group
class WorldGenCustom(OptionDict):
    """
    Only used when world_gen is set to 'custom'.
    Overview of options at https://wiki.factorio.com/Map_generator,
    with in-depth documentation at https://lua-api.factorio.com/latest/concepts/MapGenSettings.html .

    Other resources that may help:
    * https://lua-api.factorio.com/latest/types/MapGenPreset.html
    * https://github.com/wube/factorio-data/blob/master/map-gen-settings.example.json
    * https://github.com/wube/factorio-data/blob/master/map-settings.example.json
    * https://fesc.pages.dev/ ( https://github.com/rfvgyhn/factorio-exchange-string-parser )

    Specify a combination of the 'basic' and 'advanced' settings in this object; they will be pulled apart appropriately.
    TODO: currently only preset settings can be used, not regular settings. If you don't know what that means, neither do I,
    but it means you can't fiddle with the spoil rate for example.

    If you wish you could just use a map exchange string, please contribute to this forum discussion:
    https://forums.factorio.com/viewtopic.php?p=689150
    """
    display_name = "Custom World Generation"
    # FIXME: do we want default be a rando-optimized default or in-game DS?
    value: dict[str, dict[str, typing.Any]]
    default = {}
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
            },
            Optional("difficulty_settings"): {
                Optional("technology_price_multiplier"): FloatRange(0.01, 1000),
            },
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
    def from_any(cls, data: dict[str, typing.Any]) -> WorldGenCustom:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")


option_groups.append(OptionGroup("Technologies", []))

@auto_group
class TechnologyPrerequisites(Choice):
    """
    Researching a technology location requires researching the prerequisite locations first,
    the connections in the technology graph.
    vanilla: Imitate the vanilla tech tree connections (TODO: unimplemented).
    removed: No prerequisites. All technology locations can be researched simply by meeting the individual requirements.
    """
    display_name = "Technology Prerequisites"
    option_vanilla = 0
    option_removed = 1
    default = 1

@auto_group
class ProgressiveTechs(Choice):
    """
    Whether to group technologies that end with -1, -2, -3, etc. into a sequence of progressive items so that they are always received in sequential order.

    off: All technologies will be separate items, which means you might received inserter-capacity-bonus-7 before inserter-capacity-bonus-2.
    bonuses: Technologies that grant global bonuses will be grouped together and received in sequence, for example there will be 7 copies of progressive-inserter-capacity-bonus instead of the individual -1, -2, etc. items.
    all: In addition, technologies that unlock recipes will also be grouped, for example 3 copies of progressive-automation, 4 copies of progressive-military, 3 copies of progressive-speed-module, etc.

    In addition to technology names that end with numbers, epic-quality and legendary-quality are bonuses called progressive-quality-upgrade,
    and turbo-transport-belt is the fourth recipe unlock in the progressive-logistics chain.
    """
    display_name = "Progressive Technologies"
    option_off = 0
    option_bonuses = 1
    option_all = 2
    default = 2

@auto_group
class InfiniteTechs(Choice):
    """
    How to handle infinitely researchable technologies, e.g. steel-plate-productivity.
    vanilla: They are not randomized, e.g. research productivity always requires promethium science packs (TODO: unimplemented).
    shuffled: The cost and prerequisites of each infinite tech is shuffled, e.g. research productivity mighty require only military, utility, and agricultural science packs (normally the health technology) (TODO: unimplemented).
    removed: Infinite technologies are removed.
    """
    display_name = "Infinite Technologies"
    option_vanilla = 0
    option_shuffled = 1
    option_removed = 2
    default = 2

@auto_group
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


option_groups.append(OptionGroup("Speedups/Balance", []))

@auto_group
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

@auto_group
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

@auto_group
class FreeSamplesQuality(Choice):
    """If free samples are on, determine the quality of the granted items."""
    display_name = "Free Samples Quality"
    option_normal = 0
    option_uncommon = 1
    option_rare = 2
    option_epic = 3
    option_legendary = 4
    default = 0

@auto_group
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

@auto_group
class TechCostDivisor(Range):
    """
    Reduce the cost of research technologies by dividing by this number.
    1 = Vanilla. 10 = All technologies require 1/10th as much science.
    """
    range_start = 1
    range_end = 10
    default = 1

@auto_group
class RocketPartsPerRocket(Range):
    """Normally a rocket requires 50 of each ingredient."""
    range_start = 1
    range_end = 200
    default = 50

@auto_group
class IngredientsPerSpacePlatformFoundation(Range):
    """Normally a space platform foundation requires 20 of each ingredient."""
    range_start = 1
    range_end = 400
    default = 20


option_groups.append(OptionGroup("Logic", []))

@auto_group
class LogicMiningDrill(DefaultOnToggle):
    """
    Logically require electric mining drills for logistic science pack automation (green science).
    Otherwise, you may need to use burner mining drills for automation until Vulcanus or uranium is required.
    """

@auto_group
class LogicLogistics(DefaultOnToggle):
    """
    Logically require logistics (underground belts and splitters) for logistic science pack automation (green science).
    """

@auto_group
class LogicElectricFurnace(DefaultOnToggle):
    """
    Logically require electric furnaces for space science pack automation and for traveling space.
    Otherwise, you may need to supply space platforms with metal plates shipped up via rocket.
    """

@auto_group
class LogicIceMelting(DefaultOnToggle):
    """
    Logically require ice melting for traveling space.
    Otherwise, you may need to supply space platforms with water barrels shipped up via rocket.
    """

@auto_group
class LogicGunTurret(DefaultOnToggle):
    """
    Logically require gun turrets for destroying medium asteroids.
    Otherwise, you may need to use walls and speed regulation to survive space travel.
    (Large and huge asteroids always logically require rocket turrets and railgun turrets respectively.)
    """

@auto_group
class LogicSpoilage(DefaultOnToggle):
    """
    Logically require Gleba for access to spoilage.
    Otherwise, you may need to wait >2 hours (configurable) for fish to spoil on Nauvis to get nutrient-triggered technology.
    """

@auto_group
class LogicLightningRod(DefaultOnToggle):
    """
    Logically require lightning rods for setting up mining drills on Fulgora.
    Otherwise, you may need to solve the lightning problem some other way.
    NOTE: This option does nothing, because the requirements for landing on Fulgora include all the requirements for crafting lightning rods.
    """

@auto_group
class LogicDarkPower(DefaultOnToggle):
    """
    Logically require nuclear power to reach Aquilo.
    Otherwise, you may need to rely on poorly performing solar panels in dark space.
    """

@auto_group
class LogicFastInserter(Toggle):
    """
    Logically require fast inserters to automate advanced circuits.
    """

@auto_group
class LogicAssemblingMachine2(Toggle):
    """
    Logically require assembling machine 2 to automate advanced circuits.
    """

@auto_group
class LogicFluidHandling(Toggle):
    """
    Logically require pumps and storage tanks for advanced oil processing.
    """

@auto_group
class LogicConstructionRobots(Toggle):
    """
    Logically require construction robots before automating production or utility science (purple/yellow) or traveling to another planet.
    """

@auto_group
class LogicLogisticRobots(Toggle):
    """
    Logically require requester chests and logistic robots before traveling to another planet.
    """


option_groups.append(OptionGroup("Energy Link", [], start_collapsed=True))

@auto_group
class EnergyLink(Toggle):
    """
    Allow sending and receiving energy to/from a shared pool in the multiworld.
    The Archipelago EnergyLink Bridge item is craftable in-game and functions like an accumulator for sending and receiving energy.
    25% of the energy is lost during sending.

    All EnergyLink-enabled games in the multiworld use the same pool.
    Unit conversions between Factorio (Joules), Mega Man (HP), Roller Coaster Tycoon (USD),
    Donkey Kong Country (Bananas), etc. is left to the apworld developers.

    EnergyLink can also be used to transport energy between planets in Factorio: Space Age or to/from space platforms.
    (TODO: Consider this in logic.)
    """
    display_name = "Energy Link"

@auto_group
class EnergyLinkRecipe(Choice):
    """
    The recipe to craft an Archipelago EnergyLink Bridge.
    early game: Made from iron plates and copper plates.
    mid game: Made from accumulator and radar (requires oil, acid, and battery).
    fulgora: Made from supercapacitor and radar.
    """
    option_early_game = 0
    option_mid_game = 1
    option_fulgora = 2
    default = 1

@auto_group
class EnergyLinkTechnology(Toggle):
    """
    Should the Archipelago EnergyLink Bridge recipe be unlocked by a technology, which is an item in the multiworld?
    Note that this interacts with the free samples option.
    (TODO: unimplemented)
    """

@auto_group
class LogicEnergyLink(Toggle):
    """
    Logically require Archipelago EnergyLink Bridges for the following, depending on the setting of energy_link_recipe:
    early_game: logistic science pack automation (green science).
    mid_game: chemical science pack automation (blue science).
    fulgora: electromagnetic science pack automation.
    """


option_groups.append(OptionGroup("Traps", [], start_collapsed=True))

class TrapCount(Range):
    range_end = 25

@auto_group
class AttackTrapCount(TrapCount):
    """Trap items that when received trigger an attack on your base."""
    display_name = "Attack Traps"

@auto_group
class TeleportTrapCount(TrapCount):
    """Trap items that when received trigger a random teleport.
    It is ensured the player can walk back to where they got teleported from."""
    display_name = "Teleport Traps"

@auto_group
class GrenadeTrapCount(TrapCount):
    """Trap items that when received trigger a grenade explosion on each player."""
    display_name = "Grenade Traps"

@auto_group
class ClusterGrenadeTrapCount(TrapCount):
    """Trap items that when received trigger a cluster grenade explosion on each player."""
    display_name = "Cluster Grenade Traps"

@auto_group
class ArtilleryTrapCount(TrapCount):
    """Trap items that when received trigger an artillery shell on each player."""
    display_name = "Artillery Traps"

@auto_group
class AtomicRocketTrapCount(TrapCount):
    """Trap items that when received trigger an atomic rocket explosion on each player.
    Warning: there is no warning. The launch is instantaneous."""
    display_name = "Atomic Rocket Traps"

@auto_group
class AtomicCliffRemoverTrapCount(TrapCount):
    """Trap items that when received trigger an atomic rocket explosion on a random cliff.
    Warning: there is no warning. The launch is instantaneous."""
    display_name = "Atomic Cliff Remover Traps"

@auto_group
class EvolutionTrapCount(TrapCount):
    """Trap items that when received increase the enemy evolution."""
    display_name = "Evolution Traps"
    range_end = 10

@auto_group
class EvolutionTrapIncrease(Range):
    """How much an Evolution Trap increases the enemy evolution.
    Increases scale down proportionally to the session's current evolution factor
    (40 increase at 0.50 will add 0.20... 40 increase at 0.75 will add 0.10...)"""
    display_name = "Evolution Trap % Effect"
    range_start = 1
    default = 10
    range_end = 100

@auto_group
class InventorySpillTrapCount(TrapCount):
    """Trap items that when received trigger dropping your main inventory and trash inventory onto the ground."""
    display_name = "Inventory Spill Traps"




@dataclass
class FactorioOptions(PerGameCommonOptions):
    goal: Goal
    allow_imported_blueprints: AllowImportedBlueprints
    world_gen: WorldGen
    world_gen_enemies: WorldGenEnemies
    world_gen_asteroid_spawn_rate: WorldGenAsteroids
    world_gen_spoil_rate: WorldGenSpoilage
    world_gen_custom: WorldGenCustom

    technology_prerequisites: TechnologyPrerequisites
    progressive_technologies: ProgressiveTechs
    infinite_technologies: InfiniteTechs
    tech_tree_information: TechTreeInformation

    starting_items: StartingItems
    free_samples: FreeSamples
    free_samples_quality: FreeSamplesQuality
    free_sample_excludes: FreeSampleExcludes
    tech_cost_divisor: TechCostDivisor
    rocket_parts_per_rocket: RocketPartsPerRocket
    ingredients_per_space_platform_foundation: IngredientsPerSpacePlatformFoundation

    require_electric_mining_drill: LogicMiningDrill
    require_logistics: LogicLogistics
    require_electric_furnace: LogicElectricFurnace
    require_ice_melting: LogicIceMelting
    require_gun_turret: LogicGunTurret
    require_lightning_rod: LogicLightningRod
    require_gleba_for_spoilage: LogicSpoilage
    require_dark_power: LogicDarkPower
    require_fast_inserter: LogicFastInserter
    require_assembling_machine_2: LogicAssemblingMachine2
    require_fluid_handling: LogicFluidHandling
    require_construction_robots: LogicConstructionRobots
    require_logistic_robots: LogicLogisticRobots

    energy_link: EnergyLink
    energy_link_recipe: EnergyLinkRecipe
    energy_link_technology: EnergyLinkTechnology
    require_energy_link: LogicEnergyLink

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
    start_inventory_from_pool: StartInventoryPool
