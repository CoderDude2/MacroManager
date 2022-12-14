class HotKey:
    def __init__(self, hotkey=[]):
        self.hotkey = hotkey
    
    def getFormattedHotkey(self):
        # Return a format that looks nice on a GUI
        pass
    
    def getHotkey(self):
        formattedHotkey = ""
        for key in self.hotkey:
            if(len(key) > 1):
                formattedHotkey += f'<{key}>+'
            else:
                formattedHotkey += key
        return formattedHotkey