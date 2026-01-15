from typing import Dict, List

from .Technologies import factorio_base_id, recipes
from .Options import MaxSciencePack

# The AP id for every location name.
location_table: Dict[str, int] = {}

_id_cursor: int = factorio_base_id
def _new_location(name: str):
    global _id_cursor
    location_table[name] = _id_cursor
    _id_cursor += 1
    return name

# Every possible research location name grouped by their max science pack ingredient name.
#  "automation-science-pack": ["AP-1-001", ... "AP-1-999"],
#  "logistic-science-pack":   ["AP-2-001", ... "AP-2-999"],
#  ...
# The second number determines how expensive the research is.
location_pools: Dict[str, List[str]] = {
    pack: [_new_location("AP-{}-{:03}".format(i, x)) for x in range(1, 999+1)]
    for i, pack in enumerate(MaxSciencePack.get_ordered_science_packs(), start=1)
}

_valid_items = set()
for recipe_name, recipe in recipes.items():
    if not recipe_name.endswith(("-barrel", "-science-pack")):
        _valid_items.update(recipe.products)
    craftsanity_locations.append(_new_location(f"Craft {item}"))

# Every possible craftsanity location name.
craftsanity_locations = [_new_location(f"Craft {item}") for item in sorted(_valid_items)]
