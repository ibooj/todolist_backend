"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from rest_framework.authtoken import views
from .views import TaskList, TaskDetail, SubTaskCreateAPIView, SubTaskDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^task/$', TaskList.as_view(), name='task-list'),
    url(r'^task/(?P<pk>\w+)/$', TaskDetail.as_view(), name='task-detail'),
    url(r'^subtask/$', SubTaskCreateAPIView.as_view(), name='subtask-create'),
    url(r'^subtask/(?P<pk>\w+)/$', SubTaskDetail.as_view(), name='subtask-detail'),
]

