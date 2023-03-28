import requests
import analysis
import json
from lxml import etree


def get_index_header(authority: str, scheme: str):
    """
    首页的请求头
    :param authority: 请求的域名
    :param scheme: 请求协议
    :return: 返回首页请求头
    """
    return {
        "authority": authority,
        "method": "GET",
        "path": "/",
        "scheme": scheme,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "referer": url,
        "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54"
    }


def get_login_header(authority: str, href: str):
    """
    登陆页面请求头
    :param authority:
    :param href:
    :return:
    """
    return {
        "authority": authority,
        "method": "GET",
        "path": "/forum/home.php?mod=spacecp&ac=credit",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        # "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "referer": href,
        "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54"
    }


def update_header(dest: dict, header: dict):
    for item in dest:
        header[item] = dest[item]
    return header


def format_url(href: str):
    if href[-1] == "/":
        return href[:-1]
    return url


def get_scheme(href: str):
    if "https" in href:
        return "https"
    return "http"


def get_authority(href: str):
    href = format_url(href)
    return href.split("//")[-1]


def load_config():
    with open("config.json", "r", encoding="utf-8") as config:
        return json.loads(config.read())["cookies"]


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
        # print(key == "PHPSESSID" or key == "existmag")
        if key == "PHPSESSID" or key == "existmag":
            continue
        cookies[key] = value
    return cookies


def save_cookies(sess: requests.session):
    with open("config.json", "w", encoding="utf=8") as config:
        temp_cookies = ""
        session_cookies = sess.cookies.get_dict()
        for i in session_cookies:
            temp_cookies += i + "=" + session_cookies[i] + ";"
        temp_cookies = temp_cookies[:-1]
        config.write(json.dumps({"cookies": temp_cookies}, indent="\t"))


def user_info(html_text: str):
    info = {}
    html = etree.HTML(html_text)
    info["username"] = html.xpath("//*[@id='ct']/div/div[2]/div/div[1]/div[1]/h2/text()")[0].strip("\n").strip()
    info["uid"] = html.xpath("//*[@id='ct']/div/div[2]/div/div[1]/div[1]/h2/span/text()")[0] \
        .strip("(").strip(")").split(":")[-1].strip()
    info["mileage"] = html.xpath("//*[@id='psts']/ul/li[2]/text()")[0]

    active_profile = html.xpath("//ul[@id='pbbs']/li")

    info["In free time"] = active_profile[0].xpath("./text()")[0]
    info["Buy time"] = active_profile[1].xpath("./text()")[0]
    info["The last time"] = active_profile[2].xpath("./text()")[0]
    info["Thank you IP"] = active_profile[3].xpath("./text()")[0]
    info["The last time you checked IP"] = active_profile[4].xpath("./text()")[0]
    info["Last active time"] = active_profile[5].xpath("./text()")[0]

    # print("user_info", info)
    print("账号：", info["username"])
    print("uid：", info["uid"])
    print("里程：", info["mileage"])
    print("在线时间：", info["In free time"])
    print("注册时间：", info["Buy time"])
    print("最后访问时间：", info["The last time"])
    print("注册IP：", info["Thank you IP"])
    print("上次访问IP：", info["The last time you checked IP"])
    print("上次访问时间：", info["Last active time"])


def main(href):
    href = format_url(href)
    # scheme = get_scheme(href)
    authority = get_authority(href)
    # index_headers = get_index_header(authority, scheme)
    # print(href, "href")
    # print(scheme, "scheme")
    # print(authority, "authority")
    # print("index_headers", type(index_headers), index_headers)
    login_url = f"{url}/forum/home.php?mod=spacecp&ac=credit"

    """获取"""
    session = requests.session()
    cookies = requests.cookies.RequestsCookieJar()
    # analysis.print_partition("——" * 50)
    # response = session.get(href, headers=headers)
    # analysis.print_header(response)

    """更新cookie信息文件，更新cookie"""
    load_cookie = load_cookies(load_config())
    # print("load_cookie", type(load_cookie), load_cookie)
    for key in load_cookie:
        cookies.set(key, load_cookie[key], domain=authority)
    # print("cookies", cookies)
    session.cookies.update(cookies)

    """请求签到的url"""
    analysis.print_partition("——" * 50)
    login_header = get_login_header(authority, url)
    response = session.get(login_url, headers=login_header)

    save_cookies(session)  # 保存cookie信息

    analysis.print_partition("——" * 50)
    mileage = f"{url}/forum/home.php?mod=space&uid=373870"
    mileage_header = get_login_header(authority, login_url)
    response = session.get(mileage, headers=mileage_header)

    analysis.print_partition("——" * 50)
    print("签到完成")
    user_info(response.content.decode("utf-8"))


if __name__ == '__main__':
    # url = "https://www.javbus.com"
    url = "https://www.javsee.cfd"
    main(url)
