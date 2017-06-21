###############################
#        POP Protocol         #
###############################

import poplib
from kivy.app import App
from kivy.core.window import Window

my_pop = poplib.POP3_SSL(host='pop.gmail.com')
my_pop.getwelcome()

import getpass
my_pop.user('my_name@gmail.com')
my_pop.pass_(getpass.getpass()) # safe way to enter password

my_pop.stat() # summary of what is on open server


email_top = my_pop.top(1, 5) # grab first five lines of newest email in list (list() is a separate method which gets explicit list of messages)

for line in email_top[1]:
	if 'Subject' in line:
		print line


my_pop.quit() # log off

class EmailApp(App):
	def build(self):
		Window.size = (480, 800)
		Window.fullscreen = False
