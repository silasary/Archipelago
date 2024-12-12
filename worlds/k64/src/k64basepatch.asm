//; Base Patch for Kirby 64 - The Crystal Shards Archipelago
.n64

.open "Kirby 64 - The Crystal Shards (USA).z64", "K64Basepatch.z64", 0x0

//; NOP CRC checks
.org 0x63C
nop

.org 0x648
nop

.headersize 0x8009B540 - 0x43790 //;ovl1

.org 0x800A28A8
OpenNewWorld:
li      at, LevelStart
addu    at, at, t7
lb      s2, 0x0000 (at)
sb      s2, 0x0007 (s6)
jr      ra

.org 0x800A3B1C
jal     RedirectStage
nop

.org 0x800A3CC0
nop

.org 0x800A3CD4
nop

.org 0x800A3E0C
jal     AllowFinalBoss
nop

.org 0x800A3E30
lw      t5, 0x6C78 (t5)
addiu   at, r0, 0x0001
addiu   a0, r0, 0x000D
bne     t5, at, 0x800A3F4C

.org 0x800A3CE8
jal     PreventBossAccess

.org 0x800A3D80
sw      s2, 0x6B7C (at)
jal     OpenNewWorld
nop

.org 0x800A3EFC
jal     SetZeroTwoComplete
nop

.org 0x800B8C94
jal     SetStartingStage

.org 0x800B9568
j       MarkStagesIncomplete
nop

.headersize 0x800f61a0 - 0x7ec10 //; ovl2

//; Block Copy Abilities and Power Combos when flag isn't set
.org 0x80127490
.db "ARCHIPELAGO_DATA"
// Starting Stage for Levels
LevelStart:
.db 0x00, 0x03, 0x04, 0x04, 0x04, 0x04, 0x03, 0x01
CrystalRequirements:
// Placeholder values for crystal requirements
.db 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0xFF, 0xFF
SlotData:
.fill 16
LevelIndex:
//; Level Order
.dw 0, 0, 0, 0, -1, -1, -1, -1
.dw 1, 1, 1, 1, 1, -1, -1, -1
.dw 2, 2, 2, 2, 2, -1, -1, -1
.dw 3, 3, 3, 3, 3, -1, -1, -1
.dw 4, 4, 4, 4, 4, -1, -1, -1
.dw 5, 5, 5, 5, -1, -1, -1, -1
StageIndex:
//; Stage Order
.dw 0, 1, 2, 3, -1, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, -1, -1, -1, -1
CopyAbilityBlocker:
lui     at, 0x800D
ld      t0, 0x6C68 (at) //; Get Copy Ability Flag dw
addiu   t7, r0, 0x0001
addiu   t2, v0, -0x0001
dsllv    t7, t7, t2      //; Shift current ability to match
and     t0, t0, t7
bnez    t0, @@ReturnToSwallow //; we are allowed to use the ability
nop
addiu   v0, r0, 0x0000
addiu   a0, r0, 0x0000
lui     at, 0x8013
sw      v0, 0xE850 (at)
@@ReturnToSwallow:
j       0x8012310C
nop

SetStartingStage:
addiu   a2, r0, 0x0003
sw      a2, 0x0014 (a3)
addiu   a2, r0, 0x0001
jr      ra
nop

PreventBossAccess:
lui     t2, 0x800D
addiu   t3, r0, 0x0002
addiu   t1, v1, -0x0001
addiu   t6, r0, 0x0006
mult    t0, t6
mflo    t6
addu    t2, t2, t6
addu    t2, t2, t1
sb      t3, 0x6BE0 (t2)
lw      t3, 0x6B90 (at)
addiu   t3, t3, -0x0001
lw      t1, 0x6C70 (at)
li      t2, CrystalRequirements
addu    t2, t2, t3
lb      t3, 0x0000 (t2)
sub     t3, t1, t3
bgez    t3, @@HasCrystals
nop
addiu   t2, v0, 0x0000
beql    t2, t2, @@ReturnToStageClear
nop
@@HasCrystals:
addiu   t2, v0, 0x0001
@@ReturnToStageClear:
li      t1, SlotData
lb      t3, 0x0002 (t1)
blez    t3, @@SkipFast
li      t1, CrystalRequirements
lb      t3, 0x0005 (t1)
lw      t1, 0x6C70 (at)
sub     t3, t1, t3
bltz    t3, @@SkipFast
nop
addiu   t3, v0, 0x0064
sw      t3, 0x6C78 (at)
@@SkipFast:
j       0x800B9C50
sw      t2, 0x6B94 (at)

MarkStagesIncomplete:
//; a2 - unlocked level, t3 - save address, t0 free
//; quickly unlock boss if crystal requirement is met
addiu   t0, a2, -0x0001
li      t2, CrystalRequirements
addu    t2, t2, t0
lb      t2, 0x0000 (t2)
lw      t0, 0x0090 (t3)
sub     t0, t0, t2
bltz    t0, @@BeginIncomplete
lw      t2, -0x0050 (t3)
li      t0, LevelStart
addu    t0, t0, t2
lb      t2, 0x0000 (t0)
lw      t0, -0x004C (t3)
sub     t0, t0, t2
bgtz    t0, @@BeginIncomplete
lw      t0, -0x004C (t3)
addiu   t0, t0, 0x0001
sw      t0, -0x004C (t3)
addiu   t2, r0, 0x0058
lw      t0, -0x0058 (t3)
mult    t0, t2
mflo    t2
li      t0, 0x800EC9F8
addu    t2, t2, t0
lw      t0, -0x004C (t3)
sw      t0, 0x0014 (t2)

@@BeginIncomplete:
addiu   s0, r0, 0x0001
addiu   t2, r0, 0x0006
addiu   t0, r0, 0x0000
@@MarkIncomplete:
addiu   t7, r0, 0x0000
addiu   t0, t0, 0x0001
beql    t0, a2, @@MarkIndividualStages
nop
@@MarkLevel:
beq     t7, t2, @@MarkIncomplete
lb      t6, 0x0000 (t3)
addiu   t7, t7, 0x0001
bnez    t6, @@IncrementStage
nop
sb      s0, 0x0000(t3)
@@IncrementStage:
b       @@MarkLevel
addiu   t3, t3, 0x0001
@@MarkIndividualStages:
lui     at, 0x800D
lw      t2, 0x6B94 (at)
@@MarkIndividualStage:
beq     t7, t2, @@Return
lb      t6, 0x0000 (t3)
addiu   t7, t7, 0x0001
bnez   t6, @@IncrementIndividualStage
nop
sb      s0, 0x0000(t3)
@@IncrementIndividualStage:
b       @@MarkIndividualStage
addiu   t3, t3, 0x0001
@@Return:
lw      s1, 0x000C (sp)
lw      s0, 0x0008 (sp)
jr      ra
addiu   sp, sp, 0x10

AllowFinalBoss:
li      s2, 0x0001
lui     at, 0x800D
sw      s2, 0x6B94 (at)
sw      s2, 0x6C78 (at)
jr      ra
nop

RedirectStage:
lw      t5, 0xE500 (at)
sll     t5, 5
sll     t3, 2
addu    t5, t5, t3
li      t3, LevelIndex
addu    t5, t5, t3
lw      t3, 0x0000 (t5)
lw      t5, 0x00C0 (t5)
sw      t3, 0xE500 (at)
sw      t5, 0xE504 (at)
addiu   t5, r0, 0x000F
jr      ra
sw      t3, 0x0000 (v0)

DeathLink:
lui     at, 0x800D
lw      t0, 0x6C7C (at)
blez    t0, @@CheckCollision
sw      r0, 0x6C7C (at)
jr      ra
addiu   v0, r0, 0x01
@@CheckCollision:
j       0x8010474C
nop

RemapStage:
//; assume level/stage is in a0/a1, add output to t8

sll     t5, a0, 5
sll     t6, a1, 2
addu    t5, t5, t6
li      t6, LevelIndex
addu    t6, t5, t6
lw      t6, 0x0000 (t6)
li      t7, StageIndex
addu    t7, t5, t7
lw      t7, 0x0000 (t7)
sll     t6, t6, 2
addu    t7, t6, t7
addu    t8, t7, t8
j       0x801532A4
nop

SetZeroTwoComplete:
addiu   t3, r0, 0x0001
lui     at, 0x800D
sb      t3, 0x6BC0 (at)
j       0x800A74D8
nop


.org 0x8011E1BC //; write our jump
jal     CopyAbilityBlocker

.org 0x80121354
jal     DeathLink

.headersize 0x80151100 - 0xF8630 //; ovl3

.org 0x8015329C
j       RemapStage
lui     t8, 0x800D

//; Give access to Dark Star only when flag is set
.org 0x80158760
b       0x80158770

.org 0x80158770
addiu   t6, r0, 0x0001 //; force 1 for miracle matter check

.org 0x80158788
nop
nop
nop
nop                     //; remove percentage check
lui     t6, 0x800D
lw      t7, 0x6B90 (t6)
lw      v0, 0x6C78 (t6) //; read from save area for cutscene check
addiu   a0, r0, 0x000D
bnez    v0, 0x801587BC

.headersize 0x801D0C60 - 0x174740 //; ovl8

.org 0x801D2C60
b       0x801D2CD4 //; always spawn a crystal shard for friend miniboss

.notice "Crystal Requirements: " + orga(CrystalRequirements)
.notice "Slot Data: " + orga(SlotData)
.notice "Level Index: " + orga(LevelIndex)
.notice "Stage Index: " + orga(StageIndex) 

.close