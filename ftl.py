#Define the imports
from twitchplays import keypresser, auths, twitch, interpreter
import sys

#TODO:
#Fix problem with staying in jump state
#Add depowering functionality
#Add QOL name recognition in commands
#Commands to power specific weapons

#Dicts of commands, systems, and sets of mouse coordinates
commands = {
    'power': lambda cmd:power(cmd), 
    'ship': lambda cmd:ship(), 
    'jump': lambda cmd:jump(cmd), 
    'buy': lambda cmd:buy(cmd), 
    'sell': lambda cmd:sell(cmd), 
    'changeslot': lambda cmd:move(cmd), 
    'dismiss': lambda cmd:dismiss(cmd), 
    'store': lambda cmd:store(), 
    'back': lambda cmd:back(), 
    'upgrade': lambda cmd:upgrade(cmd), 
    'rename': lambda cmd:rename(cmd), 
    'fire': lambda cmd:fire(cmd), 
    'move': lambda cmd:move(cmd) 
}

systems = {
    'shields':'a',
    'engines':'s',
    'medbay':'d',
    'oxygen':'f',
    'teleporter':'g',
    'cloaking':'h',
    'mindcontrol':'k',
    'hacking':'l',
    'weapons':'w',
    'drones':'e'
}

coords = {
    'upgrade':[600,160],
    'crew':[725,162],
    'inventory':[858,152],
    'upShields':[606,420],
    'upEngines':[700,420],
    'upMedbay':[805,420],
    'upOxygen':[900,420],
    'upWeapons':[1000,420],
    'upExtra1':[1105,420],
    'upExtra2':[1200,420],
    'upExtra3':[1290,420],
    'upPilot':[580,700],
    'upSensors':[670,700],
    'upDoors':[770,700],
    'upExtra4':[880,700],
    'upReactor':[1160,700],
    'dismiss1':[688,374],
    'dismiss2':[943,374],
    'dismiss3':[1200,374],
    'dismiss4':[690,544],
    'dismiss5':[947,544],
    'dismiss6':[1200,544],
    'dismiss7':[818,743],
    'dismiss8':[1080,743],
    'dismissYes':[37,230],
    'weapon1':[680,300],
    'weapon2':[860,300],
    'weapon3':[1036,300],
    'weapon4':[1200,300],
    'drone1':[680,450],
    'drone2':[860,450],
    'drone3':[1036,450],
    'drone4':[1200,450],
    'cargo1':[630,630],
    'cargo2':[830,630],
    'cargo3':[630,750],
    'cargo4':[830,750],
    'augment1':[1150,600],
    'augment2':[1150,685],
    'augment3':[1150,780],
    'shop':[1116,75],
    'shop1':[1123,167],
    'shop2':[1282,170],
    'buy':[627,160],
    'sell':[870,160],
    'buyFuel':[658,280],
    'buyMissiles':[658,349],
    'buyDrones':[658,431],
    'fix1':[658,598],
    'fixAll':[658,680],
    'buy11':[900,295],
    'buy12':[1080,364],
    'buy13':[1280,445],
    'buy21':[900,610],
    'buy22':[1080,675],
    'buy23':[1280,760],
    'sellItem':[300,436],
    'crew1':[80,250],
    'crew2':[80,300],
    'crew3':[80,345],
    'crew4':[80,390],
    'crew5':[80,435],
    'crew6':[80,480],
    'crew7':[80,525],
    'crew8':[80,570]
}

grid0 = [280,250]

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

def clickGrid(x,y):
    x += grid0[0]
    y += grid0[1]
    k.click(x,y)

def rightClickGrid(x,y):
    x += grid0[0]
    y += grid0[1]
    k.rightclick(x,y)
        
#Functions for all chat commands

def power(cmd):
    global state
    if state != 'basic':
        return
    try:
        system = cmd[1]
    except IndexError:
        print('Invalid command.')
        return
    if system in systems:
        key = systems[system]
        k.key_press(key)
    print(cmd[1]+' powered.')
    return

def back():
    global state
    if state != 'basic':
        k.key_press('{ESCAPE}')
        state = 'basic'
        print('Menu exited.')

def ship():
    global state
    if state == 'basic':
        k.key_press('u')
        state = 'ship'

def jump(cmd):
    global state
    if state == 'basic':
        k.key_press('j')
        state = 'jump'
        print('Jumping...')
    else:
        print('Incorrect state.')

def buy(cmd):
    global state
    if state != 'shop':
        return
    try:
        tab = cmd[1]
        section = cmd[2]
        purchase = cmd[3]
    except IndexError:
        try:
            tab = 'None'
            section = cmd[1]
            purchase = cmd[2]
        except IndexError:
            print('Invalid command.')
            return
    #Need to add code for buying basic supplies and repairs
    clickPos('buy')
    name = 'shop'+tab
    clickPos(name)
    name = 'buy'+section+purchase
    clickPos(name)

def sell(cmd):
    global state
    if state != 'shop':
        return
    try:
        item = cmd[1]
    except IndexError:
        print('Invalid command.')
        return
    clickPos('sell')
    dragPos(item,'sellItem')

def move(cmd):
    global state
    if state != 'ship':
        return
    try:
        item = cmd[1]
        pos = cmd[2]
    except IndexError:
        print('Invalid command.')
        return
    clickPos('inventory')
    dragPos(item,pos)

def dismiss(cmd):
    global state
    if state != 'ship':
        return
    try:
        crew = cmd[1]
    except IndexError:
        print('Invalid command.')
        return
    clickPos('crew')
    name = 'dismiss'+crew
    clickPos(name)
    pos = coords[name]
    yes = coords['dismissYes']
    pos[0] += yes[0]
    pos[1] += yes[1]
    k.click(pos[0],pos[1])

def store():
    global state
    if state == 'basic':
        clickPos('shop')
        state = 'shop'

def upgrade(cmd):
    global state
    if state != 'ship':
        return
    try:
        system = cmd[1]
    except IndexError:
        print('Invalid command.')
        return
    name = 'up' + system.capitalize()
    clickPos(name)

def rename(cmd):
    global state
    if state != 'ship':
        return
    try:
        crew = cmd[1]
        name = cmd[2]
    except IndexError:
        print('Invalid command.')
        return
    clickPos('crew')
    pos = coords['dismiss'+crew]
    pos[1] -= 31
    k.click(pos[0],pos[1])
    k.key_press(name)
    k.key_press('{ENTER}')
    print('Crew member '+crew+' renamed to '+name)

def fire(cmd):
    global state
    if state != 'basic':
        return
    try:
        weapon = cmd[1]
        x = int(cmd[2])
        y = int(cmd[3])
    except IndexError:
        print('Invalid command.')
        return
    k.key_press(weapon)
    clickGrid(x,y)
    print('Weapon '+weapon+' fired at coordinates '+cmd[2]+', '+cmd[3])

def move(cmd):
    global state
    if state != 'basic':
        print('Incorrect state.')
        return
    try:
        crew = cmd[1]
        x = int(cmd[2])
        y = int(cmd[3])
    except IndexError:
        print('Invalid command.')
        return
    clickPos('crew'+crew)
    rightClickGrid(x,y)
    print('Crew member '+crew+' moved to coordinates '+cmd[2]+', '+cmd[3])

def pause(cmd):
    global paused
    if not paused:
        k.key_press('{SPACE}')
        paused = True

def unpause(cmd):
    global paused
    if paused:
        k.key_press('{SPACE}')
        paused = False

#Initialize state and pause variables
state = 'basic'
paused = False

#Setup interpreter and keypresser
intrp = interpreter.Interpreter(commands)
k = keypresser.Keypresser()
t = twitch.Twitch()
t.twitch_connect(auths.streamername, auths.key, safety=True)

#The main loop
while True:
    intrp.twitch_interpret(t)