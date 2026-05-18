from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User,Group
from event_manager.models import*
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
# Create your views here.
def studenthome(request):
    today = timezone.now().date()
    events = Event.objects.filter(date__gte=today).order_by('date')
    notifications = list(Notification.objects.filter(is_active=False))
    Notification.objects.filter(is_active=False).update(is_active=True)
    return render(request,'student/studenthome.html',{'events': events,'notifications': notifications})

def student_register(request):
    if request.method =='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        department=request.POST['department']
        semester=request.POST['semester']
        address=request.POST['address']
        phone=request.POST['phone']
        student_id=request.FILES['student_id']
        registration_no=request.POST['registration_no']
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')

            return render(request, 'common/student_registration.html', {
                'error': 'Username already exists'
            })

        s_user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password)
        s_user.save()
        students=Student.objects.create(user=s_user,department=department,semester=semester,address=address,phone=phone,student_id=student_id,registration_no=registration_no)
        students.save()
        students_obj,created=Group.objects.get_or_create(name='STUDENT')
        students_obj.user_set.add(s_user)
        messages.success(request,'student registration was successfull')
    return render(request,'common/student_registration.html')

def join_event(request, id):
    student = Student.objects.get(user=request.user)
    programme = Programme.objects.get(id=id)

    if request.method == 'POST':
        members = int(request.POST.get('members_count'))

        if members > programme.max_members or members < programme.min_members:
            messages.error(request, 'Members limit not allowed')
            return redirect('view_programmes', programme.event.id)

        ProgrammeParticipation.objects.create(
            programme=programme,
            student=student,
            team_name=request.POST.get('team_name'),
            song_name=request.POST.get('song_name'),
            members_count=members,
            status='Requested'
        )

        messages.success(request, 'Programme participation requested')
        return redirect('student_applications')

def student_applications(request):
    events = Event.objects.all()
    

    return render(
        request,
        'student/application_status.html',
        {'event': events}
    )


def view_events_for_students(request, id):
    event = get_object_or_404(Event, id=id)
    if event.date < timezone.now().date():
        raise Http404("Event expired")
    programmes = Programme.objects.filter(event=event)

    return render(
        request,
        'student/view_events_forstudents.html',
        {
            'event': event,
            'eventdata': programmes
        }
    )



def student_view_programmes(request, id):
    event = get_object_or_404(Event, id=id)
    student = Student.objects.get(user=request.user)

    programmes = Programme.objects.filter(event=event)

    
    for p in programmes:
        p.application = ProgrammeParticipation.objects.filter(programme=p, student=student).first()
    return render(
        request,
        'student/view_programmes.html',
        {
          'event': event,
        'programmes': programmes,
        }
    )


def view_application_detail(request,id):
    student = Student.objects.get(user=request.user)

    application = get_object_or_404(
        ProgrammeParticipation,
        id=id,
        student=student
    )


    return render(
        request,
        'student/view_application_detail.html',
        {'app': application}
    )




def create_group(request):
    current_student = Student.objects.get(user=request.user)

  
    students = Student.objects.exclude(id=current_student.id)

    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        member_ids = request.POST.getlist('members') 
        if CampusGroup.objects.filter(name=group_name).exists():
            messages.warning(request,'Group already exist, please choose another name...')
            return redirect('create_group')
         
        group = CampusGroup.objects.create(name=group_name)
        group.members.add(current_student)  

        for mid in member_ids:
            member = Student.objects.get(id=mid)
            group.members.add(member)

        group.save()
        return redirect('view_groups')  
    return render(request, 'student/create_group.html', {'students': students})


def view_groups(request):
    student = Student.objects.get(user=request.user)
    groups = CampusGroup.objects.filter(members=student)
    return render(request, 'student/view_groups.html', {'groups': groups})


def group_chat(request, id):
    student = Student.objects.get(user=request.user)
    group = CampusGroup.objects.get(id=id)
    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            GroupMessage.objects.create(
                group=group,
                sender=student,
                message=msg
            )
            return redirect('group_chat',id=id)

    return render(request, 'student/group_chat.html', {
        'group': group,
        'messages': messages
    })


def student_profile(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'student/profile.html', {'student': student})

def edit_student_profile(request):
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        student.department = request.POST.get('department')
        student.semester = request.POST.get('semester')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')
        student.registration_no = request.POST.get('registration_no')

        if 'student_id' in request.FILES:
            student.student_id = request.FILES['student_id']

        student.save()
        return redirect('student_profile')

    return render(request, 'student/edit_profile.html', {'student': student})






