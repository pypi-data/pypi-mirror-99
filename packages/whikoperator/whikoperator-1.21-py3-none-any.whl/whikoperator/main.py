import requests
from requests.auth import HTTPBasicAuth
import os
from whikoperator import settings
import whikoperator.functions as funcs


class Wpicoperator:
    """ Модуль для работы с видео-камерой HikVision """

    def __init__(self, cam_ip, cam_login, cam_pass,
                 pics_folder=settings.DEF_PICS_DIR,
                 pics_journal=settings.PICS_JOURNAL_PATH,
                 count_file_path=settings.COUNT_FILE_PATH,
                 debug=False, count=True):
        self.show_print('\nИнициализация модуля работы с камерой HikVision')
        self.debug = debug
        self.pics_folder = pics_folder
        self.count_file = count_file_path
        self.pics_journal = pics_journal
        # Сохранить данные для логина к API камеры
        self.cam_ip = cam_ip
        self.cam_login = cam_login
        self.cam_pass = cam_pass
        self.if_count = count
        if self.if_count:
            self.count = self.get_photo_count()

    def get_photo_count(self):
        self.show_print('\nExtracting count..', debug=True)
        with open(self.count_file, 'r') as fobj:
            count = fobj.read()
        self.show_print('\tReturning count:', count, debug=True)
        return count

    def make_pic(self, name='deff'):
        # Сделать фото с именем name. Если имя не задано - использовать счетчик
        if name == 'deff':
            name = self.count
        photo_data = self.take_shot()
        photo_abs_name = self.get_pic_name(name)
        self.save_photo(photo_abs_name, photo_data)
        self.make_journal_record(photo_abs_name)
        if self.if_count:
            self.increm_count()
            self.save_new_count()
        return photo_data

    def take_shot(self):
        # Сделать фото
        self.show_print('\nTaking a shot', debug=True)
        shot_command = funcs.get_camera_shot(self.cam_login, self.cam_pass, self.cam_ip)
        response = requests.get(shot_command, auth=HTTPBasicAuth(self.cam_login, self.cam_pass))
        data = response.content
        return data

    def save_photo(self, pic_path, data):
        # Сохранить данные фото (data) в pic_path
        self.show_print('\tSaving photo:', pic_path, debug=True)
        pic = open(pic_path, 'wb')
        pic.write(data)
        pic.close()
        self.show_print('\tSuccess!', debug=True)

    def get_pic_name(self, name):
        # Вернуть абсолютный путь до будущей фотографии
        pic_name = '{}.jpg'.format(name)
        fullname = os.sep.join((self.pics_folder, pic_name))
        return fullname

    def increm_count(self):
        # Инкреминтировать счетчик
        if not self.count.isdigit():
            self.count = 0
        count = int(self.count)
        count += 1
        self.count = str(count)

    def save_new_count(self):
        # Сохранить новый счетчки
        count_file = open(self.count_file, 'w')
        count_file.write(self.count)
        count_file.close()

    def make_journal_record(self, photo_abs_name):
        # Добавить абсолютный путь фото в журнал
        with open(self.pics_journal, 'a') as fobj:
            fobj.write(photo_abs_name)
            fobj.write('\n')

    def erase_jornal(self):
        fpath_file = open(self.pics_journal, 'w')
        fpath_file.close()

    def show_print(self, *msg, debug=False):
        msg = funcs.join_tuple_string(msg)
        if debug and self.debug:
            print(msg)
        elif not debug:
            print(msg)
