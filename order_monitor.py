
import requests
from bs4 import BeautifulSoup
import time

LOGIN_URL = "http://127.0.0.1:5000/login"
API_URL = "http://127.0.0.1:5000/api/users/online"
USERNAME = "zucaixu"
PASSWORD = "zhongdajiang888"
CHECK_INTERVAL = 2  # 秒

def login_and_get_session():
    session = requests.Session()
    # 1. 先GET登录页，拿csrf_token
    resp = session.get(LOGIN_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})
    csrf_value = csrf_token["value"] if csrf_token else ""
    # 2. POST登录
    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "csrf_token": csrf_value,
        "remember": "y"
    }
    resp = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
    # 3. 登录后直接访问API，判断是否有数据
    api_resp = session.get(API_URL)
    try:
        data = api_resp.json()
        if "users" in data:
            print("登录成功！")
            return session
        else:
            print("登录后API无数据，可能未登录成功。")
            return None
    except Exception as e:
        print("登录后API返回异常，未登录成功。", e)
        print("API返回内容：", api_resp.text)
        return None

def get_order_counts(session):
    try:
        resp = session.get(API_URL)
        data = resp.json()
        return {f"{user['identifier']}({user['username']})": user['order_count'] for user in data['users']}
    except Exception as e:
        print("API请求失败:", e)
        return {}

def main():
    session = login_and_get_session()
    if not session:
        return
    last_counts = get_order_counts(session)
    print("初始数据:", last_counts)
    while True:
        time.sleep(CHECK_INTERVAL)
        now_counts = get_order_counts(session)
        print("当前数据:", now_counts)
        last_counts = now_counts

if __name__ == "__main__":
    main()