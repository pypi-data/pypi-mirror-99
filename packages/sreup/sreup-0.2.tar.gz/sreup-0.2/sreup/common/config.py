import os
class ServerAdress(object):
    IP="http://167.99.74.94"
    REUP_SERVER = "http://sreup.singerchart.com/"
class ImageResource(object):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ICON_GOOGLE=dir_path+"/res/google.png"
    ICON_PUBLIC=dir_path+"/res/public.png"
    UPLOAD_BUTTON=dir_path+"/res/upload_button.png"
    RECOVERY_MAIL=dir_path+"/res/confirm_email.png"
class Client(object):
    EXT=".exe"
    ROOT_FOLDER=""
class Timeout(object):
    CLIENT=600
    THREAD=86400
class TimeSleep(object):
    NO_JOB=60
    EXCEPT=30