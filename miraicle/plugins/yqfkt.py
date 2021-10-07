import miraicle
import shelve
import json
from plugins.fun.yqfkt_fun import *

# 加载信息
def get_info():
    with shelve.open("./static/info/info") as f:
        admin = f["info"]["admin"]
        usr = f["info"]["usr"]
        group = f["info"]["group"]
    return admin,usr,group

# 群提醒
@miraicle.Mirai.receiver('GroupMessage')
def group_yqfkt(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    admin, usr, group = get_info()
    if str(msg.group) in group.keys() and msg.sender in group[str(msg.group)]["qq"]:
        if msg.at_me() == True:
            account, password = group[str(msg.group)]["account"]
            session = login(account, password)
            num = get_num(session)
            if num>50:
                bot.send_group_msg(group=msg.group, msg=[miraicle.AtAll()])
                bot.send_group_msg(group=msg.group, msg='今日未填报人数：'+str(num))
            elif num>0:
                bot.send_group_msg(group=msg.group, msg="今日未填报人数："+str(num))
                qq_list = get_qqlist(session,account)
                bot.send_group_msg(group=msg.group, msg=[miraicle.At(qq=i) for i in qq_list])
            else:
                bot.send_group_msg(group=msg.group, msg=[miraicle.Plain("日汇报全部完成啦"),miraicle.Face().from_face_id(74)])

# 私聊提醒
@miraicle.Mirai.receiver('FriendMessage')
def yqfkt(bot: miraicle.Mirai, msg: miraicle.FriendMessage):
    admin, usr, group = get_info()
    if str(msg.sender) in usr.keys():
        if msg.plain == '日汇报':
            if len(usr[str(msg.sender)])==0:
                bot.send_friend_msg(qq=msg.sender, msg="你没有关联任何群")
            elif len(usr[str(msg.sender)])==1:
                g = usr[str(msg.sender)][0]
                account, password = group[str(g)]["account"]
                session = login(account, password)
                num = get_num(session)
                if num>0:
                    m = "今日未填报人数："+str(num)+"\n"+"\n".join(get_list(session))
                    bot.send_friend_msg(qq=msg.sender, msg=m)
                else:
                    bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain("日汇报全部完成啦"),miraicle.Face().from_face_id(74)])
            else:
                bot.send_friend_msg(qq=msg.sender, msg="你有以下群，请输入“日汇报+群号”，例：日汇报12345678\n"+"\n".join([str(i) for i in usr[str(msg.sender)]]))
        if msg.plain in ['日汇报'+str(i) for i in usr[str(msg.sender)]]:
            g = msg.plain.replace("日汇报","")
            account, password = group[g]["account"]
            session = login(account, password)
            num = get_num(session)
            if num>0:
                m = "今日未填报人数："+str(num)+"\n"+"\n".join(get_list(session))
                bot.send_friend_msg(qq=msg.sender, msg=m)
            else:
                bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain("日汇报全部完成啦"),miraicle.Face().from_face_id(74)])

# 定时提醒
@miraicle.scheduled_job(miraicle.Scheduler.every().day.at('10'))
def morning(bot: miraicle.Mirai):
    admin, usr, group = get_info()
    for gs in group.keys():
        if group[gs]["auto"] == True:
            account, password = group[gs]["account"]
            session = login(account, password)
            num = get_num(session)
            if num>50:
                bot.sent_group_msg(group=int(gs), msg=[miraicle.AtAll()])
                bot.send_group_msg(group=int(gs), msg='今日未填报人数：'+str(num))
            elif num>0:
                bot.send_group_msg(group=int(gs), msg="今日未填报人数："+str(num))
                qq_list = get_qqlist(session,account)
                bot.send_group_msg(group=int(gs), msg=[miraicle.At(qq=i) for i in qq_list])
            else:
                bot.send_group_msg(group=int(gs), msg=[miraicle.Plain("日汇报全部完成啦"),miraicle.Face().from_face_id(74)])

# admin操作
@miraicle.Mirai.receiver('FriendMessage')
def yqfkt(bot: miraicle.Mirai, msg: miraicle.FriendMessage):
    admin, usr, group = get_info()
    if msg.sender in admin:
        # if msg.plain == '测试':
        #     m = [str(group[gs]["auto"]) for gs in group.keys()]
        #     bot.send_friend_msg(qq=msg.sender, msg="\n".join(m))
        if msg.plain == 'admin':
            m = ["1. 查看配置", "2. 更新配置", "请输入选型（不要输入序号）"]
            bot.send_friend_msg(qq=msg.sender, msg="\n".join(m))
        if msg.plain == "查看配置":
            m = ["管理员："+", ".join([str(i) for i in admin]), "\n用户：\n"+"\n".join(["--QQ: "+i+"\n--群列表: "+str(usr[i])+"\n" for i in usr.keys()]), "\n群列表：\n"+"\n".join(["--群号: "+i+"\n--权限QQ: "+str(group[i]["qq"])+"\n--账号信息: "+str(group[i]["account"]) for i in group.keys()])]
            bot.send_friend_msg(qq=msg.sender, msg="\n".join(m))
        if msg.plain == "更新配置":
            with open("./static/info/info.json") as f:
                info = json.load(f)
            with shelve.open("./static/info/info") as f:
                f["info"] = info
            m = ["配置已更新", "请找到/miraicle/static/info/info.json文件进行配置修改", "--  admin为管理员列表，类型int", "--  usr为用户字典，字典键为用户QQ，字典值列表存放该QQ有权限的群号，类型int", "--  group为群字典，字典键为群号，字典值为群信息字典（群信息字典“qq”键的值列表存放该群有权限的QQ，“account”键的值列表存放教师数字石大账号与密码，类型str，“auto”键的值为是否开启每日10点提醒，类型bool）"]
            bot.send_friend_msg(qq=msg.sender, msg="\n\n".join(m))