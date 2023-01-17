import json
import os
import threading
import time
from copy import deepcopy

from pynput import keyboard, mouse

import hotkey
from tool import deserialize

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
        if(hasattr(key, 'vk') and (hotkey.isNumpad(key.vk) or hotkey.isFunctionKey(key.vk))):
            key = keyboard.KeyCode.from_vk(key.vk)
        elif(hasattr(key, 'name') and key.name == "space"):
            key = keyboard.Key.space
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
        # [self.activate(tool.position) for tool in self.tools if tool.hotKey.compare(self.current)]
        for tool in self.tools:
            if(tool.hotKey.compare(self.current)):
                self.activate(tool.position, tool.double_click)

    def addTool(self, tool):
        self.tools.append(tool)

    def duplicateTool(self, index):
        tool = deepcopy(self.tools[index])
        self.tools.append(tool)

    def removeTool(self, index):
        self.tools.pop(index)

    def activate(self, position, double_click=False):
        mouse_controller = mouse.Controller()

        originalPosition = mouse_controller.position

        mouse_controller.position = position
        time.sleep(0.01)
        if(double_click):
            mouse_controller.click(mouse.Button.left)
            mouse_controller.click(mouse.Button.left)
        else:
            mouse_controller.click(mouse.Button.left)
        mouse_controller.position = originalPosition

    def stop(self):
        self.saveToJson()
        self.run = False
        keyboard.Controller().tap(keyboard.Key.shift)
    
    def saveToJson(self):
        serializedTools = [tool.serialize() for tool in self.tools]
        json_object = json.dumps(serializedTools, indent=4)
        with open('tools.json', "w+") as file:
            file.write(json_object)

    def loadFromJson(self):
        # Use the os module to determine if the tools.json file exists
        if(os.path.exists("./tools.json")):
            with open('tools.json', 'r') as file:
                object = json.load(file)
            deserializedTools = [deserialize(entry) for entry in object]
            return deserializedTools
        return []