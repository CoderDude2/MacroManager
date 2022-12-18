from pynput import keyboard
import pyautogui
from tool import deserialize
import json

class MacroManager:
    def __init__(self, tools=[]):
        self.tools = tools
        self.current = set()
        
    def startListening(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
    
    def on_press(self, key):
        key = keyboard.Listener.canonical(keyboard.Listener(), key)
        self.current.add(key)
        for tool in self.tools:
            if(tool.hotKey.compare(self.current)):
                self.activate(tool.position)
    
    def on_release(self, key):
        key = keyboard.Listener.canonical(keyboard.Listener(), key)
        if(key in self.current):
            self.current.remove(key)
        if(len(self.current) <= 1):
            self.current.clear()

    def addTool(self, tool):
        self.tools.append(tool)

    def removeTool(self, index):
        self.tools.pop(index)

    def activate(self, position):
        originalPosition = pyautogui.position()
        pyautogui.moveTo(position[0], position[1])
        pyautogui.click()
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