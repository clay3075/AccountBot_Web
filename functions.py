import tkinter as tk
import sqlite3


class Window(tk.Frame):
	'''Control UI and flow of UI components'''
	def create_window(self, parent):
		'''Create basic outline of window'''
		self.parent = parent
		self.accountButtonFrame = tk.Frame(self.parent, width=400)
		self.loadTimes = 0
		self.db = sqlite3.connect('.accounts.db')
		self.db.execute('create table if not exists accounts (nickname TEXT, url TEXT, username TEXT, password TEXT);')
		#self.dbcursor = self.db.cursor()
		self.entries = []
		self.loadEntries()
		self.parent.title("AccountBot: Web")
		self.parent.geometry("650x550+300+300")
		self.addButton()
		self.deleteButton()
		self.parent.rowconfigure('all', minsize = 200)
		self.parent.columnconfigure('all', minsize = 200)

	def reloadWindow(self):
		self.parent.grid_forget()
		self.entries = []
		self.loadEntries()
		self.parent.title("AccountBot: Web")
		self.parent.geometry("650x550+300+300")
		self.addButton()
		self.deleteButton()
		self.parent.rowconfigure('all', minsize = 200)
		self.parent.columnconfigure('all', minsize = 200)

	###work on
	###

	def hideEntries(self):

		#self.accountButtonFrame.configure(state='disable')
		for child in self.accountButtonFrame.winfo_children():
			child.configure(state='disabled')

	def showEntries(self):
		#self.accountButtonFrame.configure(state='enable')
		for child in self.accountButtonFrame.winfo_children():
			child.configure(state='active')

	###
	###

	def addButton(self):
		'''If no entries exist show add button in the middle to add entry
		   if entries to exist show add button top right hand corner.
		'''
		self.addB = tk.Button(self.parent, text="Add", height=30, width= 20, command=self.addButtonClicked)
		if (not self.entriesExist()):
			self.addB.place(relx=0.5, rely=0.5, anchor='center')
		else:
			self.addB.place(relx=.2, rely=.1, anchor='center')


	def addButtonClicked(self):
		'''Bring up window to add entry and add entry internally as well'''
		print('clicked')
		if (self.entriesExist()):
			self.addB.place(relx=.2, rely=.1, anchor='center')
		self.addItem()
		self.hideEntries()


	def addItem(self):
		'''Show text fields and get user input'''
		#create labels
		self.addB.place_forget()
		self.inputBox = tk.Frame(self.parent, width=400, height=400)
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
		self.showEntries()

	def addEntry(self):
		'''Add new website to database'''
		if (self.nicknameEntry.get() and self.urlEntry.get() and self.usernameEntry.get() and self.passwordEntry.get()):
			self.inputBox.place_forget()

			self.db.execute("INSERT INTO accounts (nickname, url, username, password) \
							   VALUES (?,?,?,?)",(self.nicknameEntry.get(),self.urlEntry.get(),self.usernameEntry.get(),self.passwordEntry.get()))
			self.loadAccountButton(self.nicknameEntry.get(),self.urlEntry.get(),self.usernameEntry.get(),self.passwordEntry.get())

			self.okButton.place_forget()
			self.addB.place(relx=.2, rely=.1, anchor='center')
			self.db.commit()


	def entriesExist(self):
		'''Will return true if entries already exist'''
		exists = False
		if (len(self.entries)):
			exists = True
		return exists

	def deleteButton(self):
		'''Remove website from database'''
		self.deleteB = tk.Button(self.parent, text="Delete", height=30, width= 20, command=self.deleteButtonClicked)
		if (self.entriesExist()):
			self.deleteB.place(relx=.8, rely=.1, anchor='center')

	def deleteButtonClicked(self):
		'''Remove website from database. Give menu to enter nickname to be deleted.'''
		self.hideEntries()
		deleteFrame = tk.Frame(self.parent, width=100, height=100)
		deleteLabel = tk.Label(deleteFrame, text="Nickname: ")
		deleteEntry = tk.Entry(deleteFrame)
		deleteLabel.grid(row=0)
		deleteEntry.grid(row=0, column= 1)
		self.deleteB.place_forget()
		deleteFrame.place(relx=.5,rely=.5, anchor='center')
		self.okButton = tk.Button(self.parent, text="Done", command=lambda: self.deleteEntryFromDB(deleteEntry.get()))
		self.okButton.place(relx=.5, rely=.7)
		self.showEntries()
		pass

	def deleteEntryFromDB(self, nickname):
		print('in')
		self.db.execute("DELETE from accounts WHERE nickname=?;",(nickname,))
		self.db.commit()
		self.loadTime -= 1
		self.okButton.place_forget()
		self.reloadWindow()

	def login(self,url,username,password):
		'''Login to selected website'''
		pass

	def loadAccountButton(self, nickname, url, username, password):
		'''Load buttons to screen based on inputed information'''
		self.entries.append(tk.Button(self.accountButtonFrame, text=nickname, command=self.login(url,username,password)).grid(row=self.loadTimes))
		self.loadTimes += 1
		self.accountButtonFrame.place(relx=.5,rely=.5,anchor='center')


	def loadEntries(self):
		'''Load entries if there are any from database'''
		cursor = self.db.execute("SELECT nickname, url, username, password from accounts;")
		for row in cursor:
			self.loadAccountButton(row[0], row[1], row[2], row[3])


def main():
	root = tk.Tk()
	ui = Window(root)
	ui.create_window(root)
	root.tk.mainloop()
