import pynput

hotKeyLookup = {
    str(pynput.keyboard.Key.alt): "Alt",
    str(pynput.keyboard.Key.ctrl): "Ctrl",
    str(pynput.keyboard.Key.shift): "Shift",
}

class HotKey:
    def __init__(self, combination=set()):
        self.combination = combination

    def serialize(self):
        serializedCombination = []
        for key in self.combination:
            if(type(key) == pynput.keyboard.Key):
                # Convert to a string value and remove the first and last character, then convert to an integer
                key = int(str(key.value)[1:-1])
                serializedCombination.append(key)
            else:
               serializedCombination.append(str(key.char))
        return serializedCombination
    
    def format(self):
        formattedHotkey = []
        for key in self.combination:
            if(str(key) in hotKeyLookup.keys()):
                formattedHotkey.insert(0, hotKeyLookup[str(key)])
            elif(type(key) == pynput.keyboard.KeyCode):
                formattedHotkey.append(str(key.char))
        
        for c in formattedHotkey:
            if(len(c) == 1):
                poppedKey = formattedHotkey.pop(formattedHotkey.index(c))
                formattedHotkey.insert(len(formattedHotkey), poppedKey)

        return '+'.join(formattedHotkey)
    
    def compare(self, keyCombination):
        if(self.combination == keyCombination):
            return True
        return False
    
    def __str__(self):
        return f'HotKey({self.combination})'
    
    def __eq__(self, other):
        return self.combination == other.combination

def deserialize(hotkey):
    deserializedCombination = set()
    for key in hotkey:
        if(type(key) == str):
            deserializedCombination.add(pynput.keyboard.KeyCode(char=key) )
        else:
            deserializedCombination.add(pynput.keyboard.Key(pynput.keyboard.KeyCode.from_vk(key)))
    
    return HotKey(combination=deserializedCombination)

def parse(combination):
    parsedCombinaton = set()

    for key in combination.split("+"):
        if(key == "Shift"):
            parsedCombinaton.add(pynput.keyboard.Key.shift)
        elif(key == "Alt"):
            parsedCombinaton.add(pynput.keyboard.Key.alt)
        elif(key == "Ctrl"):
            parsedCombinaton.add(pynput.keyboard.Key.ctrl)
        else:
            parsedCombinaton.add(pynput.keyboard.KeyCode(char=key))
    return HotKey(combination=parsedCombinaton)
