from pynput import keyboard
import pyautogui
from tool import Tool
import hotkey

class MacroManager:
    def __init__(self, tools=[]):
        self.tools = tools
        self.current = set()

    def startListening(self):
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
        listener.join()

    def on_press(self, key):
        self.current.add(key)
        for tool in self.tools:
            if(tool.hotKey.compare(self.current)):
                self.activate(tool.position)
    
    def on_release(self, key):
        if(key in self.current):
            self.current.remove(key)

    def addTool(self, tool):
        self.tools.append(tool)

    def activate(self, position):
        originalPosition = pyautogui.position()
        pyautogui.moveTo(position[0], position[1])
        pyautogui.click()
        pyautogui.moveTo(originalPosition.x, originalPosition.y)

# mM = MacroManager(tools)
# mM.startListening()

# def saveToJson(contents):
#     serializedHotkeys = [i.serialize() for i in contents]
#     json_object = json.dumps(serializedHotkeys, indent=4)
#     with open('hotkeys.json', "w") as file:
#         file.write(json_object)

# def loadFromJson():
#     with open('hotkeys.json', 'r') as file:
#         object = json.load(file)
    
#     deserializedHotkeys = [deserialize(entry) for entry in object]

#     return deserializedHotkeys

# def formatHotKeys(hotKeyList):
#     formattedHotkeys = {}
#     for i,h in enumerate(hotKeyList):
#         formattedHotkeys[f'{h.hotKey}'] = h.execute

#     return formattedHotkeys