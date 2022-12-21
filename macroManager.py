import json
import pyautogui
from Listener import Listener
from tool import deserialize

class MacroManager:
    def __init__(self, tools=[]):
        self.listener = Listener(onPress=self.checkHotkey)
        self.tools = tools

        self.listener.startListener()
        self.run = True
    
    def checkHotkey(self):
        for tool in self.tools:
            if(tool.hotKey.compare(self.listener.current)):
                self.activate(tool.position)

    def addTool(self, tool):
        self.tools.append(tool)

    def removeTool(self, index):
        self.tools.pop(index)

    def activate(self, position):
        originalPosition = pyautogui.position()
        pyautogui.click(position[0], position[1])
        pyautogui.moveTo(originalPosition.x, originalPosition.y)

def saveToJson(contents):
    serializedTools = [tool.serialize() for tool in contents]
    json_object = json.dumps(serializedTools, indent=4)
    with open('tools.json', "w") as file:
        file.write(json_object)

def loadFromJson():
    with open('tools.json', 'r') as file:
        object = json.load(file)
    deserializedTools = [deserialize(entry) for entry in object]
    return deserializedTools