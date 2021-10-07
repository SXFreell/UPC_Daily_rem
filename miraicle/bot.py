import miraicle, json, shelve
from plugins import *

with open("./static/info/info.json") as f:
    info = json.load(f)
with shelve.open("./static/info/info") as f:
    f["info"] = info

qq = 000000              # 你登录的机器人 QQ 号
verify_key = '202120212021'     # 你在 setting.yml 中设置的 verifyKey
port = 8080                 # 你在 setting.yml 中设置的 port (http)

bot = miraicle.Mirai(qq=qq, verify_key=verify_key, port=port)
bot.run()