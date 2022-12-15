from pynput.keyboard import Key, KeyCode

hotKeyLookup = {
    str(Key.alt_gr): "Alt",
    str(Key.alt_l): "Alt",
    str(Key.alt_r): "Alt",
    str(Key.alt): "Alt",
    str(Key.ctrl): "Ctrl",
    str(Key.ctrl_l): "Ctrl",
    str(Key.ctrl_r): "Ctrl",
    str(Key.shift): "Shift",
    str(Key.shift_l): "Shift",
    str(Key.shift_r): "Shift"
}

class HotKey:
    def __init__(self, hotkey=[]):
        self.hotkey = hotkey

    def serialize(self):
        serializedCombination = []
        for key in self.hotkey:
            if(type(key) == Key):
                # Convert to a string value and remove the first and last character, then convert to an integer
                key = int(str(key.value)[1:-1])
                serializedCombination.append(key)
            else:
               serializedCombination.append(key)
        return serializedCombination
    
    def format(self):
        formattedHotkey = ""
        for key in self.hotkey:
            if(str(key) in hotKeyLookup.keys()):
                formattedHotkey += hotKeyLookup[str(key)] + ' + '
            elif(str(key).isalpha()):
                formattedHotkey += str(key)
        return formattedHotkey
    
    def __str__(self):
        return f'HotKey({self.hotkey})'

def deserialize(hotkey):
    deserializedCombination = []
    for key in hotkey:
        if(type(key) == str):
            deserializedCombination.append(KeyCode(char=key) )
        else:
            deserializedCombination.append(Key(KeyCode.from_vk(key)))
    
    return HotKey(hotkey=deserializedCombination)