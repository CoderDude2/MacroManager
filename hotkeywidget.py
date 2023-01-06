import tkinter as tk
from sys import platform

from pynput import keyboard

import hotkey

modifier_keys = {
    "Shift_L": keyboard.Key.shift,
    "Shift_R": keyboard.Key.shift,
    "Control_L": keyboard.Key.ctrl,
    "Control_R": keyboard.Key.ctrl,
    "Alt_L": keyboard.Key.alt,
    "Alt_R": keyboard.Key.alt
}

class HotkeyWidget(tk.Frame):
    def __init__(self, master=None, hotKey=None):
        super().__init__(master)
        self.master = master

        self.isActive = False
        if(hotKey is not None):
            self.hotKey = hotKey
        else:
            self.hotKey = hotkey.HotKey(combination=set())
        
        self.hotKeyLabel = tk.Label(self, text=self.hotKey.format(), width=15, background="grey")
        self.toggleButton = tk.Button(self, text="Set Hotkey", command=self.toggleHotkeyRecording)

        self.hotKeyLabel.pack(side=tk.LEFT)
        self.toggleButton.pack(side=tk.LEFT)

        self.master.bind("<KeyPress>", self.record)

    def record(self, event):
        if(self.isActive):
            if(platform == "win32"):
                key = self.convertToKeyWin32(event.keysym, event.keycode)
            elif(platform == "darwin"):
                key = self.convertToKeyDarwin(event.keysym)
            if(key is not None):
                self.hotKey.combination.add(key)
            
            self.hotKeyLabel.config(text=self.hotKey.format())
            
            if(len(self.hotKey.combination) > 1):
                self.toggleButton.configure(state=tk.NORMAL)
            if(len(self.hotKey.combination) == 3):
                self.deActivate()

    def getHotkey(self):
        return self.hotKey

    def activate(self):
        self.isActive = True
        self.master.focus_set()

        self.toggleButton.configure(state=tk.DISABLED, text="Save")

        self.hotKeyLabel.config(text="")
        self.hotKey.combination.clear()
        
    def deActivate(self, event=None):
        self.isActive = False
        self.toggleButton.configure(text="Set Hotkey", state=tk.NORMAL)

        if(len(self.hotKey.combination) <= 1):
            self.hotKey.combination.clear()
            self.hotKeyLabel.configure(text="")

    def toggleHotkeyRecording(self):
        if(not self.isActive):
            self.activate()
            return
        self.deActivate()

    def isNumpad(self, keysym):
        if("KP" in keysym):
            if(keysym.split("_")[1].isdigit()):
                return True
        return False

    def isNumpadKeyCode(self, keycode):
        if(platform == "win32"):
            return True if keycode in hotkey.win32_numpad else False
        elif(platform == "darwin"):
            pass

    def isModifier(self, keysym):
        if(keysym in modifier_keys.keys()):
            return True
        return False

    def clear(self):
        self.hotKey.combination.clear()
        self.hotKeyLabel.configure(text="")

    def convertToKeyWin32(self, keysym, keycode):
        if(self.isNumpadKeyCode(keycode)):
            key = keyboard.KeyCode().from_vk(keycode)
            return key
        elif(self.isModifier(keysym)):
            key = modifier_keys[keysym]
            return key
        elif(keysym.isalnum() and len(keysym) == 1):
            key =  keyboard.Listener().canonical(keyboard.KeyCode().from_char(char=keysym))
            return key

    def convertToKeyDarwin(self, keysym):
        if(self.isNumpad(keysym)):
            keyVK = hotkey.darwin_numpad[ int(keysym.split("_")[1]) ]
            key = keyboard.KeyCode().from_vk(keyVK)
            return key
        elif(self.isModifier(keysym)):
            key = modifier_keys[keysym]
            return key
        elif(keysym.isalnum() and len(keysym) == 1):
            key =  keyboard.Listener().canonical(keyboard.KeyCode().from_char(char=keysym))
            return key