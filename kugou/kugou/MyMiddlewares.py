# -*- coding: utf-8 -*-
# 随机UserAgent和代理IP的所需库
import random
from scrapy.conf import settings
# UserAgent随机
class RandomUserAgent_Middleware(object):
    def __init__(self):
        # 在settings中设置USER_AGENT_LIST列表，在中间件中调用
        self.user_agent_list = settings["USER_AGENT_LIST"]
    # 每次请求访问时，在headers中加入一个随机的UserAgent
    def process_request(self, request, spider):
        request.headers['USER_AGENT'] = random.choice(self.user_agent_list)