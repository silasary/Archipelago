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
    space science: Research victory with 4 science packs: automation, logistic, chemical, space (red, green, blue, white).
    any other planet science: (default) Research victory with 5 science packs: automation, logistic, chemical, space, and one of metallurgic, agricultural, or electromagnetic.
    aquilo orbit: Reach Aquilo orbit with a space platform.
    solar system edge: The victory condition in the normal game.
    TODO: merge shuffle_final_technology into this option.
    """
    display_name = "Goal"
    option_space_science = 0
    option_any_other_planet_science = 1
    option_aquilo_orbit = 2
    option_solar_system_edge = 3
    default = 1

class StartingPlanet(Choice):
    """
    Start on one of the other 3 inner planets.
    To randomly select a planet, use advanced option randomization to specify weights.
    Requires _CodeGreen's Any Planet Start mod: https://mods.factorio.com/mod/any-planet-start

    WARNING: starting on Gleba with enemies enabled is extremely difficult. See also pentapod_killers and gleba_coal.
    """
    option_nauvis = 0
    option_vulcanus = 1
    option_gleba = 2
    option_fulgora = 3
    default = 0

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
class ShuffleFinalTechnology(Toggle):
    """
    Should the "last" technology (see below) be shuffled as a multiworld item?
    Otherwise, it will be unlocked at its vanilla research location and require all the usual science packs.
    Setting this option to 'true' can reduce the number of science packs needed to complete the goal.

    The "last" technology depends on the goal:
    space platform: rocket-silo, which requires 3 science packs.
    any other planet science: this option has no effect.
    aquilo orbit: planet-discovery-aquilo, which requires 9 science packs.
    solar system edge: promethium-science-pack (unlocks solar-system-edge), which requires 10 science packs.
    """

@auto_group
class TechnologyPrerequisites(Choice):
    """
    Researching a technology location requires researching the prerequisite locations first,
    the connections in the technology graph.
    vanilla: Imitate the vanilla tech tree connections.
    removed: No prerequisites. All technology locations can be researched simply by meeting the individual requirements.

    Note that with prerequisites removed, the technology GUI lists all the trigger techs for planets you haven't visited yet
    before the research techs that you're actually looking for, which can be a little annoying.
    However, with prerequisites included, triggers can block large swaths of other techs, such as pumping oil and mining uranium.
    """
    display_name = "Technology Prerequisites"
    option_vanilla = 0
    option_removed = 1
    default = 0

@auto_group
class ProgressiveTechs(Choice):
    """
    Group technologies together as progressive item chains.
    For example, there are 3 copies of 'progressive-speed-module' in the multiworld item pool,
    the first one you receive gives the recipe for speed module 1, the second gives speed module 2, and so on.
    See https://github.com/thejoshwolfe/Archipelago/blob/space-age/worlds/factorio_space_age/data/ap_data.py for the full definitions of these.

    only_related: Technologies with similar names will be grouped together in a progress chain.
    This requires several specific items to progress, such as oil-gathering, oil-processing, plastics, and advanced-circuit all as individual items.
    large_groups: Loosely-related technologies will be grouped together with more critical recipes near the start and less critical bonuses near the end.
    This allows many more ways to get critical technologies, for example 2/9+ progressive-oil and 2/9+ progressive-circuit to get the same set of recipes listed in the previous example.
    Additional copies of progressive-circuit can be added to the pool with filler_processing_unit_productivity_weight, and similarly with other infinite technologies as filler items.
    """
    display_name = "Progressive Technologies"
    option_only_related = 0
    option_large_groups = 1
    default = 1

@auto_group
class InfiniteTechs(Choice):
    """
    How to handle infinitely researchable technologies, e.g. steel-plate-productivity.
    vanilla: They are not randomized, e.g. research productivity always requires promethium science packs.
    shuffled: The cost and prerequisites of the infinite techs are shuffled, e.g. research productivity might require only military, utility, and agricultural science packs (the location of the health technology).
    removed: Infinite technologies are removed.
    """
    display_name = "Infinite Technologies"
    option_vanilla = 0
    option_shuffled = 1
    option_removed = 2
    default = 1

@auto_group
class TechTreeInformation(Choice):
    """
    How much information should be displayed in the tech tree.
    None: No indication of what a research unlocks.
    Advancement: Indicates if it's a logical advancement for the recipient.
    Recipient: Reveals who the recipient is.
    Recipient Advancement: Says both who it's for and whether it's an advancement.
    Full: Reveals exact names and recipients of unlocked items; all researches are prefilled into the !hint command.
    """
    display_name = "Technology Tree Information"
    option_none = 0
    option_advancement = 1
    option_recipient = 2
    option_recipient_advancement = 3
    option_full = 4
    default = 3


option_groups.append(OptionGroup("Speedups/Balance", []))

@auto_group
class QuickStart(DefaultOnToggle):
    """
    Start with power armor, some personal bots, some bot speed upgrades,
    and a chunk of materials to help get through the early game.
    """

class SkipStartingTriggerTechs(Toggle):
    """
    Instead of needing to craft iron plates, copper plates, and a lab at the start of the run,
    start with the recipes for steam power, labs, and logistic science pack already unlocked.
    The set of technologies changes with the starting_planet setting, and it's recommended particularly on Vulcanus and Gleba.
    The free_samples setting gives items from the early triggers, so on Vulcanus, you can start with foundries straight away without setting up a lubricant build,
    and on Gleba, you can start with biochambers without looting egg rafts.
    """

@auto_group
class StartingItems(OptionDict):
    """Mapping of Factorio internal item-name to amount granted on start."""
    display_name = "Starting Items"
    default = {}
    # Validation is in generate_early().

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
    default = [
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
    ]
    # This is validated in generate_early().

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
class SpaceTechnologyLevel(Choice):
    """
    Downgrade space-related crafting ingredients to make space travel accessible earlier in the game:
    vanilla               -> mid game         -> early game;
    processing unit       -> advanced circuit -> electronic circuit;
    low density structure -> plastic bar      -> copper plate;
    rocket fuel           -> sulfur           -> coal;
    electric engine unit  -> engine unit      -> iron gear wheel;
    steel plate           -> steel plate      -> iron plate;
    concrete              -> concrete         -> stone brick;

    Changes apply to these recipes: rocket-silo, rocket-part, space-platform-foundation,
    space-platform-starter-pack, cargo-landing-pad, cargo-bay, asteroid-collector, crusher,
    thruster, chemical-plant, solar-panel.

    If require_electric_furnace is enabled, then electric-furnace will also be included in the list.
    The early_game setting unlocks chemical plants as part of space-platform-thruster so you can melt ice and make fuel.

    This setting also reduces small and medium asteroid health,
    and reduces item counts for rocket-silo, space-platform-foundation, and rocket parts per rocket.

    To get the most out of this option, you might be interested in these other changes:
      technology_prerequisites: removed
      progressive_technologies: only_related # TODO: make a better option for this mode.
      energy_link_recipe: early_game
    And if you really want to go straight into space at the start of the multiworld:
      start_inventory_from_pool:
        rocket-silo: 1
        space-platform: 1
        advanced-material-processing-2: 1  # if you want furnaces in space
        space-platform-thruster: 1
        gun-turret: 1
        # One of these:
        solar-energy: 1
        ap-energy-link-bridge: 1

    When starting_planet is not set to nauvis, then this option's behavior changes accordingly.
    """
    option_early_game = 0
    option_mid_game = 1
    option_vanilla = 2
    default = 2

@auto_group
class VulcanusRocks(Range):
    """
    When starting on Vulcanus, multiply all drops from hand-mining rocks.
    This is your only source of iron, copper, and stone until you make foundries (which are not randomized).
    Hand-mined rocks are your only source of tungsten ore to make more foundries until big mining drills,
    and until you can kill demolishers, if enabled.
    Hand-mining rocks never satisfies the logical requirements for automating metallurgic science.
    """
    range_start = 1
    default = 5
    range_end = 10

@auto_group
class GlebaCoal(Choice):
    """
    When starting on Gleba, how should coal be acquired or obviated?
    Coal is normally required for military science and may be used for defense against Gleba enemies.

    vanilla: 20 spoilage -> 1 coal through burnt spoilage and carbon synthesis.
    buffed: 1 spoilage -> 1 coal through burnt spoilage and carbon synthesis.
    alternate_explosives: add alternate recipes for explosives and grenades to avoid the need for coal on Gleba.
    """
    option_vanilla = 0
    option_buffed = 1
    option_alternate_explosives = 2
    default = 2



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
    Logically require underground belts and splitters for logistic science pack automation (green science).
    """

@auto_group
class LogicElectricFurnace(DefaultOnToggle):
    """
    Logically require electric furnaces for space science pack automation and for traveling space.
    Otherwise, you may need to supply space platforms with metal plates shipped up via rocket.
    Has no effect when starting on Vulcanus.
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
class LogicElectricPole(DefaultOnToggle):
    """
    Logically require medium electric poles for automating metallurgic and electromagnetic science packs.
    Otherwise, you may need to ship in wood to make electric poles.
    """

@auto_group
class LogicSpoilage(DefaultOnToggle):
    """
    Logically require Gleba for access to spoilage.
    Otherwise, you may need to wait >2 hours (configurable) for fish to spoil on Nauvis to get nutrient-triggered technology.
    """

@auto_group
class LogicSeedDisposal(DefaultOnToggle):
    """
    Logically require either heating towers or recyclers to automate agricultural science pack.
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

@auto_group
class LogicAsteroidProcessing(Toggle):
    """
    Logically require asteroid reprocessing and advanced asteroid processing to reach Aquilo.
    """

@auto_group
class LogicHeatingTower(Toggle):
    """
    Logically require heating towers to heat buildings on Aquilo.
    Otherwise, you may need to ship in nuclear fuel cells.
    """

@auto_group
class LogicDemolisherKillers(OptionDict):
    """
    What should the logic consider viable methods for killing small demolishers?
    When enemies are enabled (according to `world_gen_enemies` or `world_gen_custom.no_enemies_mode`),
    killing small demolishers is logically required for automating tungsten ore.
    WARNING: military bonuses for damage, weapon speed, etc. are not considered by the logic.
    """
    default = {
        "poison capsule": True,
        "land mine": False,
        "gun turret and firearm magazine": False,
        "gun turret and piercing rounds magazine": False,
        "gun turret and uranium rounds magazine": True,
        "rocket turret and rocket": False,
        "rocket turret and explosive rocket": False,
        "tesla turret": True,
        "atomic bomb": True,
        "railgun": True,
    }
    schema = Schema({k: bool for k in default.keys()})

@auto_group
class LogicPentapodKillers(OptionDict):
    """
    What should the logic consider viable methods for killing Gleba enemies and defending your base against their attacks?
    When enemies are enabled (according to `world_gen_enemies` or `world_gen_custom.no_enemies_mode`),
    killing Gleba enemies is logically required for automating agricultural science,
    and if starting on Gelba, also required for automating chemical science.
    WARNING: military bonuses for damage, weapon speed, etc. are not considered by the logic.
    """
    default = {
        "land mine": True,
        "gun turret and firearm magazine": False,
        "gun turret and piercing rounds magazine": False,
        "gun turret and uranium rounds magazine": True,
        "rocket turret": True,
        "tesla turret": True,
        "railgun": True,
    }
    schema = Schema({k: bool for k in default.keys()})


option_groups.append(OptionGroup("Energy Link", [], start_collapsed=True))

@auto_group
class EnergyLink(DefaultOnToggle):
    """
    Allow sending and receiving energy to/from a shared pool in the multiworld.
    The Archipelago EnergyLink Bridge item is craftable in-game and functions like an accumulator for sending and receiving energy.
    25% of the energy is lost during sending.

    All EnergyLink-enabled games in the multiworld use the same pool.
    Unit conversions between Factorio (Joules), Mega Man (HP), Roller Coaster Tycoon (USD),
    Donkey Kong Country (Bananas), etc. is left to the apworld developers.

    EnergyLink can also be used to transport energy between planets in Factorio: Space Age or to/from space platforms.
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
class EnergyLinkTechnology(DefaultOnToggle):
    """
    Should the Archipelago EnergyLink Bridge recipe be unlocked by a technology, which is an item in the multiworld?
    Note that this interacts with the free samples option.
    """

@auto_group
class LogicEnergyLink(Toggle):
    """
    Logically require Archipelago EnergyLink Bridges for the following, depending on the setting of energy_link_recipe:
    early_game: logistic science pack automation (green science).
    mid_game: chemical science pack automation (blue science).
    fulgora: electromagnetic science pack automation.
    """

@auto_group
class LogicEnergyLinkInSpace(Toggle):
    """
    Allow Archipelago EnergyLink Bridges to satisfy the logical requirement for generating power in space, including in dark space.
    This may make solar panels unnecessary.
    """


option_groups.append(OptionGroup("Traps/Filler", [], start_collapsed=True))

@auto_group
class FillerCount(Range):
    """
    How many filler items should there be?
    The actual number of filler items may be higher than the number specified for various reasons.

    The settings below can be used to specify the weighted chance that filler items are helpful, harmful, or nothing.

    New locations, if needed, are generated by creating copies of random existing (finite, non-trigger) research objectives.
    """
    range_end = 200
    default = 4

class FillerWeight(Range):
    range_end = 1000
    default = 0

@auto_group
class FillerNothingWeight(FillerWeight):
    """
    Weighted chance that a filler item does literally nothing.
    The name of a nothing item is chosen randomly from: laser, flammables, modules, biter-egg-handling.
    """

@auto_group
class FillerArtilleryShellDamageWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-artillery-shell-damage"""
@auto_group
class FillerArtilleryShellRangeWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-artillery-shell-range"""
@auto_group
class FillerArtilleryShellSpeedWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-artillery-shell-speed"""
@auto_group
class FillerAsteroidProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-asteroid-productivity"""
@auto_group
class FillerElectricWeaponsDamageWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-electric-weapons-damage"""
@auto_group
class FillerFollowerRobotCountWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-follower-robot-count"""
@auto_group
class FillerHealthWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-health"""
@auto_group
class FillerLaserWeaponsDamageWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-laser-weapons-damage"""
@auto_group
class FillerLowDensityStructureProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-low-density-structure-productivity"""
@auto_group
class FillerMiningProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-mining-productivity"""
@auto_group
class FillerPhysicalProjectileDamageWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-physical-projectile-damage"""
@auto_group
class FillerPlasticBarProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-plastic-bar-productivity"""
@auto_group
class FillerProcessingUnitProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-processing-unit-productivity"""
@auto_group
class FillerRailgunDamageWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-railgun-damage"""
@auto_group
class FillerRailgunShootingSpeedWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-railgun-shooting-speed"""
@auto_group
class FillerRefinedFlammablesWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-refined-flammables"""
@auto_group
class FillerResearchProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-research-productivity"""
@auto_group
class FillerRocketFuelProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-rocket-fuel-productivity"""
@auto_group
class FillerRocketPartProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-rocket-part-productivity"""
@auto_group
class FillerScrapRecyclingProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-scrap-recycling-productivity"""
@auto_group
class FillerSteelPlateProductivityWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-steel-plate-productivity"""
@auto_group
class FillerStrongerExplosivesWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-stronger-explosives"""
@auto_group
class FillerWorkerRobotsSpeedWeight(FillerWeight):
    """Weighted chance that a filler item is progressive-worker-robots-speed"""

@auto_group
class AttackTrapWeight(FillerWeight):
    """Weighted chance that a filler item is a trap that when received triggers an attack on your base."""

@auto_group
class TeleportTrapWeight(FillerWeight):
    """
    Weighted chance that a filler item is a trap that when received triggers a random teleport.
    It is ensured the player can walk back to where they got teleported from.
    """

@auto_group
class GrenadeTrapWeight(FillerWeight):
    """Weighted chance that a filler item is a trap that when received triggers a grenade explosion on each player."""

@auto_group
class ClusterGrenadeTrapWeight(FillerWeight):
    """Weighted chance that a filler item is a trap that when received triggers a cluster grenade explosion on each player."""

@auto_group
class ArtilleryTrapWeight(FillerWeight):
    """Weighted chance that a filler item is a trap that when received triggers an artillery shell on each player."""

@auto_group
class AtomicRocketTrapWeight(FillerWeight):
    """Weighted chance that a filler item is a trap that when received triggers an atomic rocket explosion on each player.
    Warning: there is no warning. The launch is instantaneous."""

@auto_group
class AtomicCliffRemoverTrapWeight(FillerWeight):
    """
    Weighted chance that a filler item is a trap that when received triggers an atomic rocket explosion on a random cliff.
    Warning: there is no warning. The launch is instantaneous.
    """

@auto_group
class EvolutionTrapWeight(FillerWeight):
    """Weighted chance that a filler item is a trap that when received increase the enemy evolution."""

@auto_group
class EvolutionTrapIncrease(Range):
    """
    How much an Evolution Trap increases the enemy evolution.
    Increases scale down proportionally to the session's current evolution factor
    (40 increase at 0.50 will add 0.20... 40 increase at 0.75 will add 0.10...)
    """
    display_name = "Evolution Trap % Effect"
    range_start = 1
    default = 10
    range_end = 100

@auto_group
class InventorySpillTrapWeight(FillerWeight):
    """Weighted chance that a filler item is a trap that when received triggers dropping your main inventory and trash inventory onto the ground."""



@dataclass
class FactorioOptions(PerGameCommonOptions):
    goal: Goal
    starting_planet: StartingPlanet
    allow_imported_blueprints: AllowImportedBlueprints

    world_gen: WorldGen
    world_gen_enemies: WorldGenEnemies
    world_gen_asteroid_spawn_rate: WorldGenAsteroids
    world_gen_spoil_rate: WorldGenSpoilage
    world_gen_custom: WorldGenCustom

    shuffle_final_technology: ShuffleFinalTechnology
    technology_prerequisites: TechnologyPrerequisites
    progressive_technologies: ProgressiveTechs
    infinite_technologies: InfiniteTechs
    tech_tree_information: TechTreeInformation

    quick_start: QuickStart
    skip_starting_trigger_techs: SkipStartingTriggerTechs
    starting_items: StartingItems
    free_samples: FreeSamples
    free_samples_quality: FreeSamplesQuality
    free_sample_excludes: FreeSampleExcludes
    tech_cost_divisor: TechCostDivisor
    space_technology_level: SpaceTechnologyLevel
    vulcanus_rocks: VulcanusRocks
    gleba_coal: GlebaCoal

    require_electric_mining_drill: LogicMiningDrill
    require_logistics: LogicLogistics
    require_electric_furnace: LogicElectricFurnace
    require_ice_melting: LogicIceMelting
    require_gun_turret: LogicGunTurret
    require_lightning_rod: LogicLightningRod
    require_medium_electric_pole: LogicElectricPole
    require_gleba_for_spoilage: LogicSpoilage
    require_seed_disposal: LogicSeedDisposal
    require_dark_power: LogicDarkPower
    require_fast_inserter: LogicFastInserter
    require_assembling_machine_2: LogicAssemblingMachine2
    require_fluid_handling: LogicFluidHandling
    require_construction_robots: LogicConstructionRobots
    require_logistic_robots: LogicLogisticRobots
    require_asteroid_processing: LogicAsteroidProcessing
    require_heating_tower: LogicHeatingTower
    demolisher_killers: LogicDemolisherKillers
    pentapod_killers: LogicPentapodKillers

    energy_link: EnergyLink
    energy_link_recipe: EnergyLinkRecipe
    energy_link_technology: EnergyLinkTechnology
    require_energy_link: LogicEnergyLink
    energy_link_satisfies_requirements: LogicEnergyLinkInSpace

    filler_count: FillerCount
    filler_nothing_weight: FillerNothingWeight
    filler_artillery_shell_damage_weight: FillerArtilleryShellDamageWeight
    filler_artillery_shell_range_weight: FillerArtilleryShellRangeWeight
    filler_artillery_shell_speed_weight: FillerArtilleryShellSpeedWeight
    filler_asteroid_productivity_weight: FillerAsteroidProductivityWeight
    filler_electric_weapons_damage_weight: FillerElectricWeaponsDamageWeight
    filler_follower_robot_count_weight: FillerFollowerRobotCountWeight
    filler_health_weight: FillerHealthWeight
    filler_laser_weapons_damage_weight: FillerLaserWeaponsDamageWeight
    filler_low_density_structure_productivity_weight: FillerLowDensityStructureProductivityWeight
    filler_mining_productivity_weight: FillerMiningProductivityWeight
    filler_physical_projectile_damage_weight: FillerPhysicalProjectileDamageWeight
    filler_plastic_bar_productivity_weight: FillerPlasticBarProductivityWeight
    filler_processing_unit_productivity_weight: FillerProcessingUnitProductivityWeight
    filler_railgun_damage_weight: FillerRailgunDamageWeight
    filler_railgun_shooting_speed_weight: FillerRailgunShootingSpeedWeight
    filler_refined_flammables_weight: FillerRefinedFlammablesWeight
    filler_research_productivity_weight: FillerResearchProductivityWeight
    filler_rocket_fuel_productivity_weight: FillerRocketFuelProductivityWeight
    filler_rocket_part_productivity_weight: FillerRocketPartProductivityWeight
    filler_scrap_recycling_productivity_weight: FillerScrapRecyclingProductivityWeight
    filler_steel_plate_productivity_weight: FillerSteelPlateProductivityWeight
    filler_stronger_explosives_weight: FillerStrongerExplosivesWeight
    filler_worker_robots_speed_weight: FillerWorkerRobotsSpeedWeight
    teleport_trap_weight: TeleportTrapWeight
    grenade_trap_weight: GrenadeTrapWeight
    cluster_grenade_trap_weight: ClusterGrenadeTrapWeight
    artillery_trap_weight: ArtilleryTrapWeight
    atomic_rocket_trap_weight: AtomicRocketTrapWeight
    atomic_cliff_remover_trap_weight: AtomicCliffRemoverTrapWeight
    inventory_spill_trap_weight: InventorySpillTrapWeight
    attack_trap_weight: AttackTrapWeight
    evolution_trap_weight: EvolutionTrapWeight
    evolution_trap_increase: EvolutionTrapIncrease

    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
