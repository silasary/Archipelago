-- Force SAWS settings because the mod generation assume a specific config
if data.raw["string-setting"]["saws-scrap-recipe"] then
    data.raw["string-setting"]["saws-scrap-recipe"].hidden = true
    data.raw["string-setting"]["saws-scrap-recipe"].allowed_values = { "space-age" }
    data.raw["string-setting"]["saws-scrap-recipe"].default_value = "space-age"
end

if data.raw["bool-setting"]["saws-lava"] then
    data.raw["bool-setting"]["saws-lava"].hidden = true
    data.raw["bool-setting"]["saws-lava"].forced_value = true
    data.raw["bool-setting"]["saws-lava"].default_value = true
end

if data.raw["bool-setting"]["saws-bacteria-cultivation"] then
    data.raw["bool-setting"]["saws-bacteria-cultivation"].hidden = true
    data.raw["bool-setting"]["saws-bacteria-cultivation"].forced_value = true
    data.raw["bool-setting"]["saws-bacteria-cultivation"].default_value = true
end
