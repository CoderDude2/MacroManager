from pynput import mouse
import time

delay = 0.05
m = mouse.Controller()

def setCursorPosition(position):
    m.position = position

def leftClick():
    m.click(mouse.Button.left)

class HotKey:
    def __init__(self, name, hotKey, position):
        self.name = name
        self.hotKey = hotKey
        self.position = position

    def execute(self):
        print(self.hotKey)
        previousPosition = m.position

        setCursorPosition(self.position)
        time.sleep(delay)
        leftClick()
        time.sleep(delay)
        setCursorPosition(previousPosition)
    
    def serialize(self):
        return [self.name, self.hotKey, self.position]
    
def deserialize(serializedObject):
    return HotKey(name=serializedObject[0], hotKey=serializedObject[1], position=serializedObject[2])
