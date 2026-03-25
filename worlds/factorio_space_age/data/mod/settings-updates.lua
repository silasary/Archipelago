require "template_parameters" -- defines PARAMS

-- Configure any-planet-start settings.
-- We want:
--  * enable safe orbit
--  * enable vulcanus-fulgora space connection
--  * configurable vulcanus rock multiplier
-- The APS settings were determined by extracting the mod zip version 1.1.28 and reading settings.lua.
-- Factorio settings API reference is here: https://wiki.factorio.com/Tutorial:Mod_settings .
if PARAMS.starting_planet ~= "nauvis" then
    data.raw["string-setting"]["aps-planet"].hidden = true
    data.raw["string-setting"]["aps-planet"].allowed_values = {PARAMS.starting_planet}
    data.raw["string-setting"]["aps-planet"].default_value = PARAMS.starting_planet
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
