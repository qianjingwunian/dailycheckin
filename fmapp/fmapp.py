# -*- coding: utf-8 -*-
import json
import os

import requests


class FMAPPCheckIn:
    def __init__(self, fmapp_account_list):
        self.fmapp_account_list = fmapp_account_list

    @staticmethod
    def sign(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/market/member/signin/sign"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = f"在坚持{data.get('nextDay')}天即可获得{data.get('nextNumber')}个发米粒\n" \
                      f"签到{data.get('lastDay')}天可获得{data.get('lastNumber')}个发米粒"
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    @staticmethod
    def user_info(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/info"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("nickName")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    @staticmethod
    def mili_count(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/v1/mili/service/detail"
            response = requests.post(url=url, headers=headers, data=json.dumps({"pageSize": 10, "pageNo": 1})).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("miliNum")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        return msg

    def main(self):
        msg_list = []
        for fmapp_info in self.fmapp_account_list:
            fmapp_token = fmapp_info.get("fmapp_token")
            fmapp_cookie = fmapp_info.get("fmapp_cookie")
            fmapp_device_id = fmapp_info.get("fmapp_device_id")
            headers = {
                'Host': 'fmapp.chinafamilymart.com.cn',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'loginChannel': 'app',
                'Accept-Language': 'zh-Hans-CN;q=1.0, en-CN;q=0.9, ja-CN;q=0.8, zh-Hant-HK;q=0.7, io-Latn-CN;q=0.6',
                'token': fmapp_token,
                'fmVersion': '2.0.0',
                'deviceId': fmapp_device_id,
                'User-Agent': 'Fa',
                "cookie": fmapp_cookie
            }
            sign_msg = self.sign(headers=headers)
            name_msg = self.user_info(headers=headers)
            mili_msg = self.mili_count(headers=headers)
            msg = f"【Fa米家 APP】\n帐号信息: {name_msg}\n签到状态: {sign_msg}\n米粒数量: {mili_msg}"
            msg_list.append(msg)
        return msg_list


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _fmapp_account_list = datas.get("FMAPP_ACCOUNT_LIST", [])
    FMAPPCheckIn(fmapp_account_list=_fmapp_account_list).main()
