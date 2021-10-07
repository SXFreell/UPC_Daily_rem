import requests
import datetime
import json

def login(username, password):
    data = {
        "username": username,
        "password": password
    }
    session = requests.Session()
    login_url = "https://app.upc.edu.cn/uc/wap/login/check"
    session.post(url=login_url, data=data)
    return session

def get_num(session):
    r = session.get("https://app.upc.edu.cn/ncov/wap/upc/groups?type=1")
    group_id = r.json()["d"]["data"][0]["id"]
    data = {
        "type": "weishangbao",
        "group_type": "1",
        "date": str(datetime.date.today()),
        "group_id": group_id
    }
    num_url = "https://app.upc.edu.cn/ncov/wap/upc/diff"
    response = session.post(url=num_url, data=data)
    return response.json()["d"]["today"]

def get_list(session):
    r = session.get("https://app.upc.edu.cn/ncov/wap/upc/groups?type=1")
    group_id = r.json()["d"]["data"][0]["id"]
    type0 = "weishangbao"
    list_url = "https://app.upc.edu.cn/ncov/wap/upc/ulists?date=" + str(datetime.date.today()) + "&type=" + type0 + "&page=1&page_size=390&"+group_id+"=10&keywords=&group_type=1"
    response = session.get(url=list_url)
    lis = response.json()["d"]["lists"]
    l = [i["realname"] for i in lis]
    return l

def get_qqlist(session,account):
    with open("./static/"+str(account)+".json","r",encoding="utf-8") as f:
        name = json.load(f)
    l = get_list(session)
    qq_list = [name[i] for i in l]
    return qq_list

