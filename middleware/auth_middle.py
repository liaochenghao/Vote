# coding: utf-8
import json
from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse

from record.models import User
from record.serializers import UserSerializer
from utils.redis_server import redis_client
from Vote.settings import ignore_auth_urls
from authentication.function import token_auth
import logging

logger = logging.getLogger("django")


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        url_path = request.path
        if url_path in ignore_auth_urls:
            return
        logger.info('Auth Url: %s' % url_path)
        # ticket = request.COOKIES.get('ticket')
        # if not ticket:
        #     data = request.GET.dict()
        #     ticket = data.get('ticket')
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            token = request.META.get('HTTP_TOKEN')
        if not token:
            return HttpResponse(content=json.dumps(dict(code=400, msg='please take your token in header')),
                                content_type='application/json')
        try:
            user_id, is_refresh = token_auth(token)
        except Exception as e:
            logger.info('*' * 60)
            logger.info(e.__repr__())
            logger.info('*' * 60)
            return HttpResponse(content=json.dumps(dict(code=401, msg='token auth failed')))
        request.refresh_token = is_refresh
        if not redis_client.get_instance(key=user_id):
            logger.info('Get User Info From DataBase')
            user = User.objects.filter(id=user_id).first()
            serializer = UserSerializer(user)
            user_info = serializer.data
            redis_client.set_instance(user_id, user_info)
        else:
            user_info = redis_client.get_instance(key=user_id)
            logger.info('Get User Info From Redis')
        request.user_info = user_info
