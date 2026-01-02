# 🔧 Troubleshooting Guide

## Issue 1: Parry Not Triggering

Problem:
- Y+LT or E doesn't work
- Weapon doesn't swap

Fix:
1. Make sure you press BOTH buttons at same time (Y AND LT together)
2. Not one after another - at the SAME TIME
3. Restart game
4. Try default keybinds first

---

## Issue 2: Sound Not Playing

Problem:
- No sound when you parry
- Game is silent

Fix:
1. Check config.json has `"enabled": true`
2. Check sounds folder has the .wem files
3. Mod works without sounds - this is OK
4. Try reducing volume and pitch in config

---

## Issue 3: Particles Not Showing

Problem:
- No visual burst on parry
- Screen is plain

Fix:
1. Check config.json - particles enabled?
2. Check if your FPS is too low
3. Try different camera angle
4. Particles disappear after 1.5 seconds (normal)

---

## Issue 4: Stack Counter Missing

Problem:
- Don't see [X/10] on screen
- No stack display

Fix:
1. Stack counter only shows after SUCCESSFUL parry
2. Make sure parry actually hit the enemy
3. Check config.json `"ui_counter": "enabled": true`
4. Counter hides after 15 seconds (normal)

---

## Issue 5: Game Crashes on Start

Problem:
- Game won't launch with mod
- Crashes immediately

Fix:
1. Check all JSON files for typos
2. Use https://jsonlint.com to validate
3. Restore backup: regulation.bin.backup
4. Run patcher again
5. Make sure Python 3.9+ installed

---

## Issue 6: Keybinds Not Working

Problem:
- Changed keybind_config.json but still old keys
- New keybinds don't work

Fix:
1. Restart game COMPLETELY (not reload)
2. Check JSON syntax is correct
3. Verify buttons are valid (Y, LT, E, Q, etc)
4. Try default first to test

---

## Issue 7: Mod Not Loading

Problem:
- Mod doesn't work in game
- No parry system

Fix:
1. Check ModEngine 2 installed
2. Check mod folder in correct place
3. Check both mods listed in modengine2.ini
4. Restart everything

---

## Console Commands

```bash
toggle    # Turn mod on/off
stats     # Show current stacks
reset     # Clear stacks
info      # Show mod info
