from . import K64TestBase
from .. import K64World


class TestAccess(K64TestBase):
    def test_crystals(self):
        world = self.world
        assert isinstance(world, K64World)
        shards = self.get_items_by_name("Crystal Shard")
        for i, shard_requirement in enumerate(world.boss_requirements, 1):
            shard_num = self.count("Crystal Shard")
            self.collect(shards[shard_num:shard_requirement])
            self.assertTrue(self.count("Crystal Shard") == shard_requirement)
            self.assertTrue(self.can_reach_entrance(f"To Level {i + 1}"))
