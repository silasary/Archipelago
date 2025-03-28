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
              for level in range(1, 11)},
    "Astronaut": {
        "Module Cleaner (Astronaut 2)"
        "Technician (Astronaut 3)"
        "Command Center Lead (Astronaut 4)"
        "Low-Orbit Specialist (Astronaut 5)"
        "Space Cadet (Astronaut 6)"
        "Astronaut (Astronaut 7)"
        "Planet Patrol (Astronaut / Space Ranger 8)"
        "Sheriff of the Stars (Astronaut / Space Ranger 9)"
        "Space Ranger (Astronaut / Space Ranger 10)"
        "Moon Mercenary (Astronaut / Interstellar Smuggler 8)"
        "Alien Goods Trader (Astronaut / Interstellar Smuggler 9)"
        "Interstellar Smuggler (Astronaut / Interstellar Smuggler 10)"
    },
    "Space Ranger": {
        "Planet Patrol (Astronaut / Space Ranger 8)"
        "Sheriff of the Stars (Astronaut / Space Ranger 9)"
        "Space Ranger (Astronaut / Space Ranger 10)"
    },
    "Interstellar Smuggler": {
        "Moon Mercenary (Astronaut / Interstellar Smuggler 8)"
        "Alien Goods Trader (Astronaut / Interstellar Smuggler 9)"
        "Interstellar Smuggler (Astronaut / Interstellar Smuggler 10)"
    },
    "Athlete": {
        "Locker Room Attendant (Athlete 2)"
        "Team Mascot (Athlete 3)"
        "Dance Team Captain (Athlete 4)"
        "Minor Leaguer (Athlete / Professional Athlete 5)"
        "Rookie (Athlete / Professional Athlete 6)"
        "Starter (Athlete / Professional Athlete 7)"
        "All-Star (Athlete / Professional Athlete 8)"
        "MVP (Athlete / Professional Athlete 9)"
        "Hall of Famer (Athlete / Professional Athlete 10)"
        "Personal Trainer (Athlete / Bodybuilder 5)"
        "Professional Bodybuilder (Athlete / Bodybuilder 6)"
        "Champion Bodybuilder (Athlete / Bodybuilder 7)"
        "Trainer to the Stars (Athlete / Bodybuilder 8)"
        "Celebrity Bodybuilder (Athlete / Bodybuilder 9)"
        "Mr. / Mrs. Solar System (Athlete / Bodybuilder 10)"
    },
    "Professional Athlete": {
        "Minor Leaguer (Athlete / Professional Athlete 5)"
        "Rookie (Athlete / Professional Athlete 6)"
        "Starter (Athlete / Professional Athlete 7)"
        "All-Star (Athlete / Professional Athlete 8)"
        "MVP (Athlete / Professional Athlete 9)"
        "Hall of Famer (Athlete / Professional Athlete 10)"
    },
    "Bodybuilder": {
        "Personal Trainer (Athlete / Bodybuilder 5)"
        "Professional Bodybuilder (Athlete / Bodybuilder 6)"
        "Champion Bodybuilder (Athlete / Bodybuilder 7)"
        "Trainer to the Stars (Athlete / Bodybuilder 8)"
        "Celebrity Bodybuilder (Athlete / Bodybuilder 9)"
        "Mr. / Mrs. Solar System (Athlete / Bodybuilder 10)"
    }
}