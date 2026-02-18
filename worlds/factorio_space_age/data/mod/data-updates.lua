require "template_parameters" -- defines PARAMS

data.raw["rocket-silo"]["rocket-silo"].rocket_parts_required = PARAMS.rocket_parts_per_rocket
data.raw["recipe"]["space-platform-foundation"].ingredients = {
    {type="item", name="steel-plate",  amount=PARAMS.ingredients_per_space_platform_foundation},
    {type="item", name="copper-cable", amount=PARAMS.ingredients_per_space_platform_foundation},
}

-- Disable and hide the base technologies.
for _, tech_name in pairs(PARAMS.hide_base_technologies) do
    local base_tech = data.raw["technology"][tech_name]
    -- You can't queue these up, so don't show them in the technology tree gui.
    base_tech.hidden = true
    -- However, you can see them in factoriopedia as the AP item that grants recipes.
    base_tech.hidden_in_factoriopedia = false
    -- These technologies will be granted by mods, not by normal in-game events.
    base_tech.research_trigger = {
        type = "scripted",
    }
end
