import pynput
from sys import platform

hotKeyLookup = {
    str(pynput.keyboard.Key.alt): "Alt",
    str(pynput.keyboard.Key.ctrl): "Ctrl",
    str(pynput.keyboard.Key.shift): "Shift",
}

win32_numpad = list(range(96, 106))

# For some reason the Apple numpad is sequential up to 7, than it skips a vk and continues
darwin_numpad = list(range(82, 90)) + [91,92]

class HotKey:
    def __init__(self, combination=set()):
        self.combination = combination

    def serialize(self):
        serializedCombination = []
        for key in self.combination:
            if(isinstance(key, pynput.keyboard.Key)):
                # Convert the key to its associated vk
                key = int(str(key.value)[1:-1])
                serializedCombination.append(key)
            elif(isNumpad(key.vk)):
                serializedCombination.append(key.vk)
            else:
               serializedCombination.append(str(key.char))
        return serializedCombination
    
    def format(self):
        formattedHotkey = []
        for key in self.combination:
            if(str(key) in hotKeyLookup.keys()):
                formattedHotkey.insert(0, hotKeyLookup[str(key)])
            elif(hasattr(key, 'vk') and isNumpad(key.vk)):
                if(platform == "win32"):
                    formattedHotkey.append(f'Num{str(key.vk-96)}')
                elif(platform == "darwin"):
                    if(key.vk < 90):
                        formattedHotkey.append(f'Num{str(key.vk-82)}')
                    else:
                        formattedHotkey.append(f'Num{str(key.vk-83)}')
            elif(isinstance(key, pynput.keyboard.KeyCode)):
                formattedHotkey.append(str(key.char))
        
        # If the key is a character, move it to the front of the list
        for key in formattedHotkey:
            if(len(key) == 1):
                poppedKey = formattedHotkey.pop(formattedHotkey.index(key))
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
        if(isinstance(key, str)):
            deserializedCombination.add(pynput.keyboard.KeyCode(char=key))
        elif(key in win32_numpad or key in darwin_numpad):
            deserializedCombination.add(pynput.keyboard.KeyCode.from_vk(key))
        else:
            deserializedCombination.add(pynput.keyboard.Key( pynput.keyboard.KeyCode.from_vk(key)) )
    
    return HotKey(combination=deserializedCombination)

def isNumpad(vk):
        if(platform == "win32" and vk in win32_numpad):
            return True
        elif(platform == "darwin" and vk in darwin_numpad):
            return True
        return False

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
