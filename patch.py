from assembler import ASM
import backgroundEditor
import entityData
import random
import patches.core


def apply(rom):
    # Debug mode
    # rom.patch(0x00, 0x0003, "00", "01")

    # patches.core.warpHome(rom, 0xF7, 0x50, 0x50)

    # Change which tile the tail key opens
    rom.patch(0x02, 0x16A6, ASM("ld a, $60"), ASM("ld a, $50"))
    rom.patch(0x02, 0x16F0, ASM("ld hl, $D727"), ASM("ld hl, $D726"))
    rom.patch(0x02, 0x16F9, ASM("ld hl, $D727"), ASM("ld hl, $D726"))
    # Change the start location
    rom.patch(0x01, 0x13A3, ASM("ld a, $a3"), ASM("ld a, $f7"))
    rom.patch(0x01, 0x13AD, ASM("ld a, $01"), ASM("ld a, $00")) # Not indoor
    rom.patch(0x01, 0x13B2, ASM("ld a, $10"), ASM("ld a, $00")) # Map
    rom.patch(0x01, 0x13B6, ASM("ld a, $50"), ASM("ld a, $50")) # X
    rom.patch(0x01, 0x13BB, ASM("ld a, $60"), ASM("ld a, $50")) # Y
    rom.patch(0x01, 0x075E, ASM("ld a, $92"), ASM("ld a, $f7")) # Debug save start room

    # Set overworld warp X/Y
    rom.patch(0x19, 0x1DE1, ASM("ld a, $68"), ASM("ld a, $28")) # X
    rom.patch(0x19, 0x1DDA, ASM("ld a, $70"), ASM("ld a, $60")) # Y
    rom.patch(0x19, 0x1DEB, ASM("ld a, $66"), ASM("ld a, $52")) # XY tile position

    # Stop facade from spawning pots in the corners
    rom.patch(0x04, 0x133A, ASM("jr nz, $03"), "", fill_nop=True)
    
    # Make genie a bit more aggressive
    rom.patch(0x04, 0x0467, ASM("ld [hl], $24"), ASM("ld [hl], $28")) # throw the fireballs a bit furter
    rom.patch(0x04, 0x03F4, ASM("cp $08"), ASM("cp $10")) # amount of fireballs to throw
    rom.patch(0x04, 0x043D, ASM("ld [hl], $30"), ASM("ld [hl], $20")) # less delay between fireballs

    # Do not give lanmola the boss message and music
    rom.patch(0x06, 0x16CB, ASM("call $3EE8"), "", fill_nop=True)
    rom.patch(0x03, 0x09E3, ASM("ldh [$B0], a"), "", fill_nop=True)
    rom.patch(0x06, 0x15F9, ASM("ldh [$B0], a"), "", fill_nop=True)
    rom.patch(0x03, 0x02F1 + 0x87, "84", "04") # Remove the boss flag
    rom.patch(0x06, 0x1650, 0x167F, "", fill_nop=True) # Do not drop the key on lanmola kill

    # Change the background palettes of the new shops
    rom.banks[0x21][0x0585 + 0x9b] = rom.banks[0x21][0x0585 + 0xA1]
    rom.banks[0x21][0x0585 + 0x9c] = rom.banks[0x21][0x0585 + 0xA1]
    rom.banks[0x21][0x0585 + 0x9d] = rom.banks[0x21][0x0585 + 0xA1]
    rom.banks[0x21][0x0585 + 0x9e] = rom.banks[0x21][0x0585 + 0xA1]
    # Change the 2nd item shop price
    rom.patch(0x04, 0x37D3 + 5, "09", "03")
    rom.patch(0x04, 0x37DC + 5, "80", "00")
    rom.patch(0x04, 0x37E5 + 5, "03", "01")
    rom.patch(0x04, 0x37EE + 5, "D4", "2C")
    rom.patch(0x04, 0x3732 + 4 * 11 + 3, "B9B8B0", "B3B0B0")

    # Diggable seashells
    rom.patch(0x03, 0x220F, ASM("cp $DA"), ASM("cp $E3"))
    rom.patch(0x03, 0x2213, ASM("cp $A5"), ASM("cp $C6"))
    rom.patch(0x03, 0x2217, ASM("cp $74"), ASM("cp $E8"))
    rom.patch(0x03, 0x221B, ASM("cp $3A"), ASM("cp $DB"))
    rom.patch(0x03, 0x221F, ASM("cp $A8"), ASM("cp $00"))
    rom.patch(0x03, 0x2223, ASM("cp $B2"), ASM("cp $00"))
    # Bonk seashells
    rom.patch(0x03, 0x0F03, ASM("cp $A4"), ASM("cp $A8"))
    rom.patch(0x03, 0x0F07, ASM("cp $D2"), ASM("cp $D6"))
    # Seashell mansion
    rom.patch(0x19, 0x31EF, 0x31F4, "", fill_nop=True) # Do not show the "ultimate sword" message
    for n in range(0x29): # Fill the bar up correctly for the 10 seashells
        rom.banks[0x19][0x3193+n] = min(int(n * 96 / 10), 0x60)
    rom.patch(0x19, 0x32A5, ASM("cp $20"), ASM("cp $10")) # Only need 10 seashells

    # Outdoor swim heartpiece
    rom.patch(0x02, 0x1037, ASM("cp $78"), ASM("cp $df")) # room
    rom.patch(0x02, 0x1047, ASM("sub $58"), ASM("sub $78")) # X
    rom.patch(0x02, 0x103D, ASM("sub $50"), ASM("sub $60")) # Y

    # Stairs under rocks
    rom.patch(0x14, 0x1638, ASM("cp $52"), ASM("cp $EA"))
    rom.patch(0x14, 0x163C, ASM("cp $04"), ASM("cp $00"))

    # Racoon tarin changes
    rom.patch(0x05, 0x09B3, ASM("ldh a, [$99]"), ASM("ldh a, [$98]")) # X position instead of Y
    rom.patch(0x05, 0x09E8, ASM("ldh a, [$99]"), ASM("ldh a, [$98]")) # X position instead of Y
    rom.patch(0x02, 0x3A74, ASM("cp $02"), ASM("cp $01")) # Left instead of up
    rom.patch(0x02, 0x3A7D, ASM("ld a, $63\nld hl, $FFF6\njr $09"), ASM("jp $7d00"), fill_nop=True) # New target room
    rom.patch(0x02, 0x3D00, "00" * 0x20, ASM("""
        ; As we move into the same room, we need to modify the "entities current room" table to make sure entities unload
        ld hl, $C3E0
        ld a, $10
loop:
        inc [hl]
        inc hl
        dec a
        jr  nz, loop

        ld a,  $E1
        ld hl, $FFF6
        jp $7A8D
    """), fill_nop=True)

    # Do not let dive spots overrule warps set in the rooms
    rom.patch(0x19, 0x08AE, ASM("ldi [hl], a"), "00")

    # Ignore stealing from the shop
    rom.patch(0x00, 0x1874, ASM("jr z, $22"), ASM("jr $22"))

    # Set mambo's target
    rom.patch(0x14, 0x0E8F, ASM("ld a, $45"), ASM("ld a, $B9")) # Room
    rom.patch(0x14, 0x0E94, ASM("ld a, $38"), ASM("ld a, $58")) # X
    rom.patch(0x14, 0x0E9B, ASM("ld a, $60"), ASM("ld a, $70")) # Y
    rom.patch(0x14, 0x0EA2, ASM("ld a, $53"), ASM("ld a, $65")) # XY

    # Patch angler fish to open the right dungeon room after defeat
    rom.patch(0x03, 0x1A0F, ASM("ld hl, $D966"), ASM("ld hl, $D95A"))

    # Patch the eagle heart container to open up the right room.
    rom.patch(0x03, 0x1A04, ASM("ld hl, $DA2E"), ASM("ld hl, $D985"))
    rom.patch(0x02, 0x1FC8, ASM("cp $06"), ASM("cp $04"))

    # Update the color dungeon guardians
    rom.patch(0x36, 0x193F, 0x1B3F, ASM("""
    ldh  a, [$E7] ;framecount
    swap a
    and  $01
    call $3B0C ; set sprite variant
    ldh  a, [$EE] ; X
    cp   $50
    ld   de, spriteDataRed
    jr   c, red
    ld   de, spriteDataBlue
red:
    call $3BC0 ; RenderSpritePair
    call $6B5C ; Block player
    ret

spriteDataRed:
    db $40, $02, $42, $02
    db $42, $22, $40, $22
spriteDataBlue:
    db $40, $03, $42, $03
    db $42, $23, $40, $23
""", 0x593F), fill_nop=True)
    rom.patch(0x03, 0x0BEB, 0x0C01, ASM("""
    ; Check if we have a tunic
    ld   a, [$DC0F]
    and  a
    ret  nz
    ; Change X
    ld   hl, $C200
    add  hl, bc
    ld   a, $28
    ld   [hl], a
    ; Change Y
    ld   hl, $C210
    add  hl, bc
    ld   a, $10
    add  a, [hl]
    ld   [hl], a
    ret
""", 0x4BEB), fill_nop=True)
    rom.patch(0x03, 0x0C01, 0x0C1F, ASM("""
    ; Check if we have a tunic
    ld   a, [$DC0F]
    and  a
    ret  nz
    ; Change X
    ld   hl, $C200
    add  hl, bc
    ld   a, $78
    ld   [hl], a
    ; Change Y
    ld   hl, $C210
    add  hl, bc
    ld   a, $10
    add  a, [hl]
    ld   [hl], a
    ret
""", 0x4C01), fill_nop=True)

    # Color dungeon transition hacks (replaces face shrine hack)
    rom.patch(0x02, 0x3A50, 0x3A67, ASM("""
    ldh  a, [$F7] ; map
    inc  a
    jr   nz, noHack
    ; We are in the color dungeon.
    jp   $7D80
noHack:
    """), fill_nop=True)
    rom.patch(0x02, 0x3D80, "00" * 0x80, ASM("""
    ; special color dungeon handling
    ld   a, [$DBAE] ; indoor room
    cp   $34
    jr   z, backToStartRoom
    cp   $3A
    jr   z, entranceRoom
    cp   $22
    jr   z, wrapLeft
    cp   $24
    jr   z, wrapRight
back:
    jp   $7A67
backToStartRoom:
    ld   a, c
    cp   $03 ; if we are not down
    jr   nz, back
    ld   a, $32
    ld   [$DBAE], a
    jr   back
entranceRoom:
    ldh  a, [$98] ; player X
    cp   $50
    jr   c, back
    ld   a, $3C
    ld   [$DBAE], a
    jr   back
wrapLeft:
    ld   a, c
    cp   $01
    jr   nz, back
    ld   a, $25
    ld   [$DBAE], a
    jr   back
wrapRight:
    ld   a, c
    and  a
    jr   nz, back
    ld   a, $21
    ld   [$DBAE], a
    jr   back
    """, 0x7D80), fill_nop=True)

    # Update indoor marin to work correctly
    rom.patch(0x05, 0x0E75, ASM("jp nz, $51CE"), "", fill_nop=True) # always act as if outside
    entityData.SPRITE_DATA[0x3E] = (2, 0xE6) # Always outdoor sprites
    rom.patch(0x05, 0x0E7C, ASM("jp z, $7B4B"), "", fill_nop=True) # ignore sword level (which else hides marin)

    # Dungeon owl statues -> old man
    rom.banks[0x2E][0x11E0:0x1200] = rom.banks[0x2E][0x0500:0x0520]
    rom.patch(0x18, 0x1E9D, ASM("jr nz, $03"), ASM("jr $03")) # ignore stone beaks just give the hint
    hints = [ #room, message
        [(0x0C, 0x80)], #D1
        [(0x23, 0x81)], #D2
        [(0x4A, 0x82)], #D3
        [(0x65, 0x83)], #D4
        [(0x9E, 0x84), (0x87, 0x85)], #D5
        [(0xD6, 0x86), (0xCB, 0x87)], #D6
        [(0x08, 0x88)], #D7
        [(0x41, 0x89), (0x4D, 0x8A)], #D8
    ]
    for index, data in enumerate(hints):
        for offset, (room, message) in enumerate(data):
            rom.banks[0x36][0x09FC+index*3+offset] = message
            rom.banks[0x36][0x0A24+index*3+offset] = room

    # Do not have the ghost follow you after dungeon 4
    rom.patch(0x03, 0x1E1B, ASM("LD [$DB79], A"), "", fill_nop=True)
    # Do not show boss intro messages
    rom.patch(0x00, 0x3F45, ASM("jp $2385"), ASM("ret"), fill_nop=True)
    rom.patch(0x36, 0x153B, ASM("ret z"), "", fill_nop=True) # Fix giant buzz blob

    # Set all the dungeon minimaps to normal 8x8 maps, and adjust the entrance arrows
    arrow_offset = [3, 2, 3, 3, 6, 3, 1, 3]
    for n in range(8):
        rom.banks[0x01][0x0385 + n] = 0x00
        rom.banks[0x01][0x2DCA + n * 2] = 0x0B + arrow_offset[n]
        
        # Set the save&quit room
        rom.banks[0x14][0x0E41 + n] = 0x38 + arrow_offset[n]

    # Change the vertical bridge to horizontal bridge tiles
    rom.banks[0x2F][0x28C0:0x28D0] = rom.banks[0x2F][0x3CD0:0x3CE0]
    rom.banks[0x2F][0x28D0:0x28E0] = rom.banks[0x2F][0x3CD0:0x3CE0]
    rom.banks[0x2F][0x29C0:0x29D0] = rom.banks[0x2F][0x3DD0:0x3DE0]
    rom.banks[0x2F][0x29D0:0x29E0] = rom.banks[0x2F][0x3DD0:0x3DE0]
    rom.banks[0x2F][0x3AC0:0x3AD0] = rom.banks[0x2F][0x3CD0:0x3CE0]
    rom.banks[0x2F][0x3AD0:0x3AE0] = rom.banks[0x2F][0x3CD0:0x3CE0]
    rom.banks[0x2F][0x3BC0:0x3BD0] = rom.banks[0x2F][0x3DD0:0x3DE0]
    rom.banks[0x2F][0x3BD0:0x3BE0] = rom.banks[0x2F][0x3DD0:0x3DE0]

    # D7 Grumble Grumble...
    rom.patch(0x20, 0x0402, ASM("dw $4B2F"), ASM("dw $4F83"))
    rom.patch(0x06, 0x220E, 0x22B3, ASM("""
        ldh  a, [$F0] ; entity state
        and  a
        jr   nz, initialCheckDone
        call $3B12 ; increment entity state

        ldh  a, [$F8] ; room status
        and  $20
        jr   z, initialCheckDone
        call $0C60 ; trigger room event
        
initialCheckDone:
        ld   de, $604D
        call $3BC0 ; render sprite
        ldh  a, [$E7] ; frame count
        swap a
        and  $01
        call $3B0C ; set sprite variant

        call $641A ; block player

        call $645D ; check if talking to NPC
        ret  nc

        ldh  a, [$F8] ; room status
        and  $20
        jr   nz, roomDone

        ld   a, $6F
        call $2373 ; OpenDialogInTable1

        ld   a, [$DB40] ; trade sequence item
        and  a
        ret  z

        xor  a
        ld   [$DB40], a

        call $0C60 ; trigger room event
        ld   hl, $DA17 ; set the room done event flag
        set  5, [hl]
        ret

roomDone:
        ld   a, $6E
        jp   $2373 ; OpenDialogInTable1
    """, 0x620E), fill_nop=True)

    rom.patch(0x19, 0x1031, ASM("jp nz, $50C4"), "", fill_nop=True) # Do not give luigi the rooster after D7
    rom.patch(0x06, 0x2A98, 0x2AA6, ASM("""
        ld   a, $41
        jp   $2373 ; open dialog 141
    """), fill_nop=True) # Phonebooth
    
    # Map texts
    rom.banks[0x01][0x1959:0x1A59] = b'\x00' * 0x100    
    rom.banks[0x01][0x1959 + 0xB7] = 0x11 # Dungeons
    rom.banks[0x01][0x1959 + 0xBC] = 0x12
    rom.banks[0x01][0x1959 + 0xF4] = 0x13
    rom.banks[0x01][0x1959 + 0xC5] = 0x14
    rom.banks[0x01][0x1959 + 0x8B] = 0x15
    rom.banks[0x01][0x1959 + 0xA2] = 0x16
    rom.banks[0x01][0x1959 + 0xC2] = 0x17
    rom.banks[0x01][0x1959 + 0xED] = 0x18
    rom.banks[0x01][0x1959 + 0xE4] = 0x22 # Witch
    rom.banks[0x01][0x1959 + 0xAF] = 0x25 # Tracy
    rom.banks[0x01][0x1959 + 0x8A] = 0x37 # Seashell mansion

    # TODO: dungeon "exit" messages on instruments
    # TODO: old man hints
    # TODO: Various NPC dialogs on overworld

    # Fix egg bg attributes at 23:6400
    rom.patch(0x23, 0x2400, 0x2800, 
      "04040404" #00
      "04040404" #01
      "04040404" #02
      "04040404" #03
      "04040404" #04
      "03030303" #05
      "03030303" #06
      "03030303" #07
      "05040504" #08
      "04040505" #09
      "05050404" #0a
      "04040505" #0b
      "05050404" #0c
      "05050505" #0d
      "00000000" #0e
      "07070707" #0f
      "05030503" #10
      "03050305" #11
      "03030505" #12
      "05050303" #13
      "05030303" #14
      "03050303" #15
      "03030503" #16
      "03030305" #17
      "00000000" #18
      "00000000" #19
      "00000000" #1a
      "00000000" #1b
      "04040404" #1c
      "04040404" #1d
      "04040404" #1e
      "04040404" #1f
      "03030303" #20
      "04040404" #21
      "04040404" #22
      "04040404" #23
      "04040404" #24
      "04040404" #25
      "04040404" #26
      "04040404" #27
      "04040404" #28
      "04040404" #29
      "04040404" #2a
      "04040404" #2b
      "04040404" #2c
      "04030403" #2d
      "03040304" #2e
      "04030403" #2f
      "03040304" #30
      "04040303" #31
      "03030404" #32
      "04040303" #33
      "03030404" #34
      "04030403" #35
      "03040304" #36
      "04030403" #37
      "03040304" #38
      "04040303" #39
      "03030404" #3a
      "04040303" #3b
      "03030404" #3c
      "05050505" #3d
      "05050505" #3e
      "04040404" #3f
      "04040404" #40
      "04040404" #41
      "04040404" #42
      "04050405" #43
      "05040504" #44
      "04030403" #45
      "03040304" #46
      "04040404" #47
      "04040404" #48
      "04040404" #49
      "04040404" #4a
      "00000000" #4b
      "00000000" #4c
      "00000000" #4d
      "00000000" #4e
      "00000000" #4f
      "00000000" #50
      "00000000" #51
      "00000000" #52
      "00000000" #53
      "00000000" #54
      "00000000" #55
      "00000000" #56
      "00000000" #57
      "00000000" #58
      "00000000" #59
      "00000000" #5a
      "00000000" #5b
      "00000000" #5c
      "00000000" #5d
      "00000000" #5e
      "03030303" #5f
      "00000000" #60
      "00000000" #61
      "00000000" #62
      "00000000" #63
      "00000000" #64
      "00000000" #65
      "00000000" #66
      "00000000" #67
      "00000000" #68
      "00000000" #69
      "00000000" #6a
      "00000000" #6b
      "00000000" #6c
      "00000000" #6d
      "00000000" #6e
      "00000000" #6f
      "00000000" #70
      "00000000" #71
      "00000000" #72
      "00000000" #73
      "00000000" #74
      "00000000" #75
      "00000000" #76
      "00000000" #77
      "00000000" #78
      "00000000" #79
      "00000000" #7a
      "00000000" #7b
      "00000000" #7c
      "00000000" #7d
      "00000000" #7e
      "00000000" #7f
      "00000000" #80
      "00000000" #81
      "00000000" #82
      "00000000" #83
      "00000000" #84
      "00000000" #85
      "00000000" #86
      "00000000" #87
      "00000000" #88
      "00000000" #89
      "00000000" #8a
      "00000000" #8b
      "00000000" #8c
      "00000000" #8d
      "00000000" #8e
      "00000000" #8f
      "00000000" #90
      "00000000" #91
      "00000000" #92
      "00000000" #93
      "00000000" #94
      "00000000" #95
      "00000000" #96
      "00000000" #97
      "00000000" #98
      "00000000" #99
      "00000000" #9a
      "00000000" #9b
      "00000000" #9c
      "00000000" #9d
      "00000000" #9e
      "00000000" #9f
      "03230323" #a0
      "03230323" #a1
      "00000000" #a2
      "00000000" #a3
      "00000000" #a4
      "00000000" #a5
      "01010101" #a6
      "01010101" #a7
      "00000000" #a8
      "00000000" #a9
      "00000000" #aa
      "03030303" #ab
      "02020303" #ac
      "00000000" #ad
      "04040404" #ae
      "04040404" #af
      "04040404" #b0
      "00000000" #b1
      "00000000" #b2
      "00000000" #b3
      "00000000" #b4
      "00000000" #b5
      "00000000" #b6
      "00000000" #b7
      "00000000" #b8
      "00000000" #b9
      "00000000" #ba
      "00000000" #bb
      "00000000" #bc
      "00000000" #bd
      "00000000" #be
      "00000000" #bf
      "00000000" #c0
      "04000400" #c1
      "00040004" #c2
      "00000000" #c3
      "00000000" #c4
      "00000000" #c5
      "00000000" #c6
      "00000000" #c7
      "00000000" #c8
      "00000000" #c9
      "00000000" #ca
      "00000000" #cb
      "00000000" #cc
      "00000000" #cd
      "00000000" #ce
      "00000000" #cf
      "00000000" #d0
      "00000000" #d1
      "00000000" #d2
      "00000000" #d3
      "00000000" #d4
      "00000000" #d5
      "00000000" #d6
      "00000000" #d7
      "00000000" #d8
      "00000000" #d9
      "00000000" #da
      "00000000" #db
      "00000000" #dc
      "00000000" #dd
      "00000000" #de
      "00000000" #df
      "00000000" #e0
      "00000000" #e1
      "00000000" #e2
      "00000000" #e3
      "00000000" #e4
      "00000000" #e5
      "00000000" #e6
      "05050505" #e7
      "05050505" #e8
      "05050505" #e9
      "05050505" #ea
      "00000000" #eb
      "00000000" #ec
      "00000000" #ed
      "00000000" #ee
      "00000000" #ef
      "00000000" #f0
      "00000000" #f1
      "00000000" #f2
      "00000000" #f3
      "00000000" #f4
      "00000000" #f5
      "00000000" #f6
      "00000000" #f7
      "00000000" #f8
      "00000000" #f9
      "00000000" #fa
      "00000000" #fb
      "00000000" #fc
      "00000000" #fd
      "00000000" #fe
      "00000000" #ff
    )