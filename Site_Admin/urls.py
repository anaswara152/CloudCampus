from django.urls import path
from Site_Admin import views

urlpatterns=[
     path('adminhome',views.adminhome,name='adminhome'),
     path('view_students',views.view_students,name='view_students'),
     path('approve_students/<int:id>',views.approve_students,name='approve_students'),
     path('remove_students/<int:id>',views.remove_students,name='remove_students'),
     path('view_managers',views.view_managers,name='view_managers'),
     path('approve_manager/<int:id>',views.approve_manager,name='approve_manager'),
     path('remove_manager/<int:id>',views.remove_manager,name='remove_manager'),
     path('view_events_foradmin',views.view_events_foradmin,name='view_events_foradmin'),
     path('view_event_participants_admin/<int:id>',views.view_event_participants_admin,name='view_event_participants_admin'),
     path('view_programmes_admin/<int:id>',views.view_programmes_admin,name='view_programmes_admin')
]