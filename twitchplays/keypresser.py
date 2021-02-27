import win32com.client as comclt
import win32api, win32con
import time
 
class Keypresser:
 
    wsh = None;
 
    def __init__(self):
        self.wsh = comclt.Dispatch("WScript.Shell");
    def key_press(self, key):
        self.wsh.SendKeys(key)
    def click(self,x,y):
        win32api.SetCursorPos((x,y))
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    def rightclick(self,x,y):
        win32api.SetCursorPos((x,y))
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
    def drag(self,x1,y1,x2,y2):
        win32api.SetCursorPos((x1,y1))
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
        time.sleep(.1)
        win32api.SetCursorPos((x2,y2))
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x2,y2,0,0)
