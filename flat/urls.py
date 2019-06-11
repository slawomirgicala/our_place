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
    path('add', views.add_todo, name='add'),
    path('complete/<todo_id>', views.complete_todo, name='complete'),
    path('deletecomplete', views.delete_completed, name='deletecomplete'),
    path('your_chores/', views.your_chores, name='your-chores'),
    path('completed_chore/<chore_id>', views.completed_chore, name='completed-chore'),
    path('done_chores/', views.done_chores, name='done-chores'),
    path('delete_announcement/<ann_id>', views.delete_announcement, name='delete-announcement'),
    path('delete_chore/<chore_id>', views.delete_chore, name='delete-chore'),
    path(r'^like/$', views.like_post, name='like_post')
]
