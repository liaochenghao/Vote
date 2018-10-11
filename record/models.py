from django.db import models


class User(models.Model):
    OPTION_CHOICE = (
        (0, '关注加拿大留学生问吧'),
        (1, '关注北美留学生'),
        (2, '全部关注'),
        (3, '没关注'),
    )
    open_id = models.CharField('open_id', max_length=64)
    union_id = models.CharField('union_id', max_length=64)
    operation = models.IntegerField('操作类型', choices=OPTION_CHOICE)
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
