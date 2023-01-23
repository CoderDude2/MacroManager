import json
import os
import threading
import time
from copy import deepcopy
from sys import platform

from pynput import keyboard, mouse
from pynput.keyboard import _NORMAL_MODIFIERS

import hotkey
from tool import deserialize

class MacroManager:
    def __init__(self, escape_sequence_callback=None):
        self.tools = self.loadFromJson()
        self.run = True
        self.action_ran = False

        self.isListening = True
        self.is_listening_to_escape_sequence = True
        self.escape_sequence_callback = escape_sequence_callback

        self.current = set()
        threading.Thread(target=self.listen).start()
    
    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if(hasattr(key, 'name')):
            if(key.value in _NORMAL_MODIFIERS.keys()):
                key = keyboard.Listener().canonical(key)
                self.current.add(key)
            else:
                self.current.add(key)
        elif(hasattr(key, 'vk') and (hotkey.isNumpad(key.vk))):
            key = keyboard.KeyCode.from_vk(key.vk)
            self.current.add(key)
        else:
            key = keyboard.Listener().canonical(key)
            self.current.add(key)

        if(self.current == set([keyboard.Key.shift, keyboard.Key.esc])):
            if(self.is_listening_to_escape_sequence and self.escape_sequence_callback):
                self.escape_sequence_callback()
        
        if(self.isListening):
            self.checkHotkey()
        return self.run

    def on_release(self, key):
        if(hasattr(key, 'name')):
            if(key.value in _NORMAL_MODIFIERS.keys()):
                key = keyboard.Listener().canonical(key)
        elif(hasattr(key, 'vk') and (hotkey.isNumpad(key.vk))):
            key = keyboard.KeyCode.from_vk(key.vk)
        else:
            key = keyboard.Listener().canonical(key)
        
        if(key in self.current):
            self.current.remove(key)
        
        if(len(self.current) == 1 and platform == "darwin"):
            self.current.clear()
        
        if(self.action_ran):
            self.action_ran = False

    def enable_listening(self, callback=None):
        self.isListening = True

    def disable_listening(self, callback=None):
        self.isListening = False

    def toggle_listening(self):
        if(self.isListening):
            self.disable_listening()
        else:
            self.enable_listening()

    def disable_escape_sequence_listening(self):
        self.is_listening_to_escape_sequence = False

    def enable_escape_sequence_listening(self):
        self.is_listening_to_escape_sequence = True

    def checkHotkey(self):
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

        self.action_ran = True

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
        if(os.path.exists("./tools.json")):
            with open('tools.json', 'r') as file:
                object = json.load(file)
            deserializedTools = [deserialize(entry) for entry in object]
            return deserializedTools
        return []
