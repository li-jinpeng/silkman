import argparse
from manage_type import *
from crawler import *
from worker import *

def _version():
    return 2.0

def _parser():
    parser = argparse.ArgumentParser()
    parser.description="please enter parameters s,x,m,v"
    parser.add_argument("-s","--select",help="select 0 to manage databse, 1 to control crawler and 2 to work.",dest="select",type=int,default="0")
    parser.add_argument("-x","--xlsx",help="xlsx file name.",dest="xlsx",type=str,default="init")
    # parser.add_argument("-m","--vedio",help="get vedio.",dest="vedio",action="store_true")
    parser.add_argument("-v",'--version',help="version infomation.",dest="version",action="store_true")
    return parser.parse_args()

def _main():
    args = _parser()
    if args.version == True:
        logging.info(f'version {_version()}')
        return
    if args.select == 0:
        type_manager = TypeManager()
        type_manager.manager()
    elif args.select == 1:
        crawler_manager = crawler()
        crawler_manager.manager()
        crawler_manager.browser.close()
    elif args.select == 2:
        worker = Worker(args.xlsx)
        worker.manager()
    else:
        logging.error(f'error parameters -s {args.select}')
    return 
    
if __name__ == '__main__':
    _main()
    