# 📥 Detailed Installation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step-by-Step Installation](#step-by-step-installation)
3. [Verification](#verification)
4. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- Python 3.9 or higher - [Download](https://www.python.org/downloads/)
  - ✅ Check "Add Python to PATH" during install
- Mod Engine 2 - [Download](https://github.com/soulsmods/ModEngine2/releases)
- Seamless Co-op Mod - [Download](https://github.com/kal997/seamless-coop/releases)

### Game Setup
- Elden Ring (Latest patch)
- Modded installation (not required but recommended)

## Step-by-Step Installation

### Step 1: Download Cursed Sword Mod

Option A: Via Git (Recommended)
```bash
git clone https://github.com/YourUsername/Cursed-Sword-Mod.git
cd Cursed-Sword-Mod

Option B: Download ZIP

    Click green "Code" button
    Click "Download ZIP"
    Extract to desired location

Step 2: Organize Files

Navigate to your Elden Ring installation:

C:\Program Files\Steam\steamapps\common\ELDEN RING\Game

Create this folder structure:

Elden Ring/Game/
├── mods/
│   ├── seamless_coop/
│   │   └── (seamless coop files here)
│   │
│   └── CursedSword/
│       ├── mod.py
│       ├── regulation_patcher.py
│       ├── config.json
│       ├── keybind_config.json
│       ├── README.md
│       └── sounds/
│           ├── parry_success.wem
│           ├── stack_milestone_1.wem
│           ├── stack_milestone_5.wem
│           └── stack_milestone_10.wem

Step 3: Copy Mod Files

    Copy all files from downloaded mod to Elden Ring/mods/CursedSword/
    Create sounds/ subfolder (optional for audio)
    Verify all 5 main files are present:
        ✅ mod.py
        ✅ regulation_patcher.py
        ✅ config.json
        ✅ keybind_config.json
        ✅ README.md

Step 4: Patch regulation.bin
Backup Original

# Copy original to safety
cp Elden Ring/Game/regulation.bin Elden Ring/Game/regulation.bin.original

Run Patcher

    Open Command Prompt/PowerShell in Elden Ring/mods/CursedSword/ folder
        Windows: Shift + Right Click → "Open PowerShell window here"

    Run the patcher:

    python regulation_patcher.py

    Wait for output:

    [Regulation] ✓ Patching complete!
    [Regulation] ✓ All patches verified!
    ✓ All systems ready!

    Replace original regulation.bin:

    # Copy patched version back to game
    cp Elden Ring/mods/CursedSword/regulation.bin Elden Ring/Game/regulation.bin

Backup is automatically created as regulation.bin.backup
Step 5: Install Mod Engine 2

    Download Mod Engine 2: Latest Release

    Extract to Elden Ring directory root:

    Elden Ring/
    ├── Game/
    ├── mods/
    ├── modengine2.exe
    └── modengine2.ini

    Configure modengine2.ini:

    [General]
    enabled=1
    mod_folder=mods

    [Mod Order]
    mod_1=seamless_coop
    mod_2=CursedSword

Step 6: (Optional) Add Sound Files

Download or create .wem audio files and place in:

Elden Ring/mods/CursedSword/sounds/

Without sound files: Mod works fine, just no audio effects.
Step 7: Launch Game
Option A: Via Batch File (Easiest)

Create launch_elden_ring.bat in Elden Ring folder:

@echo off
modengine2.exe
pause

Double-click to launch.
Option B: Manual Command

cd C:\Program Files\Steam\steamapps\common\ELDEN_RING
modengine2.exe

Option C: Steam Shortcut

In Steam, add custom launch option:

"C:\Program Files\Steam\steamapps\common\ELDEN_RING\modengine2.exe"

Verification
Test Mod Functionality

    Launch game with modengine2

    Create new character (or use existing)

    Test parry input:
        Controller: Press Y + LT
        Keyboard: Press E
        Should swap to Hand of Malenia

    Parry an enemy:
        Should see stack counter appear
        Orange glow should activate
        Sound should play (if files added)
        Particles should burst

    Check console:

    toggle    # Should show mod toggle message
    stats     # Should show current stacks
    info      # Should show mod information

Expected Output

[CursedSword] Mod initialized v2.2!
[CursedSword] Keybinds loaded:
  Controller: Y + LT
  Keyboard: E
[CursedSword] Sound configuration loaded
✓ Mod initialized!

Troubleshooting
Python Not Found

Error: python: command not found

Solution:

    Install Python 3.9+: https://www.python.org/downloads/
    ✅ Check "Add Python to PATH"
    Restart Command Prompt
    Try again

File Not Found

Error: regulation.bin not found

Solution:

    Verify regulation.bin copied to mod folder
    Check file path is correct
    Use full path: python C:\path\to\regulation_patcher.py

JSON Error

Error: JSON decode error

Solution:

    Open config file in Notepad++
    Check for extra characters
    Verify all commas are correct
    Use online JSON validator: https://jsonlint.com

Mod Not Loading

Error: Mod doesn't appear in game

Solution:

    Verify Mod Engine 2 installed correctly
    Check both mods in modengine2.ini
    Restart Elden Ring completely
    Check console for error messages

Regulation.bin Patching Failed

Error: Patch verification failed

Solution:

    Restore from backup: regulation.bin.backup
    Delete old patched version
    Copy fresh regulation.bin from game
    Run patcher again with Administrator privileges

Keybinds Not Working

Error: Y+LT or E doesn't trigger parry

Solution:

    Verify syntax in keybind_config.json
    Check file is valid JSON
    Restart game (changes take effect on startup)
    Try default keybinds to isolate issue
    Controller/keyboard input detected correctly?

Sound Not Playing

Error: No audio on parry

Solution:

    Check sound files in sounds/ folder
    Verify sound enabled in config.json
    Check volume not set to 0
    Try different audio files
    Mod works fine without sounds

Uninstallation
Remove Mod

    Delete Elden Ring/mods/CursedSword/ folder
    Restore original regulation.bin:

    cp regulation.bin.backup regulation.bin

Clean Up

    Delete mod launcher shortcuts
    Remove modengine2 files (if not using other mods)

Installation complete! Enjoy the mod! 🎉

Need help? Check FAQ.md or open an Issue.
