
class FactorioData:
    """
    This class represents all the recipes, technologies, etc. in Factorio,
    and supports making changes, such as recipe randomization, and then can compute derrived info,
    such as logical dependencies.
    """
    the_data: dict[str, dict[str, dict]]
    # Derrived:
    infinite_technology_names: set[str]
    empty_technology_names: set[str]
    def __init__(self, the_data):
        self.the_data = the_data
        # Derrived:
        self.infinite_technology_names = {
            name for name, prototype in self.the_data["technology"].items()
            if prototype.get("max_level", "") == "infinite"
        }
        self.empty_technology_names = {
            name for name, prototype in self.the_data["technology"].items()
            if len(prototype.get("effects", [])) == 0
        }

    def unrecognized_recipe_names(self, possible_names: set[str]) -> set[str]:
        return self._unrecognized_names(possible_names, self.the_data["recipe"])
    def unrecognized_item_names(self, possible_names: set[str]) -> set[str]:
        return self._unrecognized_names(possible_names, self.the_data["item"])
    def _unrecognized_names(self, possible_names: set[str], prototypes: dict[str, dict]) -> set[str]:
        bad_names = possible_names - prototypes.keys()
        for name in (possible_names & prototypes.keys()):
            prototype_data = prototypes[name]
            if prototype_data.get("hidden", False) or prototype_data.get("parameter", False):
                bad_names.add(name)
        return bad_names

    def build_logic(self, **kwargs):
        return {}
