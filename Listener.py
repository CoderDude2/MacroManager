# Create a revised MacroManager script, this is mainly to allow for a more versatile key recording system

from pynput import keyboard
import tkinter as tk
import hotkey

allowedKeys = {
    keyboard.Key.shift,
    keyboard.Key.alt,
    keyboard.Key.ctrl
}

class Listener():
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

        self.recordKeys = False
        self.hotKey = hotkey.HotKey()

        self.listen = False
        self.current = set()

    def on_press(self, key):
        # Remove any modifiers from the key
        if(hasattr(key, 'vk') and 82 <= key.vk <= 92):
            key = keyboard.KeyCode(vk=key.vk)
            print(key)
        else:    
            key = keyboard.Listener().canonical(key)

        # If recording hotkeys is activated, add the key to a HotKey object
        if(self.recordKeys):
            if(key in allowedKeys):
                self.hotKey.combination.add(key)
                print(self.hotKey)
            
            elif( isinstance(key, keyboard.KeyCode) ):
                self.hotKey.combination.add(key)
                print(self.hotKey)
            
            if(len(self.hotKey.combination) >= 3):
                self.disableRecord()
    
        # If listening, we are going to add the hotkey to the "current" set, and perform checks
        if(self.listen):
            self.current.add(key)

    def on_release(self, key):
        key = keyboard.Listener().canonical(key)
        if(key in self.current):
            self.current.remove(key)

    def enableRecord(self):
        self.hotKey.combination.clear()
        self.recordKeys = True
        self.disableListening()
    
    def disableRecord(self):
        self.recordKeys = False

    def enableListening(self):
        print(self.hotKey)
        self.listen = True
        self.disableRecord()

    def disableListening(self):
        self.listen = False

    def getRecordedHotkey(self):
        # print(self.hotKey)
        return self.hotKey

    def startListener(self):
        self.listener.start()


class Test:
    def __init__(self, listener):
        self.listener = listener
    
    def getListenerDetails(self):
        print(self.listener.getRecordedHotkey().format())

root = tk.Tk()

keyboardListener = Listener()

t = Test(keyboardListener)

enableRecordingButton = tk.Button(root, text="Enable Recording",command=keyboardListener.enableRecord)
disableRecordingButton = tk.Button(root, text="Disable Recording",command=keyboardListener.disableRecord)
getRecordedKeysButton = tk.Button(root, text="Get Keys",command=t.getListenerDetails)

enableRecordingButton.pack()
disableRecordingButton.pack()
getRecordedKeysButton.pack()

keyboardListener.startListener()

root.mainloop()