require "template_parameters" -- defines PARAMS

-- Configure any-planet-start settings.
-- We want:
--  * enable safe orbit
--  * enable vulcanus-fulgora space connection
--  * configurable vulcanus rock multiplier
-- The APS settings were determined by extracting the mod zip version 1.1.28 and reading settings.lua.
-- Factorio settings API reference is here: https://wiki.factorio.com/Tutorial:Mod_settings .
if mods["any-planet-start"] then
    local starting_planet = PARAMS.starting_planet
    if starting_planet == "nauvis" then starting_planet = "none" end -- It's called "none" I guess.
    data.raw["string-setting"]["aps-planet"].hidden = true
    data.raw["string-setting"]["aps-planet"].allowed_values = {starting_planet}
    data.raw["string-setting"]["aps-planet"].default_value = starting_planet
    data.raw["bool-setting"]["aps-safe-orbit"].hidden = true
    data.raw["bool-setting"]["aps-safe-orbit"].forced_value = true
    data.raw["bool-setting"]["aps-safe-orbit"].default_value = true
    data.raw["double-setting"]["aps-vulcanus-rock-multiplier"].hidden = true
    data.raw["double-setting"]["aps-vulcanus-rock-multiplier"].allowed_values = {PARAMS.vulcanus_rock_multiplier}
    data.raw["double-setting"]["aps-vulcanus-rock-multiplier"].default_value = PARAMS.vulcanus_rock_multiplier
    data.raw["bool-setting"]["aps-vulcanus-fulgora"].hidden = true
    data.raw["bool-setting"]["aps-vulcanus-fulgora"].forced_value = true
    data.raw["bool-setting"]["aps-vulcanus-fulgora"].default_value = true
end
if mods['planet-picker'] then
    data.raw['bool-setting']['planet-picker-modify-fulgora-ruins'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-ruins'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-ruins'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-ice'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-ice'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-ice'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-sulfur'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-sulfur'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-fulgora-sulfur'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-gleba-centrifugation'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-gleba-centrifugation'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-gleba-centrifugation'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-gleba-landfill'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-gleba-landfill'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-gleba-landfill'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-trees'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-trees'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-trees'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-plastic'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-plastic'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-plastic'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-generator'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-generator'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-generator'].forced_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-mining'].default_value = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-mining'].hidden = true
    data.raw['bool-setting']['planet-picker-modify-vulcanus-mining'].forced_value = true
end
