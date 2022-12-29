import tkinter as tk
from tkinter import ttk

from sys import platform

import macroManager
from ToolPopup import ToolPopup

class ToolList(ttk.Treeview):
	def __init__(self, master=None):
		super().__init__(master)

		self.config(columns=('tool_name', 'hotkey', 'position'), show='headings')

		self.heading('tool_name', text='Tool Name')
		self.heading('hotkey',text='Hotkey')
		self.heading('position', text='Position')
	
	def add_tool(self, tool):
		self.insert(parent='',index=tk.END, values=(tool.toolName, tool.hotKey.format(), tool.position) )
	
	def edit_tool(self, tool):
		selected_item = self.selection()[0]
		self.item(selected_item, values=(tool.toolName, tool.hotKey.format(), tool.position))

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
			
			self.protocol("WM_DELETE_WINDOW", self.on_close)

			# ------------------------------------[ Variables ]------------------------------------
			
			# ------------------------------------[ App Structure ]------------------------------------
			self.menuBar = MenuBar(self)

			self.menuBar.file_menu.add_command(label="New Tool", command=self.newToolPopup)
			self.menuBar.file_menu.add_command(label="Disable Listening", command=self.toggleListening)
			self.menuBar.file_menu.add_separator()
			self.menuBar.file_menu.add_command(label="Exit", command=self.on_close)
			self.config(menu=self.menuBar)

			self.toolList = ToolList(self)
			self.toolList.grid(row=0, column=0, sticky='news')


			# ------------------------------------[ Event Handling ]------------------------------------
			self.bind("<Button-1>", self.LeftClick)

			if(platform == "win32"):
				self.bind("<Button-3>", self.RightClick)
			elif(platform == "darwin"):
				self.bind("<Button-2>", self.RightClick)
			
			self.bind("<Delete>", self.removeTool)
			self.bind("<BackSpace>", self.removeTool)

			self._macroManager = macroManager.MacroManager()
			for tool in self._macroManager.tools:
				self.toolList.add_tool(tool)

	def toggleListening(self):
		if(self._macroManager.isListening):
			self.menuBar.file_menu.entryconfigure(1, label="Enable Listening")
			self._macroManager.isListening = False
			self.title("Macro Manager (Listening Disabled)")
		else:
			self.menuBar.file_menu.entryconfigure(1, label="Disable Listening")
			self._macroManager.isListening = True
			self.title("Macro Manager")

	def submitButton(self):
		self.popupWindow.destroy()
		self.toolPopupIsActive = False

	def RightClick(self, event):
		selectedItem = self.toolList.identify("item", event.x, event.y)
# 
		rightClickMenu = tk.Menu(self, tearoff=False)
		rightClickMenu.add_command(label="Edit", command=self.editToolPopup)
		rightClickMenu.add_command(label="Duplicate", command=self.duplicateTool)
		rightClickMenu.add_separator()
		rightClickMenu.add_command(label="Delete", command=self.removeTool)

		rightClickMenu2 = tk.Menu(self, tearoff=False)
		rightClickMenu2.add_command(label="New Tool", command=self.newToolPopup)

		if(isinstance(event.widget, ToolList)):
			if(selectedItem != ''):
				self.toolList.selection_set(selectedItem)
				rightClickMenu.tk_popup(event.x_root, event.y_root)
			else:
				rightClickMenu2.tk_popup(event.x_root, event.y_root)
			
	def LeftClick(self, event):
		if(isinstance(event.widget, ToolList)):
			selectedItem = self.toolList.identify("item", event.x, event.y)
			if(selectedItem == ''):
				self.toolList.deslectAll()

	def addTool(self, tool):
		self._macroManager.addTool(tool)
		self.toolList.add_tool(tool)

		self._macroManager.isListening = True

	def editTool(self, tool):
		selectedItem = self.toolList.selection()[0]
		selectedIndex = self.toolList.index(selectedItem)

		self._macroManager.tools[selectedIndex] = tool
		self.toolList.edit_tool(tool)
		
		self._macroManager.isListening = True

	def removeTool(self, event=None):
		for selectedItem in self.toolList.selection():
			selectedIndex = self.toolList.index(selectedItem)

			self._macroManager.removeTool(selectedIndex)
			self.toolList.delete_tool()		

	def duplicateTool(self, event=None):
		selectedItem = self.toolList.selection()[0]
		selectedIndex = self.toolList.index(selectedItem)

		self._macroManager.duplicateTool(selectedIndex)
		self.toolList.add_tool(self._macroManager.tools[-1])

	def on_cancel(self):
		self._macroManager.isListening = True

	def editToolPopup(self):
		self._macroManager.isListening = False
		tool = self.getSelectedTool()
		ToolPopup(self, title="Edit Tool", submitButtonText="Save", on_submit=self.editTool, on_cancel=self.on_cancel, tool=tool)

	def newToolPopup(self):
		self._macroManager.isListening = False
		ToolPopup(self, title="New Tool", on_submit=self.addTool, on_cancel=self.on_cancel)

	def getSelectedTool(self):
		selectedItem = self.toolList.selection()[0]
		selectedIndex = self.toolList.index(selectedItem)
		return self._macroManager.tools[selectedIndex]

	def on_close(self):
		self._macroManager.stop()
		self.destroy()