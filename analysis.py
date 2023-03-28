import requests
from lxml import etree
import time
import random
import json


# import ssl


def load_cookies(string: str):
    tmp = ""
    for i in string:
        if i == " ":
            continue
        tmp += i
    cookies = {}
    cookie_list = tmp.split(";")
    for i in cookie_list:
        key, value = i.split("=")
        cookies[key] = value
        # print(key, value)
    return cookies


def print_header(response: requests.session()):
    """
    打印请求头和响应头
    :param response: 请求返回对象
    :return:
    """
    print(" 响应头 ".center(50, "—"))
    print("{")
    for i in response.headers:
        print(f"\t\"{i}\": \"{response.headers[i]}\",")
    print("}")

    print(" 请求头 ".center(50, "—"))
    print("{")
    for i in response.request.headers:
        print(f"\t\"{i}\": \"{response.request.headers[i]}\",")
    print("}")


def print_html(response: requests.session, save: dict = None):
    """
    打印网页信息，可选是否保存
    :param response: 请求返回对象
    :param save: {"is save": False, "name": "temp.html"}
    :return:
    """
    if save is None:
        save = {"is save": False, "name": "none"}
    try:
        html = response.content.decode(response.encoding)
        print(html)
        if save["is save"]:
            with open(save["name"], "w", encoding=response.encoding) as f:
                f.write(html)
    except UnicodeDecodeError:
        print("错误了！！！！！！！！！！")


def print_partition(string='——', length=10):
    for i in range(length):
        print(string)


def update_header(response: requests.session):
    """
    更新请求头信息
    :param response:请求返回对象
    :return:
    """
    return {
        "referer": str(response.request.url),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51",
        "accept-language": "zh-CN,zh;q=0.9",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "scheme": "https",
        "method": "GET",
        "authority": "www.javbus.com"
    }
