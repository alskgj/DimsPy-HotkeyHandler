__author__ = 'Dimitri Wessels'
__email__ = 'dimitri.wessels@gmail.com'

import os
import ctypes
from ctypes import wintypes
import win32con
 
byref = ctypes.byref
user32 = ctypes.windll.user32
 
HOTKEYS = {
    1: (win32con.VK_F3, win32con.MOD_WIN),
    2: (win32con.VK_F4, win32con.MOD_WIN)
}


def handle_win_f3():
    os.startfile(os.environ['TEMP'])


def handle_win_f4():
    user32.PostQuitMessage(0)
 
HOTKEY_ACTIONS = {
    1: handle_win_f3,
    2: handle_win_f4
}
print('test')
 
for id_, (vk, modifiers) in HOTKEYS.items():
    print('Registering id', id_, 'for key', vk)
    if not user32.RegisterHotKey (None, id_, modifiers, vk):
        print('Unable to register id', id_)
 
try:
    msg = wintypes.MSG()
    while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
        if msg.message == win32con.WM_HOTKEY:
            action_to_take = HOTKEY_ACTIONS.get(msg.wParam)
            if action_to_take:
                action_to_take()
 
        user32.TranslateMessage(byref(msg))
        user32.DispatchMessageA(byref(msg))
 
finally:
    for id_ in HOTKEYS.keys():
        user32.UnregisterHotKey(None, id_)