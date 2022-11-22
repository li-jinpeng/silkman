from manage_type import *
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.ERROR)

class crawler:

    def __init__(self):
        self.sku_dict = {}
        self.global_data = Global

        #搜索页下的spu链接  f"https:{spu_url.get('href')}"
        self.spu_url_path = '#J_goodsList > ul > li > div > div.p-img > a'
        #sku详情页的spu封面图链接   f"https:{image_path.get('src')}"
        self.cover_image_path = "#spec-list > ul > li.img-hover > img"
        #品牌 brand[0].get('href')
        self.brand_path = '#parameter-brand > li > a'
        # #video  get('src')
        # self.video_path = '#video-player_html5_api > source'
        # sku_pic  'src'
        self.sku_image_path = '#spec-list > ul > li > img'
        #sku详情  'title'
        self.sku_info_path = '#detail > div.tab-con > div:nth-child(1) > div.p-parameter > ul.parameter2.p-parameter-list > li'

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # 忽略无用的日志
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        options.add_argument('--headless')
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        self.browser = webdriver.Chrome(
            'drivers/chromedriver', chrome_options=options) 
    
    def get_webcode(self,url):
        self.browser.get(url)
        # try:
        #     self.browser.find_element_by_xpath('//*[@id="spec-n1"]/ul/li/span').click()
        # except:
        #     pass
        return self.browser.page_source
        
    
    def get_attr_path(self,index):
        return f'#choose-attr-{index+1}'
    
    def get_attr_value_path(self,index):
        return f'#choose-attr-{index+1} > div.dd > div'

    def id2url(self,id):
        return f'https://item.jd.com/{id}.html'

    def url2id(self,url):
        return url.split('/')[-1].split('.')[0]

    def get_spu_info(self,url):
        spu = {}
        spu['show_sku_url'] = url
        soup = BeautifulSoup(self.get_webcode(url), 'lxml')
        for image_path in soup.select(self.cover_image_path):
            spu['cover'] = img_resize(f"https:{image_path.get('src')}")
        spu['attr_name'] = []
        attr_value_list = []
        for choose_attr_index in range(self.global_data.Default_attr_num):
            try:
                choose_attr_path = self.get_attr_path(choose_attr_index)
                attr_data = soup.select(choose_attr_path)
                for attr_item in attr_data:
                    spu['attr_name'].append(attr_item.get('data-type'))
                attr_value_path = self.get_attr_value_path(choose_attr_index)
                attr_values = soup.select(attr_value_path)
                for attr_value in attr_values:
                    attr_state = attr_value.get('class')
                    if 'selected' in attr_state:
                        attr_value_list.append(attr_value.get('data-value'))
            except:
                logging.info(f"{url} without {choose_attr_index+1}th attr!")
        title = soup.find(name="div", attrs={"class" :"sku-name"}).text.lstrip().rstrip()
        spu['title'] = title
        title_items = title.split(' ')
        for attr_v in attr_value_list:
            for title_item in title_items:
                if title_item in attr_v or attr_v in title_item:
                    title_items.remove(title_item)
        spu['name'] = ' '.join(title_item for title_item in title_items)
        sku_id = self.url2id(url)
        class_name = f"price J-p-{sku_id}"
        spu['price'] = soup.find(name="span", attrs={"class" :class_name}).text.lstrip().rstrip()
        brand = soup.select(self.brand_path)
        brand_href = brand[0].get('href')
        spu['brand'] = soup.find(name = 'a',attrs={'href':brand_href}).text.lstrip().rstrip()
        # try:
        #     spu['video'] = soup.select(self.video_path)[0].get('src')
        # except:
        #     logging.info(f'{url} does not have video!')
        self.sku_dict = {sku_id:{}}
        self.get_sku(sku_id)
        spu['sku_info'] = self.sku_dict
        return spu

    def get_spu(self,search_url,spu_pages,spu_clips):
        spu_list = []
        for page_index in range(int(spu_pages)):
            group_url = search_url + "&page=" + str(int(page_index)+1)
            print(group_url)
            soup_outer = BeautifulSoup(self.get_webcode(group_url), 'lxml')
            url_data = soup_outer.select(self.spu_url_path)
            count = 0
            print(len(url_data))
            for spu_url in url_data:
                logging.info(f'========== CRAWER PROCESS: page:{page_index+1}/{spu_pages} : {count}/{len(url_data)} ===========')
                count += 1
                url = f"https:{spu_url.get('href')}"
                try:
                    spu = self.get_spu_info(url)
                    spu_list.append(spu)  
                except:

                    logging.info(f"Can't get some infomation of {url}!") 
        clip_index = 0
        group_url = search_url + "&page=" + str(int(spu_pages)+1)
        soup_outer = BeautifulSoup(self.get_webcode(group_url), 'lxml')
        url_data = soup_outer.select(self.spu_url_path)
        for spu_url in url_data:
            logging.info(f'========== CRAWER PROCESS: clip:{clip_index+1}/{int(spu_clips)} ===========')
            url = f"https:{spu_url.get('href')}"
            try:
                spu = self.get_spu_info(url)
                spu_list.append(spu)  
            except:
                logging.info(f"Can't get some infomation of {url}!")
            clip_index += 1
            if clip_index >= int(spu_clips): break
        
        return spu_list

    def get_sku(self,sku_id):
        logging.info(f'=========== Current sku {sku_id} / {len(self.sku_dict.keys())}===============')
        sku_url = self.id2url(sku_id)
        soup = BeautifulSoup(self.get_webcode(sku_url), 'lxml')
        self.sku_dict[sku_id]['image'] = []
        sku_images = soup.select(self.sku_image_path)
        for sku_image in sku_images:
            sku_image_url = sku_image.get('src')
            self.sku_dict[sku_id]['image'].append(img_resize(f'https:{sku_image_url}'))
        title = soup.find(name="div", attrs={"class" :"sku-name"}).text.lstrip().rstrip()
        self.sku_dict[sku_id]['title'] = title
        class_name = f"price J-p-{sku_id}"
        self.sku_dict[sku_id]['price'] = soup.find(name="span", attrs={"class" :class_name}).text.lstrip().rstrip()
        self.sku_dict[sku_id]['attr_value'] = []
        self.sku_dict[sku_id]['info'] = {}
        info_titles = soup.select(self.sku_info_path)
        for info_title in info_titles:
            title = info_title.get('title')
            info = soup.find(name='li',attrs={'title':title}).text.lstrip().rstrip()
            info = info.split("：")
            self.sku_dict[sku_id]['info'][info[0]] = info[1]
        # comment = soup.find(name='div',attrs={'class':'percent-con'}).text.lstrip().rstrip()
        # self.sku_dict[sku_id]['comment'] = f'{comment}%'
        for choose_attr_index in range(self.global_data.Default_attr_num):
            try:
                attr_value_path = self.get_attr_value_path(choose_attr_index)
                attr_values = soup.select(attr_value_path)
                for attr_value in attr_values:
                    attr_state = attr_value.get('class')
                    sku_id_ = attr_value.get('data-sku')
                    if 'selected' in attr_state:
                        self.sku_dict[sku_id]['attr_value'].append(attr_value.get('data-value'))
                    if 'no-stock' not in attr_state and sku_id_ not in self.sku_dict:
                        self.sku_dict[sku_id_] = {}
                        self.get_sku(sku_id_)              
            except:
                logging.info(f"{sku_url} without {choose_attr_index+1}th attr!")
 
    def get_image(self,out_path,url):
        os.system(f'wget {url} -O {out_path} -q')


    def get_video(self,url):
        pass

    def manager(self):
        while True:
            command = input("输入0下载图片;输入1下载spu_sku信息;输入2退出:")
            if command == '0':
                url = input("输入图片url:")
                out_path = input("输入图片输出路径:")
                self.get_image(out_path,url)
                logging.info(f'{url} download in {out_path} just now')
            elif command == '1':
                url = input("输入一个商品详情页url:")
                logging.info(f'we need a few minutes to finish it...')
                spu = self.get_spu_info(url)
                out_path = os.path.join(self.global_data.OUT_PATH,self.global_data.OUT_SPU_NAME)
                json.dump(spu, open(out_path,'w',encoding='utf-8'), indent=4, ensure_ascii=False)
                logging.info(f'spu信息已保存在{out_path}')
            elif command == '2':
                logging.info('crawler qiut!')
                break
            else:
                logging.info(f'ERROR command {command}')


