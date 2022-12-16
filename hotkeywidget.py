import tkinter as tk
from pynput import keyboard
import hotkey

allowedKeys = [
    keyboard.Key.shift,
    keyboard.Key.shift_l,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.alt_gr,
]

class HotkeyWidget(tk.Frame):
    def __init__(self, master=None, hotKey=None):
        super().__init__(master)
        self.isActive = False
            
        if(hotKey != None):
            self.hotKey = hotKey
        else:
            self.hotKey = hotkey.HotKey()
        
        self.hotKeyLabel = tk.Label(self, text=self.hotKey.format(), width=15, background="grey")
        self.toggleButton = tk.Button(self, text="Set Hotkey", command=self.toggleHotkeyRecording)

        self.hotKeyLabel.pack(side=tk.LEFT)
        self.toggleButton.pack(side=tk.LEFT)
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def on_press(self, key):
        if(self.isActive):
                self.hotKey.combination.add(key)
                self.hotKeyLabel.configure(text=self.hotKey.format())
        if(len(self.hotKey.combination) >= 2):
            self.toggleButton.configure(state=tk.NORMAL)
    
    def getHotkey(self):
        pass

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

root = tk.Tk()

h = HotkeyWidget()
h.pack()

root.mainloop()