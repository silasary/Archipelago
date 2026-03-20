# Factorio: Space Age apworld Changelog

## 2.0.0

### Gameplay changes

* `goal: any_other_planet_science` now creates victory technologies to research instead of reacting to researching anything that matches the condition. Includes low-effort art I drew of a trophy. Fixes #5.
* split up some progressive item chains to be individual instead:
    * steel furnace and electric furnace are no longer progressive, because neither is an ingredient for the other, and getting them out of order is interesting for a randomizer.
    * electric energy distribution is no longer progressive for the same reason. Getting substations before medium electric poles sounds interesting.
    * `progressive-military` is removed. all 4 individual military technologies are separate. (`military-4` items are crafted out of `military-2` items, but I made the whole set not progressive for simplicity.) This makes it slightly harder to find all requirements for `military-science-pack`, since now `military-2` specifically is required instead of 2/4 `progressive-military`.

### Options changes

These may require updates to your player yaml configuration.

* `progressive_technologies` has changed: TODO.
* `automation` (the first assembling machine technology) is no longer part of `progressive-automation` because it is not randomized.
* Simplified several progressive pseudo item names to remove the `progressive-` prefix. E.g. `progressive-steel-plate-productivity` is now just called `steel-plate-productivity`, and `worker-robot-speed-1` through `worker-robot-speed-7` are part of a progressive group called simply `worker-robot-speed`. The rough generalization is that recipe unlock chains still say `progressive-` but bonus unlock chains don't.

### Internal changes

* Internal logic overhaul to better prepare for recipe randomization and other hypothetical future flexibility. The data pipeline starts with prototype data instead of runtime data, and we shipped a pruned-down json version instead of the generated python code in previous versions. This should make this code base more friendly to contributions by way of being less confusing/clever/innovative/messy/etc. We do lose the git-controlled representation of the logic graph, which is a little disappointing, but necessary to make it more flexible.
* Fixed subtle bug with `on_entity_died` event handler clobbering found by @CostmicWolf. No observable change to the player.
* Fixed `/collect` on your own world printing `Unknown Item` warnings related to infinite technologies.

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

