from rest_framework.routers import DefaultRouter
from apiv1.views import user as user_view

router = DefaultRouter()
router.register(r'users', user_view.UserViewSet)


urlpatterns = router.urls
