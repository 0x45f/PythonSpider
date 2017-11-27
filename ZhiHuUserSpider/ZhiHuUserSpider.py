import json
import random
import time
from builtins import classmethod

import requests
from db.RedisHandler import RedisHandler
from lxml import html
from http import cookiejar
import threading
from Tools import Tools
from db.MongoHandler import MongoHandler
from LogHandler import LogHandler


# 只抓取了type为people的用户
class ZhiHuUserSpider(threading.Thread):
    headers = {
        'accept': 'application / json, text / plain, * / *',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh - CN, zh;q = 0.8',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'X-UDID': 'AFDC3cbZvguPTk1xbYYtpQt214bsP2px88I='
    }
    redis_handler = RedisHandler()
    mongo_handler = MongoHandler()
    logger = LogHandler.get_logger()
    lock = threading.Lock()

    # 关注的人最多抓取100个
    user_count = 100
    # 防止带抓取的list中累计太多的url_token
    list_count = 1000
    # 请求超时时间
    timeout = 20

    def __init__(self):
        super(ZhiHuUserSpider, self).__init__()
        self.__session = requests.session()
        # self.__mysql_handler = MySqlHandler()
        # 字典的update方法进行并集更新
        self.__session.headers.update(self.headers)
        self.__session.cookies = cookiejar.LWPCookieJar(filename='./login/cookies')
        self.__session.cookies.load()
        # session的mount函数可以设置请求失败后的重复次数
        self.update_ua()
        self.update_proxy()

    @classmethod
    def count_thread(cls, threads):
        count = 0
        for t in threads:
            if t.isAlive():
                count = count + 1
        cls.logger.info('Main:运行的线程数为' + str(count))

    def update_ua(self):
        self.__session.headers.update({'User-Agent': Tools.get_ua()})

    def update_proxy(self):
        self.lock.acquire()
        self.__session.proxies.update({'HTTPS': Tools.get_proxy})
        self.lock.release()

    def get_tree(self, url):
        text = self.__session.get(url, timeout=self.timeout).text
        return html.fromstring(text)

    # 获取首页上出现的用户的主页地址并存入redis
    def get_url_token_from_index(self):
        self.logger.debug(self.name + ':开始抓取 https://www.zhihu.com/explore 的用户！')
        tree = self.get_tree('https://www.zhihu.com/explore')
        users_url = tree.xpath('//a[@class="author-link"]/@href')
        # 将类型为people的url存入redis
        for u in [i[8:] for i in users_url if 'people' in i]:
            # print(u)
            self.redis_handler.save_url_token(u)
        self.logger.debug(self.name + ':抓取 https://www.zhihu.com/explore 的用户完毕')

    '''
    通过用户的url_token获取该用户关注的人或者关注该用户的人
    根据is_followers的值来确定获取哪一类
    默认获取用户关注的人的url_token并存入redis
    '''
    def get_follow_url_token(self, url_token, is_following=True):
        follow = 'followees' if is_following else 'followers'
        self.logger.debug(self.name + ':' + url_token + ' ' + follow + '开始抓取...')
        is_end = False
        next_url = 'https://www.zhihu.com/api/v4/members/' + url_token + '/' + follow + '?' \
                                                                                        'include=data%5B*%5D.answer_count%2Carticles_count%2Cgender' \
                                                                                        '%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F' \
                                                                                        '(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
        # 改变请求头的referer
        ref_follow = 'following' if is_following else 'followers'
        referer = 'https://www.zhihu.com/people/' + url_token + '/' + ref_follow
        self.__session.headers.update({'Referer': referer})

        # 最多抓取100个该用户关注的人或关注该用户的人
        count = 0
        while (not is_end) and (count <= self.user_count):
            try:
                text = self.__session.get(next_url, timeout=self.timeout).text
            except requests.exceptions.ConnectionError as e:
                self.logger.error(self.name + ':' + str(e.args))
                self.update_proxy()
                self.update_ua()
                # 不太好应该设定一个尝试的最大次数
                continue
            else:
                # dump和dumps是将python对象转换成json格式；load和loads是将json格式转换成python对象
                res = json.loads(text)
                # 会有未通过验证的用户信息，会有key为error的字段
                if 'error' in res.keys():
                    self.logger.warning(self.name + ':' + url_token + ' 获取到的信息未通过认证')
                    return
                # 是否获取了所有的用户, 是bool类型
                is_end = res['paging']['is_end']
                # 下一组20个用户的xhr地址
                next_url = res['paging']['next']
                # 存入redis
                for u in [user['url_token'] for user in res['data'] if user['type'] == 'people']:
                    self.redis_handler.save_url_token(u)
                    count = count + 1
                self.update_ua()
                time.sleep(random.randint(2, 4))
        self.logger.debug(self.name + ':' + url_token + ' ' + follow + '抓取完毕')

    # 传入一个用户的url_token,将该用户的信息存入mongo
    def save_info_to_mongo(self, url_token):
        url = 'https://www.zhihu.com/api/v4/members/' + url_token + '?include=' \
                                                                    'locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2C' \
                                                                    'voteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2C' \
                                                                    'cover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2C' \
                                                                    'following_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2C' \
                                                                    'answer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2C' \
                                                                    'columns_count%2Ccommercial_question_count%2Cfavorite_count%2C' \
                                                                    'favorited_count%2Clogs_count%2Cmarked_answers_count%2C' \
                                                                    'marked_answers_text%2Cmessage_thread_token%2Caccount_status%2C' \
                                                                    'is_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2C' \
                                                                    'is_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2C' \
                                                                    'show_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2C' \
                                                                    'is_followed%2Cis_org_createpin_white_user%2Cmutual_followees_count%2C' \
                                                                    'vote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2C' \
                                                                    'thanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2C' \
                                                                    'allow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2C' \
                                                                    'badge%5B%3F(type%3Dbest_answerer)%5D.topics'
        try:
            # 发生错误后，错误语句之后的代码不会执行
            text = self.__session.get(url, timeout=self.timeout).text
            res = json.loads(text)
        except requests.exceptions.ConnectionError as e:
            self.redis_handler.delete_from_hash(url_token)
            self.logger.error(self.name + ':' + str(e.args))
            self.update_proxy()
            self.update_ua()
        # except requests.exceptions.Timeout as e:
        #     pass
        except json.decoder.JSONDecodeError as e:
            # 保存失败，从hash中弹出该url_token
            self.redis_handler.delete_from_hash(url_token)
            self.logger.error(self.name + ':' + str(e.args) + ' ' + url_token + '保存失败')
        # 没有错误的时候执行
        else:
            # 会有未通过验证的用户信息，会有key为error的字段
            if 'error' in res.keys():
                self.redis_handler.delete_from_hash(url_token)
                self.logger.warning(self.name + ':' + url_token + ' 获取到的信息未通过认证')
                return
            self.mongo_handler.save_info(res)
            self.logger.debug(self.name + ':' + url_token + '用户已经信息保存进mongo')
            self.update_ua()
            time.sleep(random.randint(2, 4))

    def entry(self):
        self.lock.acquire()
        # 刚开始redis中没有数据，抓取主页上的用户
        if self.redis_handler.get_list_len() == 0:
            self.get_url_token_from_index()
        self.lock.release()

        # 从redis的list中弹出一个url，找到该用户关注的人和关注该用户的人，并保存用户数据进mongo
        while True:
            self.lock.acquire()
            url_token = self.redis_handler.get_url_token()
            self.lock.release()
            # 保存该用户的信息
            self.save_info_to_mongo(url_token)
            # 加快抓取用户信息，现在的情况就是redis中保存了太多的url_token而mongo中数据很少
            if self.redis_handler.get_list_len() < self.list_count:
                # 该用户关注的人
                self.get_follow_url_token(url_token, True)
                # 关注该用户的人
                self.get_follow_url_token(url_token, False)

    def run(self):
        # super().run()
        self.logger.debug(threading.current_thread().name + ' is running')
        self.entry()


if __name__ == '__main__':
    threads = []
    n = 5
    for i in range(n):
        t = ZhiHuUserSpider()
        threads.append(t)
    for i in range(n):
        threads[i].start()
    # for i in range(n):
    #     # join将主线程阻塞在这里
    #     # 默认情况下主线程会等待子线程的结束
    #     threads[i].join()
    # 定时任务！！定时统计运行的线程，当线程数过少的时候开启新的线程
    while True:
        time.sleep(300)
        ZhiHuUserSpider.count_thread(threads)
