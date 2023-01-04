import hotkey as hk

class Tool:
    def __init__(self, toolName, hotKey, position):
        self.toolName = toolName
        self.hotKey = hotKey
        self.position = position
    
    def serialize(self):
        return [self.toolName, self.hotKey.serialize(), self.position]
    
    def __str__(self):
        return f"{self.toolName} {self.hotKey} {self.position}"

    def __eq__(self, other):
        return ( (self.toolName == other.toolName) and (self.hotKey == other.hotKey) and (self.position == other.position) )
    
def deserialize(serializedObject):
    return Tool(toolName=serializedObject[0], hotKey=hk.deserialize(serializedObject[1]), position=tuple(serializedObject[2]))