require "template_parameters" -- defines PARAMS

-- Balance tuning.
data.raw["rocket-silo"]["rocket-silo"].rocket_parts_required = PARAMS.rocket_parts_per_rocket
data.raw["recipe"]["space-platform-foundation"].ingredients = {
    {type="item", name="steel-plate",  amount=PARAMS.ingredients_per_space_platform_foundation},
    {type="item", name="copper-cable", amount=PARAMS.ingredients_per_space_platform_foundation},
}

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
