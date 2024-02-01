from worlds.ffxiitm.test import FFXIITMTestBase


class TenFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 10,
    }

class SixtyFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 60,
    }

class MaxFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 100,
    }
