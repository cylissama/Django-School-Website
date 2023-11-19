"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#import the view from personal folder, with the function name
from personal.views import (
    home_screen_view,
)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
    del_user,
    scores_view,
    set_grade,
    view_attempts,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
    path('blog/', include('blog.urls', 'blog')),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account"),
    path('scores/', scores_view, name="scores"),
    path('set_grade/', set_grade, name="set_grade"),
    path('view_attempts/', view_attempts, name="view_attempts"),
    path('delete/', del_user, name="delete"),
    path('quiz/', include('quiz.urls')),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    ]   

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



