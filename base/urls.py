from django.urls import path
from . import views

from . views import CustomLoginView, TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,RegisterPage, PendingTaskList, FinishedTaskList, SkippedTaskList
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('accounts/login/', CustomLoginView.as_view (),name='login'),
    path('logout/', LogoutView.as_view (next_page='login'),name='logout'),
    path('register/',RegisterPage.as_view(), name='register'),
    path('',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('create-task/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),
    path('pending/', PendingTaskList.as_view(), name='pending_tasks'),
     path('finished/', FinishedTaskList.as_view(), name='finished_tasks'),
      path('skipped/', SkippedTaskList.as_view(), name='skipped_tasks'),
     path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),
     path('calendar/', views.CalendarView.as_view(), name='calendar'),
]