import pygame
import os.path

# -- Sound --
# Plays sounds and music
class Sound(object):
    def __init__(self):
        # Pre-initialize sound, needs to be done before pygame is initialized
        pygame.init()
        pygame.mixer.pre_init(int(22050), -16, 2, 2**6)
        pygame.mixer.init()
        # Maximum amount of sounds being able to play at once (Normally 8)
        pygame.mixer.set_num_channels(16)
        
        # Sounds
        self.sounds = {}

               
    # Load a sound into self.sounds
    def load_sound(self, name, path):
        if not os.path.isfile(path):
            print('ERROR - Sound \'{}\' not found at \'{}\''.format(name, path))
            return
        try: self.sounds[name] = pygame.mixer.Sound(path)
        except: print('ERROR - Sound \'{}\' not loaded at \'{}\''.format(name, path))
    
    # Play a sound
    def play_sound(self, file, where=0):
        if not file in self.sounds:
            print('ERROR - Sound \'{}\' doesn\'t exist'.format(file))
            return
        try: sound = self.sounds[file].play(where)
        except: print('ERROR - Can\'t play sound \'{}\''.format(file))

    # Play a sound and let it loop
    def loop_sound(self, file):
        self.play_sound(file, -1)
    
    # Stop a sound from playing
    def stop_sound(self, file):
        try: self.sounds[file].stop()
        except: print('ERROR - Can\'t stop sound \'{}\''.format(file))
            
    # Stop all sounds from playing
    def stop_all_sounds(self):
        for sound in self.sounds.values():
            sound.stop()

    # Set volume of a sound
    def set_volume(self, file, volume):
        try: self.sounds[file].set_volume(volume**2)
        except: print('ERROR - Can\'t change volume of sound \'{}\''.format(file))

