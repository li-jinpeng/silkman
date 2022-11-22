from utils import *
import os
import datetime
import json
import logging
import shutil
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

SUCCESS = 1
FAIL = 0
ERROR = -1

GroupIDLength = 8
TypeIDLength = 12
SpuIDLength = 20

class TypeManager:
    database = ''

    def __init__(self):
        self.global_data = Global
        self.database = self.global_data.Default_database
        database_path = os.path.join(self.global_data.data_root,self.database)
        if os.path.exists(database_path) is False:
            self.create_database(self.database)
        self.log = os.path.join(database_path, 'log.json')
        self.error = os.path.join(database_path, 'error.txt')

    def create_database(self, database_name):
        database_path = os.path.join(self.global_data.data_root,database_name)
        if os.path.exists(database_path) is False:
            os.mkdir(database_path)
            init_json = {}
            init_json['title'] = 'silkman_data'
            now_time=datetime.datetime.now()
            init_json['last_edited'] = str(now_time)
            init_json['group'] = []
            log_json = open(os.path.join(database_path,'log.json'),'w',encoding='utf-8')
            json.dump(init_json,log_json,indent=4,ensure_ascii=False)
            log_json.close()
            error = open(os.path.join(database_path,'error.txt'),'w')
            error.close()
            logging.info(f'{database_name} is created!')
        else:
            logging.info(f'{database_name} already exists! \n \
                ==========Input 0 to delete {database_name} and create the new one or enter to ignore this message!==========\n')
            command = input('Please input:')
            if command is '0':
                self.delete_database(database_name)
                return self.create_database(database_name)
        return database_name

    def delete_database(self,database_name):
        database_path = os.path.join(self.global_data.data_root,database_name)
        if os.path.exists(database_path) is False:
            logging.info(f'You want to delete {database_name}, but it not exists!')
        else:
            shutil.rmtree(database_path)
            logging.info(f'{database_name} is deleted')
        return 
    
    def set_database(self,database_name):
        self.database = database_name
        database_path = os.path.join(self.global_data.data_root,self.database)
        self.log = os.path.join(database_path, 'log.json')
        self.error = os.path.join(database_path, 'error.txt')
        if os.path.exists(database_path) is False:
            logging.info(f'{database_name} not exists! But it is created!')
            self.create_database(self.database)
        logging.info(f'Success! Current database is {database_name}!')

    def create_type(self, group_name, type_name):
        group_path = os.path.join(self.global_data.data_root,self.database,group_name)
        type_path = os.path.join(group_path, type_name)
        try:
            if os.path.exists(group_path) is True:
                os.mkdir(type_path)
                with open(self.log,'r',encoding='utf-8') as log_file:
                    json_log = json.load(log_file)
                log_file.close()
                new_log = {}
                new_log['title'] = 'silkman_data'
                now_time=datetime.datetime.now()
                new_log['last_edited'] = str(now_time)
                new_log['group'] = []
                for i in json_log['group']:
                    if i['group_name'] != group_name:
                        new_log['group'].append(i)
                    else:
                        tmp = i['types']
                        tmp_type = {}
                        tmp_type['type_name'] = type_name
                        new_type_json['type_id'] = get_random_str(TypeIDLength)
                        tmp_type['spu'] = []
                        tmp.append(tmp_type)
                        tmp_group = {}
                        tmp_group['group_name'] = i['group_name']
                        tmp_group['types'] = tmp
                        new_log['group'].append(tmp_group)
                with open(self.log,'w',encoding='utf-8') as log_file:
                    json.dump(new_log, log_file, indent=4, ensure_ascii=False)
                    log_file.close()
            else:
                os.mkdir(group_path)
                os.mkdir(type_path)
                with open(self.log,'r',encoding='utf-8') as log_file:
                    size = os.path.getsize(self.log)
                    if size != 0:
                        log_json = json.load(log_file)
                log_file.close()
                new_log = {}
                new_log['title'] = 'silkman_data'
                now_time=datetime.datetime.now()
                new_log['last_edited'] = str(now_time)
                new_log['group'] = []
                if size != 0 and 'group' in log_json:
                    new_log['group'] = log_json['group']
                new_group_json = {}
                new_group_json['group_name'] = group_name
                new_group_json['group_id'] = get_random_str(GroupIDLength)
                new_group_json['types'] = []
                new_type_json = {}
                new_type_json['type_name'] = type_name
                new_type_json['type_id'] = get_random_str(TypeIDLength)
                new_type_json['spu'] = []
                new_group_json['types'].append(new_type_json)
                new_log['group'].append(new_group_json)
                with open(self.log,'w',encoding='utf-8') as log_file:
                    json.dump(new_log, log_file, indent=4, ensure_ascii=False)
                    log_file.close()
            logging.info(f'The {type_name} of {group_name} is created!')
            return SUCCESS
        except:
            logging.info(f'Creating {type_name} of {group_name} is failed!')
            return ERROR
    
    def delete_type(self,group_name,type_name):
        try:
            group_path = os.path.join(self.global_data.data_root,self.database,group_name)
            type_path = os.path.join(group_path, type_name)
            if os.path.exists(type_path) is False:
                logging.info(f'{type_name} in {group_name} not exists!')
                return FAIL
            else:
                shutil.rmtree(type_path)
                with open(self.log,'r',encoding='utf-8') as log_file:
                    json_log = json.load(log_file)
                    log_file.close()
                for group in json_log['group']:
                    if group['group_name'] == group_name:
                        for type in group['types']:
                            if type['type_name'] == type_name:
                                group['types'].remove(type)
                                log_json = open(self.log,'w',encoding='utf-8')
                                json.dump(json_log,log_json,ensure_ascii=False,indent=4)
                                log_json.close()
                                logging.info(f'{type_name} in {group_name} is deleted!')
                                return SUCCESS
                return FAIL
        except:
            return ERROR
    
    def delete_group(self,group_name):
        try:
            group_path = os.path.join(self.global_data.data_root,self.database,group_name)
            if os.path.exists(group_path) is False:
                logging.info(f'{group_name} not exists!')
                return FAIL
            else:
                shutil.rmtree(group_path)
                with open(self.log,'r',encoding='utf-8') as log_file:
                    json_log = json.load(log_file)
                    log_file.close()
                for group in json_log['group']:
                    if group['group_name'] == group_name:
                        json_log['group'].remove(group)
                        log_json = open(self.log,'w',encoding='utf-8')
                        json.dump(json_log,log_json,ensure_ascii=False,indent=4)
                        log_json.close()
                        logging.info(f'{group_name} is deleted!')
                        return SUCCESS
                return FAIL
        except:
            return ERROR

    def get_groupID(self,group_name):
        try:
            with open(self.log,'r',encoding='utf-8') as log_file:
                log_json = json.load(log_file)
                log_file.close()
            for group in log_json['group']:
                if group['group_name'] == group_name:
                    return group['group_id']
            return FAIL
        except:
            logging.error(f'Something error when getting ID of group named {group_name}!')
            return ERROR
        
        
    def get_typeID(self,group_name,type_name):
        try:
            with open(self.log,'r',encoding='utf-8') as log_file:
                log_json = json.load(log_file)
                log_file.close()
            for group in log_json['group']:
                if group['group_name'] == group_name:
                    for type in group['types']:
                        if type['type_name'] == type_name:
                            return type['type_id']
            return FAIL
        except:
            logging.error(f'Something error when getting ID of type named {type_name} in {group_name}!')
            return ERROR

    def create_spu(self,group_name,type_name):
        spu_id = get_random_str(SpuIDLength)
        group_path = os.path.join(self.global_data.data_root,self.database,group_name)
        type_path = os.path.join(group_path, type_name)
        if os.path.exists(type_path) is False:
            self.create_type(group_name,type_name)
            logging.info(f'{type_path} not exists, but is created just now!')
        spu_path = os.path.join(type_path,spu_id)
        os.mkdir(spu_path)
        spu_info = {}
        spu_info['id'] = spu_id
        spu_info['created_time'] = str(datetime.datetime.now())
        spu_info['in_group'] = self.get_groupID(group_name)
        spu_info['in_type'] = self.get_typeID(group_name,type_name)
        spu_info['sku'] = []
        spu_info_path = os.path.join(spu_path,'spu_info.json')
        spu_json = open(spu_info_path,'w',encoding='utf-8')
        json.dump(spu_info,spu_json,indent=4,ensure_ascii=False)
        spu_json.close()
        cover_path = os.path.join(spu_path,'cover')
        os.mkdir(cover_path)
        sku_path = os.path.join(spu_path,'sku')
        os.mkdir(sku_path)
        with open(self.log,'r',encoding='utf-8') as log_file:
            json_log = json.load(log_file)
            log_file.close()
        for group in json_log['group']:
            if group['group_name'] == group_name:
                for type in group['types']:
                    if type['type_name'] == type_name:
                        type['spu'].append(spu_id)
                        log_json = open(self.log,'w',encoding='utf-8')
                        json.dump(json_log,log_json,ensure_ascii=False,indent=4)
                        log_json.close()
                        logging.info(f'spu {spu_id} of {type_name} in {group_name} is init!')
                        return spu_id
        return spu_id
    
    def delete_spu(self,group_name,type_name,spu_id):
        try:
            group_path = os.path.join(self.global_data.data_root,self.database,group_name)
            type_path = os.path.join(group_path, type_name)
            spu_path = os.path.join(type_path,spu_id)
            if os.path.exists(spu_path) is False:
                logging.info(f'spu {spu_id} of {type_name} in {group_name} not exists!')
                return FAIL
            else:
                shutil.rmtree(spu_path)
                with open(self.log,'r',encoding='utf-8') as log_file:
                    json_log = json.load(log_file)
                    log_file.close()
                for group in json_log['group']:
                    if group['group_name'] == group_name:
                        for type in group['types']:
                            if type['type_name'] == type_name:
                                for i in range(len(type['spu'])):
                                    if type['spu'][i] == spu_id:
                                        type['spu'].pop(i)
                                        log_json = open(self.log,'w',encoding='utf-8')
                                        json.dump(json_log,log_json,ensure_ascii=False,indent=4)
                                        log_json.close()
                                        logging.info(f'spu {spu_id} of {type_name} in {group_name} now is deleted!')
                                        return SUCCESS
                return FAIL
        except:
            logging.error(f'Something error when deleting spu {spu_id} of {type_name} in {group_name}!')
            return ERROR

    def create_sku(self,group_name,type_name,spu_id,sku_id):
        group_path = os.path.join(self.global_data.data_root,self.database,group_name)
        type_path = os.path.join(group_path, type_name)
        spu_path = os.path.join(type_path,spu_id)
        if os.path.exists(spu_path) is False:
            spu_id = self.create_spu(group_name,type_name)
            logging.info(f'spu {spu_id} not exists, but is created just now!')
        sku_path = os.path.join(spu_path,'sku',sku_id)
        os.mkdir(sku_path)
        spu_info_path = os.path.join(spu_path,'spu_info.json')
        with open(spu_info_path,'r',encoding='utf-8') as info:
            json_info = json.load(info)
            info.close
        json_info['sku'].append(sku_id)
        json.dump(json_info,open(spu_info_path,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
        image_path = os.path.join(sku_path,'image')
        os.mkdir(image_path)
        sku_info = {}
        sku_info['id'] = sku_id
        sku_info['created_time'] = str(datetime.datetime.now())
        sku_info['in_spu'] = spu_id
        sku_info_path = os.path.join(sku_path,'sku_info.json')
        json.dump(sku_info,open(sku_info_path,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
        logging.info(f'sku {sku_id} is init!')
        return SUCCESS

    
    def delete_sku(self,group_name,type_name,spu_id,sku_id):
        try:
            group_path = os.path.join(self.global_data.data_root,self.database,group_name)
            type_path = os.path.join(group_path, type_name)
            spu_path = os.path.join(type_path,spu_id)
            sku_path = os.path.join(spu_path,'sku',sku_id)
            if os.path.exists(sku_path) is False:
                logging.info(f'sku {sku_id} not exists!')
                return FAIL
            else:
                shutil.rmtree(sku_path)
                spu_info_path = os.path.join(spu_path,'spu_info.json')
                with open(spu_info_path,'r',encoding='utf-8') as info:
                    json_info = json.load(info)
                    info.close
                for i in range(len(json_info['sku'])):
                    if json_info['sku'][i] == sku_id:
                        json_info['sku'].pop(i)
                        json.dump(json_info,open(spu_info_path,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
                        logging.info(f'sku {sku_id} now is deleted!')
                        return SUCCESS
                return FAIL
        except:
            logging.error(f'Something error when deleting sku {sku_id}!')
            return ERROR


    def get_groups(self):
        size = os.path.getsize(self.log)
        if size == 0:
            return {}
        group_list = []
        with open(self.log,'r',encoding='utf-8') as log:
            json_log = json.load(log)
            log.close()
            group = json_log['group']
            for i in group:
                group_list.append(i['group_name'])
        return group_list
    
    def show_groups(self):
        logging.info(f'The groups in {self.database} is as follows:')
        print(self.get_groups())
        return self.get_groups()
        
    def get_types(self,group_name):
        size = os.path.getsize(self.log)
        if size == 0:
            return []
        type_list = []
        with open(self.log,'r',encoding='utf-8') as log:
            json_log = json.load(log)
            log.close()
            group = json_log['group']
            for i in group:
                if i['group_name'] != group_name:
                    continue
                types = i['types']
                for j in types:
                    type_list.append(j['type_name'])
        return list2dict(type_list)
    
    def show_types(self,group_name):
        logging.info(f'The types in group {group_name} of {self.database} is as follows:')
        print(self.get_types(group_name))
        return self.get_types(group_name)

    def get_all_types(self):
        groups = self.get_groups()
        type_list = []
        for group in groups:
            type_list.extend(self.get_types(group))
        return list2dict(type_list)
    
    def show_all_types(self):
        logging.info(f'All types in {self.database} is as follows:')
        print(self.get_all_types())
        return self.get_all_types()
    
    def get_spu_id(self,group_name,type_name):
        spu_list = []
        with open(self.log,'r',encoding='utf-8') as log:
            json_log = json.load(log)
            log.close()
            group = json_log['group']
            for i in group:
                if i['group_name'] == group_name:
                    for type in i['types']:
                        if type['type_name'] == type_name:
                            for j in type['spu']:
                                spu_list.append(j)
        return list2dict(spu_list)

    def show_spu_id(self,group_name,type_name):
        logging.info(f'The spu in type {type_name} of group {group_name} of {self.database} is as follows:')
        print(self.get_spu_id(group_name,type_name))
        return self.get_spu_id(group_name,type_name)

    def get_sku_id(self,group_name,type_name,spu_id):
        sku_list = []
        group_path = os.path.join(self.global_data.data_root,self.database,group_name)
        type_path = os.path.join(group_path, type_name)
        spu_path = os.path.join(type_path,spu_id)
        spu_info_path = os.path.join(spu_path,'spu_info.json')
        with open(spu_info_path,'r',encoding='utf-8') as info:
            json_info = json.load(info)
            info.close
        for i in range(len(json_info['sku'])):
            sku_list.append(json_info['sku'][i])
        return list2dict(sku_list)
    
    def show_sku_id(self,group_name,type_name,spu_id):
        logging.info(f'sku in spu {spu_id} of {type_name} is as follows:')
        print(self.get_sku_id(group_name,type_name,spu_id))
        return self.get_sku_id(group_name,type_name,spu_id)

    def manager(self):
        logging.info(f'current database is {self.database}')
        while True:
            command = input("输入0设置数据库；1创建操作；2删除操作；3退出:")
            if command == '3':
                return
            elif command == '0':
                database_name = input("输入数据库名称:")
                self.set_database(database_name)
            elif command == '1':
                create_command = input('输入0创建数据库；输入1创建类；输入2创建spu；输入3创建sku：')
                if create_command == '0':
                    database_name = input("输入数据库名称:")
                    self.create_database(database_name)
                else:
                    self.show_groups()
                    group_name = input("输入group_name：")
                    if create_command == '1':
                        type_name = input("输入type_name：")
                        self.create_type(group_name,type_name)
                    else:
                        type_dict = self.show_types(group_name)
                        type_id = input("输入type_id：")
                        if create_command == '2':
                            self.create_spu(group_name,type_dict[int(type_id)])
                        else:
                            spu_dict = self.show_spu_id(group_name,type_dict[int(type_id)])
                            spu_id = input("输入spu_id：")
                            sku_id = input("输入sku_id：")
                            self.create_sku(group_name,type_dict[int(type_id)],spu_dict[int(spu_id)],sku_id)
            elif command == '2':
                delete_command = input('输入0删除数据库；输入1删除group；输入2删除类；输入3删除spu；输入4删除sku：')
                if delete_command == '0':
                    database_name = input("输入数据库名称:")
                    self.delete_database(database_name)
                else:
                    self.show_groups()
                    group_name = input("输入group_name：")
                    if delete_command == '1':
                        self.delete_group(group_name)
                    else:
                        type_dict = self.show_types(group_name)
                        type_id = input("输入type_id：")
                        if delete_command == '2':
                            self.delete_type(group_name,type_dict[int(type_id)])
                        else:
                            spu_dict = self.show_spu_id(group_name,type_dict[int(type_id)])
                            spu_id = input("输入spu_id：")
                            if delete_command == '3':
                                self.delete_spu(group_name,type_dict[int(type_id)],spu_dict[int(spu_id)])
                            else:
                                sku_dict = self.show_sku_id(group_name,type_dict[int(type_id)],spu_dict[int(spu_id)])
                                sku_id = input("输入sku_id：")
                                self.delete_sku(group_name,type_dict[int(type_id)],spu_dict[int(spu_id)],sku_dict[int(sku_id)])

            else:
                logging.info('ERROR COMMAND!')


