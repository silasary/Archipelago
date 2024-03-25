# How Universal Tracker works

![image](https://github.com/FarisTheAncient/Archipelago/assets/162540354/32ae372a-a833-4f98-9d8e-e03066ea7f7f)

![image](https://github.com/FarisTheAncient/Archipelago/assets/162540354/4e9d3ac6-b5f9-4f9f-9667-b01aa39c754b)

However with some games, the internal logic state of UT and the **actual** state of the server don't match, this is usually caused by the game implementing randomness in the logic that isn't soley tied to items

When this happens the World Dev needs to implement one of a few hooks that UT provides to allow UT to properly track the logic

# interpret_slot_data

The First and simplest hook is for the world to have a function called `interpret_slot_data` that takes in a dict as a parameter  
If a world implements this function, after UT's internal generation when the tracker connects to the slot on the server, it will pass the slot_data (that the original world created) to the internal world  
This allows for the internal world to have a space in time before logic is tracked to modify any connections/settings it can in runtime to correct and differences between it and the actual state on the server  

![image](https://github.com/FarisTheAncient/Archipelago/assets/162540354/41578c5f-da5d-418f-be2d-bc2d98182501)

However not all settings can be changed **after** generation occurs, so there's another hook available to world devs to provide UT support in their apworlds

# re_gen_passthrough

If the `interpret_slot_data` function returns non-None, this will cause UT to restart generation, but this time passing in whatever was returned as an extra value in the multiworld gen

The value will be added to the `multiworld.re_gen_passthrough` dict, with the key being the game name.  
This is to prevent a game trying to process a different game's `interpret_slot_data` (like if there's more then one game with UT support in the internal multiworld)

![image](https://github.com/FarisTheAncient/Archipelago/assets/162540354/03b22004-8017-457e-be3c-26d20091f678)


