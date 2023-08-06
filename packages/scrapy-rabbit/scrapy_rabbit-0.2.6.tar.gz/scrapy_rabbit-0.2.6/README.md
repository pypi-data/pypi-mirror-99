# Scrapy-Rabbit

<p align="center">
    <img src ="https://img.shields.io/pypi/v/tqsdk?color=blueviolet">
    <img src ="https://img.shields.io/pypi/pyversions/Scrapy.svg" />
</p>

## 1.简介

基于Scrapy爬虫框架与RabbitMQ消息队列结合，一款新的分布式采集框架



##  2.快速入门

> 1. 安装
>
>    `pip install scrapy_rabbit`
>
> 2. 创建项目
>
>    `scrapy_rabbit startproject ProjectName`
>
>    - ProjectName：要创建的项目名称
>
> 3. 创建爬虫
>
>    `scrapy_rabbit genspider SpidersClass SpiderName Url`
>
>    - SpidersClass：爬虫分类
>
>    - SpiderName：爬虫名字
>
>    - Url：初始连接
>
>    是否使用代理以及是否清空队列都可以在Spider中单独配置  
>
> 4. 修改配置
>
>    在conf下config.ini中设置rabbit的链接方式即可。
>
> 5. 指定运行方式
>
>    ![scrapy_rabbit_run.png][1]
>
>    run方法需要传一个列表，列表里第一个元素为当前`爬虫分类名字`，第二元素为`爬虫名字`，第三元素为`运行模式`（auto(自动)：所有请求生产完成后直接开始消费。m(生产模式)：只生产不消费。w(消费模式)：只消费不生产），第四元素为`并发量`。
>
> 6. 运行
>    接下来就可以直接右键运行，或者使用命令行`python spider.py`运行，spider.py为当前爬虫文件。
>
> 7. 整体目录结构
>
>    ![scrapy_rabbit_tree.png][3]





## 3.架构图

![scrapy_rabbit.png][2]

>Spider（爬虫）：负责处理所有Responses，从中分析提取数据，获取Item字段需要的数据，并将需要跟进的URL提交给引擎，再次进入RabbitMQ
>
>Engine（引擎）：框架核心，负责Spider、RabbitMQ、Downloader、ItemPipeline中间的通讯，信号、数据传递等
>
>RabbitMQ（消息队列）：负责接受引擎发送过来的Request请求，并按照指定优先级存入消息队列
>
>Downloader（下载器）：负责下载RabbitMQ中所有Requests请求，并将其获取到的Responses交还给Engine，由引擎交给Spider来处理
>
>ItemPipeline（管道）：负责处理Spider中获取到的Item，并进行进行后期处理（详细分析、过滤、存储等）的地方
>
>Downloader Middlewares（下载中间件）：介于Scrapy引擎和下载器之间的中间件，主要是处理Scrapy引擎与下载器之间的请求及响应
>
>Spider Middlewares（Spider中间件）：介于Scrapy引擎和爬虫之间的中间件，主要工作是处理蜘蛛的响应输入和请求输出



## 4.运行流程

> 1. Spider将所有Requests发送给Engine
>
> 2. 引擎把Url封装成一个请求(Request)传给RabbitMQ，RabbitMQ将所有的请求按照优先级保存下来
> 3. 下载器把资源下载下来，并封装成应答包(Response)交给Spider，如果请求失败则重新放入到RabbitMQ中
> 4. 爬虫解析Response
> 5. 若是解析出实体（Item）,则交给实体管道进行进一步的处理
> 6. 若是解析出的是链接（Url）,则把Url交给引擎，封装成一个请求(Request)传给RabbitMQ等待下载



## 5.监控截图

![rabbit.png][4]



## 6.Todo

- [x] 生产结束后自动消费

- [x] Spiders里可以指定ItemPipeline

- [x] 请求失败重新返回到消息队列

- [ ] 支持Middlewares

- [x] 与Scarpy兼容

- [ ] 可以在Spider里指定RabbitMQ队列

- [ ] Log日志需要整理

- [ ] 脚本采集信息以及日志存入MongoDB

- [ ] 使用平台化来开发爬虫

- [ ] 对当前项目下所有爬虫进行控制

  

[1]: https://elanpy.com/usr/uploads/2021/03/scrapy_rabbit_run.png
[2]: https://elanpy.com/usr/uploads/2021/03/scrapy_rabbit.png
[3]: https://elanpy.com/usr/uploads/2021/03/scrapy_rabbit_tree.png
[4]: https://elanpy.com/usr/uploads/2021/03/rabbitmq.png

