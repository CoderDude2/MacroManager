import hotkey as hk

class Tool:
    def __init__(self, toolName, hotKey, position, double_click=False):
        self.toolName = toolName
        self.hotKey = hotKey
        self.position = position
        self.double_click = double_click
    
    def serialize(self):
        return [self.toolName, self.hotKey.serialize(), self.position, self.double_click]
    
    def __str__(self):
        return f"{self.toolName} {self.hotKey} {self.position}"

    def __eq__(self, other):
        return ( (self.toolName == other.toolName) and (self.hotKey == other.hotKey) and (self.position == other.position) )
    
def deserialize(serializedObject):
    try:
        return Tool(toolName=serializedObject[0], hotKey=hk.deserialize(serializedObject[1]), position=tuple(serializedObject[2]), double_click=serializedObject[3])
    except IndexError:
        return Tool(toolName=serializedObject[0], hotKey=hk.deserialize(serializedObject[1]), position=tuple(serializedObject[2]))