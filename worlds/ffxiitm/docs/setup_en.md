# Final Fantasy XII Trial Mode Setup Guide

# Required Software
- The Steam release of [Final Fantasy XII: The Zodiac Age](https://store.steampowered.com/app/595520/FINAL_FANTASY_XII_THE_ZODIAC_AGE)
- [FF12 LUA Loader](https://www.nexusmods.com/finalfantasy12/mods/171) mod
- [FF12 External File Loader](https://www.nexusmods.com/finalfantasy12/mods/170)
- The Trial Mode [mod files](https://github.com/silasary/FFXII-Trial-Mode-AP-Source/releases/latest)

# Important Note

The Trial Mode randomizer and Open World randomizer are not compatible.

Be sure to remove the Trial Mode lua script and entry in ff12-file-loader.ini before starting an Open World seed, and be sure to remove an Open World seed before loading a Trial Mode run.

# Setup

1. Download test.zip, ffxii_tm_ap.lua, and FFXII_001
2. Navigate to your installation of FFXII (usually C:\\Program Files (x86)\\Steam\\steamapps\\common\\FINAL FANTASY XII THE ZODIAC AGE)
3. In this folder, navigate to the mods folder (or create it if it doesn't exist)
4. Extract the contents of test.zip into the mods folder
5. Back in the root directory, navigate to /x64/scripts/ and place ffxii_tm_ap.lua inside
6. Navigate to /x64/modules/config/ and find your ff12-file-loader.ini file
7. Edit ff12-file-loader.ini to add the line "test=mods\\test" under [Paths]
8. Open steam, right click FINAL FANTASY XII THE ZODIAC AGE, and click properties
9. In the general tab, toggle off "Keep game saves in the Steam Cloud for FINAL FANTASY XII THE ZODIAC AGE"
10. Navigate to your FFXII saved games (usually My Games\\FINAL FANTASY XII THE ZODIAC AGE\\76561198064630370)
11. Backup your saves
12. Place FFXII_001 inside
13. Get a yaml file with "Generate Template Settings", and play!

