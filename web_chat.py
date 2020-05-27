# Chat application
import requests
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from threading import Thread
import time

my_session = requests.Session()
url = 'http://165.22.14.77:8080/Satish/WebChat/'

def change_send_button_status(event):
	global send_button
	send_button.config(state = ('disabled' if send_msg.get() == '' else 'normal'))


def send_message(event = None):
	my_session.get(f'{url}sendMessage.jsp?username={user_name}&message={send_msg.get()}')
	send_msg.delete(0, last = END)


def get_active_users():
	try:
		while True:
			response = my_session.get(f'{url}activeUsers.jsp?username={user_name}')
			active_users.config(state = 'normal')
			active_users.delete(1.0, END)
			active_users.insert(END, response.text.strip().replace("<br>", ""))
			active_users.config(state = DISABLED)
			time.sleep(2)
	except:
		print("", end = '')


def signout():
	try:
		response = my_session.get(f'{url}signOut.jsp?username={user_name}')
		messagebox.showinfo('Message', 'Logged out succesfully!')	
		chat_window.destroy()
		login_registration_window()
	except:
		print("", end = '')

def get_new_messages():
	try:
		while True:
			response = my_session.get(f'{url}showMessages.jsp?username={user_name}')
			chat_box.config(state = 'normal')
			if response.text.strip() != "":
				chat_box.delete(1.0, END)
				chat_box.insert(END, f'{response.text.strip()}\n')
			chat_box.config(state = DISABLED)
			time.sleep(1)
	except:
		print("", end = '')

def change_login_button_status(event):
	login_button.config(state = ('disabled' if user_name.get() == '' or password.get() == '' else 'normal'))

def chat_window(name):
	global send_msg
	global chat_box
	global chat_window
	global send_button
	global user_name
	global active_users
	user_name = name

	chat_window = Tk()
	chat_window.geometry('500x500')
	chat_window.title('Chat window')
	chat_window.resizable(0, 0)
	chat_window.bind("<FocusIn>", change_send_button_status)
	chat_window.bind("<ButtonRelease>", change_send_button_status)

	active_users_lbl = Label(chat_window, text = 'Friends active')
	active_users_lbl.place(x = 360, y = 10)

	active_users = scrolledtext.ScrolledText(height = 20, width = 20)
	active_users.place(x = 320, y = 30)
	active_users.config(state = DISABLED)

	send_msg_lbl = Label(chat_window, text = 'Enter message: ')
	send_msg_lbl.place(x = 10, y = 400)

	send_msg = Entry(chat_window, width = 20)
	send_msg.bind("<Return>", send_message)
	send_msg.place(x = 140, y = 400)
	send_msg.focus_set()

	send_button = Button(chat_window, text = 'Send', command = send_message)
	send_button.place(x = 330, y = 395)


	signout_button = Button(chat_window, text = 'Signout', command = signout)
	signout_button.place(x = 200, y = 430)

	chat_area_lbl = Label(chat_window, text = 'Messages')
	chat_area_lbl.place(x = 100, y = 10) 
	chat_box = scrolledtext.ScrolledText(width = 36, height = 20)
	chat_box.place(x = 10, y = 30)
	chat_box.config(state = DISABLED)
	Thread(target = get_active_users).start()
	Thread(target = get_new_messages).start()

	chat_window.bind("<Key>", change_send_button_status)
	mainloop()


def login(user_name, password, login_registration_window):
	response = my_session.get(f'{url}register.jsp?username={user_name}&password={password}')
	close_window = login_registration_window
	if(response.text.find("Registered")) > 0:
		messagebox.showinfo('Success', 'Account created successfully!')
		close_window.destroy()
		chat_window(user_name)
	elif(response.text.find("Logged")) > 0:
		messagebox.showinfo('Success', 'Logged in successfully!')
		close_window.destroy()
		chat_window(user_name)
	else:
		messagebox.showinfo('Error', 'Invalid credentials!')	


def login_registration_window():
	global user_name, password, login_button, signup_button
	login_registration_window = Tk()
	login_registration_window.geometry('400x200')
	login_registration_window.title('Webchat login')
	login_registration_window.resizable(0, 0)
	login_registration_window.bind('<FocusIn>', change_login_button_status)

	user_name_lbl = Label(login_registration_window, text = 'Enter username: ')
	user_name_lbl.place(x = 10, y = 10)

	user_name = Entry(login_registration_window, width = 20)
	user_name.place(x = 160, y = 10)
	user_name.focus_set()

	password_lbl = Label(login_registration_window, text = 'Enter password: ')
	password_lbl.place(x = 10, y = 50)
	password = Entry(login_registration_window,show = '*', width = 20)
	password.place(x = 160, y = 50)

	login_button = Button(login_registration_window, text = 'Login/Register', command = lambda: login(user_name.get(), password.get(), login_registration_window))
	login_button.place(x = 160, y = 90)


	login_registration_window.bind("<Key>", change_login_button_status)
	mainloop()

login_registration_window()
