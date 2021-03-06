#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os

from glob import glob
from subprocess import PIPE
from PyQt5.QtGui import QDesktopServices, QIcon, QMovie
from PyQt5.QtCore import QFileInfo, QUrl, QSize
from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.uic import loadUi
from UIBox import pkg, item

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Results(QWidget):
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)

        self.parent = parent

        self.ui = loadUi(base_dir + "UI.ui", self)

        self.ui.list_widget.itemDoubleClicked.connect(self.add_click_path)
        self.ui.list_widget.itemSelectionChanged.connect(self.get_path_info)
        self.ui.btn_video.clicked.connect(self.start_video)
        self.ui.slide_video.sliderMoved.connect(self.set_video_pos)

        enterAction = QAction("enter", self.ui.list_widget, shortcut="Ctrl+Return", triggered=lambda: self.add_click_path(dirn=True))
        self.ui.list_widget.addAction(enterAction)
        
        self.lpermissions.hide() # label
        self.start_up()

    def __run__(self):
    	self.query_file()

    def init_ui(self):
        self.ui.list_widget.clear()

        # self.short_title(os.path.split(str(self.parent.get_text()).strip())[1])
        # self.start_up()

    def get_enter_item(self):
        self.add_click_path(self.ui.list_widget.currentItem())
        self.ui.list_widget.setFocus()

    def start_up(self):
        self.ui.slide_video.hide()
        self.ui.label_slide_value.hide()
        self.ui.btn_video.hide()

    def query_file(self):
        self.ui.list_widget.clear()

        query = self.parent.get_text()

        _in = self.parent.by_key("in", index=1)
        dirn = "~/" if not _in else _in

        _icon = pkg.icon_types(query)
        self.ui.image.setPixmap(pkg.set_image(_icon, icon=True, size=150))

        _file_count, _folder_count, _size = 0, 0, 0.00

        for _file, _path in pkg.find_in_all(query, dirn).items():
            
            if _path.endswith(tuple(pkg.api_icons("Image"))):
                _icon = QIcon(_path)
            else:
                _icon = pkg.icon_types(_path)

            if not os.path.isfile(_path):
                _folder_count += 1

            elif not os.path.isdir(_path):
                _file_count += 1

            try:
                _size += os.path.getsize(_path)
            except FileNotFoundError:
                _size = 0

            list_item = pkg.add_item(self.ui.list_widget, _icon)
            name = os.path.basename(_file).replace(query, f"<font color='#1a81da'>{query}</font>")
            item_widget = pkg.add_item_widget(list_item, item.UIBUi_Item(), name, _path)
            pkg.set_item_widget(self.ui.list_widget, item_widget)
            self.ui.status.setText(f"{_folder_count} {'Folder' if _folder_count <= 1 else 'Folders'}, {_file_count} {'File' if _file_count <= 1 else 'Files'}") # ({naturalsize(_size, True, format='%.1f ')})
        
    def hide_video(self):
        try:
            if self.video_player.media.is_playing():
                self.video_player.media.stop()
        except AttributeError:
            pass
        
        self.ui.btn_video.hide()
        self.ui.slide_video.hide()
        self.ui.label_slide_value.clear()
        self.ui.slide_video.hide()

    def show_video(self):
        self.ui.btn_video.setIcon(QIcon(base_dir + "icons/play.png"))
        self.ui.slide_video.setValue(0)
        self.ui.btn_video.show()
        self.ui.slide_video.show()
        self.ui.label_slide_value.show()

    def get_path_info(self):
        item = self.ui.list_widget.currentItem()
        litem = item.listWidget().itemWidget(item)

        _file = litem.title.text()
        _path = litem.desc.text()

        self.short_title(_file)
        self.set_data(_path)

        try:
            img = tuple(pkg.api_icons("Image"))
            video = tuple(pkg.api_icons("Video"))
            audio = tuple(pkg.api_icons("Audio"))
        except TypeError:
            pass

        if _file.endswith(".gif"):
            self.hide_video()
            movie = QMovie(_path)
            movie.setScaledSize(QSize(300, 200))
            self.ui.image.setMovie(movie)
            movie.start()
       
        elif _file.endswith(img):
            self.hide_video()
            self.ui.image.setPixmap(pkg.set_image(item.icon(), size=300))

        elif _file.endswith(video) or _file.endswith(audio):
            self.video_player = pkg.video_player(
                self.ui.image, "", self.media_time_changed)
            
            self.ui.image.setPixmap(pkg.set_image(item.icon(), size=150))
            self.video_player.set_media(_path)
            self.show_video()

            video_screen_img_path = base_dir + "icons/"
            self.video_player.media.video_take_snapshot(0, 
                str(video_screen_img_path + _file),
                i_width=self.video_player.media.video_get_width() + 10, 
                i_height=self.video_player.media.video_get_height() + 10)
        else:
            self.hide_video()
            self.ui.image.setPixmap(pkg.set_image(item.icon(), size=150))
            
    def set_data(self, _file):
        ff = QFileInfo(_file)
        self.short_title(ff.fileName())
        self.ui.lsize.setText(pkg.get_size(ff.size()))

        if ff.isDir():
            self.ui.litems.show()
            self.ui.label_3.show()
            self.ui.litems.setText(str(len(glob(_file + "/*"))))
        else:
            self.ui.label_3.hide()
            self.ui.litems.hide()

        self.ui.lcreated.setText(ff.created().toString())
        self.ui.lmodified.setText(ff.lastModified().toString())
        self.ui.laccessed.setText(ff.lastRead().toString())
        self.ui.luser.setText(ff.owner())
        self.ui.luid.setText(str(ff.ownerId()))
        self.ui.lgroup.setText(str(ff.group()))
        self.ui.lgid.setText(str(ff.groupId()))
        self.ui.lpath.setText(ff.path())
        # self.lpermissions.setText(str(ff.permissions())

    def add_click_path(self, dirn: bool=False):
        try:
            main_item = self.ui.list_widget.currentItem()
            item = main_item.listWidget().itemWidget(main_item)
            _path = item.desc.text()

            self.set_data(_path)

            if dirn:
                _path = os.path.dirname(_path)

            QDesktopServices().openUrl(QUrl().fromUserInput(_path))
            
            self.parent.hide_win()
        except AttributeError:
            # self.query_file()
            pass

    def short_title(self, item: str):
        if len(item) <= 20:
            self.ui.title.setText(item)
        else:
            self.ui.title.setText(item[0:21] + "...")

    def start_video(self):
        if self.video_player.media.is_playing():
            self.video_player.media.pause()
            self.ui.btn_video.setIcon(QIcon(base_dir + "icons/play.png"))
        else:
            self.video_player.media.play()
            self.ui.btn_video.setIcon(QIcon(base_dir + "icons/pause.png"))

    def set_video_pos(self):
        pos = self.ui.slide_video.value()
        self.video_player.media.set_position(pos / 100)

    def media_time_changed(self, event):
        pos = self.video_player.media.get_position() * 100
        self.ui.slide_video.setValue(int(pos))        
        self.ui.label_slide_value.setText(str(int(pos)) + "%")

        if int(pos) >= 100 or int(pos) >= 99:
        	self.ui.slide_video.clear()
        	self.video_player.media.set_position(0.00)
        	self.ui.slide_video.setValue(0)
        	self.video_player.media.pause()
