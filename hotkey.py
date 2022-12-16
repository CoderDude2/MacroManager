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
    def __init__(self, combination=set()):
        self.combination = combination

    def serialize(self):
        serializedCombination = []
        for key in self.combination:
            if(type(key) == Key):
                # Convert to a string value and remove the first and last character, then convert to an integer
                key = int(str(key.value)[1:-1])
                serializedCombination.append(key)
            else:
               serializedCombination.append(key)
        return serializedCombination
    
    def format(self):
        formattedHotkey = []
        for key in self.combination:
            if(str(key) in hotKeyLookup.keys()):
                formattedHotkey.append(hotKeyLookup[str(key)])
            elif(type(key) == KeyCode):
                formattedHotkey.append(str(key.char))
        return '+'.join(formattedHotkey)
    
    def compare(self, keyCombination):
        if(self.combination == keyCombination):
            return True
        return False
    
    def __str__(self):
        return f'HotKey({self.combination})'

def deserialize(hotkey):
    deserializedCombination = []
    for key in hotkey:
        if(type(key) == str):
            deserializedCombination.append(KeyCode(char=key) )
        else:
            deserializedCombination.append(Key(KeyCode.from_vk(key)))
    
    return HotKey(hotkey=deserializedCombination)