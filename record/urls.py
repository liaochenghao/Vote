# coding:utf-8
from rest_framework.routers import SimpleRouter
from record.views import UserView, VoteRecordView

router = SimpleRouter()
router.register(r'user', UserView)
router.register(r'user/vote', VoteRecordView)
urlpatterns = router.urls
