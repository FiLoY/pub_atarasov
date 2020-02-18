"""atarasov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('bot/', include('apps.telegram_bot.urls')),
    path('twitch_api/', include('apps.twitch_api.urls')),

    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),

    path('api/', include('apps.api.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('api/token/refresh/', refresh_jwt_token, name='token_obtain_pair'),

    path('account/', include('apps.account.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
