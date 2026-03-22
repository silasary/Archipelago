require "template_parameters" -- defines PARAMS

-- Recipe changes.
for name, updates in pairs(PARAMS.recipe_changes) do
    for k, v in pairs(updates) do
        data.raw["recipe"][name][k] = v
    end
end
data.raw["rocket-silo"]["rocket-silo"].rocket_parts_required = PARAMS.rocket_parts_per_rocket

-- Asteroid HP changes.
for name, health in pairs(PARAMS.asteroid_hp_changes) do
    data.raw["asteroid"][name].max_health = health
end

-- Technology changes.
for name, effects in pairs(PARAMS.technology_effect_additions) do
    for _, effect in pairs(effects) do
        table.insert(data.raw["technology"][name].effects, effect)
    end
end

-- Disable and hide base technologies.
for _, tech_name in pairs(PARAMS.hide_base_technologies) do
    local base_tech = data.raw["technology"][tech_name]
    -- You can't queue these up, so don't show them in the technology tree gui.
    base_tech.hidden = true
    -- Even if we set this to false, it still doesn't show up in Factoriopedia.
    base_tech.hidden_in_factoriopedia = true
    -- These technologies will be granted by mods, not by normal in-game events.
    base_tech.research_trigger = {
        type = "scripted",
    }
end
