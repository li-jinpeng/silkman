import requests
import json

class Tools:

    def __init__(self):
        self.infomation = '15660603091',\
            'https://login.bce.baidu.com/',\
                '15660603091Ljp'

    def translate_text(self,text,fr,to):
        url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=24.3126b7c829ff89c077d798fc4b627655.2592000.1669792992.282335-28173688"
        data = {
            "from":fr,
            "to":to,
            "q":text,
        }
        headers = {'Content-Type': 'application/json'}
        try:
            res = requests.post(url=url,params=data,headers=headers)
            response = res.json()
        except:
            return 'fail',''
        if 'result' in response:
            dst = response['result']["trans_result"][0]['dst']
            return 'success', dst
        return 'fail',''
        
    def translate_image(self,image_path,fr,to,v='3',paste='0'):
        url = "https://aip.baidubce.com/file/2.0/mt/pictrans/v1?access_token=24.3126b7c829ff89c077d798fc4b627655.2592000.1669792992.282335-28173688"
        data = {
            "from":fr,
            "to":to,
            "v":v,
            "paste":paste
        }
        files = {'image':open(image_path,'rb')}
        try:
            res = requests.post(url=url,data=data,files=files)
            response = json.loads(res.text)
        except:
            return 'fail',{}
        if response['error_code'] == '0':
            text = []
            for i in response['data']['content']:
                tmp_text = {}
                tmp_text['zh'] = i['src']
                tmp_text['en'] = i['dst']
                text_ = i['dst']
                state, text_ = self.translate_text(text_,'en','ru')
                if state == 'success':
                    tmp_text['ru'] = text_
                tmp_text['rect'] = i['rect']
                text.append(tmp_text)
            text_json = {}
            text_json['content'] = text
            return 'success', text_json
        return 'fail', {}