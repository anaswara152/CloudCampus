from django.shortcuts import render,redirect,get_object_or_404
from .models import*
from django.contrib.auth.models import User,Group
from django.contrib import messages
from student.models import*
# Create your views here.
def manager_home(request):
    return render(request,'event/manager_home.html')

def eventmaneger_register(request):
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        department=request.POST['department']
        phone=request.POST['phone']
        semester=request.POST['semester']
        student_id=request.FILES['student_id']
        registration_no=request.POST['registration_no']
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return render(request, 'common/eventmanager_registration.html', {
                'error': 'Username already exists'
            })
        if User.objects.filter(email=email).exists():
            return render(request,'common/eventmanager_registration.html', {
                'error': 'Username already exists'})
        e_user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        e_user.save()
        evenet_manager=EventManager.objects.create(user=e_user,department=department,semester=semester,phone=phone,student_id=student_id,registration_no=registration_no)
        evenet_manager.save()
        evenet_manager_obj,created=Group.objects.get_or_create(name='EVENTMANAGER')
        evenet_manager_obj.user_set.add(e_user)
        messages.success(request,'Registration was successfull')
    return render(request,'common/eventmanager_registration.html')

def create_event(request):
    manager = EventManager.objects.get(user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        poster=request.FILES.get('poster')

        Event.objects.create(
            event_manager=manager,
            title=title,
            description=description,
            date=date,
            time=time,
            venue=venue,
            poster=poster
        )
        return redirect('view_events_for_manager')

    return render(request, 'event/create_event.html')


def view_events_for_manager(request):
    eventdata=Event.objects.all()
    return render(request,'event/view_events.html',{'edata':eventdata})


def edit_events(request,id):
    e=get_object_or_404(Event,id=id)
    manager = EventManager.objects.get(user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        e.event_manager=manager
        e.title=title
        e.description=description
        e.date=date
        e.time=time
        e.venue=venue
        if 'poster' in request.FILES:
            e.poster = request.FILES['poster']
        e.save()
        Notification.objects.create(
            title="Event Updated",
            message=f"The event '{e.title}' has been updated."
        )
        return redirect('view_events_for_manager')
    e=Event.objects.filter(id=id)
    return render(request,'event/edit_events.html',{'events':e})


def delete_events(request,id):
    Event.objects.filter(id=id).delete()
    return redirect('view_events_for_manager')
        



def create_programme(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        Programme.objects.create(
            event=event,
            name=request.POST.get('name'),
            programme_type=request.POST.get('programme_type'),
            min_members=request.POST.get('min_members'),
            max_members=request.POST.get('max_members'),
            allowed_song_type=request.POST.get('allowed_song_type'),
            time_limit=request.POST.get('time_limit')
        )
        return redirect('view_events_for_manager')

    return render(request, 'event/create_programme.html', {'event': event})


def view_event_participants(request):
    manager = EventManager.objects.get(user=request.user)

    events = Event.objects.filter(event_manager=manager).prefetch_related(
        'programme_set__programmeparticipation_set'
    )

    return render(request, 'event/view_participants.html', {
        'events': events
    })


def view_programmes(request):
    programme=Programme.objects.all()
    return render(request,'event/view_programme.html',{'p':programme})


def edit_programme(request, id):
    p = get_object_or_404(Programme, id=id)
    manager = EventManager.objects.get(user=request.user)
    
    if request.method == 'POST':
        p.name = request.POST.get('name')
        p.programme_type = request.POST.get('programme_type')
        p.min_members = request.POST.get('min_members')
        p.max_members = request.POST.get('max_members')
        p.allowed_song_type = request.POST.get('allowed_song_type')
        p.time_limit = request.POST.get('time_limit')
        p.save()
        Notification.objects.create(
        title="Programme Updated",
        message=f"The programme '{p.name}' under event '{p.event.title}' has been updated."
    )
        return redirect('view_programmes')

    return render(request, 'event/edit_programme.html', {'programme': p})


def delete_programme(request,id):
    Programme.objects.filter(id=id).delete()
    return redirect('view_programmes')

def accept_participants(request,id):
    ProgrammeParticipation.objects.filter(id=id).update(status='Accepted')
    return redirect('view_event_participants')

def reject_participants(request,id):
    ProgrammeParticipation.objects.filter(id=id).update(status='Rejected')
    return redirect('view_event_participants')