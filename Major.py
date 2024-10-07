import asyncio
import json
from pickle import LONG
import threading
import time
from typing import Any
import requests
import random
from datetime import datetime
from marshmallow_dataclass import dataclass

#nullable enable

class MajorQuery:
    def __init__(self, index, name, auth):
        self.index = index
        self.name = name
        self.auth = auth

class MajorApi:
    def __init__(self, mode, query_id, query_index):
        self.client = requests.Session()
        self.client.timeout = 30
        if mode == 1:
            self.client.headers.update({"Authorization": f"Bearer {query_id}"})
        self.client.headers.update({
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3",
            "Connection": "keep-alive",
            "Origin": "https://major.bot",
            "Referer": "https://major.bot/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": Tools.get_user_agents(query_index),
            "accept": "*/*",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f"\"{Tools.get_user_agents(query_index, True)}\""
        })

    def mapi_get(self, request_uri):
        try:
            response = self.client.get(request_uri)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as ex:
            return requests.Response()

    def mapi_post(self, request_uri, content):
        try:
            response = self.client.post(request_uri, data=content)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as ex:
            return requests.Response()

class MajorBot:
    def __init__(self, query):
        self.pub_query = query
        get_token = self.majpr_get_token()
        if get_token:
            self.access_token = get_token.access_token
            self.user_id = get_token.user.id
            self.has_error = False
            self.error_message = ""
        else:
            self.has_error = True
            self.error_message = "get token failed"

    def majpr_get_token(self):
        mapi = MajorApi(0, self.pub_query.auth, self.pub_query.index)
        request = {"init_data": self.pub_query.auth}
        serialized_request = json.dumps(request)
        response = mapi.mapi_post("https://major.bot/api/auth/tg/", serialized_request)
        if(response.text != ""):
            response_json = response.json()
            return MajorAccessTokenResponse.Schema().load(response_json)
        return None

    def majpr_user_detail(self):
        mapi = MajorApi(1, self.access_token, self.pub_query.index)
        response = mapi.mapi_get(f"https://major.bot/api/users/{self.user_id}/")
        if(response.text != ""):
            response_json = response.json()
            return MajorUserDetailResponse.Schema().load(response_json)
        return None

    def major_get_tasks(self, daily):
        mapi = MajorApi(1, self.access_token, self.pub_query.index)
        response = mapi.mapi_get(f"https://major.bot/api/tasks/?is_daily={str(daily).lower()}")
        if(response.text != ""):
            response_json = response.json()
            return [MajorGetTaskResponse.Schema().load(task) for task in response_json]
        return None

    def major_done_task(self, task_id):
        mapi = MajorApi(1, self.access_token, self.pub_query.index)
        request = {"task_id": task_id}
        serialized_request = json.dumps(request)
        response = mapi.mapi_post("https://major.bot/api/tasks/", serialized_request)
        if(response.text != ""):
            response_json = response.json()
            return MajorDoneTaskResponse.Schema().load(response_json)
        return None

    def pre_major_durov(self):
        client = requests.Session()
        client.timeout = 30
        response = client.get("https://raw.githubusercontent.com/glad-tidings/MajorBot/refs/heads/main/roulette.json")
        if(response.text != ""):
            response_json = response.json()
            return self.major_durov(MajorDurovRequest.Schema().load(response_json))
        return False

    def major_durov(self, request):
        mapi = MajorApi(1, self.access_token, self.pub_query.index)
        response = mapi.mapi_get("https://major.bot/api/durov/")
        if(response.text != ""):
            response_json = response.json()
            if response_json.get("success"):
                time.sleep(15)
                request = {"choice_1": request.choice_1,"choice_2": request.choice_2,"choice_3": request.choice_3,"choice_4": request.choice_4}
                serialized_request = json.dumps(request)
                response = mapi.mapi_post("https://major.bot/api/durov/", serialized_request)
                if(response.text != ""):
                    response_json = response.json()
                    return len(response_json.get("correct", [])) == 4
        return False

    def major_hold_coin(self):
        mapi = MajorApi(1, self.access_token, self.pub_query.index)
        response = mapi.mapi_get("https://major.bot/api/bonuses/coins/")
        if(response.text != ""):
            response_json = response.json()
            if response_json.get("success"):
                time.sleep(15)
                request = {"coins": 915}
                serialized_request = json.dumps(request)
                response = mapi.mapi_post("https://major.bot/api/bonuses/coins/", serialized_request)
                if(response.text != ""):
                    response_json = response.json()
                    return response_json.get("success")
        return False

    def major_roulette(self):
        mapi = MajorApi(1, self.access_token, self.pub_query.index)
        response = mapi.mapi_get("https://major.bot/api/roulette/")
        if(response.text != ""):
            response_json = response.json()
            if response_json.get("success"):
                time.sleep(15)
                response = mapi.mapi_post("https://major.bot/api/roulette/", None)
                if(response.text != ""):
                    response_json = response.json()
                    return response_json.get("rating_award", 0) > 0
        return False

    def major_swipe_coin(self, coins):
        mapi = MajorApi(1, self.access_token, self.pub_query.index)
        response = mapi.mapi_get("https://major.bot/api/swipe_coin/")
        if(response.text != ""):
            response_json = response.json()
            if response_json.get("success"):
                time.sleep(15)
                request = {"coins": coins}
                serialized_request = json.dumps(request)
                response = mapi.mapi_post("https://major.bot/api/swipe_coin/", serialized_request)
                if(response.text != ""):
                    response_json = response.json()
                    return response_json.get("success")
        return False

class Tools:
    @staticmethod
    def get_user_agents(index, plat=False):
        user_agents = ["Mozilla/5.0 (Linux; Android 7.0; SM-G925F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3096.19 Safari/537.36", "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-A202F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36", "Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.86 Mobile DuckDuckGo/5 Safari/537.36", "Mozilla/5.0 (Linux; Android 11; GM1901) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36", "Mozilla/5.0 (Linux; Android 10; SOV40) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36", "Mozilla/5.0 (Linux; Android 8.0.0; SM-A520F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.46 Mobile Safari/537.36", "Dalvik/2.1.0 (Linux; U; Android 10; Redmi 7 Build/QQ3A.200605.002.A1)", "Mozilla/5.0 (Linux; Android 10; SM-J610G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36", "MMozilla/5.0 (Linux; Android 8.1.0; B450) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36", "Opera/9.80 (Android; Opera Mini/10.0.1884/191.227; U; en) Presto/2.12.423 Version/12.16", "Mozilla/5.0 (Linux; arm_64; Android 8.1.0; DUA-L22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.4.76.00 SA/1 Mobile Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.66", "Mozilla/5.0 (Linux; Android 7.1.2; GT-P7300 Build/N2G48C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.81 Safari/537.36", "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 EdgiOS/45.11.1 Mobile/15E148 Safari/605.1.15", "Mozilla/5.0 (iPhone; CPU OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/32.0 Mobile/15E148 Safari/605.1.15"]
        platform = ["Android", "iPhone", "Windows", "Android", "Android", "Android", "Android", "Android", "Android", "Android", "Android", "Android", "Android", "Windows", "Android", "iPad", "iPhone"]
        return platform[index] if plat else user_agents[index]

@dataclass
class MajorAccessTokenRequest:
        init_data:Any

@dataclass
class MajorAccessTokenUser:
        id:Any
        username:Any
        first_name:Any
        last_name:Any
        is_premium:Any
        rating:Any
        squad_id:Any
        is_telegram_hidden:Any
        status_id:Any
        notifications_enabled:Any

@dataclass
class MajorAccessTokenResponse:
        access_token:Any
        token_type:Any
        user:MajorAccessTokenUser

@dataclass
class MajorUserDetailResponse:
        id:Any
        username:Any
        first_name:Any
        last_name:Any
        rating:Any
        squad_id:Any
        notifications_enabled:Any
        is_premium:Any
        is_telegram_hidden:Any
        status_id:Any

@dataclass
class MajorGetTaskResponse:
        id:Any
        title:Any
        type:Any
        award:Any
        is_completed:Any
        payload:Any
        description:Any
        icon_url:Any

@dataclass
class MajorDoneTaskRequest:
        task_id:Any

@dataclass
class MajorDoneTaskResponse:
        task_id:Any
        is_completed:Any

@dataclass
class MajorDurovRequest:
        choice_1:Any
        choice_2:Any
        choice_3:Any
        choice_4:Any

@dataclass
class MajorDurovResponse:
    correct:Any

@dataclass
class MajorRouletteResponse:
    rating_award:Any

@dataclass
class MajorCoinRequest:
    coins:Any

@dataclass
class MajorCoinResponse:
    success:Any

if __name__ == "__main__":
    major_queries = []
    major_queries.append(MajorQuery(0, "Account 1", "query_id"))

    print("----------------------- Major Bot Starting -----------------------")
    print()

    def major_thread(query):
        while True:
            bot = MajorBot(query)
            if not bot.has_error:
                print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] login successfully.")
                sync = bot.majpr_user_detail()
                if sync is not None:
                    print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] synced successfully. B<{sync.rating}>")
                    task_list = bot.major_get_tasks(True)
                    if task_list is not None:
                        for task in [x for x in task_list if not x.is_completed and (x.id == 5 or x.id == 16)]:
                            claim_task = bot.major_done_task(task.id)
                            if claim_task is not None:
                                if claim_task.is_completed:
                                    print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] task '{task.title}' completed")
                                else:
                                    print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] task '{task.title}' failed")

                                each_task_rnd = random.randint(7, 20)
                                time.sleep(each_task_rnd)

                    durev = bot.pre_major_durov()
                    if durev:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] puzzle durov completed")
                    else:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] puzzle durov failed")
                    time.sleep(25)

                    hold_coin = bot.major_hold_coin()
                    if hold_coin:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] hold coin completed")
                    else:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] hold coin failed")
                    time.sleep(25)

                    roulette = bot.major_roulette()
                    if roulette:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] roulette completed")
                    else:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] roulette failed")
                    time.sleep(25)

                    swipe_coin = bot.major_swipe_coin(random.randint(1500, 2500))
                    if swipe_coin:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] swipe coin completed")
                    else:
                        print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] swipe coin failed")
                    time.sleep(25)
                else:
                    print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] synced failed")
            else:
                print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] {bot.error_message}")

            sync_rnd = random.randint(25000, 30000)
            print(f"[{time:YYYY-MM-DD HH:mm:ss}] [Major] [{query.name}] sync sleep '{int(sync_rnd / 3600)}h {int(sync_rnd % 3600 / 60)}m {sync_rnd % 60}s'")
            time.sleep(sync_rnd)

    for query in major_queries:
            bot_thread = threading.Thread(target=major_thread, args=(query,))
            bot_thread.start()
            time.sleep(60)

    input()

