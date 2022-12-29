import threading
import json
from os.path import exists

import pyautogui

from pynput import keyboard
from tool import Tool, deserialize
import hotkey

class MacroManager:
    def __init__(self):
        self.tools = self.loadFromJson()
        self.run = True
        self.isListening = True

        self.current = set()
        threading.Thread(target=self.listen).start()
    
    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if(hasattr(key, 'vk') and hotkey.isNumpad(key.vk)):
            key = keyboard.KeyCode.from_vk(key.vk)
        else:
            key = keyboard.Listener().canonical(key)
        self.current.add(key)
        if(self.isListening):
            self.checkHotkey()
        return self.run

    def on_release(self, key):
        if(hasattr(key, 'vk') and hotkey.isNumpad(key.vk)):
            key = keyboard.KeyCode.from_vk(key.vk)
        else:
            key = keyboard.Listener().canonical(key)
        if(key in self.current):
            self.current.remove(key)
        if(len(self.current) == 1):
            self.current.clear()

    def checkHotkey(self):
        for tool in self.tools:
            if(tool.hotKey.compare(self.current)):
                self.activate(tool.position)

    def addTool(self, tool):
        self.tools.append(tool)

    def duplicateTool(self, index):
        tool = self.tools[index]
        toolName = f'{tool.toolName} copy'
        hotKey = hotkey.HotKey(combination=tool.hotKey.combination)
        position = tool.position
        self.tools.append(Tool(toolName, hotKey ,position))

    def removeTool(self, index):
        self.tools.pop(index)

    def activate(self, position):
        originalPosition = pyautogui.position()
        pyautogui.click(position[0], position[1])
        pyautogui.moveTo(originalPosition.x, originalPosition.y)

    def stop(self):
        self.saveToJson()
        self.run = False
        keyboard.Controller().press(keyboard.Key.shift)
        keyboard.Controller().release(keyboard.Key.shift)
    
    def saveToJson(self):
        serializedTools = [tool.serialize() for tool in self.tools]
        json_object = json.dumps(serializedTools, indent=4)
        with open('tools.json', "w+") as file:
            file.write(json_object)

    def loadFromJson(self):
        # Use the os module to determine if the tools.json file exists
        if(exists("./tools.json")):
            with open('tools.json', 'r') as file:
                object = json.load(file)
            deserializedTools = [deserialize(entry) for entry in object]
            return deserializedTools
        return []