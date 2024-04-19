from worlds.ffxiitm.test import FFXIITMTestBase


class StartingInventoryTest(FFXIITMTestBase):
    options = {
        "trial_victory": 100,
        "start_inventory": {"Bangle": 1, "Charge": 1, "Zodiark": 1}
    }

    def test_starting_inventory(self):
        for item in self.multiworld.itempool:
            self.assertNotIn(item.name, self.options["start_inventory"])
