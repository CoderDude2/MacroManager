import gui
import macroManager
from tool import Tool

tools = [
    Tool("Extrude Tool", "<ctrl>+e", (0,0)),
    Tool("Trim Tool", "<ctrl>+x", (200,200)),
    Tool("Line Tool", "<ctrl>+l", (300,300)),
]

app = gui.App()

macroManager = macroManager.MacroManager(app.getTools())
macroManager.startListening()

app.mainloop()