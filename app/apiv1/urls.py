from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from apiv1.views import user as user_view

user_patterns = format_suffix_patterns([
    url(r'signup/', user_view.CreateUserView.as_view(), name='user_signup'),
])

urlpatterns = [
    url(r'^user/', include(user_patterns, namespace='user')),
]