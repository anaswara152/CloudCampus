from django.urls import path
from student import views

urlpatterns=[
    path('student_register',views.student_register,name='student_register'),
    path('studenthome',views.studenthome,name='studenthome'),
    path('view_events_for_students/<int:id>',views.view_events_for_students,name='view_events_for_students'),
    path('join_event/<int:id>',views.join_event,name='join_event'),
    path('student_applications',views.student_applications,name='student_applications'),
    path('student_view_programmes/<int:id>',views.student_view_programmes,name='student_view_programmes'),
    path('view_application_detail/<int:id>',views.view_application_detail,name='view_application_detail'),
    path('create_group',views.create_group,name='create_group'),
    path('view_groups',views.view_groups,name='view_groups'),
    path('group_chat/<int:id>',views.group_chat,name='group_chat'),
    path('student_profile',views.student_profile,name='student_profile'),
    path('edit_student_profile',views.edit_student_profile,name='edit_student_profile')
]