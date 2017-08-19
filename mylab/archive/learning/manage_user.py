from time import sleep
import operator
class User:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	def get_name(self):
		return self.name
	def get_age(self):
		return self.age
		
userList=[]
user = User("memphis", 28)
userList.append(user)
user = User("hulk", 24)
userList.append(user)
user = User("duck duck", 11)
userList.append(user)

def view_user_list():
	if not userList:
		print "List is empty"
		
	else:
		for user in userList:
			print user.get_name() + " " + str(user.get_age())
def add_user():
	name = raw_input("Enter your name: ")
	age = int(raw_input("Enter your age: "))
	print "Adding..."
	sleep(3)
	user = User(name, age)
	userList.append(user)
	print "Done!"

def search_user_by_name():
	by_name = raw_input("Search by name: ")
	flag = False
	for user in userList:
		if user.get_name() == by_name:
			flag = True
			print "Got an user: name = %s age = %s" % (user.get_name(), user.get_age())
	if not flag:
		print "Found nothing"

def sort_user_by_name():
	userList.sort(key=operator.attrgetter('name'))
	print "Sorting..."
	sleep(3)
	print "Done!"

def get_user_choice():
	user_choice = int(raw_input("Your choice: "))
	return user_choice

def show_menu():
	print "1. View list"
	print "2. Add user"
	print "3. Search by user name"
	print "4. Sorted by user name"
	user_choice = get_user_choice()
	if user_choice == 1:
		view_user_list()
		show_menu()
	elif user_choice == 2:
	    add_user()
	    show_menu()
	elif user_choice == 3:
	    search_user_by_name()
	    show_menu()
	elif user_choice == 4:
		sort_user_by_name()
		show_menu()
	else:
		print "You choose wrong"
		return			

show_menu()
