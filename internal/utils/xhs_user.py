import requests

headers = {
    'Host': 'edith.xiaohongshu.com',
    'Connection': 'Keep-Alive',
    'xy-platform-info': 'platform=iOS&version=7.43&build=7430183&deviceId=19B4BA29-FE0E-4010-82EC-E90D65024F07&bundle=com.xingin.discover',
    'X-raw-ptr': '0',
    'xy-direction': '38',
    'x-legacy-did': '19B4BA29-FE0E-4010-82EC-E90D65024F07',
    'x-mini-mua': 'eyJhIjoiRUNGQUFGMDIiLCJrIjoiMjI5N2U4YzgyYWU2N2UzNzE4NDdjYWU3ZjY0ZmI5YmJjY2UxMjFjNDU5MDEzYzRjNDdkZGE5NmEyYzNkYmIzMCIsInAiOiJpIiwicyI6ImRiMDdmZThmMjk0NGZjMGMwOGM1ODhhZTE4MDQxZTVkIiwidSI6IjAwMDAwMDAwMDE5ZDA4Njg2YjE2ZmE1YjliM2FhOTEyZWQxMGU2MjQiLCJ2IjoiMS4xLjIifQ.zs5C_AswbsNcw4FJIlOWnlgybn1faAxY6xP_i5Xy7cEheQqnQVFqJaBV8DPWbQP1FqpA_1MqGUgSH4H3gooiZ1JbKiA4T9S3Z3N3AEpYxmtbF2gXz-SQi9-DcHLbojMjU-9j3234UsrLb0BEb3uTYPvFO5129LcqtsFR7zHnMbtg62G4KqYNz8EApolelqG7IfVTPKH_FelqvsXsM-IptbkNA_upTC_5P8hqGNVtiZQY8Y_Yu7TX8AYfWb5zGXbn95DsIdoLi6SL8vIqC_MhXpZVyTw3bz4xHA6URtgcmjn937VF1OYfhbA8vt6h8uCru-THKY9psHV3MmGcSrFooNYqlMEuLusKwwGGKZ88Etmo4DYraWDstdb7zsC-McSGFeYf9aozYJGDHCWSo0ptT32AQRDbHseGk2wxaqElAVu4VXYlgZ4rxZ534lCTjBileBFm_nKItVNam9q-WfD1jjUawu63xVmM76GjbMsqT73_O1tyLmBG2R5i6AcQWrOGHR_62Ua0G3QsSAElkpuTAPFzyX4cwggwWE-fa39OkBc.',
    'X-Net-Core': 'crn',
    'X-B3-TraceId': 'b90bead2e4cc65ef',
    'x-legacy-fid': '1621348937-0-0-dba081b4acd918a264073409eae89bc5',
    # 'Accept-Encoding': 'br;q=1.0, gzip;q=1.0, compress;q=0.5',
    'Mode': 'rawIp',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'x-legacy-sid': 'session.1655632817703329615464',
    'User-Agent': 'discover/7.43 (iPhone; iOS 15.0; Scale/3.00) Resolution/1125*2436 Version/7.43 Build/7430183 Device/(Apple Inc.;iPhone10,3) NetType/WiFi',
    'xy-common-params': 'app_id=ECFAAF02&build=7430183&deviceId=19B4BA29-FE0E-4010-82EC-E90D65024F07&device_fingerprint=20210518224218b78014579b97de8900950d32045d0dea01b876a892da510b&device_fingerprint1=20210518224218b78014579b97de8900950d32045d0dea01b876a892da510b&fid=1621348937-0-0-dba081b4acd918a264073409eae89bc5&identifier_flag=0&lang=zh-Hans&launch_id=677331377&platform=iOS&project_id=ECFAAF&sid=session.1655632817703329615464&t=1655638590&teenager=0&tz=Asia/Shanghai&uis=light&version=7.43',
    'x-legacy-smid': '20210518224218b78014579b97de8900950d32045d0dea01b876a892da510b',
    'x-mini-sig': 'b276105f575a276e5223c2d267eb47819e9f03887e228d9a7230fce615eff5ed',
    'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe4xG1IYD9/c+qCLOlKGmTtFa+lG43EKf+FXTK5DzPa07MdlRZ2OiuAqz8Qq3c1+2aBHYww7GGX8Yr703i8WhuPkF4Bzw0XSasWCXGQf+EiH',
    'Accept': '*/*',
}

params = {
    'profile_page_head_exp': '1',
    'user_id': '5baed2811634f90001bcd27a',
}


if __name__ == '__main__':
    response = requests.get('https://edith.xiaohongshu.com/api/sns/v3/user/info', params=params, headers=headers)
    print(response.text)

