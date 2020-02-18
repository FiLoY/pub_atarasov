from django.urls import path
from apps.blog.views import PostViewSet
from apps.account.views import UserViewSet, GetUserViewSet, SignUpViewSet
from rest_framework.routers import DefaultRouter

# app_name = "articles"
# # app_name will help us do a reverse look-up latter.
lol_patterns = [
    path('users/getuser/', GetUserViewSet.as_view()),
    path('users/register/', SignUpViewSet.as_view()),
#     path('articles/<int:pk>/', SingleArticleView.as_view()),
#
]
app_name = 'api'

router = DefaultRouter()
router.register(r'posts', PostViewSet)
# router.register(r'u/getuser', GetUserViewSet, 'username')
router.register(r'users', UserViewSet)
urlpatterns = lol_patterns + router.urls

