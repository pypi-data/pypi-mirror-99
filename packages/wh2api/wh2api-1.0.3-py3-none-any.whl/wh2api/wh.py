# -*- coding: utf-8 -*-


import hashlib
import base64
import json

from .lib import wh_setting

api_version = "1.0.2"



class Login:
    url =""
    id = ""
    pw = ""
    whtoken = {}

    def __init__(self, wh_url, user_id, user_pw="",wh_token="",outside="0"):
        if wh_token =="":
            Login.url = wh_url
            Login.id = user_id
            Login.pw = user_pw

            # 웜홀 API URI 세팅
            whtoken_api = "/api/user/auth"  # 웜홀2 API 상세.
            login_api_url = wh_url + whtoken_api

            # 파라미터 확인
            origin_server = wh_url
            outside = outside

            # 비밀번호 추가 세팅 - 이용자가 입력한 비밀번호를 sha256 해시 후 base64 인코딩 함
            user_pw = user_pw.encode("utf-8")
            user_pw_hashed = hashlib.sha256(user_pw).hexdigest()
            user_pw_hashed = user_pw_hashed.encode("utf-8")
            user_pw_encoded = base64.b64encode(user_pw_hashed).decode("utf-8")

            # 파라미터 세팅
            data = {"userid": user_id, "userpw": user_pw_encoded, "origin_server": origin_server,
                    "outside": outside}

        # API 호출
            login_result = wh_setting.post_requests(api=whtoken_api, data=data,login="login")  # JSon형태로 호출



        #토큰 확인

            whtoken = login_result["token"]
            Login.whtoken = {"whtoken": whtoken}
            # print(whtoken)
            print(user_id,': login success')
            print("wh2api_ver : ",api_version)
        else:
            print(user_id,": wh_token_apply")
            print("wh2api_ver : ", api_version)
            Login.url = wh_url
            Login.id = user_id
            Login.pw = user_pw
            Login.whtoken={"whtoken": wh_token}






