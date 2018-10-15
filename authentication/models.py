from django.db import models


# Create your models here.
class Token(models.Model):
    token = models.CharField('token', max_length=64, primary_key=True)
    user_id = models.CharField('用户编号', max_length=64)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    expire_time = models.DateTimeField('过期时间')

    class Meta:
        db_table = 'token'
