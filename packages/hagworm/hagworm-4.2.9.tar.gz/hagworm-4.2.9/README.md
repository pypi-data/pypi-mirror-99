# Hagworm

![](https://img.shields.io/pypi/v/hagworm.svg)
![](https://img.shields.io/pypi/format/hagworm.svg)
![](https://img.shields.io/pypi/implementation/hagworm.svg)
![](https://img.shields.io/pypi/pyversions/hagworm.svg)



## 快速开始



### 1. 下载

```bash
git clone git@gitee.com:wsb310/hagworm.git
```



### 2. 安装

```bash
pip install hagworm
```



### 3. 设计定位

* Hagworm是原生框架、原生库的中间层，对它们进行了更高层次的抽象，用来屏蔽直接的调用，达到不改变使用习惯的情况下可以随意更换框架或库。
* Hagworm整合了它支持的各种框架和库，使它们成为一个整体，屏蔽了底层细节，简化了使用方式。
* Hagworm提供了一个打包的环境，建立了工程质量的底线，开发者只需要关注业务逻辑本身，不需要再关注底层的性能和安全等问题。

```mermaid
graph LR
原生框架-->Hagworm
原生库-->Hagworm
Hagworm-->业务代码
```



### 5. 代码树结构

```text
├── extend                                      基础扩展
│    ├── asyncio                                asyncio扩展
│    │    ├── base.py                           异步工具库
│    │    ├── buffer.py                         缓冲相关
│    │    ├── cache.py                          缓存相关
│    │    ├── command.py                        命令行相关
│    │    ├── database.py                       数据库相关
│    │    ├── event.py                          分布式事件总线
│    │    ├── file.py                           文件读写相关
│    │    ├── future.py                         协程相关
│    │    ├── net.py                            网络工具
│    │    ├── ntp.py                            时间同步
│    │    ├── task.py                           任务相关
│    │    ├── transaction.py                    事务相关
│    │    └── zmq.py                            ZMQ扩展
│    ├── base.py                                基础工具
│    ├── cache.py                               缓存相关
│    ├── compile.py                             pyc编译
│    ├── crypto.py                              加解密相关
│    ├── error.py                               错误定义
│    ├── event.py                               事件总线
│    ├── excel.py                               excel封装
│    ├── interface.py                           接口定义
│    ├── logging.py                             日志相关
│    ├── media.py                               媒体相关
│    ├── metaclass.py                           元类相关
│    ├── process.py                             多进程工具
│    ├── qrcode.py                              二维码工具
│    ├── struct.py                              数据结构
│    └── transaction.py                         事务相关
├── frame                                       三方框架扩展
│    └── fastapi                                fastapi扩展
│    │    └── base.py                           基础工具
│    └── tornado                                tornado扩展
│    │    ├── base.py                           基础工具
│    │    ├── socket.py                         socket工具
│    │    └── web.py                            http工具
│    └── gunicorn.py                            gunicorn相关
│    └── stress_tests.py                        压力测试工具
├── static                                      静态资源
│    └── cacert.pem                             SSL根证书
└── third                                       三方库扩展
     └── aliyun                                 阿里云相关
          └── rocketmq.py                       消息总线
```



### 6. 重要提示

* 不要在非异步魔术方法中调用异步函数，例如在__del__中调用异步函数，在该函数结束前，对象一直处于析构中的状态，此时弱引用是有效的，但如果此时另外一个线程或者协程通过弱引用去使用它，然后意外就可能发生了
* 使用contextvars库时，要注意使用asyncio的call_soon、call_soon_threadsafe、call_later和call_at函数时（建议使用hagworm.extend.asyncio.base.Utils提供的函数），其中的context参数，必须给出独立的contextvars.Context对象，使其上下文环境独立，否则会出现伪内存泄漏现象
