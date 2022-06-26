import json

import requests

CURRENT_USER_ID = "623eac5e000000001000d844"
HEADERS = {
    'Host': 'www.xiaohongshu.com',
    'Connection': 'Keep-Alive',
    'xy-platform-info': 'platform=iOS&version=7.43&build=7430183&deviceId=70804187-8F8A-4AEE-9C6A-AAB7705AEFF5&bundle=com.xingin.discover',
    'X-raw-ptr': '0',
    'xy-direction': '75',
    'x-legacy-did': '70804187-8F8A-4AEE-9C6A-AAB7705AEFF5',
    'x-mini-mua': 'eyJhIjoiRUNGQUFGMDIiLCJrIjoiZmI3NjM5ZTAwNmE1YzY4NDcwYjkzZjRkYjFkYjJhNzUzNzJiM2NiOWNmZjJlZmNlYWQxOTgwMTdiY2ExZDIwYSIsInAiOiJpIiwicyI6Ijc5OGQzZWYyN2M3Yzk0ZjQwZjVlMWVjYjUzNzM0NzI2IiwidSI6IjAwMDAwMDAwOTYyYmM4NTBlMWNiNDU2NGNiYWM1YzM3ODE0ZWViNjAiLCJ2IjoiMS4xLjIifQ.pDpf6fywNvzltINuDs_dWCzLjK5kDEBPvqlTOoHxjNi_idMQDqeC8Knwy6ook6hmUyHMsTn-PB-D0e4GYys43K2jKzIqrzt4uqn6sHfZF-wVaoqZGg0PWm2Y6kU9ZOZLaH5gExvmLFG3DP18WxGEmqKo6_t5InqtLW1CeJ5bvoiR9PvpE_m-pqm1etfL9L6m0M3k06PorVxlrX3Lilrn1DmOl83Qfn-Qn6PNzr8HLWPreoWoZEqEjCkIgii-A8WS_0QM1Zk7F8OvLuhkbjrAmaR2U-nbLrgJNjvB9cMoe2zBxNGMU0FMq887sURwR5Q7-zZcl0Wn-L4z7S7zekVFyQwWTBjjhQsRuY3LkH85d458I8cCrqKrwZNnRuu72ArZV7fjJMYsIapnouOl6m1ob-G5HL-e4cGnOQ02KAd4RzpVTOfXpJeCYVGq0SI1I3KrFm7Z_xMPOTyoCfsAMiZ-thclFQ-3qfkzWs8RQtkTGcOLwvdMWxGBCCWZP_KVd96VKqi7rW-I6tJzzLD6tK8S9w.',
    'X-Net-Core': 'crn',
    'X-B3-TraceId': '63cafd665fddf365',
    'x-legacy-fid': '1655522477-0-0-c30b1f138419fb423397a68ea0bc8f68',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-HK;q=0.8, zh-Hant-CN;q=0.7',
    'Mode': 'rawIp',
    # 'Accept-Encoding': 'br;q=1.0, gzip;q=1.0, compress;q=0.5',
    'x-legacy-sid': 'session.1655560320757055767435',
    'User-Agent': 'discover/7.43 (iPhone; iOS 14.7.1; Scale/2.00) Resolution/750*1334 Version/7.43 Build/7430183 Device/(Apple Inc.;iPhone12,8) NetType/WiFi',
    'xy-common-params': 'app_id=ECFAAF02&build=7430183&deviceId=70804187-8F8A-4AEE-9C6A-AAB7705AEFF5&device_fingerprint=202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5&device_fingerprint1=202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5&fid=1655522477-0-0-c30b1f138419fb423397a68ea0bc8f68&identifier_flag=0&lang=zh-Hans&launch_id=677903524&platform=iOS&project_id=ECFAAF&sid=session.1655560320757055767435&t=1656210761&teenager=0&tz=Asia/Shanghai&uis=light&version=7.43',
    'x-legacy-smid': '202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5',
    'x-mini-sig': '4cb42d560f2497a6446dab81a02db6f4ea3880904bb41b52b88c59b6dab593d2',
    'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe4xG1IYD9/c+qCLOlKGmTtFa+lG43EKf+FXTK5FxYywmrdvS53wieguz8Rbqbh+2NE0YQw/YBePY7vxrV4W8OGgRp06w1pKIRQsQYiWrLA1',
    'Accept': '*/*',
}

CHECK_GROUP_URL = 'https://www.xiaohongshu.com/api/im/red/group/personal_page_group_show_info'
GET_GROUP_MEMBERS_URL = 'https://www.xiaohongshu.com/api/im/red/group/userinfo'
GET_MY_GROUP_URL = 'https://www.xiaohongshu.com/api/im/chats/group'


class XHSHelper(object):

    def __init__(self, headers=HEADERS):
        self.headers = headers

    def get_user_groups(self, userid):
        """
        获取用户所有群组
        :param userid: 用户id
        :return:
        """
        data = {
            'user_id': userid,
        }
        try:
            res = requests.post(url=CHECK_GROUP_URL, data=data, headers=self.headers)
        except Exception as e:
            print(e)
            return {}
        return res.json()

    def get_my_groups(self):
        """
        获取我的所有群组
        :return:
        """
        params = params = {
            'complete': '1',
            'limit': '100',
        }
        try:
            resp = requests.get(GET_MY_GROUP_URL, params=params, headers=self.headers)
        except Exception as e:
            print(e)
            return {}
        return resp.json()

    def get_get_group_members(self, group_id):
        """
        获取群组成员(当前用户必须在群组中)
        :param group_id:
        :return:
        """
        params = {
            'group_id': group_id,
            'limit': '500',
            'page': '0',
        }
        try:
            resp = requests.get(GET_GROUP_MEMBERS_URL, params=params, headers=self.headers)
        except Exception as e:
            print(e)
            return {}
        return resp.json()


xhs_helper = XHSHelper(headers=HEADERS)

if __name__ == '__main__':
    user_id = '5cc730f7000000001601b891'
    print(json.dumps(xhs_helper.get_user_groups(user_id)))
    # group_id = '135861640641118838'
    # print(json.dumps(xhs_helper.get_get_group_members(group_id=group_id)))
    print(json.dumps(xhs_helper.get_my_groups()))