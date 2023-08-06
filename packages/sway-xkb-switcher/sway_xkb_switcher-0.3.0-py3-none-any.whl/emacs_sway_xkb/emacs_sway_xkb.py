#!/usr/bin/env python

from os import system
from i3ipc import Connection


def main():
    name = "1:1:AT_Translated_Set_2_keyboard"
    sway = Connection()
    focused = sway.get_tree().find_focused()
    if(focused.window_class == 'Emacs'):
        system('emacsclient -e "(with-current-buffer (window-buffer) (toggle-input-method))"')
    else:
        sway.command(f"input {name} xkb_switch_layout next")


if __name__ == '__main__':
    main()
