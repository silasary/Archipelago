require "lib"
require "template_parameters" -- defines PARAMS

local technologies = data.raw["technology"]

local template_tech = table.deepcopy(technologies["automation"])
template_tech.effects = {} -- The effect is implemented by the multiworld.
template_tech.upgrade = false -- Never collapse multiple technologies together as an upgrade set.
template_tech.prerequisites = {} -- Will be set later.

-- The base technologies are triggered behind the scenes in control.lua.
-- Hide them from the player and make them impossible to trigger normally.
for _, tech_name in pairs(PARAMS.hide_base_technologies) do
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

for tech_name, tech_data in pairs(PARAMS.new_technology_data) do
    -- https://lua-api.factorio.com/stable/prototypes/TechnologyPrototype.html
    local new_tech = table.deepcopy(template_tech)
    new_tech.name = tech_name
    new_tech.unit = tech_data.unit
    new_tech.research_trigger = tech_data.research_trigger
    new_tech.prerequisites = tech_data.prerequisites

    -- Set icon.
    if string.sub(tech_data.icon, 1, 1) == "/" then
        -- Generic icon.
        new_tech.icon = "__" .. PARAMS.mod_name .. "__/graphics/icons" .. tech_data.icon
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

--for tech_name, tech_data in pairs(PARAMS.new_technology_data) do
--    local prerequisites = {}
--    for _, name in pairs(tech_data.prerequisites) do
--        prerequisites[name] = technologies[name]
--    end
--    technologies[tech_name].prerequisites = prerequisites
--end
