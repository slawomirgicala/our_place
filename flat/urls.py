from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='flat-home'),
    path('about/', views.about, name='about-app'),
    path('new_flat/', views.new_flat, name='new-flat'),
    path('enter_flat/', views.enter_flat, name='enter-flat'),
    path('new_chore/', views.new_chore, name='new-chore'),
    path('chores_list/', views.chores_list, name='chores-list'),
    path('announcements/', views.announcements, name='flat-announcements'),
    path('new_announcement', views.new_announcement, name='new-announcement'),
    path('add', views.addTodo, name='add'),
    path('complete/<todo_id>', views.completeTodo, name='complete'),
    path('deletecomplete', views.deleteCompleted, name='deletecomplete'),
    path('your_chores/', views.your_chores, name='your-chores'),
    path('completed_chore/<chore_id>', views.completed_chore, name='completed-chore'),
    path('done_chores/', views.done_chores, name='done-chores')
]
