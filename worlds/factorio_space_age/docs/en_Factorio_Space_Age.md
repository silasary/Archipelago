# Factorio: Space Age

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

The technologies are shuffled.
Researching things in Factorio sends items to the multiworld,
and crafting recipes are unlocked by receiving items from the multiworld.

### What does another world's item look like in Factorio?

The research tech tree in Factorio contains the "locations", typically represented by the Archipelago icon.
You can configure whether the technology tree tells you what the item is or whether you have to research it to find out.

### When the engineer receives an item, what happens?

When the player receives a technology, it is instantly learned and able to be crafted. A message will appear in the chat
log to notify the player, and if free samples are enabled the player may also receive some items directly to their
inventory.

## What is EnergyLink?

EnergyLink is an energy storage supported by certain games that is shared across all worlds in a multiworld.
In Factorio, if enabled in the player options, EnergyLink Bridge buildings can be crafted and placed, which allow
depositing excess energy and supplementing energy deficits, much like Accumulators.

Each placed EnergyLink Bridge provides 10 MW of throughput. The shared storage has unlimited capacity, but 25% of energy
is lost during depositing. The amount of energy currently in the shared storage is displayed in the Archipelago client.
It can also be queried by typing `/energy-link` in-game.

## Unique Local Commands
The following commands are only available when using the FactorioClient to play Factorio with Archipelago.

- `/factorio <command text>` Sends the command argument to the Factorio server as a command.
- `/energy-link` Displays the amount of energy currently in shared storage for EnergyLink
