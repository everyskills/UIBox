#!/usr/bin/python3

import re
from PyQt5 import QtWidgets

class Controls:
    def __init__(self, parent=None) -> None:
        self.__parent = parent
        self.cb = QtWidgets.QApplication.clipboard()

        ## Whenever clipboard data changes
        # self.cb.dataChanged.connec()

    def close_win(self):
        self.__parent.close()

    def hide_win(self):
        self.__parent.hide()

    def show_win(self):
        self.__parent.show()

    def set_win_height(self, h: int):
        if not h < 70:
            self.__parent.setFixedHeight(h)
        
    def set_win_width(self, w: int):
        if not w > 700:
            self.__parent.setFixedWidth(w)

    def set_win_size(self, w: int, h: int):
        self.__parent.setFixedSize(w, h)

    def set_small_mode(self):
        self.__parent.def_setup.small_size()
    
    def set_extend_mode(self):
        self.__parent.def_setup.larg_size()

    def get_input(self, text: str):
        patt = re.compile(r"\$\(([a-z-A-Z_0-9]+)\)")
        find = patt.findall(text)
        for i in find:
            text = patt.sub(self.__parent.global_vars.get(i.strip(), ""), text)
        return text

    def text_changed(self, func: object):
        self.__parent.input.textChanged.connect(func)
    
    def get_text(self):
        try:
            return self.__parent.get_kv(self.__parent.input.text())[1].strip()
        except IndexError:
            return ""

    def set_text(self, text: str):
        self.__parent.input.setText(self.__parent.get_kv(self.__parent.input.text())[0] + " " + text)

    def insert_text(self, text: str):
        self.__parent.input.setText(self.__parent.input.text() + text)

    def insert_in_cursor(self, text: str):
        cur = self.__parent.input.cursorPosition()
        self.__parent.input.setCursorPosition(cur)
        txt = self.__parent.get_kv(self.__parent.input.text())[1]
        txt = txt[0:cur] + text + txt[cur:]
        self.__parent.input.insert(text)
        self.__parent.input.setFocus()

    def return_pressed(self, call: object):
        self.__parent.input.blockSignals(True)
        self.__parent.input.returnPressed.connect(call)
        self.__parent.input.blockSignals(False)

    def set_auto_complete(self, Iterable: list=[]):
        text = self.get_text()
        for i in Iterable:
            if text and text.startswith(i[0].lower()) and text in i:
                self.__parent.input.blockSignals(True)
                ######### auto type 1
                self.set_text(text + i[len(text):] + " ")
                self.__parent.input.setCursorPosition(
                    int(len(text)) + len(self.__parent.get_kv(self.__parent.input.text())[0]) + 1)
                self.__parent.input.cursorForward(True, int(len(text)) + int(len(i)))
                self.__parent.input.blockSignals(False)

    @property
    def mode_style(self):
        return 'dark' if 'dark' in self.__parent.win_setting.mode_style else 'light'

    @property
    def style_mode(self):
        return self.mode_style

    @property
    def style(self):
        return self.mode_style

    @property
    def text(self):
        return self.get_text()

    @property
    def value(self):
        return self.get_text()
        
    @property
    def result(self):
        return self.get_text()

    def text_copy(self, text: str=""):
        if not text:
            self.__parent.input.copy()
        else:
            self.cb.setText(text)

    def text_cut(self):
        self.__parent.input.cut()

    def text_paste(self, get: bool=False):
        if not get:
            self.__parent.input.paste()
        else:
            return self.cb.text()


    def by_key(self, key: str, default=None) -> dict:
        _dict = {}
        args = self.text.split()
        for i in range(len(args)):
            try:
                _dict.update({args[i]: args[i + 1]})
            except IndexError:
                _dict.update({args[i]: ""})
        return _dict.get(key, default)

    def reload_page(self, count: int=1):
        # print("web is reloaded")
        for _ in range(count):
            self.__parent.web.run_plugin(self.__parent.web_running_data)
            # self.__parent.web.web_view.reload()


    # def web_reload(self):
    #     self.__parent.run_plugin(self.__parent.get_kv(self.__parent.input.text())[0])

    # def insert_in_selecte(self, text: str=""):
    #     # self.__parent.input.selectedText()
    #     self.send = self.__parent.input.selectionEnd()
    #     self.sstart = self.__parent.input.selectionStart()
    #     print("Start: ", self.sstart, "End: ", self.send)
