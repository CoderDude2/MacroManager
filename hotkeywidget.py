import tkinter as tk
import hotkey

class HotkeyWidget(tk.Frame):
    def __init__(self, master=None, hotKey=None):
        super().__init__(master)
        self.isActive = False

        self.combination = []
        self.hotKey = tk.StringVar()

        if(hotKey):
            self.hotKey.set(hotKey)
        
        self.hotKeyLabel = tk.Label(self, textvariable=self.hotKey, width=15, background="grey")
        self.toggleButton = tk.Button(self, text="Set Hotkey", command=self.toggleHotkeyRecording)

        self.hotKeyLabel.pack(side=tk.LEFT)
        self.toggleButton.pack(side=tk.LEFT)

    def record(self):
        pass
    
    def getHotkey(self):
        pass

    def activate(self):
        self.toggleButton.configure(state=tk.DISABLED, text="Save")
        self.combination = []
        self.hotKey.set("")

        self.isActive = True
    
    def deActivate(self):
        self.isActive = False
        self.toggleButton.configure(text="Set Hotkey")

    def toggleHotkeyRecording(self):
        if(not self.isActive):
            self.activate()
            return
        self.deActivate()