from django.urls import path
from event_manager import views

urlpatterns=[
       path('eventmaneger_register',views.eventmaneger_register,name='eventmaneger_register'),
       path('manager_home',views.manager_home,name='manager_home'),
       path('create_event',views.create_event,name='create_event'),
       path('view_events_for_manager',views.view_events_for_manager,name='view_events_for_manager'),
       path('edit_events/<int:id>',views.edit_events,name='edit_events'),
       path('delete_events/<int:id>',views.delete_events,name='delete_events'),
       path('create_programme/<int:id>',views.create_programme,name='create_programme'),
       path('view_event_participants',views.view_event_participants,name='view_event_participants'),
       path('view_programmes',views.view_programmes,name='view_programmes'),
       path('edit_programme/<int:id>',views.edit_programme,name='edit_programme'),
       path('delete_programme/<int:id>',views.delete_programme,name='delete_programme'),
       path('accept_participants/<int:id>',views.accept_participants,name='accept_participants'),
       path('reject_participants/<int:id>',views.reject_participants,name='reject_participants')

]