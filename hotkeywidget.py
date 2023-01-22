import tkinter as tk
from sys import platform

from pynput import keyboard

import hotkey

key_table = {
    "Shift_L": keyboard.Key.shift,
    "Shift_R": keyboard.Key.shift,
    "Control_L": keyboard.Key.ctrl,
    "Control_R": keyboard.Key.ctrl,
    "Alt_L": keyboard.Key.alt,
    "Alt_R": keyboard.Key.alt,
    "Win_L": keyboard.Key.cmd,
    "Win_R": keyboard.Key.cmd,
    "Meta_L": keyboard.Key.cmd,
    "Meta_R": keyboard.Key.cmd,
    "Tab": keyboard.Key.tab,
    "Left": keyboard.Key.left,
    "Right": keyboard.Key.right,
    "Up": keyboard.Key.up,
    "Down": keyboard.Key.down,
    "space": keyboard.Key.space,
    "F1": keyboard.Key.f1,
    "F2":keyboard.Key.f2,
    "F3":keyboard.Key.f3,
    "F4":keyboard.Key.f4,
    "F5":keyboard.Key.f5,
    "F6":keyboard.Key.f6,
    "F7":keyboard.Key.f7,
    "F8":keyboard.Key.f8,
    "F9":keyboard.Key.f9,
    "F10":keyboard.Key.f10,
    "F11":keyboard.Key.f11,
    "F12":keyboard.Key.f12,
    "F13":keyboard.Key.f13,
    "F14":keyboard.Key.f14,
    "F15":keyboard.Key.f15,
    "F16":keyboard.Key.f16,
    "F17":keyboard.Key.f17,
    "F18":keyboard.Key.f18,
    "F19":keyboard.Key.f19,
    "F20":keyboard.Key.f20
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
        self.master.bind("<space>", self.record)

    def record(self, event):
        if(self.isActive):
            if(platform == "win32"):
                key = self.convertToKeyWin32(event)
            elif(platform == "darwin"):
                key = self.convertToKeyDarwin(event)
            if(key is not None):
                self.hotKey.combination.add(key)
            
            self.hotKeyLabel.config(text=self.hotKey.format())
            
            if(len(self.hotKey.combination) >= 1):
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

    def toggleHotkeyRecording(self):
        if(not self.isActive):
            self.activate()
            return
        self.deActivate()

    def isKeypad(self, keycode, keysym):
        if(platform == "win32"):
            return True if keycode in hotkey.win32_numpad else False
        elif(platform == "darwin"):
            if("KP" in keysym):
                if(keysym.split("_")[1].isdigit()):
                    return True
            return False

    def clear(self):
        self.hotKey.combination.clear()
        self.hotKeyLabel.configure(text="")

    def convertToKeyWin32(self, event):
        if(key_table.get(event.keysym)):
            return key_table.get(event.keysym)
        elif(self.isKeypad(event.keycode, event.keysym)):
            key = keyboard.KeyCode().from_vk(event.keycode)
            return key
        elif(event.char != "" and event.char.isascii()):
            key =  keyboard.Listener().canonical(keyboard.KeyCode().from_char(char=event.char))
            return key

    def convertToKeyDarwin(self, event):
        if(key_table.get(event.keysym)):
            return key_table.get(event.keysym)
        elif(self.isKeypad(event.keycode, event.keysym)):
            keyVK = hotkey.darwin_keypad[int(event.keysym.split("_")[1])]
            key = keyboard.KeyCode.from_vk(keyVK)
            return key
        elif(event.char != "" and event.char.isascii()):
            key =  keyboard.Listener().canonical(keyboard.KeyCode().from_char(char=event.char))
            return key