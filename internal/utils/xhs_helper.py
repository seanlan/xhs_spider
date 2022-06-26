import json

import requests

CURRENT_USER_ID = "623eac5e000000001000d844"
HEADERS = {
    'Host': 'www.xiaohongshu.com',
    'Connection': 'Keep-Alive',
    'xy-platform-info': 'platform=iOS&version=7.43&build=7430183&deviceId=70804187-8F8A-4AEE-9C6A-AAB7705AEFF5&bundle=com.xingin.discover',
    'X-raw-ptr': '0',
    'xy-direction': '27',
    'x-legacy-did': '70804187-8F8A-4AEE-9C6A-AAB7705AEFF5',
    'x-mini-mua': 'eyJhIjoiRUNGQUFGMDIiLCJrIjoiZjI2ZmM2ZWVlMjI2YTA3MDk2YmZmZmZjZjkxZTY0ODVkNTdjMzliZWU1YjU5ZTg3ZGI0MjhiNjYzZDQ1ZWMxZSIsInAiOiJpIiwicyI6IjBkYzJlMmY5MjAxZTUzMGJiNzk3ZDNlMmE5ZDIwY2ZjIiwidSI6IjAwMDAwMDAwOTYyYmM4NTBlMWNiNDU2NGNiYWM1YzM3ODE0ZWViNjAiLCJ2IjoiMS4xLjIifQ.rHJgNLi1bzJcrt0VLED0N48LA3jbSbi3cyDbV5AJw-Rza2BKf3j57A-_sslMUrpmG122TiHDsWC4GWJ28IuNI5RcxMErqVqNzPGkkOtEpRMAfAMRErRR8LCr--Yuxlpx0MHjD76E3GLckVJ3WaME22fknfqSwLWDFJcLoWLoZBzHexeJ8t2gtmWYjNQmsZCTgQUmW9s3At3AOP_p7zLkaHLvOcsrsU1yqtL8m1CwVE5igfr493J_KNyA9dKOfM9m-ybuevHYWKir0pBdCPWegYxlHnWKEDGu-XsZvDKJv0-AVwticZyo8Vg_jC4e_sXx9cr5ovqmLxRzNvgqMTVJKPkmWP3sazPgvEVAx5DrG2F49qD5_keb6_kv-Gg_8i9X5I3aBcv9I9Pe9kDeeItpCbNlr99FD616SXM5-adyRvpp0PV-VqkGWBHsFYF7XIvKWJryeZhTXPJRPA0jPhRu47--II9qUhOLMBVgD3HYTiowthaimkLDmMST3TIHilWVe1Ie8uoIBhVn8qRaOARRTw.',
    'X-Net-Core': 'crn',
    'X-B3-TraceId': '884ad9e1dcf9b694',
    'x-legacy-fid': '1655522477-0-0-c30b1f138419fb423397a68ea0bc8f68',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-HK;q=0.8, zh-Hant-CN;q=0.7',
    'Mode': 'rawIp',
    # 'Accept-Encoding': 'br;q=1.0, gzip;q=1.0, compress;q=0.5',
    'x-legacy-sid': 'session.1656221397072048863703',
    'User-Agent': 'discover/7.43 (iPhone; iOS 14.7.1; Scale/2.00) Resolution/750*1334 Version/7.43 Build/7430183 Device/(Apple Inc.;iPhone12,8) NetType/WiFi',
    'xy-common-params': 'app_id=ECFAAF02&build=7430183&deviceId=70804187-8F8A-4AEE-9C6A-AAB7705AEFF5&device_fingerprint=202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5&device_fingerprint1=202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5&fid=1655522477-0-0-c30b1f138419fb423397a68ea0bc8f68&identifier_flag=0&lang=zh-Hans&launch_id=677913203&platform=iOS&project_id=ECFAAF&sid=session.1656221397072048863703&t=1656221437&teenager=0&tz=Asia/Shanghai&uis=light&version=7.43',
    'x-legacy-smid': '202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5',
    'x-mini-sig': 'e08752769e9c3038932fc1901db69e38a75e99de2478a43774aff854ade85688',
    'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe4xG1IYD9/c+qCLOlKGmTtFa+lG43EKf+FXTK5FxYywmrdvS53wieguz8Rbqbh+2NE0YQw/YBePY7vxrV4W8OFWv/YPU0h0WchgVw0sYGG1',
    'Accept': '*/*',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'a1=1819e720698ei0yz1djjv175j43u4oqggf72ae3fp00000245301; xhsTrackerId=04506bf7-979a-4ad7-ca1e-345d42a2b615; extra_exp_ids=wx_launch_open_app_decrement_clt,wx_launch_open_app_duration_origin,recommend_comment_hide_exp2,recommend_comment_hide_v2_exp1,recommend_comment_hide_v3_origin,supervision_exp,supervision_v2_exp,commentshow_clt1,gif_exp1,ques_exp1',
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
