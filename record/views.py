from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response

from record.models import User, VoteRecord, Student, SubscribeMessage
from record.serializers import UserSerializer, VoteRecordSerializer, StudentSerializer, SubscribeMessageSerializer


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
