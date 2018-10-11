from rest_framework import serializers

from record.models import User, VoteRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['open_id', 'name', 'email', 'phone', 'student', 'create_time', 'modified_time']


class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRecord
        fields = ['open_id', 'student', 'create_time', 'modified_time']
