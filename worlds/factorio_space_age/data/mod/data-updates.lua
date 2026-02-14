require "template_parameters" -- defines PARAMS

data.raw["rocket-silo"]["rocket-silo"].rocket_parts_required = PARAMS.rocket_parts_per_rocket
data.raw["recipe"]["space-platform-foundation"].ingredients = {
    {type="item", name="steel-plate",  amount=PARAMS.ingredients_per_space_platform_foundation},
    {type="item", name="copper-cable", amount=PARAMS.ingredients_per_space_platform_foundation},
}
