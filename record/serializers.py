from rest_framework import serializers

from record.models import User, VoteRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['open_id', 'union_id', 'operation', 'name', 'email', 'phone', 'create_time', 'modified_time']


class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRecord
        fields = ['union_id', 'student', 'create_time', 'modified_time']
