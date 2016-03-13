import tkinter as tk


def entriesExist():
	'''Will return true if entries already exist'''

def addEntry(websitename,url,name,password):
	'''Add new website to database'''

def deleteEntry(url):
	'''Remove website from database'''

def login():
	'''Login to selected website'''


class Window(tk.Frame):
	'''Control UI and flow of UI components'''
	def create_window(self, parent):
		'''Create basic outline of window'''
		self.parent = parent
		self.parent.title("Webpage Opener")
		self.parent.geometry("250x150+300+300")
		self.addButton()
		self.grid(row=0)

	def addButton(self):
		'''If no entries exist show add button in the middle to add entry
		   if entries to exist show add button top right hand corner.
		'''
		addB = tk.Button(self.parent, text="Add", command=self.addButtonClicked)
		#addB.pack()
		addB.grid(row=0)
		addB.place(relx=0.5, rely=0.5, anchor='center')

	def addButtonClicked(self):
		'''Bring up window to add entry and add entry internally as well'''
		print('clicked')

	# Bring up text fields
	# Website Name
	# Url
	# login name
	# password


def main():
	ui = Window()
	root = tk.Tk()
	ui.create_window(root)
	root.tk.mainloop()
