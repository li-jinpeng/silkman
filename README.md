## 文件结构

```
-skilman_dbms_v2
    -data 
        -[database_name]
            -error.txt
            -log.json
            -[group_name]
                -[type_name]
                    -[spu_id]
                        -spu_info.json
                        -cover
                            -image.jpg
                        -sku
                            -[sku_id]
                                -image
                                    -[image_id]
                                        -image.jpg
                                        -*text_layout.json
                                -sku_info.json
    -dirvers
        -chromedriver.exe
    -out
        -*.json
    -xlsx
        -[work_name]
            -work_name.xlsx
            -work.json
    -control_consol.py
    -crwaler.py
    -manage_type.py
    -readme.md
    -requirements.txt
    -utils.py
    -web_tools.py
    -worker.py
```

## 版本信息

​    V 2.0

## 未来工作

​    

```
V 2.2
        爬取商品评价信息
    V 2.5
        爬取商品视频
    V 2.8
        爬取商品detail_images
    V 3.0
        实现向数据库push数据自动化
    V 4.0
        实现分布式爬取
```

## 使用方法

```
1.
    pip install -r requirements
2.
    修改crawler.py第33行路径为本地chrome路径
    更换./drivers下的chromedriver.exe为本地chrome对应版本的driver
    driver下载连接https://chromedriver.chromium.org/downloads
    查看chrome版本：
        启动chrome，访问url  chrome://version/
3.
    在./xlsx下新建文件夹，文件夹名称任意，将成为爬取数据存储所在的数据库名称
    在新建文件夹下，创建与文件夹同名的xlsx文件，并输入分配的任务
        任务每一行为一个spu，只需要填写前四列，分别为group_name,type_name,pages_num,clips_num
        与version==1.0不同的是，pages_num和clips_num没有限制，例如pages_num=2,clips_num=3将爬取2页零3个spu商品数据
4.
    //爬取数据工作台
        //提示：设置工作时间，单位为min或者h，将会在即将达到工作时自动停止；如果不设置，则默认工作完成时停止
        //注意：执行任务可以选择从头开始（命令行提示删除原有数据库），或者接着上次任务继续
        //注意：工作途中若强行停止任务，无需担心，在下次重新执行该任务时，已完成的type将无需重复工作
    python control_consol.py -s 2 -x [your_xlsx_name]
    eg. python control_consol.py -s 2 -x test

    //增删数据库内容控制台
    python control_consol.py -s 0  
    
    //爬取指定内容控制台
    python control_consol.py -s 1


```

