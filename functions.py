import tkinter as tk
import sqlite3
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import robobrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Window(tk.Frame):
	'''Control UI and flow of UI components'''
	def create_window(self, parent):
		'''Create basic outline of window'''
		self.browserOption = 'chrome'
		self.parent = parent
		self.accountButtonFrame = tk.Frame(self.parent, width=400)
		self.loadTimes = 0
		self.db = sqlite3.connect('.accounts.db')
		self.db.execute('create table if not exists accounts (nickname TEXT, url TEXT, username TEXT, password TEXT);')
		self.entries = []
		self.nicknames = []
		self.loadEntries()
		self.parent.title("AccountBot: Web")
		self.parent.geometry("650x550+300+300")
		self.addButton()
		self.deleteButton()
		self.parent.rowconfigure('all', minsize = 200)
		self.parent.columnconfigure('all', minsize = 200)

	def reloadWindow(self):
		for child in self.parent.winfo_children():
			for child2 in child.winfo_children():
				child2.grid_forget()
				child2.place_forget()
			child.grid_forget()
			child.place_forget()

		self.entries = []
		self.loadEntries()
		#self.parent.title("AccountBot: Web")
		#self.parent.geometry("650x550+300+300")
		self.addButton()
		self.deleteButton()
		#self.parent.rowconfigure('all', minsize = 200)
		#self.parent.columnconfigure('all', minsize = 200)

	###work on
	###

	def hideEntries(self):

		self.accountButtonFrame.place_forget()
		#for child in self.accountButtonFrame.winfo_children():
		#	child.configure(state='disabled')

	def showEntries(self):
		self.accountButtonFrame.place(relx=.5,rely=.5,anchor='center')
		#for child in self.accountButtonFrame.winfo_children():
		#	child.configure(state='active')

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
		self.reloadWindow()
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
		self.cancelButton = tk.Button(self.parent, text="Cancel", command=self.reloadWindow)
		self.cancelButton.place(relx=.4, rely=.7)
		self.showEntries()

	def addEntry(self):
		'''Add new website to database'''
		if (self.nicknameEntry.get() and self.urlEntry.get() and self.usernameEntry.get() and self.passwordEntry.get() and self.nicknameUnique(self.nicknameEntry.get())):
			self.inputBox.place_forget()

			self.db.execute("INSERT INTO accounts (nickname, url, username, password) \
							   VALUES (?,?,?,?)",(self.nicknameEntry.get(),self.urlEntry.get(),self.usernameEntry.get(),self.passwordEntry.get()))
			self.loadAccountButton(self.nicknameEntry.get(),self.urlEntry.get(),self.usernameEntry.get(),self.passwordEntry.get())

			self.okButton.place_forget()
			self.cancelButton.place_forget()
			self.addB.place(relx=.2, rely=.1, anchor='center')
			self.db.commit()

	def nicknameUnique(self, nickname):
		unique = True

		for name in self.nicknames:
			if name is nickname:
				unique = False
		return unique

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
		self.reloadWindow()
		deleteFrame = tk.Frame(self.parent, width=100, height=100)
		deleteLabel = tk.Label(deleteFrame, text="Nickname: ")
		deleteEntry = tk.Entry(deleteFrame)
		deleteLabel.grid(row=0)
		deleteEntry.grid(row=0, column= 1)
		self.deleteB.place_forget()
		deleteFrame.place(relx=.5,rely=.5, anchor='center')
		self.okButton = tk.Button(self.parent, text="Done", command=lambda: self.deleteEntryFromDB(deleteEntry.get()))
		self.okButton.place(relx=.5, rely=.7,)
		self.cancelButton = tk.Button(self.parent, text="Cancel", command=self.reloadWindow)
		self.cancelButton.place(relx=.4, rely=.7)
		self.hideEntries()
		pass

	def deleteEntryFromDB(self, nickname):
		print('in')
		self.db.execute("DELETE from accounts WHERE nickname=?;",(nickname,))
		self.db.commit()
		self.loadTimes -= 1
		self.okButton.place_forget()
		self.cancelButton.place_forget()
		self.showEntries()
		self.reloadWindow()

	def login(self,url,username,password):
		'''Login to selected website'''
		loginAliasesUserName = ['username','userid','user-id','user_name','user-name','user_id', 'login', 'email', 'Email']
		loginAliasesPassword = ['password', 'pass_word', 'passkey', 'pass_key', 'pass-word', 'passcode', 'pass_code', 'pass-key','pass-code']
		loginAliasesLogin    = ['login','signin','sign-in','LogIn','session', 'Login', 'Session','commit', 'submit']
		print(url + " " + username + " " + password)
		with requests.session() as s:
			site = urlopen(url).read()
			soup = BeautifulSoup(site, 'html.parser')
			soup.prettify()
		user = ''
		passw = ''
		action   = ''
		log      = ''
		for name in loginAliasesUserName:
			inputs = soup.find('input', {'name' : name})
			if inputs:
				user = name
				print (user)
				break
		for passcode in loginAliasesPassword:
			inputs = soup.find('input', {'name' : passcode})
			if inputs:
				passw = passcode
				print (passw)
				break
		'''for login in loginAliasesLogin:
			inputs = soup.find_all('form')
			for input in inputs:
				if login in input['action']:
					action = input.get('action')
					print(action)
					break
		if (not action):
			for login in loginAliasesPassword:
				inputs = soup.find('form', {'name' : login})
				if inputs:
					log = login
					print (log)
					break

		print ('action is ' + action)

		br = robobrowser.RoboBrowser()
		br.open(url, verify=False)
		if (action):
			form = br.get_form(action=action)
		else:
			form = br.get_form(name=log)
		print(form)
		form[user] = username
		form[passw]= password
		br.submit_form(form)
		print(str(br.select))'''
		if self.browserOption is 'firefox':
			browser = webdriver.Firefox()
		if self.browserOption is 'chrome':
			browser = webdriver.Chrome()
		browser.get(url)
		userName = browser.find_element_by_name(user)
		passWord = browser.find_element_by_name(passw)

		userName.send_keys(username)
		passWord.send_keys(password)

		for login in loginAliasesLogin:
			inputs = soup.find('input', {'name' : login})
			if inputs:
				log = login
				print (log)
				break
		print('log is ' + log)
		print (browser.find_element_by_name(log).click())
		#browser.find_element_by_name(log).send_keys(Keys.RETURN)





	def loadAccountButton(self, nickname, url, username, password):
		'''Load buttons to screen based on inputed information'''
		self.entries.append(tk.Button(self.accountButtonFrame, text=nickname, command=lambda: self.login(url,username,password)).grid(row=self.loadTimes))
		self.nicknames.append(nickname)
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
