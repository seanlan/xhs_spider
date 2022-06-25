import requests


HEADERS = {
    'Host': 'www.xiaohongshu.com',
    'Connection': 'Keep-Alive',
    # 'Content-Length': '32',
    'X-raw-ptr': '0',
    'x-legacy-fid': '1655522477-0-0-c30b1f138419fb423397a68ea0bc8f68',
    'User-Agent': 'discover/7.43 (iPhone; iOS 14.7.1; Scale/2.00) Resolution/750*1334 Version/7.43 Build/7430183 Device/(Apple Inc.;iPhone12,8) NetType/WiFi',
    'xy-direction': '75',
    'x-mini-mua': 'eyJhIjoiRUNGQUFGMDIiLCJrIjoiZDhlM2MwZDYxM2M3ODZhY2NkNDA3ZDQ3ZjE3M2MxMGRkZGRkNWFiMTkyZjQ0N2JiOWJjNmQ0YTViZDMyZGM3ZSIsInAiOiJpIiwicyI6IjI4ZjcyMzJiMWYwYmFlNjBkMjNkNmY4MjRjNGQ2NGNiIiwidSI6IjAwMDAwMDAwOTYyYmM4NTBlMWNiNDU2NGNiYWM1YzM3ODE0ZWViNjAiLCJ2IjoiMS4xLjIifQ.Lx32WJbyxIWEeaf54OiUaMvoahOEsNNq_KxJq5u5sLZglDHhYH9iu2uoOMF-xfZGLEOeCTuLh57vWbxycuShzisezC3IYX2WpeTAn62bP8HKhOFl0Xc1FFuYuHmXqDbT8z0BAfCJC695v68LO0UAmbQ5jCt5-9npYZuZbxSw-y_v1wzxYg__fbdt5hyB1_o800QAyCmsCTCgoLyjPzfVdnBO2qeMuX1L9b6AASGwwegEtcgbqN2VKikUUI0ASJ5qVnn_bnBdj_xx4EXx_FCs7_RxiiewyuhLGbk4KjkJajEfvNEdE4xXLjQzmIuGHKAvaK4aK2auNoHzJR6700_LuU-Chc7g9jzaG-UYRjArZ9DIG__Ury0MLlmu8ZkHfbDnqdC07ZqOypKpZ2F1XS0vb7Y9g4-6e5LxA0jnXSkRNq9UNF6xNEnQ_PKXPssJ5WR24F6Usf3jO90sHOz27mq5XOMtmgwlGNcTnmIgjjzvVgikY2Tv0N9Nzk31z8e6FS5rVw43IOHkxGBeMbEd6pq1Tw.',
    'X-B3-TraceId': '40d00b251fa94ebb',
    'x-mini-sig': '487b318ef3c799e0f7ee6fdd09d434b172c40f11b4b31a0e5c05dee727a56a1b',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-HK;q=0.8, zh-Hant-CN;q=0.7',
    'X-Net-Core': 'crn',
    'x-legacy-did': '70804187-8F8A-4AEE-9C6A-AAB7705AEFF5',
    'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe4xG1IYD9/c+qCLOlKGmTtFa+lG43EKf+FXTK5FxYywmrdvS53wieguz8Rbqbh+2NE0YQw/YBePY7vxrV4W8OEBPQ3IQrg6NvHJEO7Ibia/',
    'x-legacy-smid': '202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5',
    'xy-platform-info': 'platform=iOS&version=7.43&build=7430183&deviceId=70804187-8F8A-4AEE-9C6A-AAB7705AEFF5&bundle=com.xingin.discover',
    'xy-common-params': 'app_id=ECFAAF02&build=7430183&deviceId=70804187-8F8A-4AEE-9C6A-AAB7705AEFF5&device_fingerprint=202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5&device_fingerprint1=202206181121231ec2a2c5edd493fda59bfa4881f3e14c012e7d43d51408e5&fid=1655522477-0-0-c30b1f138419fb423397a68ea0bc8f68&identifier_flag=0&lang=zh-Hans&launch_id=677261327&platform=iOS&project_id=ECFAAF&sid=session.1655560320757055767435&t=1655569452&teenager=0&tz=Asia/Shanghai&uis=light&version=7.43',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    # 'Accept-Encoding': 'br;q=1.0, gzip;q=1.0, compress;q=0.5',
    'Mode': 'rawIp',
    'x-legacy-sid': 'session.1655560320757055767435',
    'Accept': '*/*',
}

CHECK_GROUP_URL = 'https://www.xiaohongshu.com/api/im/red/group/personal_page_group_show_info'
GET_GROUP_MEMBERS_URL = 'https://www.xiaohongshu.com/api/im/red/group/userinfo'


class XHSHelper(object):

    def __int__(self, headers=HEADERS):
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
        res = requests.post(url=CHECK_GROUP_URL, data=data, headers=self.headers)
        print(res.text)
        return res.json()

    def get_get_group_members(self, group_id):
        """
        获取群组成员
        :param group_id:
        :return:
        """
        data = {
            'group_id': group_id,
        }
        res = requests.post(url=CHECK_GROUP_URL, data=data, headers=self.headers)
        print(res.text)
        return res.json()


xhs_helper = XHSHelper(headers=HEADERS)


if __name__ == '__main__':
    user_id = '5cc730f7000000001601b891'
    xhs_helper.get_user_groups(user_id)
    group_id = '135861640641118838'
    xhs_helper.get_get_group_members(group_id='5cc730f7000000001601b891')
