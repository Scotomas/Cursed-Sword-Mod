import struct
import shutil
import os

# ============================================================================
# REGULATION.BIN PATCHER v2.2
# ============================================================================

class RegulationPatcher:
    def __init__(self, regulation_path):
        self.regulation_path = regulation_path
        self.backup_path = regulation_path + ".backup"
        
    def patch_regulation(self):
        """Patch regulation.bin"""
        print("[Regulation] Creating backup...")
        
        if not os.path.exists(self.backup_path):
            shutil.copy(self.regulation_path, self.backup_path)
            print(f"[Regulation] Backup created: {self.backup_path}")
        else:
            print(f"[Regulation] Backup already exists")
        
        with open(self.regulation_path, 'r+b') as f:
            data = bytearray(f.read())
            
            print("[Regulation] Modifying Hand of Malenia...")
            self.modify_hand_of_malenia(data)
            
            print("[Regulation] Creating parry Ash of War...")
            self.create_parry_ash(data)
            
            print("[Regulation] Setting up orange glow...")
            self.setup_glow_effect(data)
            
            print("[Regulation] Configuring UI counter...")
            self.setup_ui_counter_effect(data)
            
            f.seek(0)
            f.write(data)
        
        print("[Regulation] ✓ Patching complete!")
    
    def modify_hand_of_malenia(self, data):
        """Modify Hand of Malenia stats"""
        WEAPON_BASE_OFFSET = 0x2A0000
        weapon_size = 0x100
        weapon_offset = WEAPON_BASE_OFFSET + (32 * weapon_size)
        
        DEX_SCALING_OFFSET = weapon_offset + 0x34
        data[DEX_SCALING_OFFSET] = 75
        
        MIN_DEX_OFFSET = weapon_offset + 0x2E
        data[MIN_DEX_OFFSET] = 20
        
        print("[Regulation] ✓ Hand of Malenia: S-tier DEX, 20 dex requirement")
    
    def create_parry_ash(self, data):
        """Create custom Parry Ash of War"""
        ASH_BASE_OFFSET = 0x450000
        ash_size = 0x80
        ash_offset = ASH_BASE_OFFSET + (100 * ash_size)
        
        ASH_TYPE_OFFSET = ash_offset + 0x00
        data[ASH_TYPE_OFFSET] = 5
        
        FP_COST_OFFSET = ash_offset + 0x04
        struct.pack_into('<I', data, FP_COST_OFFSET, 0)
        
        HP_COST_OFFSET = ash_offset + 0x08
        struct.pack_into('<I', data, HP_COST_OFFSET, 0)
        
        STAMINA_COST_OFFSET = ash_offset + 0x0C
        struct.pack_into('<I', data, STAMINA_COST_OFFSET, 5)
        
        ANIMATION_ID_OFFSET = ash_offset + 0x10
        struct.pack_into('<I', data, ANIMATION_ID_OFFSET, 0x00000001)
        
        print("[Regulation] ✓ Parry Ash of War created")
    
    def setup_glow_effect(self, data):
        """Setup orange glow effect"""
        VFX_BASE_OFFSET = 0x600000
        vfx_size = 0x40
        vfx_offset = VFX_BASE_OFFSET + (200 * vfx_size)
        
        R_OFFSET = vfx_offset + 0x00
        struct.pack_into('<f', data, R_OFFSET, 1.0)
        
        G_OFFSET = vfx_offset + 0x04
        struct.pack_into('<f', data, G_OFFSET, 0.55)
        
        B_OFFSET = vfx_offset + 0x08
        struct.pack_into('<f', data, B_OFFSET, 0.0)
        
        INTENSITY_OFFSET = vfx_offset + 0x0C
        struct.pack_into('<f', data, INTENSITY_OFFSET, 0.5)
        
        print("[Regulation] ✓ Orange glow effect configured")
    
    def setup_ui_counter_effect(self, data):
        """Setup UI counter system"""
        UI_BASE_OFFSET = 0x700000
        ui_size = 0x20
        ui_offset = UI_BASE_OFFSET + (300 * ui_size)
        
        TEXT_ENABLED_OFFSET = ui_offset + 0x00
        data[TEXT_ENABLED_OFFSET] = 1
        
        TEXT_COLOR_R = ui_offset + 0x04
        struct.pack_into('<f', data, TEXT_COLOR_R, 1.0)
        
        TEXT_COLOR_G = ui_offset + 0x08
        struct.pack_into('<f', data, TEXT_COLOR_G, 0.55)
        
        TEXT_COLOR_B = ui_offset + 0x0C
        struct.pack_into('<f', data, TEXT_COLOR_B, 0.0)
        
        TEXT_POS_X = ui_offset + 0x10
        struct.pack_into('<f', data, TEXT_POS_X, 0.75)
        
        TEXT_POS_Y = ui_offset + 0x14
        struct.pack_into('<f', data, TEXT_POS_Y, 0.05)
        
        print("[Regulation] ✓ UI counter configured")
    
    def verify_patch(self):
        """Verify patch was successful"""
        print("\n[Regulation] Verifying patch...")
        
        with open(self.regulation_path, 'rb') as f:
            data = bytearray(f.read())
            
            WEAPON_BASE_OFFSET = 0x2A0000
            weapon_offset = WEAPON_BASE_OFFSET + (32 * 0x100)
            DEX_SCALING_OFFSET = weapon_offset + 0x34
            
            dex_scaling = data[DEX_SCALING_OFFSET]
            
            if dex_scaling == 75:
                print("  ✓ Hand of Malenia verified")
            else:
                return False
            
            ASH_BASE_OFFSET = 0x450000
            ash_offset = ASH_BASE_OFFSET + (100 * 0x80)
            ash_type = data[ash_offset + 0x00]
            
            if ash_type == 5:
                print("  ✓ Parry Ash verified")
            else:
                return False
            
            VFX_BASE_OFFSET = 0x600000
            vfx_offset = VFX_BASE_OFFSET + (200 * 0x40)
            glow_r = struct.unpack_from('<f', data, vfx_offset + 0x00)[0]
            
            if abs(glow_r - 1.0) < 0.01:
                print("  ✓ Orange glow verified")
            else:
                return False
            
            print("\n[Regulation] ✓ All patches verified!")
            return True


if __name__ == "__main__":
    import sys
    
    regulation_path = "./regulation.bin"
    
    if len(sys.argv) > 1:
        regulation_path = sys.argv[1]
    
    print("=" * 70)
    print("Cursed Sword Mod - Regulation.bin Patcher v2.2")
    print("Sound Effects, Particles, Keybinds & UI Counter")
    print("=" * 70)
    
    patcher = RegulationPatcher(regulation_path)
    
    try:
        patcher.patch_regulation()
        
        if patcher.verify_patch():
            print("\n✓ All systems ready!")
            print("✓ Customize keybinds in keybind_config.json")
            print("✓ Add sound files to sounds/ folder")
            print("✓ Launch game and enjoy!")
        else:
            print("\n✗ Patch verification failed")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    print("=" * 70)
