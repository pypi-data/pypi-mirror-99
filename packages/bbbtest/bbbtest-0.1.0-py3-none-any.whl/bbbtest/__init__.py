__version__ = '0.1.0'

x = None

def config(user_x):
	global x
	x = user_x

def display_x():
	print(x)
	return x

