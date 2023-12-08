from typing import Dict
from Options import Option, Toggle


class LearnSkillItem(Toggle):
    """An item is needed to earn the first skill point of a skill"""
    display_name = "Need Item for First Skill"


sims4_options: Dict[str, type(Option)] = {
    "learn_skill_item": LearnSkillItem
}
