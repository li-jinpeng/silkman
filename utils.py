import os
import datetime
import random
import string
import re

def get_random_str(length=20):
        return ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(length))
    
def list2dict(list):
    dict = {}
    index = 0
    for i in list:
        dict[index] = i
    return dict

def img_resize(url):
    url = url.replace('n0','n1').replace('.avif','')
    pattern = '(/s.*jfs/)|(/jfs/)'
    return re.sub(pattern,'/s800x800_jfs/',url)

class Global:
    data_root = os.path.join(os.getcwd(),'data')
    Default_database = 'init'
    Default_attr_num = 3
    Default_imgName = 'origin.jpg'
    Default_TextName = 'text_layout.json'
    OUT_PATH = os.path.join(os.getcwd(),'out')
    OUT_SPU_NAME = 'spu.json'
    XLSX_PATH = os.path.join(os.getcwd(),'xlsx')
    stop_time = 5*60

    def __init__(self):
        self.time = datetime.datetime.now()
    
    