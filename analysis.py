import requests
from lxml import etree
import time
import random
import httpx
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
        "authority": "www.javbus.com",
        "cookie": "4fJN_2132_lastvisit=1679815628; 4fJN_2132_lastcheckfeed=373870%7C1679819265; existmag=mag; "
                  "4fJN_2132_visitedfid=2; PHPSESSID=av5ophckfbpnh9du5roj75rct1; 4fJN_2132_sid=b44Yy8; "
                  "4fJN_2132_lip=38.94.108.84%2C1679819265; "
                  "4fJN_2132_ulastactivity=64e6DD8yqmvdfDxJmTb4H2TTPga%2BRPUDeJ7fVP7sGlroV8UpNiNQ; "
                  "4fJN_2132_lastact=1679841706%09uc.php%09; "
                  "4fJN_2132_auth=2090lUvJLaPZHyyI8u51FHhLx%2FxkbpCM4lhc8wU2sikj7POMJG2uX92xBl2"
                  "%2B8wav5YwHbVk3tShbDvfr3pisrRnNSyc; "
                  "bus_auth=d112Ls100BAeU2s6u%2FxgILFioAuU1vmMs4oijCV%2FX04wF9tSKBK6BHKW1wvmnVqq"

    }


def analysis(url, headers):
    # ssl_context = httpx.create_ssl_context()
    # ssl_context.options ^= ssl.OP_NO_TLSv1  # Enable TLS 1.0 back

    with httpx.Client(http2=True) as client:
        """
        获取游客用户的cookie
        """
        print_partition("——" * 50)
        r = client.get(url, headers=headers)
        # print_header(r)

        """获取登陆地址url"""
        if url[-1] == "/":
            url = url[:-1]
        login_link = url + '/forum/member.php?mod=logging&action=login&referer=%2F%2Fwww.javbus.com%2F'
        print("login_link: ", login_link)

        # """用已经登陆过的cookie请求论坛文章，获取经验"""
        # """读取配置文件的cookie信息"""
        # with open("config.json", encoding="utf-8") as config:
        #     loads = json.loads(config.read())
        #     config.close()
        #     cookie = load_cookies(loads["cookies"])
        #     for item in cookie:
        #         # print(item, cookie[item])
        #         r.cookies.set(item, cookie[item])
        print_partition("——" * 50)
        time.sleep(random.randint(2, 5) + random.random())
        r = client.get(login_link, headers=headers)
        print_header(r)
        # print_html(r) # 未知返回的格式

        """
        获取首页内容, 并选择随机选择番号的链接
        """
        print_partition("——" * 50)
        headers = update_header(r)
        time.sleep(random.randint(2, 5) + random.random())
        r = client.get(url, headers=headers)
        print_header(r)
        print_html(r)

        """网页源码"""
        html = etree.HTML(r.content.decode(r.encoding))

        """选择随机番号"""
        item = html.xpath("//div[@class='item']")
        page_random_number = random.randint(0, len(item) - 1)
        page_link = item[page_random_number].xpath("./a/@href")[0]
        print("page_link: ", page_link)

        """
        随机选择番号的信息，然后随机选这论坛文章的链接
        """
        print_partition("——" * 50)
        time.sleep(random.randint(8, 15) + random.random())
        headers = update_header(r)
        r = client.get(page_link, headers=headers)
        print_header(r)
        print_html(r)

        html = etree.HTML(r.content.decode(r.encoding))

        forum = html.xpath("//div[@id='related-waterfall']")[-1]
        forum_element = forum.xpath("./a")
        forum_random_number = random.randint(0, len(forum_element) - 1)
        forum_link = forum_element[forum_random_number].xpath("./@href")[0]
        print("forum_link", forum_link)

        print_partition("——" * 50)
        time.sleep(random.randint(10, 18) + random.random())
        headers = update_header(r)
        r = client.get(forum_link, headers=headers)
        print_header(r)
        print_html(r)

        print_partition("——" * 50)
        time.sleep(random.randint(5, 8) + random.random())
        headers = update_header(r)
        r = client.get("https://www.javbus.com/forum/home.php?mod=spacecp&ac=credit&op=log&suboperation=creditrulelog",
                       headers=headers)
        print_header(r)
        print_html(r)

        print("签到结束")
