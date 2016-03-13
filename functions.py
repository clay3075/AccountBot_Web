import tkinter as tk


class Window(tk.Frame):
	'''Control UI and flow of UI components'''
	def create_window(self, parent):
		'''Create basic outline of window'''
		self.entries = []
		self.parent = parent
		self.parent.title("AccountBot: Web")
		self.parent.geometry("650x550+300+300")
		self.addButton()
		#self.parent.grid()
		self.parent.rowconfigure('all', minsize = 200)
		self.parent.columnconfigure('all', minsize = 200)

	def addButton(self):
		'''If no entries exist show add button in the middle to add entry
		   if entries to exist show add button top right hand corner.
		'''
		self.addB = tk.Button(self.parent, text="Add", height=30, width= 20, command=self.addButtonClicked)
		#self.addB.grid(row=0, column=0, sticky=tk.E)
		if (not self.entriesExist()):
			self.addB.place(relx=0.5, rely=0.5, anchor='center')

	def addButtonClicked(self):
		'''Bring up window to add entry and add entry internally as well'''
		print('clicked')
		if (self.entriesExist()):
			self.addB.place(relx=.8, rely=.1)
		self.addItem()


	def addItem(self):
		'''Show text fields and get user input'''
		#create labels
		self.addB.place_forget()
		self.inputBox = tk.Frame(self.parent, width=400, height=400)
		#self.grid()
		self.inputBox.place(relx=.5,rely=.3, anchor='center')
		self.nicknameLabel = tk.Label(self.inputBox, text="Nickname: ")
		self.urlLabel      = tk.Label(self.inputBox, text="URL:      ")
		self.usernameLabel = tk.Label(self.inputBox, text="User Name:")
		self.passwordLabel = tk.Label(self.inputBox, text="Password: ")
		#create texts boxes
		self.nicknameEntry = tk.Entry(self.inputBox)
		self.urlEntry      = tk.Entry(self.inputBox)
		self.usernameEntry = tk.Entry(self.inputBox)
		self.passwordEntry = tk.Entry(self.inputBox)
		# Bring up text fields
		self.nicknameLabel.grid(row=0, sticky=tk.NW, columnspan=2)
		self.nicknameEntry.grid(row=0, column=1)
		self.urlLabel.grid(row=1, sticky=tk.NW)
		self.urlEntry.grid(row=1, column=1)
		self.usernameLabel.grid(row=2, sticky=tk.NW)
		self.usernameEntry.grid(row=2, column=1)
		self.passwordLabel.grid(row=3, sticky=tk.NW)
		self.passwordEntry.grid(row=3, column=1)
		self.addEntry()

		self.okButton = tk.Button(self.parent, text="Done", command=self.addEntry)
		self.okButton.place(relx=.5, rely=.7)

	def addEntry(self):
		'''Add new website to database'''
		if (self.nicknameEntry.get() and self.urlEntry.get() and self.usernameEntry.get() and self.passwordEntry.get()):
			self.inputBox.place_forget()


			self.okButton.place_forget()
			self.addB.place(relx=.8, rely=.1)


	def entriesExist(self):
		'''Will return true if entries already exist'''
		exists = False
		if (len(self.entries)):
			exists = True
		return exists

	def deleteEntry(url):
		'''Remove website from database'''

	def login():
		'''Login to selected website'''

def main():
	ui = Window()
	root = tk.Tk()
	ui.create_window(root)
	root.tk.mainloop()
