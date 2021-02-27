class Interpreter:
	commands = None
	t = None

	def __init__(self,commands={}):
		self.commands = commands
	def interpret_command(self,cmd,execute=True):
		#Split command into args by spaces, leaving anything inside quotes as one arg
		args = []
		while cmd != '':
			try: ispace = cmd.index(' ')
			except: ispace = len(cmd)
			try: iquote = cmd.index('"')
			except: iquote = len(cmd)
			if ispace == 0:
				cmd = cmd[1:]
			elif iquote == 0 and cmd.count('"') > 0:
				cmd = cmd[1:]
				iquote = cmd.index('"')
				args.append(cmd[:iquote])
				cmd = cmd[iquote+1:]
			else:
				args.append(cmd[:ispace])
				cmd = cmd[ispace+1:]

		#Run corresponding lambda function with given args, unless execute has been set to false
		if execute and (args[0] in self.commands):
			key = args[0]
			self.commands[key](args)

		return args

	def twitch_interpret(self,t):
		new_messages = t.twitch_recieve_messages();
		
		if not new_messages:
			#No new messages...
			return []
		else:
			for message in new_messages:
				#Wuhu we got a message. Let's extract some details from it
				msg = message['message'].lower()
				username = message['username']
				print(username + ": " + msg)
	 
				cmd = self.interpret_command(msg,execute=False)
				if cmd[0] in self.commands:
					key = cmd[0]
					cmd[0] = username
					self.commands[key](cmd)
				if msg == 'kill' and username == auths.streamername:
					sys.exit()
		return new_messages

if __name__ == '__main__':
	i = Interpreter()
	c = input()
	a = i.interpret_command(c,execute=False)
	print(a)
	input()