from twitchplays import twitch, interpreter, auths
import threading

#Command dict for streamer
commands = {
	'add': lambda cmd:add(cmd),
	'whisper': lambda cmd:whisper(cmd),
	'remove': lambda cmd:remove(cmd)
}

#Command dict for Twitch users
tcommands = {
	'!join': lambda cmd:join(cmd)
}

#Function definitions
def add(cmd):
	try:
		num = int(cmd[1])
	except:
		print('Syntax: add [number]')
		return
	for i in range(0,num):
		try: user = queue.pop(0)
		except IndexError: 
			print('No more users in queue.')
			break
		except: 
			print('Unknown error.')
			break
		users.append(user)
		print('Added {}'.format(user))

def whisper(cmd):
	try:
		msg = cmd[1]
	except:
		print('Syntax: whisper [message]')
		return
	for u in users:
		t.twitch_send_message('/w {} {}'.format(u,msg))
		print('Whispered {}'.format(u))

def remove(cmd):
	try:
		num = int(cmd[1])
	except IndexError:
		num = len(users)
	except:
		print('Syntax: remove [number] or remove')
		return
	for i in range(0,num):
		try: user = users.pop(0)
		except IndexError:
			print('No more users to remove.')
			break
		except:
			print('Unknown error.')
			break 
		if user not in removed:
			removed.append(user)
		print('Removed {}'.format(user))

#Function defs for Twitch users
def join(cmd):
	user = cmd[0]
	if user not in queue and user not in users:
		queue.append(user)

#Setup 2 interpreters and twitch
tintrp = interpreter.Interpreter(tcommands)
intrp = interpreter.Interpreter(commands)
t = twitch.Twitch()
t.twitch_connect(auths.streamername, auths.key)

#Define user lists
queue = []
users = []
removed = []

#Start thread
def input_process():
	while True:
		cmd = input('{} users> '.format(len(users)))
		intrp.interpret_command(cmd)
thread = threading.Thread(target=input_process, daemon=True)
thread.start()

#Main loop
while True:
	new_messages = tintrp.twitch_interpret(t)