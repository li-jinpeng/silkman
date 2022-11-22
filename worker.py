from utils import * 
import xlrd
from manage_type import *
from crawler import *
from web_tools import *
from web_tools import *
import time

class Worker:

    def __init__(self,xlsx_name):
        self.global_data = Global
        self.xlsx_name = xlsx_name
        self.xlsx_path = os.path.join(self.global_data.XLSX_PATH,xlsx_name,f'{xlsx_name}.xlsx')
        self.work_time = '99999h'
        self.work_log = os.path.join(self.global_data.XLSX_PATH,xlsx_name,'work.txt')
        if os.path.exists(self.work_log) is False:
            with open(self.work_log,'w',encoding='utf-8') as log:
                    log.write(' '.join(['name','type','done']))
                    log.close()
        self.tasks = xlrd.open_workbook(self.xlsx_path).sheets()[0]
        self.type_manager = TypeManager()
        self.type_manager.create_database(xlsx_name)
        self.type_manager.set_database(xlsx_name)
        self.tools = Tools()
        self.crawler_manager = crawler()
        
    def get_search_url(self,key_word):
        return f'https://search.jd.com/Search?keyword={key_word}&psort=3'

    def get_work_time(self):
        if 'min' in self.work_time:
            work_time = float(self.work_time.replace('min',''))
            return 60*work_time
        elif 'h' in self.work_time:
            work_time = float(self.work_time.replace('h',''))
            return 60*60*work_time

    def pull_data(self):
        with open(self.work_log,'r',encoding='utf-8') as log:
            log_text = log.read()
            log_texts = log_text.split(' ')
            if log_texts[-1] != 'done':
                _group_name, _type_name = log_texts
                self.type_manager.delete_type(_group_name,_type_name)
        work_time = self.get_work_time()
        start = time.clock()
        for task in range(self.tasks.nrows):
            end = time.clock()
            if work_time - (end - start) < self.global_data.stop_time:
                logging.info(f'==== Time Over: {task}/{self.tasks.nrows}  ======')
                return
            logging.info(f'======= TASK PROCESS: {task}/{self.tasks.nrows}; TIME: {(end - start)//60}/{work_time//60} min=========')
            group_name = self.tasks.cell(task,0).value
            type_name = self.tasks.cell(task,1).value
            spu_pages = self.tasks.cell(task,2).value
            spu_clips = self.tasks.cell(task,3).value
            with open(self.work_log,'w',encoding='utf-8') as log:
                log.write(' '.join([group_name,type_name]))
                log.close()
            group_path = os.path.join(self.global_data.data_root,self.type_manager.database,group_name)
            type_path = os.path.join(group_path, type_name)
            if os.path.exists(type_path) is False:
                self.type_manager.create_type(group_name,type_name)
                spu_list = self.crawler_manager.get_spu(self.get_search_url(type_name),spu_pages,spu_clips)
                for spu in spu_list:
                    spu_id = self.type_manager.create_spu(group_name,type_name)
                    spu_path = os.path.join(type_path,spu_id)
                    spu_info_json_path = os.path.join(spu_path,'spu_info.json')
                    with open(spu_info_json_path,'r',encoding='utf-8') as info_file:
                        info_json = json.load(info_file)
                        info_file.close()
                    info_json['content'] = spu
                    json.dump(info_json,open(spu_info_json_path,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
                    cover_path = os.path.join(spu_path,'cover','cover.jpg')
                    cover_url = spu['cover']
                    self.crawler_manager.get_image(cover_path,cover_url)
                    for sku_id,sku_content in spu['sku_info'].items():
                        self.type_manager.create_sku(group_name,type_name,spu_id,sku_id)
                        sku_path = os.path.join(spu_path,'sku',sku_id)
                        image_path_ = os.path.join(sku_path,'image')
                        for image_url in sku_content['image']:
                            image_path = os.path.join(image_path_,f'{sku_id}_{get_random_str(10)}')
                            os.mkdir(image_path)
                            image_name = self.global_data.Default_imgName
                            self.crawler_manager.get_image(os.path.join(image_path,image_name),image_url)
                            state, text_json = self.tools.translate_image(os.path.join(image_path,image_name),'zh','en')
                            if state == 'success':
                                json.dump(text_json,open(os.path.join(image_path,self.global_data.Default_TextName),'w',encoding='utf-8'),indent=4,ensure_ascii=False)
            with open(self.work_log,'w',encoding='utf-8') as log:
                log.write(' '.join([group_name,type_name,'done']))
                log.close()

    def push_data(self):
        pass

    def merge_data(self):
        pass
    
    def manager(self):
        work_time = input('输入执行时间，单位min或h，跳过则默认任务完成时停止:')
        if work_time != '':
            self.work_time = work_time
        logging.info(f'--------------------------开始执行任务 {self.xlsx_name}------------------------')
        logging.info('---------------------------------阶段1：爬取数据--------------------------------')
        self.pull_data()
        self.crawler_manager.browser.close()
        logging.info('------------------------------- 完成 -------------------------------------')
        #logging.info('--------------------------------阶段2：上传到数据库----------------------')
        #self.push_data()


