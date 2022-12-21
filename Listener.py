# Create a revised MacroManager script, this is mainly to allow for a more versatile key recording system
from pynput import keyboard
import hotkey

allowedKeys = {
    keyboard.Key.shift,
    keyboard.Key.alt,
    keyboard.Key.ctrl
}

class Listener():
    def __init__(self, onPress=None):
        self.listener = keyboard.Listener(on_press=lambda key:self.on_press(key, callback=onPress), on_release=self.on_release)

        self.recordKeys = False
        self.hotKey = hotkey.HotKey()

        self.listening = True
        self.current = set()

    def on_press(self, key, callback=None):
        # Check if the incoming key is from the number pad, if so use the virtual key code and not the char. Otherwise just use the passed key
        if(hasattr(key, 'vk') and hotkey.isNumpad(key.vk)):
            key = keyboard.KeyCode(vk=key.vk)
        else:
            key = keyboard.Listener().canonical(key)

        # If recording hotkeys is activated, add the key to a HotKey object
        if(self.recordKeys):
            if(key in allowedKeys):
                self.hotKey.combination.add(key)
                # print(self.hotKey)
            if(hasattr(key, 'char')):
                if(key.char is not None):
                    self.hotKey.combination.add(key)
                    # print(self.hotKey)
            if(hasattr(key, 'vk') and hotkey.isNumpad(key.vk)):
                self.hotKey.combination.add(key)
                # print(self.hotKey)
            
            if(len(self.hotKey.combination) >= 3):
                self.disableRecording()
    
        self.current.add(key)

        # Add a way to activate external callbacks
        if(callback != None and self.listening):
            callback()

    def on_release(self, key):
        if(hasattr(key, 'vk') and hotkey.isNumpad(key.vk)):
            key = keyboard.KeyCode(vk=key.vk)
        else:
            key = keyboard.Listener().canonical(key)
        
        if(key in self.current):
            self.current.remove(key)
        if(len(self.current) <= 1):
            self.current.clear()

    def enableRecording(self):
        self.hotKey.combination.clear()
        self.recordKeys = True
        self.disableListening()
    
    def disableRecording(self):
        self.recordKeys = False

    def enableListening(self):
        self.listening = True

    def disableListening(self):
        self.listening = False

    def getRecordedHotkey(self):
        # print(self.hotKey)
        return self.hotKey

    def startListener(self):
        self.listener.start()