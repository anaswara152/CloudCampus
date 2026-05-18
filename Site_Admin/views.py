from django.shortcuts import render,redirect,get_object_or_404
from student.models import*
from event_manager.models import*
# Create your views here.
def adminhome(request):
    return render(request,'admin/adminhome.html')


def view_students(request):
    studentsdata = Student.objects.select_related('user').all()

   
    departments = Student.objects.values_list('department', flat=True).distinct()

    selected_department = request.GET.get('department')

    if selected_department:
        studentsdata = studentsdata.filter(department=selected_department)

    return render(request, 'admin/view_students.html', {
        'studentsdata': studentsdata,
        'departments': departments,
        'selected_department': selected_department
    })

def approve_students(request,id):
    Student.objects.filter(id=id).update(status='approved')
    return redirect('view_students')

def remove_students(request,id):
    Student.objects.filter(id=id).update(status='removed')
    return redirect('view_students')

def view_removed_students(request):
    rs=Student.objects.filter(id=id).update(status='removed')
    return render(request,'admin/removed_students.html',{'removeddata':rs})



def view_managers(request):
    managerdata=EventManager.objects.all()
    return render(request,'admin/view_manager.html',{'managerdata':managerdata})

def approve_manager(request,id):
    EventManager.objects.filter(id=id).update(status='approved')
    return redirect('view_managers')

def remove_manager(request,id):
    EventManager.objects.filter(id=id).update(status='removed')
    return redirect('view_managers')
def view_removed_managers(request):
    rm=EventManager.objects.filter(status='removed')
    return render(request,'admin/removed_managers.html',{'removeddatamanagers':rm})

def view_events_foradmin(request):
    eventsdata=Event.objects.all()
    return render(request,'admin/view_events_foradmin.html',{'eventdata':eventsdata})

def view_event_participants_admin(request,id):
    programme = get_object_or_404(Programme, id=id)

    participants = ProgrammeParticipation.objects.filter(
        programme=programme,
        status='Accepted'
    )

    return render(
        request,
        'admin/view_event_participants.html',
        {
            'programme': programme,
            'participants': participants
        }
    )

def view_programmes_admin(request, id):
    event = get_object_or_404(Event, id=id)
    programmes = Programme.objects.filter(event=event)

    return render(
        request,
        'admin/view_programmes_admin.html',
        {
            'event': event,
            'programmes': programmes
        }
    )


