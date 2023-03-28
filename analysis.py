import requests


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
    return cookies


def print_html(response: requests.session, save: dict = None):
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
    }
