from django.urls import path

from .views import TaskList,TaskDetail,CreateTask,UpdateTask,DeleteTask,customUserLogin,RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),

    path('login/',customUserLogin.as_view(),name='login'),
    path('signup/',RegisterPage.as_view(),name='signup'),
    path("",TaskList.as_view(),name='todolist'),
    path("detail/<int:pk>/",TaskDetail.as_view(),name='taskdetail'),
    path("create-task",CreateTask.as_view(),name='create-task'),
    path("edit-task/<int:pk>/",UpdateTask.as_view(),name='edit-task'),
    path("delete-task/<int:pk>/",DeleteTask.as_view(),name='delete-task'),

]
