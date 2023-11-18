// Base Patch for Kirby 64 - The Crystal Shards Archipelago
.n64

.open "Kirby 64 - The Crystal Shards (USA).z64", "K64Basepatch.z64", 0x0

// NOP CRC checks
.org 0x63C
nop

.org 0x648
nop

.headersize 0x8009B540 - 0x43790 //ovl1

.org 0x800A28A8
OpenNewWorld:
lui     at, 0xB200
addu    at, at, t7
lb      s2, 0xF000 (at)
sb      s2, 0x0007 (s6)
jr      ra

.org 0x800A3CC0
nop

.org 0x800A3CD4
nop

.org 0x800A3E0C
jal     AllowFinalBoss
nop

.org 0x800A3E30
lw      t5, 0x6C64 (t5)
addiu   at, r0, 0x0001
addiu   a0, r0, 0x000D
bne     t5, at, 0x800A3F4C

.org 0x800A3CE8
jal     PreventBossAccess

.org 0x800A3D80
sw      s2, 0x6B7C (at)
jal     OpenNewWorld
nop

.org 0x800B8C94
jal     SetStartingStage

.org 0x800B9568
j       MarkStagesIncomplete
nop

.headersize 0x800f61a0 - 0x7ec10 // ovl2

// Block Copy Abilities and Power Combos when flag isn't set
.org 0x80127490
CopyAbilityBlocker:
lui     at, 0x800D
ld      t0, 0x6C68 (at) // Get Copy Ability Flag dw
addiu   t7, r0, 0x0001
addiu   t2, v0, -0x0001
sllv    t7, t7, t2      // Shift current ability to match
and     t0, t0, t7
bnez    t0, @@ReturnToSwallow // we are allowed to use the ability
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
lw      t1, 0x6C70 (at)
lui     t2, 0xB200
addu    t2, t2, t0
lb      t3, 0xF100 (t2)
sub     t3, t1, t3
bgez    t3, @@HasCrystals
nop
addiu   t2, v0, 0x0000
beql    t2, t2, @@ReturnToStageClear
nop
@@HasCrystals:
addiu   t2, v0, 0x0001
@@ReturnToStageClear:
j       0x800B9C50
sw      t2, 0x6B94 (at)
MarkStagesIncomplete:
// a2 - unlocked level, t3 - save address, t0 free
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
bnez   t6, @@IncrementStage
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
lui     at, 0x800D
sw      s2, 0x6B94 (at)
sw      s2, 0x6C64 (at)
jr      ra


.org 0x8011E1BC // write our jump
jal     CopyAbilityBlocker

.headersize 0x80151100 - 0xF8630 // ovl3

// Give access to Dark Star only when flag is set
.org 0x80158760
b       0x80158770

.org 0x80158770
addiu   t6, r0, 0x0001 // force 1 for miracle matter check

.org 0x80158788
nop
nop
nop
nop                     // remove percentage check
lui     t6, 0x800D
lw      t7, 0x6B90 (t6)
lw      v0, 0x6C64 (t6) // read from save area for cutscene check
addiu   a0, r0, 0x000D
bnez    v0, 0x801587BC


// Set Constants
.headersize 0xB0000000
.org 0xB1FFF000
// Starting Stage for Levels
.db 0x00, 0x03, 0x04, 0x04, 0x04, 0x04, 0x03, 0x01
.org 0xB1FFF100
// Placeholder values for crystal requirements
.db 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07
.close