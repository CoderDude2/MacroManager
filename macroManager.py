from pynput import keyboard, mouse
from tool import Tool
import time

class MacroManager:
    def __init__(self, tools=[]):
        self.tools = tools
        self.hotKeysDict = {}

    def startListening(self):
        self.updateListener()
        listener = keyboard.GlobalHotKeys(hotkeys=self.hotKeysDict)
        listener.start()
        # listener.join()

    def addTool(self, tool):
        print("Tool List:")
        tool.hotKey = '+'.join([f'<{key.lower()}>' if len(key) > 1 else key.lower() for key in tool.hotKey.split(' ')])
        self.tools.append(tool)
        for t in self.tools:
            print(t.toolName, t.hotKey, t.position)
        self.hotKeysDict[tool.hotKey] = lambda:self.activate(self.position)
        print("Tool Dictionary")
        for hK in self.hotKeysDict:
            print(hK)
    
    def updateListener(self):
        hotKeys = [tool.hotKey for tool in self.tools]
        position = [tool.position for tool in self.tools]
        for i in zip(hotKeys, position):
            self.hotKeysDict[i[0]] = lambda:self.activate(i[1])

    def activate(self, position):
        mouseController = mouse.Controller()
        delay = 0.05
        previousPosition = mouseController.position

        mouseController.position = position
        time.sleep(delay)
        mouseController.click(mouse.Button.left)
        time.sleep(delay)
        mouseController.position = previousPosition

        

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