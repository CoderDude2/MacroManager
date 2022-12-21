import tkinter as tk
from pynput import keyboard
import hotkey

class HotkeyWidget(tk.Frame):
    def __init__(self, master=None, listener=None, hotKey=None):
        super().__init__(master)

        self.isActive = False
        if(hotKey is None):
            self.hotKey = hotkey.HotKey()
        else:
            self.hotKey = hotKey
        
        self.hotKeyLabel = tk.Label(self, text=self.hotKey.format(), width=15, background="grey")
        self.toggleButton = tk.Button(self, text="Set Hotkey", command=self.toggleHotkeyRecording)

        self.hotKeyLabel.pack(side=tk.LEFT)
        self.toggleButton.pack(side=tk.LEFT)

        self.listener = listener

    def record(self, event):
        self.hotKey = self.listener.getRecordedHotkey()
        self.hotKeyLabel.config(text=self.hotKey.format())
        
        if(len(self.hotKey.combination) > 1):
            self.toggleButton.configure(state=tk.NORMAL)
        if(len(self.hotKey.combination) == 3):
            self.deActivate()

    def getHotkey(self):
        return self.hotKey

    def activate(self):
        self.master.focus_set()
        self.master.bind("<KeyPress>", self.record)
        self.listener.enableRecording()

        self.toggleButton.configure(state=tk.DISABLED, text="Save")
        self.hotKeyLabel.config(text="")

        self.hotKey.combination = set()
        self.isActive = True

    def deActivate(self):
        self.isActive = False
        self.listener.disableRecording()
        self.toggleButton.configure(text="Set Hotkey")

    def toggleHotkeyRecording(self):
        if(not self.isActive):
            self.activate()
            return
        self.deActivate()