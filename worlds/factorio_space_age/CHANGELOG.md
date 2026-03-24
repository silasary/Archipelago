# Factorio: Space Age apworld Changelog

## 2.0.0

### Gameplay changes

Default options are now a significantly accelerated experience relative to vanilla.

* Added `quick_start` option, enabled by default, that gives personal construction bots and a chunk of basic resources at the start.
* Added `skip_starting_trigger_techs` option, disabled by default, that starts with electronics, steam-power, etc. unlocked from the start without needing to do the crafting to trigger them.
* Added `starting_planet` option, disabled by default, that integrates with CodeGreen's Any Planet Start mod: https://mods.factorio.com/mod/any-planet-start . Interacts with `skip_starting_trigger_techs` and `free_samples` in fun ways.
* Added `space_technology_level` option to enable space flight with early or mid game technology, effectively downgrading all the ingredients for rocket silo, space platform, thruster, etc. to more primitive items. Puts the Space in Factorio: Space Age sooner rather than near the end of the game. (This could someday be obsoleted by recipe randomization.)
* Added `progressive_technologies: large_groups` option, enabled by default, which puts critical technologies, such as advanced circuit, early in large progressive chains with non-critical bonuses later in the chains. This makes it less likely to get stuck waiting for someone to find a specific item. Details here: https://github.com/thejoshwolfe/Archipelago/blob/space-age/worlds/factorio_space_age/data/ap_data.py
* `goal: any_other_planet_science` is now the default goal, and creates victory technologies to research instead of the mod reacting to researching anything that matches the condition. Includes low-effort art I drew of a trophy. Fixes #5.
* `goal: space_platform` replaced by `goal: space_science`, which requires researching a victory technology with 4 science packs including space science (red, green, blue, white).

Minor adjustments:

* Energy Link is now enabled by default and the recipe unlocked by a multiworld item.
* Furnaces, electric poles, and `military` through `military-4` recipe technologies are no longer progressive (with `progressive_technologies: only_related`). Getting the recipes out of order is interesting in a randomizer, and there are almost no crafting dependencies between them.

### Breaking changes to options

These changes may require updates to your player yaml configuration.

* `progressive_technologies` has been completely overhauled. The old `bonuses` option is gone. The old `recipes` option is very similar to `only_related`. The default has changed to the new `large_groups` option.
* TODO: consolidate filler weights and trap options.
* `goal: space_platform` removed. Try `goal: space_science` instead.
* The speedups `rocket_parts_per_rocket` and `ingredients_per_space_platform_foundation` are removed because they're now implied by `space_technology_level`.
* `automation` (the first assembling machine technology) is no longer part of any progressive chain because it is not randomized.
* With some `progressive_technologies` settings, several progressive pseudo item names have been simplified to remove the `progressive-` prefix. E.g. `progressive-steel-plate-productivity` is now just called `steel-plate-productivity`, and `worker-robot-speed-1` through `worker-robot-speed-7` are part of a progressive group called simply `worker-robot-speed`. The rough generalization is that recipe unlock chains still say `progressive-` but bonus unlock chains don't.
* With `progressive_technologies: large_groups`, if you want to give yourself levels of an infinite tech that's part of a progressive group, name the last item in the chain rather than the chain itself. e.g. `!getitem worker-robot-speed-7` or `start_inventory_from_pool: {mining-productivity-3: 5}`.

### Internal changes

* Internal logic overhaul to support configurable progressive groups, swappable recipes, and other hypothetical future flexibility. The data pipeline starts with Factorio's "prototype" data instead of "runtime" data, and we ship a pruned-down json file instead of generated python code. This change should make this apworld more friendly to contributions by being less confusing/clever/innovative/messy/etc. We do lose the git-controlled representation of the logic graph, which is a little disappointing, but necessary to make it more flexible.
* Fixed subtle bug with `on_entity_died` event handler clobbering found by @CosmicWolf. No observable change for the player.
* Fixed `/collect` on your own world printing `Unknown Item` warnings related to infinite technologies.
* Migrated the data exporter into this repo. Previously located here: https://github.com/thejoshwolfe/FactorioInformationExtractor

## 1.1.2

* fixed Archipelago EnergyLink Bridge would not work on space platform.

## 1.1.1

* removed debug print when building an energylink bridge (oops).
* updated docs

## 1.1.0

* Added logic option to require heating towers or recyclers for automating gleba science

## 1.0.2

* Fix corrupted factorio mod generation due to version number conflict.

## 1.0.1

* Add logic option to require steel power poles on vulcanus and fulgora.
* Fix Archipelago required version to address a settings related crash.
* Fix typos in yaml option description.

## 1.0.0

Hello everyone! I've emerged from a 6 week frenzy seeing if I could tackle getting the Space Age expansion into Archipelago. It ended up taking a very different approach from the core Factorio world by Berserker et al.

### Differences from core Factorio

There are numerous necessary changes due to Space Age being kinda a completely different game,
but some of the notable design choices here that deviate from the core Factorio world are:

* Random recipe generation is removed.
* Random technology dependency generation is removed.
* Craftsanity is removed.
* The vanilla tech tree requirements and shape are preserved. Trigger techs and dependencies are all vanilla, but the effect of each research objective is random.
* Different groupings of progressive item chains.
* Infinite technologies are shuffled locally and optionally used as filler items.

There are also a ton of options to check out (template attached with this release).

### Feedback

Please report bugs, feature requests, etc. here: https://github.com/thejoshwolfe/Archipelago/issues

(I am not very active on Discord.)

