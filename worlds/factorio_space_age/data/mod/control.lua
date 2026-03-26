require "lib"
require "util"
require "template_parameters" -- defines PARAMS

ENERGY_INCREMENT = PARAMS.energy_link_increment
ENERGY_LINK_EFFICIENCY = 0.75

if settings.global[PARAMS.death_link_setting].value then
    DEATH_LINK = 1
else
    DEATH_LINK = 0
end

CURRENTLY_DEATH_LOCK = 0

-- Handle the pathfinding result of teleport traps
script.on_event(defines.events.on_script_path_request_finished, handle_teleport_attempt)

-- EnergyLink
local function validate_energy_link_bridge(unit_number, entity)
    if entity ~= nil and entity.valid then
        return true
    end
    storage.energy_link_bridges[unit_number] = nil
    return false
end
local function count_energy_bridges()
    local count = 0
    for i, bridge in pairs(storage.energy_link_bridges) do
        if validate_energy_link_bridge(i, bridge) then
            count = count + 1 + (bridge.quality.level * 0.3)
        end
    end
    return count
end
local function get_energy_increment(bridge)
    return ENERGY_INCREMENT + (ENERGY_INCREMENT * 0.3 * bridge.quality.level)
end
local function on_check_energy_link()
    --- assuming 1 MJ increment and 5MJ battery:
    --- first 2 MJ request fill, last 2 MJ push energy, middle 1 MJ does nothing
    local force = "player"
    local bridges = storage.energy_link_bridges
    local bridgecount = count_energy_bridges()
    storage.forcedata[force].energy_bridges = bridgecount
    if storage.forcedata[force].energy == nil then
        storage.forcedata[force].energy = 0
    end
    if storage.forcedata[force].energy < ENERGY_INCREMENT * bridgecount * 5 then
        for i, bridge in pairs(bridges) do
            if validate_energy_link_bridge(i, bridge) then
                local energy_increment = get_energy_increment(bridge)
                if bridge.energy > energy_increment*3 then
                    storage.forcedata[force].energy = storage.forcedata[force].energy + (energy_increment * ENERGY_LINK_EFFICIENCY)
                    bridge.energy = bridge.energy - energy_increment
                end
            end
        end
    end
    for i, bridge in pairs(bridges) do
        if validate_energy_link_bridge(i, bridge) then
            local energy_increment = get_energy_increment(bridge)
            if storage.forcedata[force].energy < energy_increment and bridge.quality.level == 0 then
                break
            end
            if bridge.energy < energy_increment*2 and storage.forcedata[force].energy > energy_increment then
                storage.forcedata[force].energy = storage.forcedata[force].energy - energy_increment
                bridge.energy = bridge.energy + energy_increment
            end
        end
    end
end
local function string_starts_with(str, start)
    return str:sub(1, #start) == start
end
local function on_energy_bridge_constructed(entity)
    if entity and entity.valid then
        if entity.prototype.name == "ap-energy-link-bridge" then
            storage.energy_link_bridges[entity.unit_number] = entity
        end
    end
end
local function on_energy_bridge_removed(entity)
    if entity.prototype.name == "ap-energy-link-bridge" then
        storage.energy_link_bridges[entity.unit_number] = nil
    end
end
if ENERGY_INCREMENT > 0 then
    script.on_nth_tick(60, on_check_energy_link)

    script.on_event({defines.events.on_built_entity},                function(event) on_energy_bridge_constructed(event.entity) end)
    script.on_event({defines.events.on_robot_built_entity},          function(event) on_energy_bridge_constructed(event.entity) end)
    script.on_event({defines.events.on_space_platform_built_entity}, function(event) on_energy_bridge_constructed(event.entity) end)
    script.on_event({defines.events.on_entity_cloned},               function(event) on_energy_bridge_constructed(event.destination) end)

    script.on_event({defines.events.script_raised_revive}, function(event) on_energy_bridge_constructed(event.entity) end)
    script.on_event({defines.events.script_raised_built},  function(event) on_energy_bridge_constructed(event.entity) end)

    -- see below for defines.events.on_entity_died
    script.on_event({defines.events.on_player_mined_entity},         function(event) on_energy_bridge_removed(event.entity) end)
    script.on_event({defines.events.on_robot_mined_entity},          function(event) on_energy_bridge_removed(event.entity) end)
    script.on_event({defines.events.on_space_platform_mined_entity}, function(event) on_energy_bridge_removed(event.entity) end)
end

local function set_permissions()
    if not PARAMS.allow_imported_blueprints then
        local group = game.permissions.get_group("Default")
        group.set_allows_action(defines.input_action.open_blueprint_library_gui, false)
        group.set_allows_action(defines.input_action.import_blueprint, false)
        group.set_allows_action(defines.input_action.import_blueprint_string, false)
        group.set_allows_action(defines.input_action.import_blueprints_filtered, false)
    end
end

local function is_ap_technology(technology_name)
    if string.match(technology_name, "_location$") ~= nil then
        return true
    else
        return false
    end
end

-- Initialize force data, either from it being created or already being part of the game when the mod was added.
local function on_force_created(event)
    local force = event.force
    if type(event.force) == "string" then  -- should be of type LuaForce
        force = game.forces[force]
    end
    local data = {}
    data["earned_samples"] = table.deepcopy(PARAMS.starting_items)
    data["victory"] = 0
    data["death_link_tick"] = 0
    data["energy"] = 0
    data["energy_bridges"] = 0
    storage.forcedata[event.force] = data
end
script.on_event(defines.events.on_force_created, on_force_created)

-- Destroy force data.  This doesn't appear to be currently possible with the Factorio API, but here for completeness.
local function on_force_destroyed(event)
    storage.forcedata[event.force.name] = nil
end

local function dumpInfo(force)
    log("Archipelago Bridge Data available for game tick ".. game.tick .. ".") -- notifies client
end

script.on_event(defines.events.on_runtime_mod_setting_changed, function(event)
    local force
    if event.player_index == nil then
        force = game.forces.player
    else
        force = game.players[event.player_index].force
    end

    if event.setting == PARAMS.death_link_setting then
        if settings.global[PARAMS.death_link_setting].value then
            DEATH_LINK = 1
        else
            DEATH_LINK = 0
        end
        if force ~= nil then
            dumpInfo(force)
        end
    end
end)

-- Updates a player, attempting to send them any pending samples (if relevant)
local function update_player(index)
    local player = game.players[index]
    if not player or not player.valid then     -- Do nothing if we reference an invalid player somehow
        return
    end
    local character = player.character or player.cutscene_character
    if not character or not character.valid then
        return -- Might be dead
    end
    -- TODO: test when the character is riding in a space platform or cargo pod.
    local data = storage.playerdata[index]
    local samples = data["pending_samples"]
    --player.print(serpent.block(data["pending_samples"]))

    for name, count in pairs(samples) do
        local stack = {
            name = name,
            count = count,
        }
        if script.active_mods["quality"] then
            stack.quality = PARAMS.free_sample_quality
        end
        if prototypes.item[name] then
            local sent
            if character.can_insert(stack) then
                sent = character.insert(stack)
            else
                sent = 0
            end
            if sent > 0 then
                player.print("Received " .. sent .. "x [item=" .. name .. ",quality=" .. PARAMS.free_sample_quality .. "]")
                data.suppress_full_inventory_message = false
            end
            if sent ~= count then               -- Couldn't full send.
                if not data.suppress_full_inventory_message then
                    player.print("Additional items will be sent when inventory space is available.", {r=1, g=1, b=0.25})
                end
                data.suppress_full_inventory_message = true -- Avoid spamming them with repeated full inventory messages.
                samples[name] = count - sent    -- Buffer the remaining items
                break                           -- Stop trying to send other things
            else
                samples[name] = nil             -- Remove from the list
            end
        else
            player.print("Unable to receive " .. count .. "x [item=" .. name .. "] as this item does not exist.")
            samples[name] = nil
        end
    end

end

-- Initialize player data, either from them joining the game or them already being part of the game when the mod was
-- added.`
local function on_player_created(event)
    local player = game.players[event.player_index]
    -- FIXME: This (probably) fires before any other mod has a chance to change the player's force
    -- For now, they will (probably) always be on the 'player' force when this event fires.
    local data = {}
    data["pending_samples"] = table.deepcopy(storage.forcedata[player.force.name]["earned_samples"])
    storage.playerdata[player.index] = data
    update_player(player.index)  -- Attempt to send pending free samples, if relevant.
    dumpInfo(player.force)
end
script.on_event(defines.events.on_player_created, on_player_created)

script.on_event(defines.events.on_player_removed, function(event)
    storage.playerdata[event.player_index] = nil
end)

-- Goal checking
local function trigger_victory(force)
    if storage.forcedata[force.name]["victory"] == 0 then
        storage.forcedata[force.name]["victory"] = 1
        dumpInfo(force)
        game.set_game_state({
            game_finished = true,
            player_won = true,
            can_continue = true,
            victorious_force = force,
        })
    end
end
if PARAMS.goal == "solar_system_edge" or PARAMS.goal == "solar_system_edge_11_science" then
    script.on_event(defines.events.on_tick, function(event)
        local force = game.forces["player"]
        for _, platform in pairs(force.platforms) do
            if platform.last_visited_space_location ~= nil and platform.last_visited_space_location.name == "solar-system-edge" then
                trigger_victory(force)
            end
        end
    end)
elseif PARAMS.goal == "aquilo_orbit" or PARAMS.goal == "aquilo_orbit_10_science" then
    script.on_event(defines.events.on_tick, function(event)
        local force = game.forces["player"]
        for _, platform in pairs(force.platforms) do
            if platform.last_visited_space_location ~= nil and platform.last_visited_space_location.name == "aquilo" then
                trigger_victory(force)
            end
        end
    end)
elseif PARAMS.goal == "space_science" or PARAMS.goal == "any_other_planet_science" then
    -- Handled in ap-get-technology.
else
    error("unrecognized goal: " .. tostring(PARAMS.goal))
end

-- Update players upon them connecting, since updates while they're offline are suppressed.
script.on_event(defines.events.on_player_joined_game, function(event) update_player(event.player_index) end)

local function update_player_event(event)
    update_player(event.player_index)
end

script.on_event(defines.events.on_player_main_inventory_changed, update_player_event)

-- Update players when the cutscene is cancelled or finished.  (needed for skins_factored)
script.on_event(defines.events.on_cutscene_cancelled, update_player_event)
script.on_event(defines.events.on_cutscene_finished, update_player_event)

local function add_samples(force, name, count)
    local function add_to_table(t)
        if count <= 0 then
            -- Fixes a bug with single craft, if a recipe gives 0 of a given item.
            return
        end
        t[name] = (t[name] or 0) + count
    end
    -- Add to storage table of earned samples for future new players
    add_to_table(storage.forcedata[force.name]["earned_samples"])
    -- Add to existing players
    for _, player in pairs(force.players) do
        add_to_table(storage.playerdata[player.index]["pending_samples"])
        update_player(player.index)
    end
end

remote.add_interface("archipelago", {
    begin_suppress_death_link = function(player_index)
        CURRENTLY_DEATH_LOCK = 1
    end,
    end_suppress_death_link = function(player_index)
        CURRENTLY_DEATH_LOCK = 0
    end,
})
local function register_callbacks()
    -- Integrate with the respawn-to-any-planet mod.
    -- It should not send death links.
    if remote.interfaces["respawn-to-any-planet"] ~= nil then
        -- Callbacks across mods require going through the serialized remote interface interface.
        remote.call("respawn-to-any-planet", "on_pre_die",  "archipelago", "begin_suppress_death_link")
        remote.call("respawn-to-any-planet", "on_post_die", "archipelago", "end_suppress_death_link")
    end
end
script.on_init(function()
    set_permissions()
    storage.forcedata = {}
    storage.playerdata = {}
    storage.energy_link_bridges = {}
    -- Fire dummy events for all currently existing forces.
    local e = {}
    for name, _ in pairs(game.forces) do
        e.force = name
        on_force_created(e)
    end
    e.force = nil

    -- Fire dummy events for all currently existing players.
    for index, _ in pairs(game.players) do
        e.player_index = index
        on_player_created(e)
    end

    -- Disable the vanilla victory condition.
    if remote.interfaces["silo_script"] then
        remote.call("silo_script", "set_no_victory", true) -- base
    end
    if remote.interfaces["space_finish_script"] then
        remote.call("space_finish_script", "set_no_victory", true) -- space-age
    end

    register_callbacks()
end)
script.on_configuration_changed(function()
    -- As documented in the respawn-to-any-planet mod, we must re-register callbacks in this event.
    register_callbacks()
end)

-- hook into researches done
script.on_event(defines.events.on_research_finished, function(event)
    local technology = event.research
    if string.find(technology.force.name, "EE_TESTFORCE") == 1 then
        --Don't acknowledge AP research as an Editor Extensions test force
        --Also no need for free samples in the Editor extensions testing surfaces, as these testing surfaces
        --are worked on exclusively in editor mode.
        return
    end
    if technology.researched and is_ap_technology(technology.name) then
        -- Notify the server that we've unlocked an AP location.
        dumpInfo(technology.force)
        return
    end
    -- We've received an AP item, or this technology isn't randomized.
    if PARAMS.free_sample_amount == "none" then
        return  -- Nothing else to do.
    end
    if not technology.prototype.effects then
        return  -- No technology effects, so nothing to do.
    end
    for _, effect in pairs(technology.prototype.effects) do
        if effect.type == "unlock-recipe" then
            local recipe = prototypes.recipe[effect.recipe]
            for _, result in pairs(recipe.products) do
                if result.type == "item" and result.amount and PARAMS.free_sample_excludes[effect.recipe] ~= 1 then
                    local count
                    if PARAMS.free_sample_amount == "single_craft" then
                        count = result.amount
                    elseif PARAMS.free_sample_amount == "stack" then
                        count = get_any_stack_size(result.name)
                    elseif PARAMS.free_sample_amount == "half_stack" then
                        count = math.ceil(get_any_stack_size(result.name) / 2)
                    else
                        error("unrecognized free_sample_amount: " .. tostring(PARAMS.free_sample_amount))
                    end
                    add_samples(technology.force, result.name, count)
                end
            end
        end
    end
end)

local function chain_lookup(table, ...)
    for _, k in ipairs{...} do
        table = table[k]
        if not table then
            return nil
        end
    end
    return table
end

local function kill_players(force)
    CURRENTLY_DEATH_LOCK = 1
    local current_character = nil
    for _, player in ipairs(force.players) do
        current_character = player.character
        if current_character ~= nil then
            current_character.die()
        end
    end
    CURRENTLY_DEATH_LOCK = 0
end


script.on_event(defines.events.on_entity_died, function(event)
    local entity = event.entity
    if entity.name == "character" then
        if DEATH_LINK == 0 then
            return
        end
        if CURRENTLY_DEATH_LOCK == 1 then -- don't re-trigger on same event
            return
        end

        local force = event.entity.force
        storage.forcedata[force.name].death_link_tick = game.tick
        dumpInfo(force)
        kill_players(force)
    else
        on_energy_bridge_removed(entity)
    end
end)


-- add / commands
commands.add_command("ap-sync", "Used by the Archipelago client to get progress information", function(call)
    local force
    if call.player_index == nil then
        force = game.forces.player
    else
        force = game.players[call.player_index].force
    end
    local research_done = {}
    local forcedata = chain_lookup(storage, "forcedata", force.name)
    local data_collection = {
        ["research_done"] = research_done,
        ["victory"] = chain_lookup(forcedata, "victory"),
        ["death_link_tick"] = chain_lookup(forcedata, "death_link_tick"),
        ["death_link"] = DEATH_LINK,
        ["energy"] = chain_lookup(forcedata, "energy"),
        ["energy_bridges"] = chain_lookup(forcedata, "energy_bridges"),
        ["multiplayer"] = #game.players > 1,
    }

    for tech_name, tech in pairs(force.technologies) do
        if tech.researched and is_ap_technology(tech_name) then
            research_done[tech_name] = tech.researched
        end
    end
    rcon.print(helpers.table_to_json({["slot_name"] = PARAMS.slot_name, ["seed_name"] = PARAMS.seed_name, ["info"] = data_collection}))
end)

commands.add_command("ap-print", "Used by the Archipelago client to print messages", function (call)
    game.print(call.parameter)
end)

TRAP_TABLE = {
    ["Attack Trap"] = function ()
        game.surfaces["nauvis"].build_enemy_base(game.forces["player"].get_spawn_position(game.get_surface(1)), 25)
    end,
    ["Evolution Trap"] = function ()
        local new_factor = game.forces["enemy"].get_evolution_factor("nauvis") +
            (PARAMS.trap_evo_factor * (1 - game.forces["enemy"].get_evolution_factor("nauvis")))
        game.forces["enemy"].set_evolution_factor(new_factor, "nauvis")
        game.print({"", "New evolution factor:", new_factor})
    end,
    ["Teleport Trap"] = function()
        for _, player in ipairs(game.forces["player"].players) do
            if player.character then
                attempt_teleport_player(player, 1)
            end
        end
    end,
    ["Grenade Trap"] = function ()
        fire_entity_at_players("grenade", 0.1)
    end,
    ["Cluster Grenade Trap"] = function ()
        fire_entity_at_players("cluster-grenade", 0.1)
    end,
    ["Artillery Trap"] = function ()
        fire_entity_at_players("artillery-projectile", 1)
    end,
    ["Atomic Rocket Trap"] = function ()
        fire_entity_at_players("atomic-rocket", 0.1)
    end,
    ["Atomic Cliff Remover Trap"] = function ()
        local cliffs = game.surfaces["nauvis"].find_entities_filtered{type = "cliff"}

        if #cliffs > 0 then
            fire_entity_at_entities("atomic-rocket", {cliffs[math.random(#cliffs)]}, 0.1)
        end
    end,
    ["Inventory Spill Trap"] = function ()
        for _, player in ipairs(game.forces["player"].players) do
            spill_character_inventory(player.character)
        end
    end,
}

commands.add_command("ap-get-technology", "Grant a technology, used by the Archipelago Client.", function(call)
    if storage.index_sync == nil then
        storage.index_sync = {}
    end
    local force = game.forces["player"]
    if call.parameter == nil then
        game.print("ap-get-technology is only to be used by the Archipelago Factorio Client")
        return
    end
    chunks = split(call.parameter, "\t")
    local item_name = chunks[1]
    local index = chunks[2]
    local source = chunks[3] or "Archipelago"
    if index == nil then
        game.print("ap-get-technology is only to be used by the Archipelago Factorio Client")
        return
    end
    if index == -1 then -- for coop sync and restoring from an older savegame
        local tech = force.technologies[item_name]
        if tech.researched ~= true then
            game.print({"", "Received [technology=" .. tech.name .. "] as it is already checked."})
            game.play_sound({path="utility/research_completed"})
            tech.researched = true
        end
        return
    end
    if PARAMS.progressive_technology_stacks[item_name] ~= nil then
        if storage.index_sync[index] ~= item_name then -- not yet received prog item
            storage.index_sync[index] = item_name
            local tech_stack = PARAMS.progressive_technology_stacks[item_name]
            for _, tech_name in ipairs(tech_stack) do
                local tech = force.technologies[tech_name]
                if tech.researched ~= true then
                    game.print({"", "Received [technology=" .. tech.name .. "] from ", source})
                    game.play_sound({path="utility/research_completed"})
                    tech.researched = true
                    return
                end
            end
        end
        return
    end
    if PARAMS.infinite_technology_name_corrections[item_name] ~= nil then
        -- Infinite technology names include the level at the end of the name.
        -- e.g. "electric-weapons-damage-4_location" is at force.technologies["electric-weapons-damage-4_location-4"]
        item_name = PARAMS.infinite_technology_name_corrections[item_name]
    end
    if force.technologies[item_name] ~= nil then
        local tech = force.technologies[item_name]
        if tech ~= nil then
            storage.index_sync[index] = item_name
            if tech.researched ~= true then
                game.print({"", "Received [technology=" .. tech.name .. "] from ", source})
                game.play_sound({path="utility/research_completed"})
                tech.researched = true
            end
        end
    elseif TRAP_TABLE[item_name] ~= nil then
        if storage.index_sync[index] ~= item_name then -- not yet received trap
            storage.index_sync[index] = item_name
            game.print({"", "Received ", item_name, " from ", source})
            TRAP_TABLE[item_name]()
        end
    elseif item_name == "victory" then
        trigger_victory(force)
    else
        game.print("Unknown Item " .. item_name)
        log("DEBUG: Unknown Item " .. item_name)
    end
end)


commands.add_command("ap-rcon-info", "Used by the Archipelago client to get information", function(call)
    rcon.print(helpers.table_to_json({
        ["slot_name"] = PARAMS.slot_name,
        ["seed_name"] = PARAMS.seed_name,
        ["death_link"] = DEATH_LINK,
        ["energy_link"] = PARAMS.energy_link_increment,
    }))
end)

commands.add_command("ap-deathlink", "Kill all players", function(call)
    local force = game.forces["player"]
    local source = call.parameter or "Archipelago"
    kill_players(force)
    game.print("Death was granted by " .. source)
end)

commands.add_command("ap-energylink", "Used by the Archipelago client to manage Energy Link", function(call)
    local change = tonumber(call.parameter or "0")
    local force = "player"
    storage.forcedata[force].energy = storage.forcedata[force].energy + change
end)

commands.add_command("energy-link", "Print the status of the Archipelago energy link.", function(call)
    log("Player command energy-link") -- notifies client
end)

commands.add_command("toggle-ap-send-filter", "Toggle filtering of item sends that get displayed in-game to only those that involve you.", function(call)
    log("Player command toggle-ap-send-filter") -- notifies client
end)

commands.add_command("toggle-ap-connection-change-filter", "Toggle filtering of players joining or parting", function(call)
    log("Player command toggle-ap-connection-change-filter") -- notifies client
end)

commands.add_command("toggle-ap-chat", "Toggle sending of chat messages from players on the Factorio server to Archipelago.", function(call)
    log("Player command toggle-ap-chat") -- notifies client
end)
