import tkinter as tk

hotKeyLookUp = {
    "Shift_L":"Shift",
    "Shift_R":"Shift",
    "Control_L":"Ctrl",
    "Control_R":"Ctrl",
    "Alt_L":"Alt",
    "Alt_R":"Alt",
}

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

    def record(self, event):
        if(self.isActive):
            if(event.keysym in hotKeyLookUp.keys()):
                pressedKey = hotKeyLookUp[event.keysym]
                if(pressedKey not in self.combination):
                    self.combination.append(pressedKey)
            else:
                pressedKey = event.char.upper()
                if(pressedKey != '' and pressedKey not in self.combination):
                    self.combination.append( event.char.upper() )
            self.hotKey.set(' + '.join(self.combination))
        
        if(len(self.combination) > 1):
            self.toggleButton.configure(state=tk.NORMAL)
        if(len(self.combination) == 3):
            self.deActivate()
    
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
    
    def getHotkey(self):
        hotKey = []
        for key in self.combination:
            if(key in hotKeyLookUp.values()):
                hotKey.append(f"<{key}>")
            else:
                hotKey.append(key)
        return '+'.join(hotKey)