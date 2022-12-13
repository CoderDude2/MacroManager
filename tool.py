class Tool:
    def __init__(self, toolName, hotKey, position):
        self.toolName = toolName
        self.hotKey = hotKey
        self.position = position
    
    def serialize(self):
        return [self.toolName, self.hotKey, self.position]
    
def deserialize(serializedObject):
    return Tool(name=serializedObject[0], hotKey=serializedObject[1], position=serializedObject[2])