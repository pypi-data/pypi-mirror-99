import os


def get_camera_shot(cam_login, cam_pw, cam_ip):
    # Вернуть функцию для фотографирования
    cam_com = 'http://{}-{}@{}/ISAPI/Streaming/channels/101/picture?snapShotImageType=JPEG'.format(cam_login, cam_pw,
                                                                                                   cam_ip)
    return cam_com


def join_tuple_string(msg):
    return ' '.join(map(str, msg))


def remove_photo(photo_name):
    print('Removing photo:', photo_name)
    os.remove(photo_name)
