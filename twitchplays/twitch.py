import socket
import sys
import re
 
class Twitch:
 
    user = "";
    oauth = "";
    s = None;
 
    def twitch_login_status(self, data):
        if not re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data.decode('utf-8')): return True
        else: return False
 
    def twitch_connect(self, user, key, safety=False):
        if safety:
            c = input("Running this program may give {}'s twitch chat control over your computer. If you are sure you meant to do this, type 'Yes'.".format(user))
            if c != 'Yes':
                sys.exit()
        self.user = user;
        self.oauth= key;
        print("Connecting to twitch.tv");
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        s.settimeout(0.6);
        connect_host = "irc.twitch.tv";
        connect_port = 6667;
        try:
            s.connect((connect_host, connect_port));
        except:
            print("Failed to connect to twitch");
            sys.exit();
        print("Connected to twitch");
        print("Sending our details to twitch...");
        eUser = 'USER %s\r\n' % user;
        s.send(eUser.encode());
        ePass = 'PASS %s\r\n' % key;
        s.send(ePass.encode());
        eNick = 'NICK %s\r\n' % user;
        s.send(eNick.encode());
 
        if not self.twitch_login_status(s.recv(1024)):
            print("... and they didn't accept our details");
            sys.exit();
        else:
            print("... they accepted our details");
            print("Connected to twitch.tv!")
            self.s = s;
            eJoin = 'JOIN #%s\r\n' % user;
            s.send(eJoin.encode())
            s.recv(1024);
 
    def check_has_message(self, data):
        return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$', data.decode('utf-8'))
 
    def parse_message(self, data):
        return {
            'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
            'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
            'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0]
        }
 
    def twitch_recieve_messages(self, amount=1024):
        data = None
        try: data = self.s.recv(1024);
        except: return False;
 
        if not data:
            print("Lost connection to Twitch, attempting to reconnect...");
            self.twitch_connect(self.user, self.oauth);
            return None
 
        #self.ping(data)
 
        if self.check_has_message(data):
            data = data.decode('utf-8');
            return [self.parse_message(line) for line in filter(None, data.split('\r\n'))];

    def twitch_send_message(self, msg):
        try: self.s.send("PRIVMSG #{} :{}\r\n".format(self.user, msg).encode("utf-8"))
        except: return False
        return True