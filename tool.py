import hotkey

class Tool:
    def __init__(self, toolName, hotKey, position):
        self.toolName = toolName
        self.hotKey = hotKey
        self.position = position
    
    def serialize(self):
        return [self.toolName, self.hotKey.serialize(), self.position]
    
def deserialize(serializedObject):
    return Tool(toolName=serializedObject[0], hotKey=hotkey.deserialize(serializedObject[1]), position=serializedObject[2])