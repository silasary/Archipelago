# This file is somewhat arbitrary constants chosen for the randomizer.
# This file is inputs to both import-ap-dump.py and also the apworld proper.

factorio_base_id = 2 ** 17

unrandomized_technologies = {
    # These are critical at the start.
    # The fill algorithm crumbles if you let it attempt to random a way out of the early game.
    "steam-power",
    "electronics",
    "automation-science-pack",
    "automation",
}

never_give_free_samples_from_recipes = {
    # Originally derrived from the .hide_from_player_crafting recipe prototype property.
    "rocket-part",
    "biter-egg",
    "empty-crude-oil-barrel",
    "empty-fluoroketone-cold-barrel",
    "empty-fluoroketone-hot-barrel",
    "empty-heavy-oil-barrel",
    "empty-light-oil-barrel",
    "empty-lubricant-barrel",
    "empty-petroleum-gas-barrel",
    "empty-sulfuric-acid-barrel",
    "empty-water-barrel",
    "crude-oil-barrel",
    "fluoroketone-cold-barrel",
    "fluoroketone-hot-barrel",
    "heavy-oil-barrel",
    "light-oil-barrel",
    "lubricant-barrel",
    "petroleum-gas-barrel",
    "sulfuric-acid-barrel",
    "water-barrel",
}

infinite_technology_names = {
    "artillery-shell-damage-1",
    "artillery-shell-range-1",
    "artillery-shell-speed-1",
    "asteroid-productivity",
    "electric-weapons-damage-4",
    "follower-robot-count-5",
    "health",
    "laser-weapons-damage-7",
    "low-density-structure-productivity",
    "mining-productivity-3",
    "physical-projectile-damage-7",
    "plastic-bar-productivity",
    "processing-unit-productivity",
    "railgun-damage-1",
    "railgun-shooting-speed-1",
    "refined-flammables-7",
    "research-productivity",
    "rocket-fuel-productivity",
    "rocket-part-productivity",
    "scrap-recycling-productivity",
    "steel-plate-productivity",
    "stronger-explosives-7",
    "worker-robots-speed-7",
}

ap_item_names = [
    "ap-energy-link-bridge", # TODO: rename everything to use this name.
    "vulcanus-victory",
    "gleba-victory",
    "fulgora-victory",
]

trap_names = [
    "Artillery Trap",
    "Atomic Cliff Remover Trap",
    "Atomic Rocket Trap",
    "Attack Trap",
    "Cluster Grenade Trap",
    "Evolution Trap",
    "Grenade Trap",
    "Inventory Spill Trap",
    "Teleport Trap",
]

progressive_technology_stacks = {
    #"progressive-advanced-material-processing": [
    #    "advanced-material-processing",
    #    "advanced-material-processing-2",
    #],
    "progressive-armor": [
        "heavy-armor",
        "modular-armor",
        "power-armor",
        "power-armor-mk2",
        "mech-armor",
    ],
    "artillery-shell-damage": [
        "artillery-shell-damage-1",
    ],
    "artillery-shell-range": [
        "artillery-shell-range-1",
    ],
    "artillery-shell-speed": [
        "artillery-shell-speed-1",
    ],
    "asteroid-productivity": [
        "asteroid-productivity",
    ],
    "progressive-automation": [
        "automation",
        "automation-2",
        "automation-3",
    ],
    "braking-force": [
        "braking-force-1",
        "braking-force-2",
        "braking-force-3",
        "braking-force-4",
        "braking-force-5",
        "braking-force-6",
        "braking-force-7",
    ],
    "progressive-efficiency-module": [
        "efficiency-module",
        "efficiency-module-2",
        "efficiency-module-3",
    ],
    #"progressive-electric-energy-distribution": [
    #    "electric-energy-distribution-1",
    #    "electric-energy-distribution-2",
    #],
    "electric-weapons-damage": [
        "electric-weapons-damage-1",
        "electric-weapons-damage-2",
        "electric-weapons-damage-3",
        "electric-weapons-damage-4",
    ],
    "progressive-energy-shield": [
        "energy-shield-equipment",
        "energy-shield-mk2-equipment",
    ],
    "progressive-follower-robot": [
        "defender",
        "distractor",
        "destroyer",
    ],
    "follower-robot-count": [
        "follower-robot-count-1",
        "follower-robot-count-2",
        "follower-robot-count-3",
        "follower-robot-count-4",
        "follower-robot-count-5",
    ],
    "health": [
        "health",
    ],
    "progressive-inserter": [
        "fast-inserter",
        "bulk-inserter",
        "stack-inserter",
    ],
    "inserter-capacity-bonus": [
        "inserter-capacity-bonus-1",
        "inserter-capacity-bonus-2",
        "inserter-capacity-bonus-3",
        "inserter-capacity-bonus-4",
        "inserter-capacity-bonus-5",
        "inserter-capacity-bonus-6",
        "inserter-capacity-bonus-7",
    ],
    "laser-shooting-speed": [
        "laser-shooting-speed-1",
        "laser-shooting-speed-2",
        "laser-shooting-speed-3",
        "laser-shooting-speed-4",
        "laser-shooting-speed-5",
        "laser-shooting-speed-6",
        "laser-shooting-speed-7",
    ],
    "laser-weapons-damage": [
        "laser-weapons-damage-1",
        "laser-weapons-damage-2",
        "laser-weapons-damage-3",
        "laser-weapons-damage-4",
        "laser-weapons-damage-5",
        "laser-weapons-damage-6",
        "laser-weapons-damage-7",
    ],
    "progressive-logistics": [
        "logistics",
        "logistics-2",
        "logistics-3",
        "turbo-transport-belt",
    ],
    "low-density-structure-productivity": [
        "low-density-structure-productivity",
    ],
    #"progressive-military": [
    #    "military",
    #    "military-2",
    #    "military-3",
    #    "military-4",
    #],
    "progressive-mining-drill": [
        "electric-mining-drill",
        "big-mining-drill",
    ],
    "mining-productivity": [
        "mining-productivity-1",
        "mining-productivity-2",
        "mining-productivity-3",
    ],
    "progressive-personal-battery": [
        "battery-equipment",
        "battery-mk2-equipment",
        "battery-mk3-equipment",
    ],
    "progressive-personal-roboport": [
        "personal-roboport-equipment",
        "personal-roboport-mk2-equipment",
    ],
    "physical-projectile-damage": [
        "physical-projectile-damage-1",
        "physical-projectile-damage-2",
        "physical-projectile-damage-3",
        "physical-projectile-damage-4",
        "physical-projectile-damage-5",
        "physical-projectile-damage-6",
        "physical-projectile-damage-7",
    ],
    "plastic-bar-productivity": [
        "plastic-bar-productivity",
    ],
    "progressive-portable-power": [
        "solar-panel-equipment",
        "fusion-reactor-equipment",
        "fission-reactor-equipment",
    ],
    "processing-unit-productivity": [
        "processing-unit-productivity",
    ],
    "progressive-productivity-module": [
        "productivity-module",
        "productivity-module-2",
        "productivity-module-3",
    ],
    "progressive-quality-module": [
        "quality-module",
        "quality-module-2",
        "quality-module-3",
    ],
    "progressive-quality": [
        "epic-quality",
        "legendary-quality",
    ],
    "railgun-damage": [
        "railgun-damage-1",
    ],
    "railgun-shooting-speed": [
        "railgun-shooting-speed-1",
    ],
    "refined-flammables": [
        "refined-flammables-1",
        "refined-flammables-2",
        "refined-flammables-3",
        "refined-flammables-4",
        "refined-flammables-5",
        "refined-flammables-6",
        "refined-flammables-7",
    ],
    "research-productivity": [
        "research-productivity",
    ],
    "research-speed": [
        "research-speed-1",
        "research-speed-2",
        "research-speed-3",
        "research-speed-4",
        "research-speed-5",
        "research-speed-6",
    ],
    "rocket-fuel-productivity": [
        "rocket-fuel-productivity",
    ],
    "rocket-part-productivity": [
        "rocket-part-productivity",
    ],
    "scrap-recycling-productivity": [
        "scrap-recycling-productivity",
    ],
    "progressive-soil": [
        "artificial-soil",
        "overgrowth-soil",
    ],
    "progressive-speed-module": [
        "speed-module",
        "speed-module-2",
        "speed-module-3",
    ],
    "steel-plate-productivity": [
        "steel-plate-productivity",
    ],
    "stronger-explosives": [
        "stronger-explosives-1",
        "stronger-explosives-2",
        "stronger-explosives-3",
        "stronger-explosives-4",
        "stronger-explosives-5",
        "stronger-explosives-6",
        "stronger-explosives-7",
    ],
    "transport-belt-capacity": [
        "transport-belt-capacity-1",
        "transport-belt-capacity-2",
    ],
    "weapon-shooting-speed": [
        "weapon-shooting-speed-1",
        "weapon-shooting-speed-2",
        "weapon-shooting-speed-3",
        "weapon-shooting-speed-4",
        "weapon-shooting-speed-5",
        "weapon-shooting-speed-6",
    ],
    "worker-robots-speed": [
        "worker-robots-speed-1",
        "worker-robots-speed-2",
        "worker-robots-speed-3",
        "worker-robots-speed-4",
        "worker-robots-speed-5",
        "worker-robots-speed-6",
        "worker-robots-speed-7",
    ],
    "worker-robots-storage": [
        "worker-robots-storage-1",
        "worker-robots-storage-2",
        "worker-robots-storage-3",
    ],
}

technology_name_to_progressive_group_name = {
    technology_name: progressive_group_name
    for progressive_group_name, stack in progressive_technology_stacks.items()
    for technology_name in stack
}
assert all(
    technology_name_to_progressive_group_name[technology_name] == progressive_group_name
    for progressive_group_name, stack in progressive_technology_stacks.items()
    for technology_name in stack
), "progressive technology listed in multiple stacks"

energy_link_bridge_recipes = {
    "early_game": [
        dict(type="item", amount=50, name="iron-plate"),
        dict(type="item", amount=50, name="copper-plate"),
    ],
    "mid_game": [
        dict(type="item", amount=1, name="accumulator"),
        dict(type="item", amount=1, name="radar"),
    ],
    "fulgora": [
        dict(type="item", amount=10, name="supercapacitor"),
        dict(type="item", amount=1,  name="radar"),
    ],
}
