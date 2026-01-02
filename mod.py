import struct
import time
import threading
from seamless_coop_integration import seamless_hook

# ============================================================================
# CURSED SWORD MOD v2.2 - Auto-Parry Swap with Stacking Buffs & UI Counter
# Compatible with Seamless Co-op (Latest Version)
# ============================================================================

class CursedSwordMod:
    def __init__(self):
        self.cursed_sword_weapon_id = 32  # Hand of Malenia weapon ID
        self.cursed_sword_ash_id = 100    # Custom Ash of War ID
        self.is_parrying = False
        self.original_weapon_id = None
        self.parry_cooldown = 0.5  # seconds
        self.last_parry_time = 0
        
        # ====== Input Mapping (from keybind config) ======
        self.CONTROLLER_PARRY_INPUT = ("Y", "LT")
        self.PC_PARRY_INPUT = "E"
        self.load_keybinds_from_config()
        
        # Seamless Co-op sync
        self.seamless_enabled = True
        self.player_session_id = None
        
        # ====== Per-Player Settings ======
        self.mod_enabled_per_player = {}
        self.default_enabled = True
        
        # ====== Stacking Buff System (RESETS PER PARRY) ======
        self.parry_stack_count = {}
        self.max_stacks = 10
        self.buff_duration = 15
        self.active_buff_timers = {}
        self.buff_expiry_time = {}
        
        # ====== Visual Effects ======
        self.glow_effect_id = "cursed_sword_orange_glow"
        self.glow_active = {}
        self.ui_counter_visible = {}
        
        # ====== NEW: Sound Effects ======
        self.sound_effects = {
            "parry_success": "parry_success.wem",
            "stack_1": "stack_milestone_1.wem",
            "stack_5": "stack_milestone_5.wem",
            "stack_10": "stack_milestone_10.wem",
        }
        self.sound_config = {}
        self.load_sound_config()
        
        # ====== NEW: Particle Effects ======
        self.particle_effects = {
            "parry_success": "cursed_sword_parry_burst",
            "stack_1": "cursed_sword_stack_1",
            "stack_5": "cursed_sword_stack_5",
            "stack_10": "cursed_sword_stack_10_burst",
        }
        self.particle_active = {}
        
    def load_keybinds_from_config(self):
        """Load keybinds from keybind_config.json"""
        import json
        
        try:
            with open("keybind_config.json", 'r') as f:
                keybind_config = json.load(f)
                
                # Load controller binds
                controller_config = keybind_config.get("controller", {})
                parry_input = controller_config.get("parry_input", ["Y", "LT"])
                self.CONTROLLER_PARRY_INPUT = tuple(parry_input)
                
                # Load keyboard binds
                keyboard_config = keybind_config.get("keyboard", {})
                self.PC_PARRY_INPUT = keyboard_config.get("parry_input", "E")
                
                print(f"[CursedSword] Keybinds loaded:")
                print(f"  Controller: {self.CONTROLLER_PARRY_INPUT[0]} + {self.CONTROLLER_PARRY_INPUT[1]}")
                print(f"  Keyboard: {self.PC_PARRY_INPUT}")
                
        except FileNotFoundError:
            print("[CursedSword] keybind_config.json not found, using defaults")
        except Exception as e:
            print(f"[CursedSword] Error loading keybinds: {e}, using defaults")
    
    def load_sound_config(self):
        """Load sound settings from config"""
        import json
        
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
                self.sound_config = config.get("sound_effects", {})
                print("[CursedSword] Sound configuration loaded")
        except Exception as e:
            print(f"[CursedSword] Error loading sound config: {e}")
    
    def initialize(self):
        """Initialize mod with Seamless Co-op hook"""
        print("[CursedSword] Initializing enhanced mod v2.2...")
        print("[CursedSword] Features: Stacking buffs, Sound effects, Particles, Custom keybinds")
        
        if self.seamless_enabled:
            seamless_hook.register_custom_sync(
                mod_name="CursedSword",
                sync_handler=self.sync_parry_state,
                priority=10
            )
            
            seamless_hook.register_network_handler(
                mod_name="CursedSword",
                handler=self.handle_remote_parry
            )
        
        print("[CursedSword] ✓ Mod initialized!")
    
    # ========================================================================
    # PER-PLAYER MOD TOGGLE
    # ========================================================================
    
    def toggle_mod_for_player(self, player_id):
        """Toggle mod on/off for individual player"""
        current_state = self.mod_enabled_per_player.get(player_id, self.default_enabled)
        new_state = not current_state
        self.mod_enabled_per_player[player_id] = new_state
        
        status = "ENABLED" if new_state else "DISABLED"
        print(f"[CursedSword] Mod {status} for player {player_id}")
        
        self.broadcast_mod_toggle(player_id, new_state)
        
        if not new_state:
            self.hide_ui_counter(player_id)
        
        return new_state
    
    def is_mod_enabled_for_player(self, player_id):
        """Check if mod is enabled for specific player"""
        return self.mod_enabled_per_player.get(player_id, self.default_enabled)
    
    def broadcast_mod_toggle(self, player_id, enabled):
        """Inform other players of mod status change"""
        if not self.seamless_enabled:
            return
        
        sync_data = {
            "mod": "CursedSword",
            "action": "mod_toggle",
            "player_id": player_id,
            "enabled": enabled,
            "timestamp": time.time(),
        }
        
        seamless_hook.broadcast_to_session(sync_data, exclude_self=False)
    
    # ========================================================================
    # INPUT DETECTION (USES KEYBIND CONFIG)
    # ========================================================================
    
    def detect_input(self, input_type):
        """Detect parry input based on device type and keybind config"""
        if input_type == "controller":
            return self.check_controller_combo()
        elif input_type == "keyboard":
            return self.check_keyboard_input()
        return False
    
    def check_controller_combo(self):
        """Check for configured controller combo"""
        from input_manager import InputManager
        
        button1 = InputManager.is_button_pressed(self.CONTROLLER_PARRY_INPUT[0])
        button2 = InputManager.is_button_pressed(self.CONTROLLER_PARRY_INPUT[1])
        
        return button1 and button2
    
    def check_keyboard_input(self):
        """Check for configured keyboard input"""
        from input_manager import InputManager
        return InputManager.is_key_pressed(self.PC_PARRY_INPUT)
    
    # ========================================================================
    # WEAPON SWAPPING
    # ========================================================================
    
    def swap_to_cursed_sword(self, player):
        """Instantly swap to Hand of Malenia"""
        player_id = player.get_id()
        self.original_weapon_id = player.get_equipped_weapon_id()
        
        player.set_equipped_weapon(self.cursed_sword_weapon_id)
        player.set_ash_of_war(self.cursed_sword_ash_id)
        
        print(f"[CursedSword] Player {player_id} swapped to Cursed Sword")
        
        if self.seamless_enabled:
            self.broadcast_weapon_swap(player, self.cursed_sword_weapon_id)
    
    def return_to_original_weapon(self, player):
        """Swap back to original weapon"""
        player_id = player.get_id()
        
        if self.original_weapon_id is None:
            return
        
        player.set_equipped_weapon(self.original_weapon_id)
        
        if self.seamless_enabled:
            self.broadcast_weapon_swap(player, self.original_weapon_id)
    
    # ========================================================================
    # PARRY EXECUTION
    # ========================================================================
    
    def execute_parry(self, player):
        """Execute parry animation"""
        player_id = player.get_id()
        current_time = time.time()
        
        if current_time - self.last_parry_time < self.parry_cooldown:
            return False
        
        self.last_parry_time = current_time
        self.is_parrying = True
        
        player.trigger_parry_animation()
        
        parry_window_duration = 0.6
        parry_success = self.listen_for_parry_success(player, parry_window_duration)
        
        if parry_success:
            self.handle_successful_parry(player)
        
        self.is_parrying = False
        return parry_success
    
    def listen_for_parry_success(self, player, window_duration):
        """Listen for enemy hit during parry window"""
        start_time = time.time()
        
        while time.time() - start_time < window_duration:
            if player.did_parry_hit():
                return True
            time.sleep(0.01)
        
        return False
    
    # ========================================================================
    # STACKING BUFF SYSTEM WITH SOUND & PARTICLES
    # ========================================================================
    
    def handle_successful_parry(self, player):
        """Handle successful parry with all effects"""
        player_id = player.get_id()
        current_time = time.time()
        
        if player_id not in self.parry_stack_count:
            self.parry_stack_count[player_id] = 0
            self.buff_expiry_time[player_id] = current_time
            self.active_buff_timers[player_id] = None
        else:
            time_since_last_parry = current_time - self.buff_expiry_time[player_id]
            
            if time_since_last_parry > self.buff_duration:
                self.parry_stack_count[player_id] = 0
                print(f"[CursedSword] Player {player_id}: Buff expired, stacks reset")
            
            if self.active_buff_timers[player_id] is not None:
                self.active_buff_timers[player_id].cancel()
        
        # Increment stack
        self.parry_stack_count[player_id] = min(
            self.parry_stack_count[player_id] + 1,
            self.max_stacks
        )
        
        new_expiry_time = current_time + self.buff_duration
        self.buff_expiry_time[player_id] = new_expiry_time
        
        stack_count = self.parry_stack_count[player_id]
        
        print(f"[CursedSword] Player {player_id}: Successful parry! Stack {stack_count}/{self.max_stacks}")
        
        # Apply all effects
        self.apply_stacking_buffs(player, stack_count)
        self.apply_orange_glow_effect(player, stack_count)
        self.update_ui_counter(player, stack_count)
        
        # ====== NEW: Apply Sound Effects ======
        self.play_parry_sounds(player, stack_count)
        
        # ====== NEW: Spawn Particles ======
        self.spawn_parry_particles(player, stack_count)
        
        self.schedule_buff_expiry(player, self.buff_duration)
        
        if self.seamless_enabled:
            self.broadcast_parry_success(player, stack_count)
    
    def apply_stacking_buffs(self, player, stack_count):
        """Apply buffs that scale with stack count"""
        player_id = player.get_id()
        
        damage_multiplier = 1.0 + (stack_count * 0.003)
        stamina_multiplier = 1.0 + (stack_count * 0.005)
        stance_break_multiplier = 1.0 + (stack_count * 0.002)
        
        buff_duration = self.buff_duration
        
        player.apply_buff("physical_damage", damage_multiplier, buff_duration)
        player.apply_buff("stamina_regen", stamina_multiplier, buff_duration)
        player.apply_buff("poise_damage", stance_break_multiplier, buff_duration)
        
        damage_increase = (stack_count * 0.3)
        stamina_increase = (stack_count * 0.5)
        stance_increase = (stack_count * 0.2)
        
        buff_info = {
            "stack_count": stack_count,
            "physical_damage": f"+{damage_increase:.1f}%",
            "stamina": f"+{stamina_increase:.1f}%",
            "stance_break": f"+{stance_increase:.1f}%",
        }
        
        print(f"[CursedSword] Player {player_id} Buffs: {buff_info}")
        
        player.spawn_particle_effect("parry_success")
    
    def schedule_buff_expiry(self, player, duration):
        """Schedule buff expiry"""
        player_id = player.get_id()
        
        def on_buff_expire():
            print(f"[CursedSword] Player {player_id}: Buff window closing")
            self.hide_ui_counter(player_id)
            self.remove_orange_glow(player)
        
        timer = threading.Timer(duration, on_buff_expire)
        timer.daemon = True
        self.active_buff_timers[player_id] = timer
        timer.start()
    
    # ========================================================================
    # SOUND EFFECTS SYSTEM
    # ========================================================================
    
    def play_parry_sounds(self, player, stack_count):
        """
        Play sound effects for parry and stack milestones
        
        Milestones:
        - Every parry: Base parry sound
        - Stack 5: Special milestone sound
        - Stack 10: Victory/max stack sound
        """
        player_id = player.get_id()
        
        # Always play base parry sound
        self.play_sound(player, "parry_success")
        print(f"[CursedSword] Player {player_id}: Parry sound played")
        
        # Play milestone sounds
        if stack_count == 1:
            self.play_sound(player, "stack_1")
            print(f"[CursedSword] Player {player_id}: Stack 1 milestone sound")
            
        elif stack_count == 5:
            self.play_sound(player, "stack_5")
            print(f"[CursedSword] Player {player_id}: Stack 5 milestone sound!")
            
        elif stack_count == 10:
            self.play_sound(player, "stack_10")
            print(f"[CursedSword] Player {player_id}: MAX STACK 10 sound!")
    
    def play_sound(self, player, sound_type):
        """
        Play a sound effect
        
        Args:
            player: Player game object
            sound_type: Type of sound (parry_success, stack_1, stack_5, stack_10)
        """
        try:
            sound_file = self.sound_effects.get(sound_type, "parry_success.wem")
            
            # Get sound settings
            volume = self.sound_config.get("volume", 1.0)
            pitch = self.sound_config.get("pitch", 1.0)
            
            # Play sound at player position
            player.play_sound_effect(
                sound_file=sound_file,
                volume=volume,
                pitch=pitch,
                follow_player=True
            )
            
        except Exception as e:
            print(f"[CursedSword] Error playing sound: {e}")
    
    # ========================================================================
    # PARTICLE EFFECTS SYSTEM
    # ========================================================================
    
    def spawn_parry_particles(self, player, stack_count):
        """
        Spawn particle effects around player on successful parry
        
        Effects:
        - Every parry: Base parry burst
        - Stack 5: Special 5-stack effect
        - Stack 10: Epic max stack burst
        """
        player_id = player.get_id()
        
        # Always spawn base parry burst
        self.spawn_particles(player, "parry_success", stack_count)
        print(f"[CursedSword] Player {player_id}: Parry burst particles spawned")
        
        # Spawn milestone particles
        if stack_count == 1:
            self.spawn_particles(player, "stack_1", stack_count)
            print(f"[CursedSword] Player {player_id}: Stack 1 particle effect")
            
        elif stack_count == 5:
            self.spawn_particles(player, "stack_5", stack_count)
            print(f"[CursedSword] Player {player_id}: Stack 5 milestone particles!")
            
        elif stack_count == 10:
            self.spawn_particles(player, "stack_10", stack_count)
            print(f"[CursedSword] Player {player_id}: MAX STACK 10 particle burst!")
    
    def spawn_particles(self, player, effect_type, stack_count):
        """
        Spawn particle effect around player
        
        Args:
            player: Player game object
            effect_type: Type of particle effect
            stack_count: Current stack count (affects particle scale/intensity)
        """
        try:
            effect_id = self.particle_effects.get(effect_type, "cursed_sword_parry_burst")
            
            # Scale particle intensity with stack count
            particle_scale = 0.5 + (stack_count / self.max_stacks) * 1.0
            
            # Get player position and spawn particles
            player_pos = player.get_position()
            
            player.spawn_particle_effect_at_location(
                effect_id=effect_id,
                location=player_pos,
                scale=particle_scale,
                lifetime=1.5,  # Duration in seconds
                color_override={
                    "r": 1.0,      # Orange
                    "g": 0.55,
                    "b": 0.0,
                    "intensity": particle_scale
                }
            )
            
            self.particle_active[player.get_id()] = True
            
        except Exception as e:
            print(f"[CursedSword] Error spawning particles: {e}")
    
    # ========================================================================
    # VISUAL EFFECTS - ORANGE GLOW
    # ========================================================================
    
    def apply_orange_glow_effect(self, player, stack_count):
        """Apply orange glow to weapon"""
        player_id = player.get_id()
        
        glow_intensity = 0.3 + (stack_count / self.max_stacks) * 0.7
        
        glow_color = {
            "r": 1.0,
            "g": 0.55,
            "b": 0.0,
            "intensity": glow_intensity
        }
        
        player.apply_weapon_glow(
            weapon_id=self.cursed_sword_weapon_id,
            color=glow_color,
            effect_id=self.glow_effect_id,
            duration=self.buff_duration
        )
        
        self.glow_active[player_id] = True
        
        print(f"[CursedSword] Player {player_id}: Glow applied ({glow_intensity * 100:.0f}%)")
    
    def remove_orange_glow(self, player):
        """Remove glow effect"""
        player_id = player.get_id()
        
        if self.glow_active.get(player_id, False):
            player.remove_weapon_glow(self.glow_effect_id)
            self.glow_active[player_id] = False
    
    # ========================================================================
    # UI COUNTER (POSITIONED WITH STATUS EFFECT ICONS)
    # ========================================================================
    
    def update_ui_counter(self, player, stack_count):
        """
        Display stack counter positioned with status effect icons
        
        Position: Top-right area where buff icons display
        """
        player_id = player.get_id()
        
        damage_increase = (stack_count * 0.3)
        stamina_increase = (stack_count * 0.5)
        stance_increase = (stack_count * 0.2)
        
        # Simple format for status icon area
        ui_text = f"CURSE: [{stack_count:2d}/10]"
        
        # Display as buff icon overlay
        player.display_hud_element(
            text=ui_text,
            position="top_right_with_buffs",  # Positions with other buff icons
            duration=self.buff_duration,
            priority=100,
            element_id="cursed_sword_stack_counter",
            element_type="buff_counter",
            icon_color={
                "r": 1.0,
                "g": 0.55,
                "b": 0.0
            }
        )
        
        self.ui_counter_visible[player_id] = True
        
        print(f"[CursedSword] Player {player_id}: UI counter updated - [{stack_count}/10]")
    
    def hide_ui_counter(self, player_id):
        """Hide the UI counter"""
        if self.ui_counter_visible.get(player_id, False):
            from game_manager import GameManager
            game_manager = GameManager.get_instance()
            player = game_manager.get_player(player_id)
            
            if player:
                player.remove_hud_element("cursed_sword_stack_counter")
            
            self.ui_counter_visible[player_id] = False
    
    # ========================================================================
    # SEAMLESS CO-OP INTEGRATION
    # ========================================================================
    
    def sync_parry_state(self, player_data):
        """Sync parry state"""
        player_id = player_data["id"]
        stack_count = self.parry_stack_count.get(player_id, 0)
        
        return {
            "mod": "CursedSword",
            "action": "parry_executed",
            "player_id": player_id,
            "weapon_id": self.cursed_sword_weapon_id,
            "stack_count": stack_count,
            "buff_duration": self.buff_duration,
            "timestamp": time.time(),
        }
    
    def broadcast_weapon_swap(self, player, weapon_id):
        """Broadcast weapon swap"""
        sync_data = {
            "mod": "CursedSword",
            "action": "weapon_swap",
            "player_id": player.get_id(),
            "weapon_id": weapon_id,
            "timestamp": time.time(),
        }
        
        seamless_hook.broadcast_to_session(sync_data)
    
    def broadcast_parry_success(self, player, stack_count):
        """Broadcast successful parry"""
        sync_data = {
            "mod": "CursedSword",
            "action": "parry_success",
            "player_id": player.get_id(),
            "stack_count": stack_count,
            "weapon_id": self.cursed_sword_weapon_id,
            "buff_duration": self.buff_duration,
            "timestamp": time.time(),
        }
        
        seamless_hook.broadcast_to_session(sync_data)
    
    def handle_remote_parry(self, sync_data):
        """Handle remote parry events"""
        remote_player_id = sync_data["player_id"]
        action = sync_data["action"]
        
        if action == "weapon_swap":
            print(f"[CursedSword] Remote player {remote_player_id} swapped weapon")
            
        elif action == "parry_success":
            stack_count = sync_data.get("stack_count", 0)
            print(f"[CursedSword] Remote player {remote_player_id} executed parry (Stack {stack_count})")
            
        elif action == "mod_toggle":
            enabled = sync_data.get("enabled", True)
            status = "ENABLED" if enabled else "DISABLED"
            print(f"[CursedSword] Remote player {remote_player_id} mod {status}")
    
    # ========================================================================
    # MAIN LOOP
    # ========================================================================
    
    def on_update(self, game_state):
        """Main update loop"""
        player = game_state.get_player()
        
        if player is None:
            return
        
        player_id = player.get_id()
        
        if not self.is_mod_enabled_for_player(player_id):
            return
        
        input_type = self.detect_input_type()
        
        if self.detect_input(input_type):
            self.swap_to_cursed_sword(player)
            time.sleep(0.1)
            self.execute_parry(player)
    
    def detect_input_type(self):
        """Detect input type"""
        from input_manager import InputManager
        return InputManager.get_active_input_type()
    
    # ========================================================================
    # UTILITY
    # ========================================================================
    
    def get_player_stats(self, player_id):
        """Get player stats"""
        stack_count = self.parry_stack_count.get(player_id, 0)
        time_until_expiry = max(0, self.buff_expiry_time.get(player_id, 0) - time.time())
        
        return {
            "mod_enabled": self.is_mod_enabled_for_player(player_id),
            "parry_stacks": stack_count,
            "max_stacks": self.max_stacks,
            "glow_active": self.glow_active.get(player_id, False),
            "time_until_expiry": f"{time_until_expiry:.1f}s",
            "ui_counter_visible": self.ui_counter_visible.get(player_id, False),
            "particle_effects_active": self.particle_active.get(player_id, False),
        }
    
    def reset_player_stacks(self, player_id):
        """Reset stacks for a player"""
        self.parry_stack_count[player_id] = 0
        self.hide_ui_counter(player_id)
        
        from game_manager import GameManager
        game_manager = GameManager.get_instance()
        player = game_manager.get_player(player_id)
        if player:
            self.remove_orange_glow(player)
        
        print(f"[CursedSword] Player {player_id}: Stacks reset to 0")
    
    def get_mod_info(self):
        """Get mod information"""
        return {
            "name": "Cursed Sword - Auto Parry System v2.2",
            "version": "2.2.0",
            "features": [
                "Per-player mod toggle",
                "Stacking buff system (max 10%)",
                "Buff timer resets on each parry",
                "Orange glow effect (scales with stacks)",
                "Stack counter with buff icons",
                "Sound effects & milestones",
                "Particle effects on parry",
                "Custom keybind config",
                "Seamless Co-op support",
                "Works on all enemies",
            ],
        }


# ============================================================================
# INITIALIZATION
# ============================================================================

cursed_sword_mod = CursedSwordMod()

def mod_init():
    """Entry point for Mod Engine 2"""
    cursed_sword_mod.initialize()
    print(cursed_sword_mod.get_mod_info())

def mod_update(game_state):
    """Update hook"""
    cursed_sword_mod.on_update(game_state)

def mod_command(command, args):
    """Handle console commands"""
    player = args.get("player")
    
    if command == "toggle":
        player_id = player.get_id()
        cursed_sword_mod.toggle_mod_for_player(player_id)
        
    elif command == "stats":
        player_id = player.get_id()
        stats = cursed_sword_mod.get_player_stats(player_id)
        print(f"\n[CursedSword] Player {player_id} Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
    elif command == "reset":
        player_id = player.get_id()
        cursed_sword_mod.reset_player_stacks(player_id)
        
    elif command == "info":
        info = cursed_sword_mod.get_mod_info()
        print(f"\n[CursedSword] Mod Information:")
        for key, value in info.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value:
                    print(f"    - {item}")
            else:
                print(f"  {key}: {value}")
