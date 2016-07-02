"""JagDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from JagDB import views 
from django.contrib.auth.views import login, logout
import debug_toolbar

#app_name = "jagdb"
urlpatterns = [
    url(r'^accounts/login/$',  login, name="login"),
    url(r'^accounts/logout/$', logout, name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^view_questions', views.view_questions, name="view_questions"),
    url(r'^add_questions', views.add_questions, name="add_questions"),
    url(r'^__debug__/', debug_toolbar.urls),
    url(r'^home/', views.home, name="home"),
]
