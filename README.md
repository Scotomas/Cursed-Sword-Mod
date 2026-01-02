# 🗡️ Cursed Sword - Elden Ring Auto-Parry Mod v2.2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Elden Ring](https://img.shields.io/badge/Elden%20Ring-Latest%20Patch-success.svg)]()
[![Mod Engine 2](https://img.shields.io/badge/Mod%20Engine-2-orange.svg)]()

> Auto-parry Hand of Malenia with stacking buffs, sound effects, particle effects, and custom keybinds. Full Seamless Co-op multiplayer support.

## ✨ Features

### Core Mechanics
- 🎯 Auto-Parry System - Press Y+LT (or E) to instantly swap to Hand of Malenia and parry
- 📈 Stacking Buff System - Buffs increase with each successful parry (max 10 stacks)
- ⏱️ Buff Duration Resets - 15-second timer resets on every parry (keeps buffs active!)
- 🟠 Orange Glow Effect - Weapon glows orange, intensity scales with stacks (disappears when buff expires)
- 📍 Status Icon Counter - Stack counter displays with other buff effects for clean UI

### Effects & Customization
- 🎵 Sound Effects - Base parry sound + milestone sounds (1st, 5th, 10th stack)
- ✨ Particle Effects - Visual bursts around player on parry, scales with stacks
- ⚙️ Custom Keybinds - Edit `keybind_config.json` to remap inputs without code changes
- 👤 Per-Player Toggle - Each player can disable mod independently without affecting co-op

### Multiplayer
- 🎮 Seamless Co-op - Full multiplayer support (Host, Summons, Invaders)
- 🔄 Network Sync - All parry events, sounds, and particles sync across co-op
- 🌍 PvE & PvP - Works in all game modes
- 🎪 All Enemies - Use parry on humanoids, bosses, all enemy types

### Balance
- ⚖️ Balanced Scaling - Max 3% damage, 5% stamina, 2% stance break
- 🎯 Stack Cap at 10 - Prevents power creep, creates progression goal
- 🛡️ Accessible - Available to all character builds, any weapons

## 📊 Buff Scaling

| Stack | Physical Damage | Stamina Regen | Stance Break |
|-------|-----------------|---------------|--------------|
| 1 | +0.3% | +0.5% | +0.2% |
| 5 | +1.5% | +2.5% | +1.0% |
| 10 | +3.0% | +5.0% | +2.0% |

All buffs last 15 seconds and RESET on each successful parry.

## 🎮 Controls

### Default Controls
| Action | Controller | Keyboard |
|--------|-----------|----------|
| Parry + Swap to Cursed Sword | Y + LT | E |
| Return to Original Weapon | Manual swap | Manual swap |
| Toggle Mod On/Off | Console: `toggle` | Console: `toggle` |

### Custom Controls
Edit `keybind_config.json` to use different buttons/keys.

## 📥 Installation

### Prerequisites
- Elden Ring (Latest Patch)
- Seamless Co-op Mod ([Download](https://github.com/kal997/seamless-coop))
- Mod Engine 2 ([Download](https://github.com/soulsmods/ModEngine2))
- Python 3.9+ ([Download](https://www.python.org/downloads/))

### Quick Start (5 minutes)

1. Download This Mod
```bash
git clone https://github.com/Scotomas/Cursed-Sword-Mod/
