import tkinter as tk
from tkinter import ttk
from tool import Tool
from hotkeywidget import HotkeyWidget
from sys import platform
from pynput import mouse
from macroManager import MacroManager

class ToolList(ttk.Treeview):
	def __init__(self, master=None):
		super().__init__(master)

		self.config(columns=('tool_name', 'hotkey', 'position'), show='headings')

		self.heading('tool_name', text='Tool Name')
		self.heading('hotkey',text='Hotkey')
		self.heading('position', text='Position')
	
	def add_tool(self, tool):
		self.insert(parent='',index=tk.END, values=(tool.toolName, tool.hotKey, tool.position) )
	
	def edit_tool(self, tool):
		selected_item = self.selection()[0]
		self.item(selected_item, values=(tool.toolName, tool.hotKey, tool.position))

	def delete_tool(self, event=None):
		selected_item = self.selection()[0]
		self.delete(selected_item)
	
	def deslectAll(self):
		for item in self.selection():
			self.selection_remove(item)

class MenuBar(tk.Menu):
	def __init__(self, master=None):
		super().__init__(master)

		self.file_menu = tk.Menu(self, tearoff=False)

		self.add_cascade(label='File', menu=self.file_menu)

class App(tk.Tk):
	def __init__(self):
			# ------------------------------------[ App Intialization ]------------------------------------
			super().__init__()
			self.title("Macro Manager")
			self.geometry("600x500")

			self.grid_rowconfigure(0, weight=1)
			self.grid_columnconfigure(0, weight=1)

			# ------------------------------------[ Variables ]------------------------------------
			self.toolPopupIsActive = False
			self.isTracking = False
			self.macroManager = MacroManager()
			
			# ------------------------------------[ App Structure ]------------------------------------
			menuBar = MenuBar(self)
			menuBar.file_menu.add_command(label="New Tool", command=self.ToolPopup)
			self.config(menu=menuBar)

			self.toolList = ToolList(self)
			self.toolList.grid(row=0, column=0, sticky='news')
			self.toolList.add_tool(Tool("Extrude Tool", "Alt E", "0 0"))
			self.toolList.add_tool(Tool("Trim Tool", "Ctrl X", "800 800"))
			
			# ------------------------------------[ Event Handling ]------------------------------------
			self.bind("<Button-1>", self.LeftClick)
			self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

			if(platform == "win32"):
				self.bind("<Button-3>", self.RightClick)
			elif(platform == "darwin"):
				self.bind("<Button-2>", self.RightClick)
			
			self.bind("<Delete>", self.toolList.delete_tool)
			self.bind("<BackSpace>", self.toolList.delete_tool)

			mouseListener = mouse.Listener(on_move=self.update_coordinates)
			mouseListener.start()
			self.macroManager.startListening()
			
	def ToolPopup(self, createTool=True, tool=None):
		if(self.toolPopupIsActive == False):
			self.popupWindow = tk.Toplevel()
			self.toolPopupIsActive = True

		# ------------------------------------[ Variables ]------------------------------------
		self.toolName = tk.StringVar()
		self.xPosition = tk.IntVar()
		self.yPosition = tk.IntVar()

		if(not createTool):
			self.toolName.set(tool.toolName)
			self.xPosition.set(tool.position[0])
			self.yPosition.set(tool.position[1])

		if(createTool):
			self.popupWindow.title("New Tool")
		else:
			self.popupWindow.title("Edit Tool")
		
		# ------------------------------------[ Popup Window Configuration ]------------------------------------
		self.popupWindow.geometry("350x350")
		self.popupWindow.config(padx=10, pady=10)
		self.popupWindow.resizable(False, False)

		# ------------------------------------[ Column and Row Configuration ]------------------------------------
		self.popupWindow.columnconfigure(0, weight=1)
		self.popupWindow.columnconfigure(1, weight=1)
		self.popupWindow.columnconfigure(2, weight=1)
		self.popupWindow.columnconfigure(3, weight=1)
		self.popupWindow.columnconfigure(4, weight=1)

		self.popupWindow.rowconfigure(0, weight=1)
		self.popupWindow.rowconfigure(1, weight=1)
		self.popupWindow.rowconfigure(2, weight=1)
		self.popupWindow.rowconfigure(3, weight=1)

		# ------------------------------------[ Widgets ]------------------------------------
		toolNameLabel = tk.Label(self.popupWindow, text="Tool Name")
		toolNameEntry = tk.Entry(self.popupWindow, textvariable=self.toolName)

		hotKeyLabel = tk.Label(self.popupWindow, text="Hotkey")
		if(createTool):
			self.hotkeyWidget = HotkeyWidget(self.popupWindow)
		else:
			self.hotkeyWidget = HotkeyWidget(self.popupWindow, tool.hotKey)
		self.popupWindow.bind("<KeyPress>", self.hotkeyWidget.record)

		positionLabel = tk.Label(self.popupWindow, text="Position")

		xLabel = tk.Label(self.popupWindow,text="X")
		xEntry = tk.Entry(self.popupWindow, width=5, textvariable=self.xPosition)

		yLabel = tk.Label(self.popupWindow,text="Y")
		yEntry = tk.Entry(self.popupWindow, width=5, textvariable=self.yPosition)

		setPositionButton = tk.Button(self.popupWindow, text="Set", command=self.toggleOn)

		buttonContainer = tk.Frame(self.popupWindow)
		cancelButton = tk.Button(buttonContainer, text="Cancel", command=self.cancelButton)

		if(createTool):
			createToolButton = tk.Button(buttonContainer, text="Create", command=lambda: self.submitButton(createTool))
		else:
			createToolButton = tk.Button(buttonContainer, text="Save", command=lambda: self.submitButton(createTool))

		# ------------------------------------[ Widget Placement ]------------------------------------
		# ROW 0
		toolNameLabel.grid(row=0, column=0, sticky='w')
		toolNameEntry.grid(row=0, column=1, columnspan=5, sticky='ew')
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
		createToolButton.pack(side='right', fill='x', expand=True)
		buttonContainer.grid(row=3, column=0,columnspan=6,sticky='ew')

		# ------------------------------------[ Event Handling ]------------------------------------
		self.popupWindow.bind("<space>", self.toggleOff)

	def cancelButton(self):
		self.popupWindow.destroy()
		self.toolPopupIsActive = False

	def submitButton(self, createTool=True):
		tool = Tool(self.toolName.get(), self.hotkeyWidget.hotKey.get(), (self.xPosition.get(), self.yPosition.get()))
		if(createTool):
			self.toolList.add_tool(tool)
			self.macroManager.addTool(tool)
		else:
			self.toolList.edit_tool(tool)
		self.popupWindow.destroy()
		self.toolPopupIsActive = False

	def update_coordinates(self, x,y):
		if(self.isTracking):
			self.xPosition.set(x)
			self.yPosition.set(y)

	def toggleOn(self):
		self.isTracking = True

	def toggleOff(self, event):
		self.isTracking = False

	def RightClick(self, event):
		selectedItem = self.toolList.identify("item", event.x, event.y)
		if(selectedItem != ''):
			toolName = self.toolList.item(selectedItem)['values'][0]
			hotKey = self.toolList.item(selectedItem)['values'][1]
			position = [int(i) for i in self.toolList.item(selectedItem)['values'][2].split(' ')]
			tool = Tool(toolName, hotKey, position)

		rightClickMenu = tk.Menu(self, tearoff=False)
		rightClickMenu.add_command(label="Edit", command=lambda:self.ToolPopup(createTool=False, tool=tool))
		rightClickMenu.add_command(label="Delete", command=self.toolList.delete_tool)

		rightClickMenu2 = tk.Menu(self, tearoff=False)
		rightClickMenu2.add_command(label="New Tool", command=self.ToolPopup)

		if(type(event.widget) == ToolList):
			if(selectedItem != ''):
				self.toolList.selection_set(selectedItem)
				rightClickMenu.tk_popup(event.x_root, event.y_root)
			else:
				rightClickMenu2.tk_popup(event.x_root, event.y_root)
			
	def LeftClick(self, event):
		if(type(event.widget) == ToolList):
			selectedItem = self.toolList.identify("item", event.x, event.y)
			if(selectedItem == ''):
				self.toolList.deslectAll()

	def getTools(self):
		tools = []
		for child in self.toolList.get_children():
			toolItem = self.toolList.item(child)["values"]

			toolName = toolItem[0]
			toolHotkey = '+'.join( [f'<{key.lower()}>' if len(key) > 1 else key.lower() for key in toolItem[1].split(' ')])

			toolPosition = [int(i) for i in toolItem[2].split(' ')]

			tool = Tool(toolName, toolHotkey, toolPosition)
			tools.append(tool)
		return tools