from typing import Dict, Set

location_name_groups: Dict[str, Set[str]] = {
    "Writing": {f"Writing Skill {i}" for i in range(2, 11)},
    "Charisma": {f"Charisma Skill {i}" for i in range(2, 11)},
    "Comedy": {f"Comedy Skill {i}" for i in range(2, 11)},
    "Cooking": {f"Cooking Skill {i}" for i in range(2, 11)},
    "Gourmet": {f"Gourmet Skill {i}" for i in range(2, 11)},
    "Fishing": {f"Fishing Skill {i}" for i in range(2, 11)},
    "Fitness": {f"Fitness Skill {i}" for i in range(2, 11)},
    "Gardening": {f"Gardening Skill {i}" for i in range(2, 11)},
    "Handiness": {f"Handiness Skill {i}" for i in range(2, 11)},
    "Logic": {f"Logic Skill {i}" for i in range(2, 11)},
    "Mischief": {f"Mischief Skill {i}" for i in range(2, 11)},
    "Mixology": {f"Mixology Skill {i}" for i in range(2, 11)},
    "Painting": {f"Painting Skill {i}" for i in range(2, 11)},
    "Piano": {f"Piano Skill {i}" for i in range(2, 11)},
    "Programming": {f"Programming Skill {i}" for i in range(2, 11)},
    "Rocket Science": {f"Rocket Science Skill {i}" for i in range(2, 11)},
    "Video Gaming": {f"Video Gaming Skill {i}" for i in range(2, 11)},
    "Violin": {f"Violin Skill {i}" for i in range(2, 11)},
    "Photography": {f"Photography Skill {i}" for i in range(2,6)},
    "Guitar": {f"Guitar Skill {i}" for i in range(2,11)},
    "Music": {f"{instrument} Skill {level}"
              for instrument in ["Piano", "Violin", "Guitar"]
              for level in range(1, 11)}
}