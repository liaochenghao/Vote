from django.db import transaction
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from record.models import User, VoteRecord, Student, SubscribeMessage
from record.serializers import UserSerializer, VoteRecordSerializer, StudentSerializer, SubscribeMessageSerializer
import logging

from utils.redis_server import redis_client

logger = logging.getLogger('django')


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(['POST'])
    @transaction.atomic
    def check_account(self, request):
        """
        检查用户信息
        :param request:
        :return:
        """
        params = request.data
        encryptedData = params.get('encryptedData')
        iv = params.get('iv')
        if not (iv, encryptedData):
            raise serializers.ValidationError('encryptedData、iv参数不能为空')
        user_info = User.objects.filter(union_id=params.get('user_id')).first()
        data = UserSerializer(user_info)
        if not data.data:
            logger.info('无法通过用户union_id获取用户记录: user_id=%s' % params.get('user_id'))
            raise serializers.ValidationError('无法通过用户union_id获取用户记录: user_id=%s' % params.get('user_id'))
        # 录入用户信息到数据库，同时也要注意微信用户可能会更换信息
        if user_info.nick_name != params.get('nick_name') or user_info.avatar_url != params.get('avatar_url'):
            logger.info('check_account更新用户信息: user_id=%s' % params.get('user_id'))
            user_info.nick_name = params.get('nick_name')
            user_info.avatar_url = params.get('avatar_url')
            user_info.save()
            temp = UserSerializer(user_info).data
            logger.info('Update User from Redis')
            logger.info(temp)
            redis_client.set_instance(user_info.union_id, temp)
        return Response()


class VoteRecordView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = VoteRecord.objects.all()
    serializer_class = VoteRecordSerializer


class StudentView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SubscribeMessageView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = SubscribeMessage.objects.all()
    serializer_class = SubscribeMessageSerializer
