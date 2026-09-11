from .bases import FFXIITMTestBase


class StartingInventoryFromPoolTest(FFXIITMTestBase):
    options = {
        "trial_victory": 100,
        "start_inventory_from_pool": {"Cura": 1, "Seitengrat": 1, "Zodiark": 1}
    }

class StartingInventoryTest(FFXIITMTestBase):
    options = {
        "trial_victory": 100,
        "start_inventory_from_pool": {"Cura": 1, "Seitengrat": 1, "Zodiark": 1}
    }

