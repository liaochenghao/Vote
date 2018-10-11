from django.db import models


class User(models.Model):
    open_id = models.CharField('open_id', max_length=64, primary_key=True)
    name = models.CharField('姓名', max_length=64, null=True)
    email = models.EmailField('邮箱', max_length=30, null=True)
    phone = models.CharField('联系手机', max_length=30, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField('创建时间', auto_now=True, null=True)

    class Meta:
        db_table = "user"


class VoteRecord(models.Model):
    open_id = models.CharField('open_id', max_length=64, primary_key=True)
    student = models.CharField('投票对象', max_length=30, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField('创建时间', auto_now=True, null=True)

    class Meta:
        db_table = "vote_record"
