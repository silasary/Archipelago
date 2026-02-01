-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require('lib')

local MOD_NAME = {{ lua_mod_name }}
local HIDE_BASE_TECHNOLOGIES = {{ lua_hide_base_technologies }}
local NEW_TECHNOLOGY_DATA = {{ lua_new_technology_data }}


local technologies = data.raw["technology"]

local template_tech = table.deepcopy(technologies["automation"])
template_tech.effects = {} -- The effect is implemented by the multiworld.
template_tech.upgrade = false -- Never collapse multiple technologies together as an upgrade set.
template_tech.prerequisites = {} -- Will be set later.

-- The base technologies are triggered behind the scenes in control.lua.
-- Hide them from the player and make them impossible to trigger normally.
for _, tech_name in pairs(HIDE_BASE_TECHNOLOGIES) do
    local base_tech = technologies[tech_name]
    base_tech.hidden = true
    base_tech.hidden_in_factoriopedia = true
    base_tech.research_trigger = nil
    base_tech.unit = {
        -- Unreachable non-zero cost.
        count = 1,
        ingredients = { {"automation-science-pack", 1} },
        time = 60,
    }
end

for tech_name, tech_data in pairs(NEW_TECHNOLOGY_DATA) do
    -- https://lua-api.factorio.com/stable/prototypes/TechnologyPrototype.html
    local new_tech = table.deepcopy(template_tech)
    new_tech.name             = tech_name
    new_tech.research_trigger = tech_data.research_trigger
    new_tech.unit             = tech_data.unit
    new_tech.max_level        = tech_data.max_level
    new_tech.prerequisites    = tech_data.prerequisites

    -- Set icon.
    if string.sub(tech_data.icon, 1, 1) == "/" then
        -- Generic icon.
        new_tech.icon = "__" .. MOD_NAME .. "__/graphics/icons" .. tech_data.icon
        new_tech.icon_size = 128
        new_tech.icons = nil
    else
        -- Copy icon from a technology.
        local source_tech = technologies[tech_data.icon]
        new_tech.icon = table.deepcopy(source_tech.icon)
        new_tech.icon_size = table.deepcopy(source_tech.icon_size)
        new_tech.icons = table.deepcopy(source_tech.icons)
    end

    data:extend{new_tech}
end
