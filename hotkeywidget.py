import tkinter as tk
from pynput import keyboard
import hotkey

hotKeyLookUp = {
    "Shift_L": keyboard.Key.shift,
    "Shift_R": keyboard.Key.shift,
    "Control_L": keyboard.Key.ctrl,
    "Control_R": keyboard.Key.ctrl,
    "Alt_L": keyboard.Key.alt,
    "Alt_R": keyboard.Key.alt,
}

class HotkeyWidget(tk.Frame):
    def __init__(self, master=None, hotKey=None):
        super().__init__(master)
        self.isActive = False

        if(hotKey == None):
            self.hotKey = hotkey.HotKey()
        else:
            self.hotKey = hotkey.parse(hotKey)
        
        self.hotKeyLabel = tk.Label(self, text=self.hotKey.format(), width=15, background="grey")
        self.toggleButton = tk.Button(self, text="Set Hotkey", command=self.toggleHotkeyRecording)

        self.hotKeyLabel.pack(side=tk.LEFT)
        self.toggleButton.pack(side=tk.LEFT)

    def record(self, event):
        if(self.isActive):
            if(event.keysym in hotKeyLookUp.keys()):
                pressedKey = hotKeyLookUp[event.keysym]
                self.hotKey.combination.add(pressedKey)
            else:
                pressedKey = event.char
                if(pressedKey != ''):
                    self.hotKey.combination.add(keyboard.KeyCode(char=pressedKey))
            self.hotKeyLabel.config(text=self.hotKey.format())
        if(len(self.hotKey.combination) > 1):
            self.toggleButton.configure(state=tk.NORMAL)
        if(len(self.hotKey.combination) == 3):
            self.deActivate()

    def getHotkey(self):
        return self.hotKey

    def activate(self):
        self.toggleButton.configure(state=tk.DISABLED, text="Save")
        self.hotKeyLabel.config(text="")
        self.hotKey.combination = set()
        self.isActive = True

    def deActivate(self):
        self.isActive = False
        self.toggleButton.configure(text="Set Hotkey")

    def toggleHotkeyRecording(self):
        if(not self.isActive):
            self.activate()
            return
        self.deActivate()