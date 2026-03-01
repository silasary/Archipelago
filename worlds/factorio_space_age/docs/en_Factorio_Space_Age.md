# Factorio: Space Age

Factorio is a game in which you build and maintain factories.

You will be mining resources, researching technologies, building infrastructure,
automating production, and fighting enemies. Use your imagination to design your factory,
combine simple elements into ingenious structures, apply management skills to keep it working,
and protect it from the creatures who don't really like you.

https://www.factorio.com/

## What does randomization do to this game?

The technologies are shuffled.
Researching things in Factorio sends items to the multiworld, and technologies are unlocked by receiving items from the multiworld.

Technologies include crafting recipes, weapon damage bonuses, recipe productivity bonuses, planet discovery, and more.

### What does another world's item look like in Factorio?

The research tech tree in Factorio is the set of "locations", typically represented by the Archipelago icon.
You can configure whether the technology menu tells you what the item is or whether you have to research it to find out.

### When the engineer receives an item, what happens?

When the player receives a technology, it is instantly learned and able to be crafted. A message will appear in the chat
log to notify the player, and if free samples are enabled the player may also receive some items directly to their
inventory.

## What options are available?

There are numerous options to customize the game to your taste.

* Configurable goal. Reach solar system edge (long), reach Aquilo orbit (still pretty long), research anything with an offworld technology (medium), or simply build a space platform (short).
* Tech cost multiplier/divisor. You can reduce the science packs required for researching technologies by up to 10x.
* Free samples. You can optionally receive the craftable items directly when you received a technology that unlocks crafting recipes. For example, receiving the `biolab` technology can give 5 legendary biolabs without needing to craft them. Quality and quantity of free samples is configurable, and is not considered by the logic.
* Infinite technologies are local. Configure whether to keep them all vanilla, shuffle them amongst each other, or remove them. Filler items can also be configured to increment infinite technologies of your choice.
* Tons of quality-of-life logical dependencies. By default, gun turrets are considered a logical requirement for traveling space, but you can disable that dependency if you'd like to maybe be required to travel space before unlocking gun turrets. Similarly, many other optional dependencies can be enabled/disabled, such as fast inserters, medium power poles, and electric mining drills. These are logical dependencies only, which means that someone in the multiworld will be able to send you the item before you're absolutely required to do without it, but you can still attempt to do without it "out of logic" if you're impatient.
* EnergyLink is provided by a craftable item optionally unlocked by a new technology. See below. EnergyLink can be configured to be considered by logic, which might make solar panels unnecessary.
* Add filler items if you want. In addition to the ~250 technology locations that always exist, you can create up to 100 additional research objectives that are copies of random existing ones. A corresponding number of filler items will be added to the multiworld pool, and you can configure whether these items are helpful (infinite technology increments), nothing, or traps.
* Traps are the same as in the core Factorio world: trigger an attack from the biters, detonate a cluster grenade on the player, spill your inventory, etc.
* Death Link is supported, and you can opt out mid-game (same as core Factorio world).
* World gen settings are still a bit of a WIP. Currently, you can either fully define a world gen preset in the yaml (you're on your own for the syntax), or use one of the conveniently provided presets: vanilla, or ultra buffed resources. There is also a convenient setting to turn off enemies if you'd like. If you want more world gen presets, let me know here: https://github.com/thejoshwolfe/Archipelago/issues

### What is EnergyLink?

EnergyLink is an energy storage supported by some games that is shared across all worlds in a multiworld.
In Factorio, if enabled in the player options, Archipelago EnergyLink Bridge buildings can be crafted and placed, which allow
depositing excess energy and supplementing energy deficits, much like Accumulators.

The recipe can be configured to be early-game (craftable from the start), mid-game (requiring oil processing), or requiring Fulgoran resources. EnergyLink is extremely powerful in Factorio: Space Age specifically, because it can transport power within across planets and space platforms.

Each placed EnergyLink Bridge provides limited throughput, and multiple can be built to increase throughput.
The shared storage has unlimited capacity, but some energy is lost during transit.
The amount of energy currently in the shared storage is displayed in the Archipelago client.
It can also be queried by typing `/energy-link` in-game.

## Unique Local Commands

The following commands are only available when using the FactorioClient to play Factorio with Archipelago.

- `/factorio <command text>` Sends the command argument to the Factorio server as a command.
- `/energy-link` Displays the amount of energy currently in shared storage for EnergyLink
