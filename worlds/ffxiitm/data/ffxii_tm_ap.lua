--TABLE DEFINITIONS
function define_location_ids()
    location_ids = {450011,
                    450012,
                    450021,
                    450022,
                    450031,
                    450032,
                    450041,
                    450042,
                    450051,
                    450052,
                    450061,
                    450062,
                    450071,
                    450072,
                    450081,
                    450082,
                    450091,
                    450092,
                    450101,
                    450102,
                    450111,
                    450112,
                    450121,
                    450122,
                    450131,
                    450132,
                    450141,
                    450142,
                    450151,
                    450152,
                    450161,
                    450162,
                    450171,
                    450172,
                    450181,
                    450182,
                    450191,
                    450192,
                    450201,
                    450202,
                    450211,
                    450212,
                    450221,
                    450222,
                    450231,
                    450232,
                    450241,
                    450242,
                    450251,
                    450252,
                    450261,
                    450262,
                    450271,
                    450272,
                    450281,
                    450282,
                    450291,
                    450292,
                    450301,
                    450302,
                    450303,
                    450311,
                    450312,
                    450313,
                    450314,
                    450315,
                    450321,
                    450322,
                    450323,
                    450331,
                    450332,
                    450341,
                    450342,
                    450351,
                    450352,
                    450353,
                    450354,
                    450361,
                    450362,
                    450363,
                    450371,
                    450372,
                    450381,
                    450382,
                    450391,
                    450392,
                    450401,
                    450402,
                    450411,
                    450412,
                    450421,
                    450422,
                    450431,
                    450432,
                    450441,
                    450442,
                    450451,
                    450452,
                    450461,
                    450462,
                    450471,
                    450472,
                    450481,
                    450482,
                    450491,
                    450492,
                    450501,
                    450502,
                    450511,
                    450512,
                    450521,
                    450522,
                    450531,
                    450532,
                    450541,
                    450542,
                    450551,
                    450552,
                    450561,
                    450562,
                    450571,
                    450572,
                    450581,
                    450582,
                    450591,
                    450592,
                    450601,
                    450602,
                    450611,
                    450612,
                    450621,
                    450622,
                    450623,
                    450624,
                    450631,
                    450632,
                    450641,
                    450642,
                    450651,
                    450652,
                    450661,
                    450662,
                    450671,
                    450672,
                    450681,
                    450682,
                    450691,
                    450692,
                    450701,
                    450702,
                    450711,
                    450712,
                    450721,
                    450722,
                    450731,
                    450732,
                    450741,
                    450742,
                    450751,
                    450752,
                    450761,
                    450762,
                    450771,
                    450772,
                    450781,
                    450782,
                    450791,
                    450792,
                    450801,
                    450802,
                    450811,
                    450812,
                    450821,
                    450822,
                    450823,
                    450831,
                    450832,
                    450833,
                    450841,
                    450842,
                    450843,
                    450851,
                    450852,
                    450853,
                    450861,
                    450862,
                    450863,
                    450871,
                    450872,
                    450873,
                    450874,
                    450881,
                    450882,
                    450883,
                    450891,
                    450892,
                    450901,
                    450902,
                    450911,
                    450912,
                    450913,
                    450914,
                    450921,
                    450922,
                    450923,
                    450931,
                    450932,
                    450941,
                    450942,
                    450943,
                    450951,
                    450961,
                    450962,
                    450971,
                    450972,
                    450973,
                    450974,
                    450991,
                    451001,
                    451002,
                    451003}
    return location_ids
end

location_ids = define_location_ids()


--FUNCTION DEFINITIONS
function file_exists(name)
   local f=io.open(name,"r")
   if f~=nil then io.close(f) return true else return false end
end

function create_client_communcation_path(path)
    ok, err, code = os.rename(path, path)
    exists = true
    if not ok and code ~= 13 then
        exists = false
    end
    if not exists then
        os.execute("mkdir " .. path)
    end
end

function create_empty_file(path, filename)
    file = io.open(path .. filename, "w")
    io.output(file)
    io.write("")
    io.close(file)
end

function define_add_item()
    argMem = memory.allocExe(0x0100)
    memory.registerSymbol("test_args", argMem)
    assembly =
    [[
    test_code:
      sub rsp,0x28
      lea rax,[%test_args%]

      movzx ecx,word ptr [rax]
      movsx edx,byte ptr [rax+0x02]
      xor r8d,r8d
      lea r9d,[r8+0x01]

      xor eax,eax
      test edx,edx
      cmovns eax,r9d
      mov [rsp+0x20],eax

      call 0x003008A0
      add rsp,0x28
      ret
    ]]

    memory.assemble(assembly, {"test_code"})
end

function add_item(arg1,arg2)
    argBase = memory.getSymbol("test_args")
    memory.u16[argBase] = arg1
    memory.s8[argBase+2] = arg2
    memory.execute("test_code")
end

function define_heal_all()
    healArgMem = memory.allocExe(0x0100)
    memory.registerSymbol("heal_args", argMem)
    assembly = [[
heal_code:
  push rbx
  sub rsp,0x20
  lea rbx,[%test_args%]

  mov edx,[rbx]
  call 0x0030F4B0

  add rsp,0x20
  pop rbx
  ret
]]
    memory.assemble(assembly, {"heal_code"})
end

function onMapJump(mapNumber, mapEntry)
    heal_all()

    file = io.open(client_communication_path .. "current_map", "w")
    io.output(file)
    io.write(tostring(mapNumber) .. "\n" .. tostring(mapEntry))
    io.close(file)
end

function heal_all()
    argBase = memory.getSymbol("heal_args")
    memory.u32[argBase] = 29  -- 0b11101 (Everything but MP/Mist)
    memory.execute("heal_code")
end

function get_u8(byte_table, index)
    index = (index*2) - 1
    return (byte_table[index] + (256*byte_table[index+1]))
end

function receive_items()
    byte_array = memory.readArray(ap_voucher_qty_address, (5*2))
    ap_voucher_qty = {get_u8(byte_array, 1), get_u8(byte_array, 2), get_u8(byte_array, 3), get_u8(byte_array, 4), get_u8(byte_array, 5)}
    check_num = ap_voucher_qty[1] + ap_voucher_qty[2] + ap_voucher_qty[3] + ap_voucher_qty[4] + ap_voucher_qty[5] + 1
    while file_exists(client_communication_path .. "AP_" .. tostring(check_num) .. ".item") do
        file = io.open(client_communication_path .. "AP_" .. tostring(check_num) .. ".item", "r")
        io.input(file)
        received_item_id = tonumber(io.read())
        io.close(file)
        received_item_id = received_item_id % 4400000
        if ap_voucher_qty[1] < 99 then
            add_item(ap_voucher_item_id,1)
             ap_voucher_qty[1] = ap_voucher_qty[1] + 1
            check_num = check_num + 1
        elseif ap_voucher_qty[1] >= 99 and ap_voucher_qty[2] < 99 then
            add_item(ap_voucher_item_id+1,1)
            ap_voucher_qty[2] = ap_voucher_qty[2] + 1
            check_num = check_num + 1
        elseif ap_voucher_qty[2] >= 99 and ap_voucher_qty[3] < 99 then
            add_item(ap_voucher_item_id+2,1)
            ap_voucher_qty[3] = ap_voucher_qty[3] + 1
            check_num = check_num + 1
        elseif ap_voucher_qty[3] >= 99 and ap_voucher_qty[4] < 99 then
            add_item(ap_voucher_item_id+3,1)
            ap_voucher_qty[4] = ap_voucher_qty[4] + 1
            check_num = check_num + 1
        elseif ap_voucher_qty[4] >= 99 and ap_voucher_qty[5] < 99 then
            add_item(ap_voucher_item_id+4,1)
            ap_voucher_qty[5] = ap_voucher_qty[5] + 1
            check_num = check_num + 1
        else
            print("No more AP vouchers can be received, failed at " .. tostring(check_num) .. ".item")
            break
        end
        if received_item_id >= 49200 then
            -- add_guest(received_item_id % 49200,1)
        else
            add_item(received_item_id,1)
        end
    end
end

function send_items()
    i = 1
    byte_array = memory.readArray(chest_item_id_address, ((#location_ids+1)*2))
    while i <= #location_ids+1 do
        if get_u8(byte_array, i) > 0 then
            if i <= #location_ids then
                if not file_exists(client_communication_path .. "send" .. tostring(location_ids[i])) then
                    file = io.open(client_communication_path .. "send" .. tostring(location_ids[i]), "w")
                    io.output(file)
                    io.write("")
                    io.close(file)
                end
                if not file_exists(client_communication_path .. "send" .. tostring(location_ids[i] + 5)) then
                    file = io.open(client_communication_path .. "send" .. tostring(location_ids[i] + 5), "w")
                    io.output(file)
                    io.write("")
                    io.close(file)
                end

            else
                if not file_exists(client_communication_path .. "victory") then
                    file = io.open(client_communication_path .. "victory", "w")
                    io.output(file)
                    io.write("")
                    io.close(file)
                end
            end
        end
        i = i + 1
    end
end

function check_keys()
    if input.getKeyPressed(input.key.KEY_F11) then --Jump to save/store
        if (memory.s8[0x215F1AE] ~= 0) then
            call.mapJump(53, 0, 2)
        end
    end
    if input.getKeyPressed(input.key.KEY_F1) then --Jump to level 1
        if (memory.s8[0x215F1AE] ~= 0) then
            call.mapJump(1155, 0, 2)
        end
    end
    if input.getKeyPressed(input.key.KEY_F10) then --Jump to previous map
        if (memory.s8[0x215F1AE] ~= 0) then
            call.mapJump(call.getPreviousMap(), 0, 2)
        end
    end
    if input.getKeyPressed(input.key.KEY_F9) then -- test
        if (memory.s8[0x215F1AE] ~= 0) then
            call.mapJump(1155, 1, 2)
        end
    end
    
end

--INITIALIZATIONS
client_communication_path = os.getenv('LOCALAPPDATA') .. "\\FFXIITM\\"
ap_voucher_item_id = 8472
ap_voucher_qty_address = 0x021B764C
chest_item_id_address = 0x021B765E
chest_item_id_base = 8481
lightworks_story_progress_address = 0x02164E41
current_map_address = 0x20441F0
create_client_communcation_path(client_communication_path)
define_add_item()
define_heal_all()

function main_loop()
    memory.u8[lightworks_story_progress_address] = 0
    receive_items()
    send_items()
    check_keys()
    event.executeAfterMs(5000, main_loop)
end

function debug()
    x = memory.readArray(ap_voucher_qty_address, 6)
    for k,v in pairs(x) do
        print("Key: " .. tostring(k))
        print("Value: " .. tostring(v))
    end
    print("APV1 QTY: " .. tostring(x[2]*256 + x[1]))
    print("APV2 QTY: " .. tostring(x[4]*256 + x[3]))
    print("APV3 QTY: " .. tostring(x[6]*256 + x[5]))
    check_keys()
    event.executeAfterMs(5000, debug)
end

print("FFXIV Trial Mode AP v0.0.4")

-- event.registerEventAsync("onInitDone", debug)
event.registerEventAsync("onInitDone", main_loop)
event.registerEventAsync("onMapJump", onMapJump)
