# Create your views here.
import json
import os
import re
import requests
import time
import queue

from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread

from urllib import parse
from django.http import HttpResponse

ies_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"  # ies地址

user_post = "https://www.iesdouyin.com/web/api/v2/aweme/post/"  # 用户作品
user_like = "https://www.iesdouyin.com/web/api/v2/aweme/like/"  # 用户喜欢
user_info_url = "https://www.iesdouyin.com/web/api/v2/user/info/"  # 用户详情

challenge_url = "https://www.iesdouyin.com/web/api/v2/challenge/aweme/"  # 挑战地址
challenge_info_url = "https://www.iesdouyin.com/web/api/v2/challenge/info/"  # 挑战详情

music_url = "https://www.iesdouyin.com/web/api/v2/music/list/aweme/"  # 音乐地址
music_info_url = "https://www.iesdouyin.com/web/api/v2/music/info/"  # 音乐详情

hd = {
    'authority': 'aweme.snssdk.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                  'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}

THREADS = 2
# 每次分页数量
PAGE_NUM = 10

# 10个线程
pool = ThreadPoolExecutor(10)

HEADERS = {
    'authority': 'aweme.snssdk.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'x-requested-with': 'XMLHttpRequest',
    'accept': 'application/json',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) "
                  "Version/11.0 Mobile/15A372 Safari/604.1",
}


def index(request):
    url = request.GET.get("url")
    play_url = download_share_videos(url=get_real_address(url))
    return HttpResponse(play_url)


def user_post(request):
    url = request.GET.get("url")
    page_number = request.GET.get("pageNumber")
    page_size = request.GET.get("pageSize")
    play_url = download_user_post(url=get_real_address(url))
    return HttpResponse(play_url)


def user_like(request):
    url = request.GET.get("url")
    page_number = request.GET.get("pageNumber")
    page_size = request.GET.get("pageSize")
    play_url = download_user_like(url=get_real_address(url))
    return HttpResponse(play_url)


def challenge(request):
    url = request.GET.get("url")
    page_number = int(request.GET.get("pageNumber", 0))
    page_size = int(request.GET.get("pageSize", 9))
    play_urls = download_challenge_videos(url=get_real_address(url), page_number=page_number, page_size=page_size)
    return HttpResponse(play_urls)


def music(request):
    url = request.GET.get("url")
    page_number = int(request.GET.get("pageNumber", 0))
    page_size = int(request.GET.get("pageSize", 9))
    play_urls = download_music_videos(url=get_real_address(url), page_number=page_number, page_size=page_size)
    return HttpResponse(play_urls)


def get_dy_url_id(url, char="?"):
    return url.split(char)[0].split("/")[-1]


def generate_signature(uid):
    """
    生成_signature
    :param uid: id
    :return: _signature
    """
    # p = os.popen('node my.js %s' % uid)
    p = os.popen('node ./fuck-byted-acrawler.js %s' % uid)
    return p.readlines()[0].replace("\n", "")


def get_real_address(url):
    """
    获取真实地址
    :param url: 分享的url
    :return: 真实地址
    """
    if url.find('v.douyin.com') < 0:
        return url
    res = requests.get(url, headers=HEADERS, allow_redirects=False)
    return res.headers['location'] if res.status_code == 302 else None


def download_share_videos(url):
    """
    下载用户分享视频
    :param url: 视频地址
    """
    # 从url中取出视频的id
    video_id = get_dy_url_id(url, "/?")

    data = requests.get(url=ies_url, params={"item_ids": video_id, "dytk": ""}).json()
    play_url = data['item_list'][0]['video']['play_addr']['url_list'][0].replace('playwm', "play")
    return play_url
    # download(play_url, video_id)


def download_user_videos(url, _max_cursor=0):
    """
    下载用户的视频，包括作品和喜欢
    :param url: 用户主页地址
    :param _max_cursor: 最大游标
    :return:
    """
    # 获取sec_uid
    params = parse.parse_qs(parse.urlparse(url).query)
    sec_uid = params['sec_uid'][0]

    # 获取uid
    uid = get_dy_url_id(url)
    _signature = generate_signature(uid)

    download_user_post(sec_uid, _signature, _max_cursor)
    # self.download_user_like(sec_uid, _signature, _max_cursor)


def download_user_post(sec_uid, _signature, _count=9, _max_cursor=0):
    """
    下载作品
    :param sec_uid:
    :param _signature:
    :param _count:
    :param _max_cursor:
    :return:
    """
    post_data = ''
    while True:
        content = requests.get(url=user_post, params={
            "sec_uid": str(sec_uid),
            "count": _count,
            "max_cursor": str(_max_cursor),
            "aid": 1128,
            "_signature": str(_signature),
            "dytk": "",
        }, allow_redirects=False).text.replace("\n", "")
        post_data = json.loads(content)
        print(post_data)
        if len(post_data['aweme_list']) > 0:
            break
        time.sleep(2)

    print("获取分页数据成功")
    max_cursor = post_data['max_cursor']
    print("最新_cursor", max_cursor)
    for x in post_data['aweme_list']:
        video_id = x['aweme_id']
        # download(x['video']['play_addr']['url_list'][0], video_id)

    if _max_cursor != max_cursor:
        download_user_post(sec_uid, _signature, PAGE_NUM, _max_cursor)


def download_user_like(sec_uid, _signature, _count=9, _max_cursor=0):
    """
     下载喜欢
    :param sec_uid:
    :param _signature:
    :param _count:
    :param _max_cursor:
    :return:
    """
    post_data = ''
    while True:
        content = requests.get(url=user_like, params={
            "sec_uid": str(sec_uid),
            "count": 100,
            "max_cursor": str(_max_cursor),
            "aid": 1128,
            "_signature": str(_signature),
            "dytk": "",
        }, allow_redirects=False).text.replace("\n", "")
        post_data = json.loads(content)
        if len(post_data['aweme_list']) > 0:
            break
        time.sleep(1)

    print("获取分页数据成功")
    max_cursor = post_data['max_cursor']
    print("最新_cursor", max_cursor)
    for x in post_data['aweme_list']:
        video_id = x['aweme_id']
        # download(x['video']['play_addr']['url_list'][0], video_id)

    if _max_cursor != max_cursor:
        download_user_like(sec_uid, _signature, PAGE_NUM, _max_cursor)


def download_challenge_videos(url, page_number, page_size):
    """
    下载挑战视频
    :param url: 视频地址
    :param page_number: 页码
    :param page_size: 页面尺寸
    :return: 播放地址urls
    """
    challenge_id = get_dy_url_id(url, "/?")  # 获取challenge_id

    challenge_info = requests.get(url=challenge_info_url, params={
        "ch_id": str(challenge_id)
    }).json()

    user_count = challenge_info['ch_info']['user_count']  # 总数量
    view_count = challenge_info['ch_info']['view_count']  # 总数量
    data = requests.get(url=challenge_url, params={
        "ch_id": str(challenge_id),
        "count": page_size,
        "cursor": page_size * page_number,
        "aid": 1128,
        "screen_limit": 3,
        "download_click_limit": 0,
        "_signature": generate_signature(str(challenge_id))
    }).json()
    return playvm2play(data['aweme_list'])


def download_music_videos(url, page_number, page_size):
    """
    根据音乐下载
    :param url: 地址
    :param page_number: 页码
    :param page_size: 页面尺寸
    :return: 播放地址urls
    """
    music_id = get_dy_url_id(url)

    # music_info = requests.get(url=music_info_url, params={
    #     "music_id": str(music_id)
    # }).json()

    data = requests.get(url=music_url, params={
        "music_id": str(music_id),
        "count": page_size,
        "cursor": page_size * page_number,
        "aid": 1128,
        "screen_limit": 3,
        "download_click_limit": 0,
        "_signature": generate_signature(str(music_id))
    }).json()
    return playvm2play(data['aweme_list'])


def playvm2play(data):
    result = []
    for x in data:
        _url = x['video']['play_addr']['url_list'][0].replace('playwm', "play")
        x['video']['play_addr']['url_list'][0] = _url
        result.append(x)
    return result
