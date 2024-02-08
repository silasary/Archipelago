
from test.bases import WorldTestBase


class FFXIITMTestBase(WorldTestBase):
    game = "Final Fantasy XII Trial Mode"

    def test_has_enough_vouchers(self):
        assert len(self.multiworld.itempool) <= 5*99, "More items than AP Vouchers"
