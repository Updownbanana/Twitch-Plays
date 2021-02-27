from twitchplays import keypresser, interpreter, twitch, auths
import sys

#Dict of commands
commands = {
    
}

#Functions to click or drag at a position in the above coordinate dict, or on the grid
def clickPos(name):
    if name in coords:
        pos = coords[name]
        k.click(pos[0],pos[1])

def dragPos(name1,name2):
    if name1 in coords and name2 in coords:
        pos1 = coords[name1]
        pos2 = coords[name2]
        k.drag(pos1[0],pos1[1],pos2[0],pos2[1])

#Setup interpreter, keypresser, twitch
intrp = interpreter.Interpreter(commands)
k = keypresser.Keypresser()
t = twitch.Twitch()
t.twitch_connect(auths.streamername, auths.key, safety=True)

#The main loop
while True:
    intrp.twitch_interpret()