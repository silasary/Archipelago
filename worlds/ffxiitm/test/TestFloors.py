from .bases import FFXIITMTestBase

class OneFloorTest(FFXIITMTestBase):
    options = {
        "trial_victory": 1,
    }

class EightFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 8,
    }

class TenFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 10,
    }

class ThirtyFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 30,
    }

class SixtyFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 60,
    }

class MaxFloorsTest(FFXIITMTestBase):
    options = {
        "trial_victory": 100,
    }
