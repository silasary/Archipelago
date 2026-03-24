require "template_parameters" -- defines PARAMS


-- CREATE NEW STUFF.

-- (Note: conceptually, this belongs in data.lua, not in data-updates.lua,
--  but we must do this after any-planet-start creates technology planet-discovery-nauvis,
--  which happens in that mod's data-updates.lua.)

local function energy_bridge_tint()
    return { r = 0, g = 1, b = 0.667, a = 1}
end
local function tint_icon(obj, tint)
    obj.icons = { {icon = obj.icon, icon_size = obj.icon_size, icon_mipmaps = obj.icon_mipmaps, tint = tint} }
    obj.icon = nil
    obj.icon_size = nil
    obj.icon_mipmaps = nil
end

-- Create new technologies.
for tech_name, tech_data in pairs(PARAMS.new_technology_data) do
    -- https://lua-api.factorio.com/stable/prototypes/TechnologyPrototype.html
    local new_tech = {
        type = "technology",
        name = tech_name,
        level = tech_data.level,
        max_level = tech_data.max_level,
        unit = tech_data.unit,
        research_trigger = tech_data.research_trigger,
        prerequisites = tech_data.prerequisites,
        effects = tech_data.effects,
    }

    if new_tech.level ~= nil then
        -- Infinite technologies should not send to the multiworld.
        -- Change the name suffix to keep them local.
        new_tech.name = new_tech.name .. "-" .. tostring(new_tech.level)
    end

    -- Set icon.
    if string.sub(tech_data.icon, 1, 1) == "/" then
        -- Generic icon.
        new_tech.icon = "__" .. PARAMS.mod_name .. "__/graphics/icons" .. tech_data.icon
        new_tech.icon_size = 128
        new_tech.icons = nil
    elseif tech_data.icon == "ap-energy-link-bridge" then
        -- Give it the energy link icon.
        new_tech.icon = data.raw["item"]["accumulator"].icon
        tint_icon(new_tech, energy_bridge_tint())
    else
        -- Copy icon from a technology.
        local source_tech = data.raw["technology"][tech_data.icon]
        new_tech.icon = table.deepcopy(source_tech.icon)
        new_tech.icon_size = table.deepcopy(source_tech.icon_size)
        new_tech.icons = table.deepcopy(source_tech.icons)
    end

    data:extend{new_tech}
end

-- Create new items.
if PARAMS.energy_link_increment > 0 then
    -- TODO: Replace the tinting code with an actual rendered picture of the energy bridge icon.
    -- This tint is so that one is less likely to accidentally mass-produce energy-bridges, then wonder why their rocket is not building.
    local entity = table.deepcopy(data.raw["accumulator"]["accumulator"])
    entity.name = "ap-energy-link-bridge"
    entity.minable.result = "ap-energy-link-bridge"
    entity.localised_name = "Archipelago EnergyLink Bridge" -- TODO: move to locale.cfg
    entity.energy_source.buffer_capacity = "50MJ"
    entity.energy_source.input_flow_limit = "1MW"
    entity.energy_source.output_flow_limit = "1MW"
    tint_icon(entity, energy_bridge_tint())
    entity.chargable_graphics.picture.layers[1].tint = energy_bridge_tint()
    entity.chargable_graphics.charge_animation.layers[1].layers[1].tint = energy_bridge_tint()
    entity.chargable_graphics.discharge_animation.layers[1].layers[1].tint = energy_bridge_tint()
    data.raw["accumulator"]["ap-energy-link-bridge"] = entity

    local item = table.deepcopy(data.raw["item"]["accumulator"])
    item.name = "ap-energy-link-bridge"
    item.localised_name = "Archipelago EnergyLink Bridge"
    item.place_result = entity.name
    tint_icon(item, energy_bridge_tint())
    data.raw["item"]["ap-energy-link-bridge"] = item

    local recipe = table.deepcopy(data.raw["recipe"]["accumulator"])
    recipe.name = "ap-energy-link-bridge"
    recipe.ingredients = PARAMS.energy_link_bridge_ingredients
    recipe.results = { {type = "item", name = item.name, amount = 1} }
    recipe.energy_required = 10
    recipe.enabled = PARAMS.energy_link_bridge_starts_unlocked
    recipe.localised_name = "Archipelago EnergyLink Bridge"
    data.raw["recipe"]["ap-energy-link-bridge"] = recipe

    local technology = {
        type = "technology",
        name = "ap-energy-link-bridge",
        icons = table.deepcopy(item.icons),
        effects = {
            {type="unlock-recipe", recipe="ap-energy-link-bridge"},
        },
        research_trigger = {type="scripted"},
        hidden = true,
        hidden_in_factoriopedia = true,
    }
    data:extend{technology}
end

-- Create map preset.
data.raw["map-gen-presets"].default["archipelago"] = PARAMS.world_gen_preset


-- UPDATES TO EXISTING STUFF.

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
