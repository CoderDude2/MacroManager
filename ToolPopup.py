import tkinter as tk
from pynput import mouse

from hotkeywidget import HotkeyWidget
from tool import Tool

class ToolPopup(tk.Toplevel):
    def __init__(self, master=None, title=None, submitButtonText=None, on_submit=None, on_cancel=None, tool=None):
        # ------------------------------------[ Popup Window Configuration ]------------------------------------
        super().__init__(master)
        if(title is not None):
            self.title(title)
        else:
            self.title("Tool Popup")
        self.geometry("350x350")
        self.config(padx=10, pady=10)
        self.resizable(False, False)

        # ------------------------------------[ Variables ]------------------------------------

        self.toolName = tk.StringVar()
        self.xPosition = tk.IntVar()
        self.yPosition = tk.IntVar()

        if(tool is not None):
            self.toolName.set(tool.toolName)
            self.xPosition.set(tool.position[0])
            self.yPosition.set(tool.position[1])
            self.hotKey = tool.hotKey

        self.isTrackingMouse = False

        self.on_submit = on_submit
        self.on_cancel = on_cancel

        # ------------------------------------[ Column and Row Configuration ]------------------------------------
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # ------------------------------------[ Widgets ]------------------------------------
        self.toolNameLabel = tk.Label(self, text="Tool Name")
        self.toolNameEntry = tk.Entry(self, textvariable=self.toolName)

        hotKeyLabel = tk.Label(self, text="Hotkey")
        if(tool is not None):
            self.hotkeyWidget = HotkeyWidget(self, hotKey=tool.hotKey)
        else:
            self.hotkeyWidget = HotkeyWidget(self)

        positionLabel = tk.Label(self, text="Position")

        xLabel = tk.Label(self,text="X")
        xEntry = tk.Entry(self, width=5, textvariable=self.xPosition)

        yLabel = tk.Label(self,text="Y")
        yEntry = tk.Entry(self, width=5, textvariable=self.yPosition)

        setPositionButton = tk.Button(self, text="Set", command=self.enableMouseTracking)

        buttonContainer = tk.Frame(self)
        cancelButton = tk.Button(buttonContainer, text="Cancel", command=self.cancelButton)
        if(submitButtonText is not None):
            submitButton = tk.Button(buttonContainer, text=submitButtonText, command=self.submitButton)
        else:
            submitButton = tk.Button(buttonContainer, text="Create", command=self.submitButton)

        # ------------------------------------[ Widget Placement ]------------------------------------
        # ROW 0
        self.toolNameLabel.grid(row=0, column=0, sticky='w')
        self.toolNameEntry.grid(row=0, column=1, columnspan=5, sticky='ew')
        # ROW 1
        hotKeyLabel.grid(row=1, column=0, sticky='w')
        self.hotkeyWidget.grid(row=1, column=1, columnspan=5, sticky='w')
        # ROW 2
        positionLabel.grid(row=2, column=0, sticky='w')
        xLabel.grid(row=2, column=1)
        xEntry.grid(row=2, column=2, sticky='w')
        yLabel.grid(row=2, column=3)
        yEntry.grid(row=2, column=4, sticky='w')
        setPositionButton.grid(row=2, column=5, sticky='w')
        # ROW 3
        cancelButton.pack(side='left', fill='x', expand=True)
        submitButton.pack(side='right', fill='x', expand=True)
        buttonContainer.grid(row=3, column=0,columnspan=6,sticky='ew')

        # ------------------------------------[ Event Handling ]------------------------------------
        self.mouseController = mouse.Controller()

        self.bind("<Motion>", self.setPosition)
        self.bind("<space>", self.disableMouseTracking)
    
    def setPosition(self, event=None):
        if(self.isTrackingMouse):
            mousePosition = self.mouseController.position
            self.xPosition.set( round(mousePosition[0]) )
            self.yPosition.set( round(mousePosition[1]) )

    def enableMouseTracking(self, event=None):
        self.isTrackingMouse = True
    
    def disableMouseTracking(self, event=None):
        self.isTrackingMouse = False
    
    def getTool(self):
        return Tool(self.toolName.get(), self.hotkeyWidget.getHotkey(), (self.xPosition.get(), self.yPosition.get()))

    def submitButton(self):
        self.withdraw()
        if(self.on_submit is not None):
            self.on_submit(self.getTool())
        self.destroy()
    
    def cancelButton(self):
        if(self.on_cancel is not None):
            self.on_cancel()
        self.destroy()