from django.urls import path, re_path
from .views import bot_view
urlpatterns = [
    re_path(r'^', bot_view, name='bot_view'),
]
# add to core urls
# path('bot/', include('telegram_bot.urls')),


