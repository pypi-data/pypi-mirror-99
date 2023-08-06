import os
class ServerAdress(object):
    MF_SERVER = "http://api-magicframe.automusic.win"
    MAIL_SERVER="http://178.128.211.227"
    COLAB_URL = "https://colab.research.google.com/drive/1h8B8nTG-fzSN2SXW_yItCG1KtBldUQR0"
class ImageResource(object):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ICON_GOOGLE=dir_path+"/res/google.png"
    ICON_PUBLIC=dir_path+"/res/public.png"
    UPLOAD_BUTTON=dir_path+"/res/upload_button.png"
    RECOVERY_MAIL=dir_path+"/res/confirm_email.png"
class Client(object):
    FF_EXT=".exe"
    FF_ROOT_FOLDER=""
    CLIENT_TIMEOUT=23400 #6h30
    GECKO_LOG=''


