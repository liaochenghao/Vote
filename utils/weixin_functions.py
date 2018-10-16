# coding: utf-8
import datetime
import json
import logging
import random

import requests
from rest_framework import exceptions

# from Vote.settings import WX_SMART_CONFIG
# from authentication.models import User
# from ticket.functions import TicketAuthorize
from Vote.settings import WX_SMART_CONFIG
from authentication.function import generate_token
from record.models import User

logger = logging.getLogger('django')


class WxInterface:
    def __init__(self):
        self.appid = WX_SMART_CONFIG['appid']
        self.secret = WX_SMART_CONFIG['secret']

    # 微信公众号code认证
    def code_authorize(self, code):
        url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.get(url=url, params=params, verify=False)
        if response.status_code != 200:
            logger.info('X' * 70)
            logger.info(response.text)
            logger.info('X' * 70)
            raise exceptions.ValidationError('连接微信服务器异常')
        res = response.json()
        if res.get('unionid'):
            # 首先查询数据库中是否存在该用户信息
            user_info = User.objects.filter(union_id=res['unionid']).first()
            if not user_info:
                # 给用户生成邀请码
                # while True:
                #     seed = random.random()
                #     code = str(int(seed * 1000000))
                #     code = code + '8' * (6 - len(code)) if len(code) < 6 else code
                #     code_exist = UserInfo.objects.filter(code=code).count()
                #     if code_exist == 0:
                #         break
                # qr_code = self.get_forever_qrcode(res.get('openid'))
                # 如果用户不存在，则向数据库插入数据
                user_info = User.objects.create(union_id=res['unionid'], last_login=datetime.datetime.now())
            else:
                # 如果用户存在，更新用户信息
                user_info.last_login = datetime.datetime.now()
                user_info.save()
            token = generate_token(user_info.id)
            return {'user_id': user_info.id, 'token': token}
        else:
            logger.info('X' * 70)
            logger.info(response.text)
            logger.info('X' * 70)
            raise exceptions.ValidationError('微信认证异常： %s' % json.dumps(res))

    # 调用微信接口向用户发送客服文本消息
    def send_customer_message(self, to_user, text, access_token):
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=" + access_token
        params = {
            "touser": to_user,
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        response = requests.post(url=url, params=params, verify=False)
        if response.status_code != 200:
            logger.info('WxInterface code_authorize response: %s' % response.text)
            raise exceptions.ValidationError('连接微信服务器异常')
        res = response.json()
        logger.info('8' * 70)
        logger.info(res)
        logger.info('8' * 70)
        return


WxInterfaceUtil = WxInterface()
