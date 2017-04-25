from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from apiv1.views import user as user_view

user_patterns = format_suffix_patterns([
    url(r'^signup/$', user_view.UserCreateViewSet.as_view({'post':'create'}), name='user_signup'),
    url(
        r'^activate/(?P<pk>\d+)/$',
        user_view.UserCreateViewSet.as_view({'get':'activate'}),
        name='user_activate'
    ),
    url(r'^list/$', user_view.UserViewSet.as_view({'get':'list'}), name='user_list'),
    url(
        r'^change-password/$',
        user_view.UserViewSet.as_view({'post': 'change_password'}),
        name='user_changepass'
    ),
    url(
        r'^login/$',
        user_view.UserLoginViewSet.as_view({'post': 'login'}),
        name='user_login'
    ),
])

urlpatterns = [
    url(r'^user/', include(user_patterns, namespace='user')),
]
