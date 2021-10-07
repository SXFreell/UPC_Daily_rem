# UPC_Daily_rem

基于mirai与miraicle的每日疫情防控通提醒qq机器人

## 准备依赖

### 1. 安装openjdk

官网：<https://jdk.java.net/>

### 2. 安装python

官网：<https://www.python.org/>

### 3. 安装miraicle

```bash
# 安装miraicle
pip install miraicle
```

## 配置机器人

### 1. 准备内容

- 机器人QQ一个
- 疫情防控通总名单及对应每人对应QQ一份(json文件)

### 2. 配置 `mcl`

在 `mcl` 目录中打开终端

```bash
# 运行mcl
mcl
```

```mcl
# 添加自动登录机器人QQ
/autoLogin add 123456 pwd
```

输入 `stop` 停止运行

如果出现滑动验证码或设备锁请参考<https://txhelper.glitch.me/>

### 3. 配置 `miraicle`

找到 `miraicle/bot.py` 文件，并修改

```python
import miraicle, json, shelve
from plugins import *

with open("./static/info/info.json") as f:
    info = json.load(f)
with shelve.open("./static/info/info") as f:
    f["info"] = info

# 将'000000'换成你登录的机器人 QQ 号
qq = 000000              

verify_key = '202120212021'
port = 8080

bot = miraicle.Mirai(qq=qq, verify_key=verify_key, port=port)
bot.run()
```

找到 `miraicle/static/info/info.json` 文件，并修改

```js
{
    /* 管理员QQ列表 */
    "admin": [
        123456
    ],
    
    /* 有权限用户字典 */
    "usr": {
        /* 键为QQ号，值为有权限的群列表 */
        "123456": [
            12345678
        ]
    },

    /* 群字典 */
    "group": {
        /* 群号 */
        "12345678": {
            /* 有权限的用户QQ列表 */
            "qq": [
                123456
            ],
            /* 教师数字石大账号与密码 */
            "account": [
                "user",
                "pwd"
            ],
            /* 每日10点自动提醒是否开启 */
            "auto": true
        }
    }
}
```

将疫情防控通总名单及对应每人对应QQ的 `json` 文件放入 `miraicle/static/info` 目录

文件命名为工号，例如 `20200000.json`

文件内容示例如下(缺少信息会导致@不成功)：

```js
/* 名字必须与疫情防控通上名字一致，否则@不成功 */
{
    /* "姓名": QQ, */
    "张三": 12345678,
    "李四": 12345679,
    "王五": 12345680,
    "孙六": 12345681,
    "马七": 12345682,
    "郭八": 12345683,
    "钱九": 12345684,
    "余十": 12345685,
    "董十一": 12345686,
    "刘十二": 12345687,
    "赵十三": 12345688
}
```

在 `miraicle` 目录打开终端

```bash
python bot.py
```

### 4. 使用方法

需要同时打开 `mcl` 与 `miraicle` 才能提供服务。

有权限QQ可私聊机器人发送 `日汇报` 获取当前日汇报信息。

有权限QQ可通过在群中 `@机器人` 来获取当前日汇报信息，如果 `未填报人数<=50` 会@未完成填报的成员。

在 `info.json` 文件中将 `group` 字典中某群的 `auto` 的值设置为 `true` 会开启该群每日10点自动提醒。

管理员QQ可私聊机器人 `admin` 来获取管理员菜单。

更新 `info.json` 文件后可以通过重启 `miraicle` 或使用管理员QQ私聊机器人 `更新配置` 来更新配置信息。

## 协议

`UPC_Daily_rem` 采用 `AGPLv3` 协议开源。

Copyright © 2021, Freell

## 联系方式

<a target="_blank" href="http://wpa.qq.com/msgrd?v=3&uin=1142484090&site=qq&menu=yes">QQ</a>
