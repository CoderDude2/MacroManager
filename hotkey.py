from pynput.keyboard import Key, KeyCode

hotKeyLookup = {
    str(Key.alt): "Alt",
    str(Key.ctrl): "Ctrl",
    str(Key.shift): "Shift",
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
               serializedCombination.append(str(key.char))
        return serializedCombination
    
    def format(self):
        formattedHotkey = []
        for key in self.combination:
            if(str(key) in hotKeyLookup.keys()):
                formattedHotkey.insert(0, hotKeyLookup[str(key)])
            elif(type(key) == KeyCode):
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
            deserializedCombination.add(KeyCode(char=key) )
        else:
            deserializedCombination.add(Key(KeyCode.from_vk(key)))
    
    return HotKey(combination=deserializedCombination)

def parse(combination):
    parsedCombinaton = set()

    for key in combination.split("+"):
        if(key == "Shift"):
            parsedCombinaton.add(Key.shift)
        elif(key == "Alt"):
            parsedCombinaton.add(Key.alt)
        elif(key == "Ctrl"):
            parsedCombinaton.add(Key.ctrl)
        else:
            parsedCombinaton.add(KeyCode(char=key))
    return HotKey(combination=parsedCombinaton)