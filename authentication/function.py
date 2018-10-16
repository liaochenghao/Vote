# coding: utf-8
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature, BadData
import time

from rest_framework import exceptions

from Vote.settings import SECURE_KEY
import logging

logger = logging.getLogger('django')


def generate_token(user_id, expires=None):
    """
    生成token
    :param user_id:  编号
    :param expires: 过期时间
    :return:
    """
    # 过期时间以秒计算
    if not expires:
        expires = 2 * 60 * 60
    s = Serializer(secret_key=SECURE_KEY['SECRET_KEY'], salt=SECURE_KEY['AUTH_SALT'], expires_in=expires)
    return s.dumps({'user_id': user_id, 'iat': time.time()})


def refresh_token(user_id):
    """
    刷新token，直接让token过期时间后延一小时
    :param user_id:
    :param is_student:
    :return:
    """
    s = Serializer(secret_key=SECURE_KEY['SECRET_KEY'], salt=SECURE_KEY['AUTH_SALT'], expires_in=2 * 60 * 60)
    return s.dumps({'user_id': user_id, 'iat': time.time()})


def token_auth(token):
    """
    验证token
    :param token:
    :return:
    """
    # logger.info('#' * 60)
    # logger.info(token)
    # logger.info('#' * 60)
    s = Serializer(secret_key=SECURE_KEY['SECRET_KEY'], salt=SECURE_KEY['AUTH_SALT'])
    data = dict()
    try:
        data = s.loads(token)
    except SignatureExpired:
        logger.info('*' * 20 + 'token expired' + '*' * 20)
        raise exceptions.ValidationError('token过期')
    except BadSignature as e:
        encoded_payload = e.payload
        if encoded_payload is not None:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                logger.info('*' * 20 + 'bad signature of token' + '*' * 20)
                raise exceptions.ValidationError('token篡改')
    except Exception as e:
        logger.info('*' * 20 + 'wrong token with unknown reason' + '*' * 20)
        raise exceptions.ValidationError('未知错误')
    # logger.info('#' * 60)
    # logger.info(data)
    # logger.info('#' * 60)
    if 'user_id' not in data:
        logger.info('*' * 20 + 'illegal payload inside' + '*' * 20)
        raise exceptions.ValidationError('不合法的载体')
    refresh = False
    # 如果token过期时间与当前时间相隔10分钟以内，则需要刷新token
    if (data['iat'] - time.time()) / 60 < 10:
        refresh = True
    return data['user_id'], refresh
