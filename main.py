# GitHub: https://github.com/xyz8848/KLPBBS_auto_sign_in

import http
import logging
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http import cookiejar

import requests
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

switch_user = int(os.environ.get("SWITCH_USER") or 0)
renewal_vip = int(os.environ.get("RENEWAL_VIP") or 0)
renewal_svip = int(os.environ.get("RENEWAL_SVIP") or 0)

klpbbs_ip = os.environ.get("KLPBBS_IP", "43.248.96.249")
debug = int(os.environ.get("DEBUG") or 0)

mail_enable = int(os.environ.get("MAIL_ENABLE") or 0)
mail_host = os.environ.get("MAIL_HOST")
mail_port = int(os.environ.get("MAIL_PORT") or 0)
mail_username = os.environ.get("MAIL_USERNAME")
mail_password = os.environ.get("MAIL_PASSWORD")
mail_to = os.environ.get("MAIL_TO") or []

wechat_enable = int(os.environ.get("WECHAT_ENABLE") or 0)
wechat_webhook = os.environ.get("WECHAT_WEBHOOK")
wechat_mentioned = os.environ.get("WECHAT_MENTIONED") or []

serverchan_enable = int(os.environ.get("SERVERCHAN_ENABLE") or 0)
serverchan_key = os.environ.get("SERVERCHAN_KEY")

ntfy_enable = int(os.environ.get("NTFY_ENABLE") or 0)
ntfy_url = os.environ.get("NTFY_URL") or "https://ntfy.sh"
ntfy_topic = os.environ.get("NTFY_TOPIC")
ntfy_username = os.environ.get("NTFY_USERNAME")
ntfy_password = os.environ.get("NTFY_PASSWORD")
ntfy_token = os.environ.get("NTFY_TOKEN")

# 设置日志级别和格式
if debug == 1:
    logging.basicConfig(
        level=logging.DEBUG, format="[%(levelname)s] [%(asctime)s] %(message)s"
    )
    logging.info("Debug mode enabled.")
else:
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] [%(asctime)s] %(message)s"
    )
    logging.info("Debug mode disabled.")

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81"

header = {
    "origin": "https://klpbbs.com",
    "Referer": "https://klpbbs.com/",
    "User-Agent": userAgent,
}

session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar()

if klpbbs_ip and klpbbs_ip != "":
    # 使用 IP 访问时需要的设置
    base_url = f"https://{klpbbs_ip}"
    header["Host"] = "klpbbs.com"  # 关键：设置 Host 头
    session.verify = False  # 关闭 SSL 验证
    logging.info(f"使用 IP 访问: {klpbbs_ip}")
else:
    base_url = "https://klpbbs.com"
    logging.info("使用域名访问")

def login(username: str, password: str):
    """
    登录苦力怕论坛

    Args:
        username: 苦力怕论坛用户名
        password: 苦力怕论坛密码
    """
    post_url = f"{base_url}/member.php?mod=logging&action=login&loginsubmit=yes"
    post_data = {
        "username": username,
        "password": password,
    }

    response_res = session.post(post_url, data=post_data, headers=header)
    logging.debug(f"statusCode = {response_res.status_code}")
    logging.debug(
        f"https://klpbbs.com/member.php?mod=logging&action=login&loginsubmit=yes = {response_res.text}"
    )

    header["Cookie"] = "; ".join(
        [f"{cookie.name}={cookie.value}" for cookie in session.cookies]
    )
    # logging.debug(f'Header: {header}')

    # soup = BeautifulSoup(response_res.text, 'html.parser')
    # a_tag = soup.find('a', href_='https://klpbbs.com/')
    # if a_tag is not None:
    #     logging.info('登录成功')
    # else:
    #     logging.info('登录失败')
    #     exit(1)


def get_url():
    """
    获取签到链接

    Returns:
        签到链接 (sign_in_url)
    """
    html_source = session.get(f"{base_url}/", headers=header, verify=False)
    logging.debug(html_source.text)
    soup = BeautifulSoup(html_source.text, "html.parser")
    a_tag = soup.find("a", class_="midaben_signpanel JD_sign")
    if a_tag is not None:
        href_value = a_tag["href"]
        sign_in_url = f"{base_url}/{href_value}"

        logging.debug(f"签到链接：{sign_in_url}")

        if sign_in_url == "https://klpbbs.com/member.php?mod=logging&action=login":
            logging.info("签到链接异常（原因：登录失败）")
            exit(1)

        logging.info("已成功获取签到链接")

        return sign_in_url
    else:
        is_sign_in()
        return None


def sign_in(sign_in_url: str):
    """
    签到

    Args:
        sign_in_url: 签到链接
    """
    session.get(sign_in_url, headers=header, verify=False)


def is_sign_in():
    """
    检测是否签到成功
    """
    html_source = session.get(f"{base_url}/", headers=header, verify=False)
    logging.debug(f"https://klpbbs.com/ = {html_source.text}")
    soup = BeautifulSoup(html_source.text, "html.parser")
    a_tag = soup.find("a", class_="midaben_signpanel JD_sign visted")
    if a_tag is not None:
        href_value = a_tag["href"]
        if href_value == "k_misign-sign.html":
            logging.info("已成功签到")
            notice("已成功签到！")
            exit(0)
        else:  # 异常处理
            # 用户组到期处理
            div_tag = soup.find("div", class_="notice")
            if (
                div_tag
                == "您当前的用户组已经到期，请选择继续续费还是要切换到其他用户组"
            ):
                if switch_user == 1:
                    session.get(
                        f"{base_url}/home.php?mod=spacecp&ac=usergroup&do=switch&groupid=10&handlekey=switchgrouphk",
                        headers=header,
                        verify=False,
                    )
                    logging.info("已切换回普通用户组")
                    notice("已切换回普通用户组")
                elif renewal_vip == 1:
                    session.get(
                        f"{base_url}/home.php?mod=spacecp&ac=usergroup&do=buy&groupid=21&inajax=1",
                        headers=header,
                        verify=False,
                    )
                    logging.info("已续费VIP")
                    notice("已续费VIP")
                    os.execl(sys.executable, sys.executable, *sys.argv)
                elif renewal_svip == 1:
                    session.get(
                        f"{base_url}/home.php?mod=spacecp&ac=usergroup&do=buy&groupid=22&inajax=1",
                        headers=header,
                        verify=False,
                    )
                    logging.info("已续费SVIP")
                    notice("已续费SVIP")
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    logging.info(f"签到失败（原因：当前用户组已到期）")
                    notice("签到失败（原因：当前用户组已到期）")
                    exit(1)

            logging.info("签到失败")
            notice("签到失败")
            exit(1)
    else:
        logging.info("签到失败")
        notice("签到失败")
        exit(1)


def notice(msg: str):
    """
    签到后提示

    Args:
        msg: 提示信息
    """
    if mail_enable == 1:
        email_notice(msg)
    if wechat_enable == 1:
        wechat_notice(msg)
    if serverchan_enable == 1:
        serverchan_notice(msg)
    if ntfy_enable == 1:
        ntfy_notice(msg)


def email_notice(msg: str):
    """
    签到后邮件提示

    Args:
        msg: 提示信息
    """
    message = MIMEMultipart()
    message["From"] = mail_username
    message["To"] = mail_to
    message["Subject"] = msg
    body = f"<h1>苦力怕论坛自动签到</h1><br><br>{msg}<br><br>Powered by <a href='https://github.com/xyz8848/KLPBBS_auto_sign_in'>https://github.com/xyz8848/KLPBBS_auto_sign_in</a>"
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(mail_host, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        server.send_message(message)
        logging.info("邮件发送成功")
    except smtplib.SMTPException as error:
        logging.info("邮件发送失败")
        logging.error(error)


def wechat_notice(msg: str):
    """
    签到后企业微信通知

    Args:
        msg: 提示信息
    """
    # 构建消息体
    data = {
        "msgtype": "text",
        "text": {
            "content": f"苦力怕论坛自动签到\n\n{msg}\n\nPowered by https://github.com/xyz8848/KLPBBS_auto_sign_in",
            # 可以在 mentioned_list 中添加 "@all"，提醒所有人查看信息
            "mentioned_list": wechat_mentioned,
        }
    }

    # 发送 POST 请求
    response = requests.post(wechat_webhook, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        logging.info("企业微信通知发送成功")
    else:
        logging.error(f"企业微信通知发送失败，状态码：{response.status_code}")


def serverchan_notice(msg: str):
    """
    签到后Server酱通知

    Args:
        msg: 提示信息
    """
    url = f"https://sctapi.ftqq.com/{serverchan_key}.send"
    data = {"title": "苦力怕论坛自动签到", "desp": msg}
    try:
        response = requests.post(url, data=data)
        logging.debug(response.text)
        logging.info("Server酱消息发送成功")
    except requests.RequestException as error:
        logging.info("Server酱消息发送失败")
        logging.error(error)


def ntfy_notice(msg: str):
    """
    签到后Ntfy通知

    Args:
        msg: 提示信息
    """
    auth = None
    if ntfy_token:
        auth = requests.auth.HTTPBasicAuth("", ntfy_token)
    elif ntfy_username and ntfy_password:
        auth = requests.auth.HTTPBasicAuth(ntfy_username, ntfy_password)
    else:
        logging.error("ntfy 认证信息异常")

    corrected_url = normalize_domain(ntfy_url)
    url = f"{corrected_url}{ntfy_topic}"
    data = msg.encode("utf-8")

    headers = {"Title": "苦力怕论坛自动签到".encode("utf-8")}
    try:
        response = requests.post(url, data=data, headers=headers, auth=auth)
        logging.debug(response.text)
        logging.info("Ntfy消息发送成功")
    except requests.RequestException as error:
        logging.info("Ntfy消息发送失败")
        logging.error(error)


def normalize_domain(domain: str):
    """
    域名规范化

    Args:
        domain: 域名

    Returns:
        normalize_domain: 规范化的域名
    """
    if not domain.startswith(("http://", "https://")):
        domain = "https://" + domain
    parts = domain.split("/", 3)
    normalize_domain = (
        parts[0] + "//" + parts[2] + "/"
        if len(parts) > 2
        else parts[0] + "//" + parts[2]
    )
    return normalize_domain


if __name__ == "__main__":
    logging.debug(f"UserAgent: {userAgent}")

    login(f"gao66", f"R^8M!44KnUG!sMX4")

    url = get_url()

    sign_in(url)

    is_sign_in()
