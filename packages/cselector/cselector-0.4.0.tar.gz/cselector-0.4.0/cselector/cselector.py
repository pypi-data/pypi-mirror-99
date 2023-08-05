#!/usr/bin/env python3

import os
import sys
import unicodedata

def to_bool(s): return s in [1,'True','TRUE','true','1','yes','Yes','YES','Y','y']


def get_char_width(c):
    data = unicodedata.east_asian_width(c)
    if data == 'Na' or data == 'H':
        return 1
    return 2


def str_len(string):
    width = 0
    for c in string:
        width += get_char_width(c)
    return width


def ljust(s, mx):
    rest = mx - str_len(s)
    if rest > 0:
        return s + rest * ' '
    return s


def yes_or_no(question, default="yes"):
    CRED = '\033[0;31m'
    CCYAN = '\033[0;36m'
    CGREEN = '\033[0;32m'
    CRESET = '\033[0m'
    valid_table = {"yes": True, "y": True, "no": False, "n": False, "1": True, "0": False}
    if default is None:
        prompt = " [y/n] "
    else:
        if to_bool(default): prompt = " (default: yes)[Y/n] > "
        else: prompt = " (default: no)[y/N] > "


    while True:
        print("\033[0;36m" + question + prompt, end="")
        try:
            choice = input().lower()
            if default is not None and choice == '':
                if to_bool(default):
                    print("\033[2A")
                    print("%s\033[0;32mYes\033[0m" % (question + prompt,), flush=True)
                else:
                    print("\033[2A")
                    print("%s\033[0;31mNo\033[0m" % (question + prompt,), flush=True)
                return to_bool(default)
            elif choice in valid_table:
                if to_bool(choice):
                    print("\033[2A")
                    print("%s\033[0;32mYes\033[0m" % (question + prompt,), flush=True)
                else:
                    print("\033[2A")
                    print("%s\033[0;31mNo\033[0m" % (question + prompt,), flush=True)
                return to_bool(choice)
            else:
                print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
        except (KeyboardInterrupt, EOFError):
            return None

def selector(options, title="Select an item.", default_index=None):
    if len(options) == 0: return None
    if len(options) == 1: return (0, options[0])
    def pre(): print("\033[2A", flush=True)
    import sys
    import time
    import termios
    import contextlib

    @contextlib.contextmanager
    def raw_mode(file):
        old_attrs = termios.tcgetattr(file.fileno())
        new_attrs = old_attrs[:]
        new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
            yield
        finally:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)
    current = 0 if default_index is None else default_index

    def dd(i):
        print(" ", title.ljust(20), flush=True, end='\n')
        index = 0
        for o in options:
            if index == i:
                print("  => ", o.ljust(10), flush=True, end='\n')
            else:
                print("     ", o.ljust(10), flush=True, end='\n')
            index += 1
    dd(current)
    with raw_mode(sys.stdin):
        try:
            while True:
                n = ord(sys.stdin.read(1))
                if n == 0x1b:
                    n = ord(sys.stdin.read(1))
                    if n == 0x5b:
                        n = ord(sys.stdin.read(1))
                        if n == 0x41:
                            # top
                            current -= 1
                            current = max(current, 0)
                            current = min(current, len(options) - 1)
                            for o in range(len(options) + 1): pre()
                            dd(current)
                        elif n == 0x42:
                            # bottom
                            current += 1
                            current = max(current, 0)
                            current = min(current, len(options) - 1)
                            for o in range(len(options) + 1): pre()
                            dd(current)
                        elif n == 0x43:
                            pass
                            # right
                        elif n == 0x44:
                            pass
                            # left
                elif n == 0x0a:  # Enter
                    return (current, options[current])
        except (KeyboardInterrupt, EOFError):
            return (None, None)


def multi_selector(options, title="Select items.", min_count=1, split=10, option_values=None, all=None, radio_button=False, preview=None, padding=True, preview_console=False):
    def pre(): print("\033[2A", flush=True)
    import sys
    import time
    import termios
    import contextlib

    @contextlib.contextmanager
    def raw_mode(file):
        old_attrs = termios.tcgetattr(file.fileno())
        new_attrs = old_attrs[:]
        new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
            yield
        finally:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)
    options2d = [[]]
    multi_selected = []
    if all is not None:
        if radio_button:
            raise "all and radio button cannot be mixed."

        options = [all] + options

        if option_values:
            t = 0
            for o in option_values:
                t += 1
            if t == len(option_values):
                multi_selected.append(1)
            else:
                multi_selected.append(0)
        else:
            multi_selected.append(0)
    for o in options:
        if len(options2d[-1]) >= split:
            options2d.append([])
        options2d[-1].append(o)
    if option_values:
        t = 0
        for o in option_values:
            if o == 0:
                pass
            else:
                t += 1
        if radio_button and t > 1:
            raise "The initial value of the radio button should be 0 or 1."
        for o in option_values:
            multi_selected.append(o)
    else:
        for o in options:
            multi_selected.append(0)

    current = 0
    page = 0
    max_page = int(len(options) / split)
    list_max = len(options2d[0])

    if len(options) % split > 0:
        max_page += 1

    max_width = 0
    for p in options2d:
        for o in p:
            max_width = max(max_width, str_len(o))
    if padding == False:
        max_width = 0

    def _update_display_(i, ignore=False):
        print("\b\r ", title.ljust(20), flush=True, end='\n')
        index = 0

        for o in options2d[page]:
            CH = ""
            if i == index and ignore == False:
                #CH = "\033[7m"
                #CH = "\033[4m"
                CH = "\033[4;32m"
                #\033[0;32m
            if multi_selected[page * list_max + index] == 1:
                #"\033[m"
                print(CH, "\r  [*] ", ljust(o, max_width), "\033[0m", flush=True, end='\n')
            else:
                print(CH, "\r  [ ] ", ljust(o, max_width), "\033[0m", flush=True, end='\n')
            index += 1
        while index < list_max:
            print("".ljust(max_width + 9))
            index += 1
        G = "\033[4;32m"
        R = "\033[0m"
        p = "  "
        if max_page > 1:
            for i in range(max_page):
                if i == page:
                    p += G + str(i + 1) + R
                else:
                    p += str(i + 1)
                p += " "
        print(p.ljust(max_width + 9))

    _update_display_(current)

    with raw_mode(sys.stdin):
        try:
            while True:
                n = ord(sys.stdin.read(1))
                if n == 0x1b:
                    n = ord(sys.stdin.read(1))
                    if n == 0x5b:
                        n = ord(sys.stdin.read(1))
                        if n == 0x41:
                            # top
                            current -= 1
                            current = max(current, 0)
                            current = min(current, len(options2d[page]) - 1)
                            for o in range(list_max + 2): pre()
                            _update_display_(current)
                        elif n == 0x42:
                            # bottom
                            current += 1
                            current = max(current, 0)
                            current = min(current, len(options2d[page]) - 1)
                            for o in range(list_max + 2): pre()
                            _update_display_(current)
                        elif n == 0x43:
                            # right
                            page += 1
                            page = max(page, 0)
                            page = min(page, max_page - 1)
                            current = max(current, 0)
                            current = min(current, len(options2d[page]) - 1)
                            for o in range(list_max + 2): pre()
                            _update_display_(current)
                        elif n == 0x44:
                            # left
                            page -= 1
                            page = max(page, 0)
                            page = min(page, max_page - 1)
                            current = max(current, 0)
                            current = min(current, len(options2d[page]) - 1)
                            for o in range(list_max + 2): pre()
                            _update_display_(current)
                elif n == 0x0a:  # Enter
                    if sum(multi_selected) >= min_count:
                        for o in range(list_max + 2): pre()
                        _update_display_(current, True)
                        ret = []
                        if all is not None:
                            multi_selected.pop(0)
                            options.pop(0)
                        i = 0
                        for f in multi_selected:
                            if f == 1: ret += [(i, options[i])]
                            i += 1
                        return ret
                    else:
                        for o in range(list_max + 2): pre()
                        _update_display_(current)

                elif n == 0x20:  # Space
                    if all and current == 0 and page == 0:
                        if multi_selected[current] == 0:
                            for i in range(len(multi_selected)):
                                multi_selected[i] = 1
                        else:
                            for i in range(len(multi_selected)):
                                multi_selected[i] = 0
                            # multi_selected[0] = 0
                    else:
                        if radio_button:
                            for i in range(len(multi_selected)):
                                multi_selected[i] = 0
                            multi_selected[page * list_max + current] = 1
                        else:
                            if multi_selected[page * list_max + current] == 0:
                                multi_selected[page * list_max + current] = 1
                            else:
                                multi_selected[page * list_max + current] = 0
                    for o in range(list_max + 2): pre()
                    _update_display_(current)
                elif n == 0x40:  # @
                    try:
                        import aimage
                        if preview:
                            if preview[page * list_max + current] is not None:
                                for i in range(100): print("\b")
                                if aimage.isnotebook(): import IPython; IPython.display.clear_output()
                                else: print("\b\033[0;0f", end="")
                                print("Previewing...\b")
                                aimage.show(preview[page * list_max + current], preview_console)
                                aimage.clear_output()
                    except:
                        pass
        except (KeyboardInterrupt, EOFError):
            pass
