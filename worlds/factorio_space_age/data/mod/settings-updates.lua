require "template_parameters" -- defines PARAMS

-- Configure any-planet-start settings.
-- We want:
--  * enable safe orbit
--  * enable vulcanus-fulgora space connection
--  * 10x vulcanus rock multiplier
-- The APS settings were determined by extracting the mod zip version 1.1.28 and reading settings.lua.
-- Factorio settings API reference is here: https://wiki.factorio.com/Tutorial:Mod_settings .
if PARAMS.starting_planet ~= "nauvis" then
    data.raw["string-setting"]["aps-planet"].hidden = true
    data.raw["string-setting"]["aps-planet"].allowed_values = {PARAMS.starting_planet}
    data.raw["string-setting"]["aps-planet"].default_value = PARAMS.starting_planet
    data.raw["bool-setting"]["aps-safe-orbit"].hidden = true
    data.raw["bool-setting"]["aps-safe-orbit"].forced_value = true
    data.raw["bool-setting"]["aps-safe-orbit"].default_value = true
end
if PARAMS.starting_planet == "vulcanus" then
    data.raw["double-setting"]["aps-vulcanus-rock-multiplier"].hidden = true
    data.raw["double-setting"]["aps-vulcanus-rock-multiplier"].allowed_values = {10}
    data.raw["double-setting"]["aps-vulcanus-rock-multiplier"].default_value = 10
end
if PARAMS.starting_planet == "vulcanus" or PARAMS.starting_planet == "fulgora" then
    data.raw["bool-setting"]["aps-vulcanus-fulgora"].hidden = true
    data.raw["bool-setting"]["aps-vulcanus-fulgora"].forced_value = true
    data.raw["bool-setting"]["aps-vulcanus-fulgora"].default_value = true
end
