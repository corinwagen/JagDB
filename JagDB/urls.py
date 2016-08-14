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
    url(r'^accounts/logout/$', logout, {'next_page': 'login'}, name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^view_questions', views.view_questions, name="view_questions"),
    url(r'^add_questions', views.add_questions, name="add_questions"),
    url(r'^__debug__/', debug_toolbar.urls),
    url(r'^home/', views.home, name="home"),
    url(r'^user/(?P<user_id>\d+)/', views.user_view, name="user_view"),
    url(r'^flag_question/$', views.flag_question, name="flag_question"),
    url(r'^unflag_question/$', views.unflag_question, name="unflag_question"),
    url(r'^export/$', views.export, name="export"),
    url(r'^edit_question/(?P<type>[a-z]+)/(?P<question_id>\d+)/(?P<params>.*)', views.edit_question, name="edit_question"),
    url(r'^delete_question/$', views.delete_question, name="delete_question"),
    url(r'^process_batch_import', views.process_batch_import, name="process_batch_import"),
    url(r'^batch_import', views.batch_import, name="batch_import"),
    url(r'^get_subject_data/$', views.get_subject_data, name="get_subject_data"),
    url(r'', views.home),
    ]
