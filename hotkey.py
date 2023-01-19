from sys import platform

import pynput

allowed_keys = ["shift", "alt", "ctrl", "space", "tab", "cmd"]

win32_numpad = list(range(96, 106))
win32_function_keys = list(range(112,123))
# For some reason the Apple numpad is sequential up to 7, then it skips a vk and continues
darwin_numpad = list(range(82, 90)) + [91,92]

class HotKey:
    def __init__(self, combination=set()):
        self.combination = combination

    def serialize(self):
        serializedCombination = []

        for key in self.combination:
            print(self.combination)
            if(key == pynput.keyboard.Key.space):
                serializedCombination.append(key.name)
            elif(hasattr(key, 'value')):
                serializedCombination.append(key.value.vk)
            elif(hasattr(key, 'vk') and key.vk != None):
                if(isNumpad(key.vk)):
                    serializedCombination.append(key.vk)
            elif(hasattr(key, 'char') and key.char != None):
                serializedCombination.append(str(key.char))
        
        return serializedCombination
    
    def format(self):
        formattedHotkey = []
        for key in self.combination:
            if(hasattr(key, "name") and key.name in allowed_keys):
                if(key.name == "cmd" and platform == "win32"):
                    formattedHotkey.append("Win")
                else:
                    formattedHotkey.insert(0, key.name.title())
            elif(hasattr(key, 'vk') and isNumpad(key.vk) and platform == "win32"):
                formattedHotkey.append(f'Num{key.vk-96}')
            elif(hasattr(key, 'vk') and isNumpad(key.vk) and platform == "darwin"):
                if(key.vk < 90):
                    formattedHotkey.append(f'Num{key.vk-82}')
                else:
                    formattedHotkey.append(f'Num{key.vk-83}')
            elif(hasattr(key, 'vk') and isFunctionKey(key.vk)):
                formattedHotkey.append(f'F{key.vk-111}')
            elif(hasattr(key, 'char')):
                formattedHotkey.append(key.char)
        
        # If the key is a character, move it to the end of the list.
        for key in formattedHotkey:
            if(len(key) == 1):
                poppedKey = formattedHotkey.pop(formattedHotkey.index(key))
                formattedHotkey.insert(len(formattedHotkey), poppedKey)

        return '+'.join(formattedHotkey)
    
    def compare(self, keyCombination):
        return self.combination == keyCombination

    def __str__(self):
        return f'HotKey({self.combination})'
    
    def __eq__(self, other):
        return self.combination == other.combination

def deserialize(hotkey):
    deserializedCombination = set()
    for key in hotkey:
        if(isinstance(key, str)):
            if(key == "space"):
                deserializedCombination.add(pynput.keyboard.Key.space)
            else:
                deserializedCombination.add(pynput.keyboard.KeyCode(char=key))
        elif(key in win32_numpad or key in darwin_numpad):
            deserializedCombination.add(pynput.keyboard.KeyCode.from_vk(key))
        elif(key in win32_function_keys):
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

def isFunctionKey(vk):
    if(platform == "win32" and vk in win32_function_keys):
        return True