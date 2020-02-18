from django.urls import path
from .views import ArticleViewSet
from rest_framework.routers import DefaultRouter

# app_name = "articles"
# # app_name will help us do a reverse look-up latter.
# urlpatterns = [
#     path('articles/', ArticleView.as_view({'get': 'list'})),
#     path('articles/<int:pk>/', SingleArticleView.as_view()),
#
# ]
app_name = 'blog'

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
urlpatterns = router.urls

