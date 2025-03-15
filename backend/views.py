from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import User, Hostel, Block, Wing, Room, Student, Housekeeper, CheckIn, Complaint, Emergency
from django.views import View
from django.shortcuts import render
from django.db.models import Count  
from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Student, Complaint, Emergency, CheckIn


User = get_user_model()

#=================LANDING PAGE=====================================================

class Landing(View):
	def get(self,request):
		return render(request,'index.html')


#========================LOGIN==========================================================




logger = logging.getLogger(__name__)

class CustomLoginView(FormView):
    template_name = 'login.html'  # Template for the login form
    form_class = AuthenticationForm  # Django's built-in login form
    success_url = reverse_lazy('home')  # Default redirect URL

    def form_valid(self, form):
        # Log the user in
        user = form.get_user()
        login(self.request, user)

        # Log the login attempt
        logger.info(f"User {user.username} logged in with role {user.role}")

        # Redirect based on user role
        if user.role == 'admin':
            return redirect(reverse_lazy('admin-dashboard'))
        elif user.role == 'student':
            return redirect(reverse_lazy('student-dashboard'))
        elif user.role == 'housekeeper':
            return redirect(reverse_lazy('housekeeper-dashboard'))
        else:
            logger.warning(f"Unknown role for user: {user.username}")
            return super().form_valid(form)  # Default redirect (landing page)




#=================================HOSTEL=======================================================



# Hostel List View
class HostelListView(LoginRequiredMixin, ListView):
    model = Hostel
    template_name = 'hostels.html'
    context_object_name = 'hostels'

# Hostel Detail View
class HostelDetailView(LoginRequiredMixin, DetailView):
    model = Hostel
    template_name = 'hostel_details.html'
    context_object_name = 'hostel'

# Hostel Create View
class HostelCreateView(LoginRequiredMixin, CreateView):
    model = Hostel
    template_name = 'hostel_create_update_form.html'
    fields = ['name', 'has_blocks', 'has_wings']
    success_url = reverse_lazy('hostel-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can create hostels
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to create a hostel.")
        return super().dispatch(request, *args, **kwargs)

# Hostel Update View
class HostelUpdateView(LoginRequiredMixin, UpdateView):
    model = Hostel
    template_name = 'hostel_create_update_form.html'
    fields = ['name', 'has_blocks', 'has_wings']
    success_url = reverse_lazy('hostel-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can update hostels
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to update a hostel.")
        return super().dispatch(request, *args, **kwargs)

# Hostel Delete View
class HostelDeleteView(LoginRequiredMixin, DeleteView):
    model = Hostel
    template_name = 'hostel_confirm_delete.html'
    success_url = reverse_lazy('hostel-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can delete hostels
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to delete a hostel.")
        return super().dispatch(request, *args, **kwargs)




#==========================BLOCK===============================================

# Block List View
class BlockListView(LoginRequiredMixin, ListView):
    model = Block
    template_name = 'blocks.html'
    context_object_name = 'blocks'

# Block Detail View
class BlockDetailView(LoginRequiredMixin, DetailView):
    model = Block
    template_name = 'block_details.html'
    context_object_name = 'block'

# Block Create View
class BlockCreateView(LoginRequiredMixin, CreateView):
    model = Block
    template_name = 'block_create_update_form.html'
    fields = ['hostel', 'name']
    success_url = reverse_lazy('block-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can create blocks
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to create a block.")
        return super().dispatch(request, *args, **kwargs)

# Block Update View
class BlockUpdateView(LoginRequiredMixin, UpdateView):
    model = Block
    template_name = 'block_create_update_form.html'
    fields = ['hostel', 'name']
    success_url = reverse_lazy('block-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can update blocks
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to update a block.")
        return super().dispatch(request, *args, **kwargs)

# Block Delete View
class BlockDeleteView(LoginRequiredMixin, DeleteView):
    model = Block
    template_name = 'block_confirm_delete.html'
    success_url = reverse_lazy('block-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can delete blocks
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to delete a block.")
        return super().dispatch(request, *args, **kwargs)
#============================WING===============================================================


# Wing List View
class WingListView(LoginRequiredMixin, ListView):
    model = Wing
    template_name = 'wings.html'
    context_object_name = 'wings'

# Wing Detail View
class WingDetailView(LoginRequiredMixin, DetailView):
    model = Wing
    template_name = 'wing_details.html'
    context_object_name = 'wing'

# Wing Create View
class WingCreateView(LoginRequiredMixin, CreateView):
    model = Wing
    template_name = 'wing_create_update_form.html'
    fields = ['hostel', 'name']
    success_url = reverse_lazy('wing-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can create wings
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to create a wing.")
        return super().dispatch(request, *args, **kwargs)

# Wing Update View
class WingUpdateView(LoginRequiredMixin, UpdateView):
    model = Wing
    template_name = 'wing_create_update_form.html'
    fields = ['hostel', 'name']
    success_url = reverse_lazy('wing-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can update wings
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to update a wing.")
        return super().dispatch(request, *args, **kwargs)

# Wing Delete View
class WingDeleteView(LoginRequiredMixin, DeleteView):
    model = Wing
    template_name = 'wing_confirm_delete.html'
    success_url = reverse_lazy('wing-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can delete wings
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to delete a wing.")
        return super().dispatch(request, *args, **kwargs)



#======================================ROOM==================================================

# Room List View
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'rooms.html'
    context_object_name = 'rooms'

# Room Detail View
class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'room_details.html'
    context_object_name = 'room'

# Room Create View
class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    template_name = 'room_create_update_form.html'
    fields = ['hostel', 'block', 'wing', 'number', 'capacity', 'occupied', 'room_type']
    success_url = reverse_lazy('room-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can create rooms
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to create a room.")
        return super().dispatch(request, *args, **kwargs)

# Room Update View
class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    template_name = 'room_create_update_form.html'
    fields = ['hostel', 'block', 'wing', 'number', 'capacity', 'occupied', 'room_type']
    success_url = reverse_lazy('room-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can update rooms
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to update a room.")
        return super().dispatch(request, *args, **kwargs)

# Room Delete View
class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can delete rooms
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to delete a room.")
        return super().dispatch(request, *args, **kwargs)

#==================================STUDENT=======================================================


# Student List View
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students.html'
    context_object_name = 'students'

# Student Detail View
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student_details.html'
    context_object_name = 'student'

# Student Create View
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'students_create_update_form.html'
    fields = ['user', 'registration_number', 'hostel', 'room']
    success_url = reverse_lazy('student-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can create students
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to create a student.")
        return super().dispatch(request, *args, **kwargs)

# Student Update View
class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'students_create_update_form.html'
    fields = ['user', 'registration_number', 'hostel', 'room']
    success_url = reverse_lazy('student-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can update students
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to update a student.")
        return super().dispatch(request, *args, **kwargs)

# Student Delete View
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('student-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can delete students
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to delete a student.")
        return super().dispatch(request, *args, **kwargs)



@login_required  # Ensure only logged-in users can access this view
def student_dashboard(request):
    # Ensure the user is a student
    if not hasattr(request.user, 'student'):
        return redirect('home')  # Redirect to landing page if the user is not a student

    # Get the logged-in student's data
    student = request.user.student
    user = student.user  # Access the associated User object

    # Filter complaints and emergencies using the User object
    complaints = Complaint.objects.filter(student=user)
    emergencies = Emergency.objects.filter(student=user)
    last_checkin = CheckIn.objects.filter(student=student).order_by('-timestamp').first()

    context = {
        'student': student,
        'checkin_status': last_checkin.checked_in if last_checkin else False,
        'last_checkin': last_checkin,
        'complaints': complaints,
        'emergencies': emergencies,
        'pending_complaints_count': complaints.filter(status='pending').count(),
        'resolved_complaints_count': complaints.filter(status='resolved').count(),
        'emergency_types': list(emergencies.values_list('emergency_type', flat=True).distinct()),
        'emergency_counts': list(emergencies.values('emergency_type').annotate(count=Count('id')).values_list('count', flat=True)),
    }
    return render(request, 'student_dashboard.html', context)


#============================HOUSEKEEPER==========================================

# Housekeeper List View
class HousekeeperListView(LoginRequiredMixin, ListView):
    model = Housekeeper
    template_name = 'housekepers.html'
    context_object_name = 'housekeepers'

# Housekeeper Detail View
class HousekeeperDetailView(LoginRequiredMixin, DetailView):
    model = Housekeeper
    template_name = 'housekeeper_details.html'
    context_object_name = 'housekeeper'

# Housekeeper Create View
class HousekeeperCreateView(LoginRequiredMixin, CreateView):
    model = Housekeeper
    template_name = 'housekeeper_create_update_form.html'
    fields = ['user', 'hostel', 'block', 'wing']
    success_url = reverse_lazy('housekeeper-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins can create housekeepers
        if request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to create a housekeeper.")
        return super().dispatch(request, *args, **kwargs)

# Housekeeper Update View
class HousekeeperUpdateView(LoginRequiredMixin, UpdateView):
    model = Housekeeper
    template_name = 'housekeeper_create_update_form.html'
    fields = ['user', 'hostel', 'block', 'wing']
    success_url = reverse_lazy('housekeeper-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins can update housekeepers
        if request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to update a housekeeper.")
        return super().dispatch(request, *args, **kwargs)

# Housekeeper Delete View
class HousekeeperDeleteView(LoginRequiredMixin, DeleteView):
    model = Housekeeper
    template_name = 'housekeeper_confirm_delete.html'
    success_url = reverse_lazy('housekeeper-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins can delete housekeepers
        if request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to delete a housekeeper.")
        return super().dispatch(request, *args, **kwargs)



from django.db.models import Count, Sum
from django.core.paginator import Paginator
from django.core.cache import cache


def housekeeper_dashboard(request):
    # Role-based permission check
    if request.user.role != 'housekeeper':
        raise PermissionDenied("You do not have permission to access this page.")

    # Cache expensive queries
    students_count = cache.get('students_count')
    if not students_count:
        students_count = Student.objects.count()
        cache.set('students_count', students_count, timeout=60 * 15)  # Cache for 15 minutes

    hostels_count = cache.get('hostels_count')
    if not hostels_count:
        hostels_count = Hostel.objects.count()
        cache.set('hostels_count', hostels_count, timeout=60 * 15)

    complaints_count = cache.get('complaints_count')
    if not complaints_count:
        complaints_count = Complaint.objects.count()
        cache.set('complaints_count', complaints_count, timeout=60 * 15)

    emergencies_count = cache.get('emergencies_count')
    if not emergencies_count:
        emergencies_count = Emergency.objects.count()
        cache.set('emergencies_count', emergencies_count, timeout=60 * 15)

    wings_count = cache.get('wings_count')
    if not wings_count:
        wings_count = Wing.objects.count()
        cache.set('wings_count', wings_count, timeout=60 * 15)

    blocks_count = cache.get('blocks_count')
    if not blocks_count:
        blocks_count = Block.objects.count()
        cache.set('blocks_count', blocks_count, timeout=60 * 15)

    pending_complaints_count = cache.get('pending_complaints_count')
    if not pending_complaints_count:
        pending_complaints_count = Complaint.objects.filter(status='pending').count()
        cache.set('pending_complaints_count', pending_complaints_count, timeout=60 * 15)

    resolved_complaints_count = cache.get('resolved_complaints_count')
    if not resolved_complaints_count:
        resolved_complaints_count = Complaint.objects.filter(status='resolved').count()
        cache.set('resolved_complaints_count', resolved_complaints_count, timeout=60 * 15)

    # Hostel data
    hostel_names = list(Hostel.objects.values_list('name', flat=True))
    hostel_occupancy = list(Hostel.objects.annotate(
        occupancy=Sum('rooms__occupied')
    ).values_list('occupancy', flat=True))

    # Paginate students and rooms
    students = Student.objects.select_related('user', 'hostel', 'room').all()
    paginator_students = Paginator(students, 20)  # Show 20 students per page
    page_number_students = request.GET.get('page_students')
    page_obj_students = paginator_students.get_page(page_number_students)

    rooms = Room.objects.select_related('hostel', 'block', 'wing').all()
    paginator_rooms = Paginator(rooms, 20)  # Show 20 rooms per page
    page_number_rooms = request.GET.get('page_rooms')
    page_obj_rooms = paginator_rooms.get_page(page_number_rooms)

    context = {
        'students_count': students_count,
        'hostels_count': hostels_count,
        'complaints_count': complaints_count,
        'emergencies_count': emergencies_count,
        'wings_count': wings_count,
        'blocks_count': blocks_count,
        'pending_complaints_count': pending_complaints_count,
        'resolved_complaints_count': resolved_complaints_count,
        'hostel_names': hostel_names,
        'hostel_occupancy': hostel_occupancy,
        'students': page_obj_students,
        'rooms': page_obj_rooms,
    }
    return render(request, 'housekeeper_dashboard.html', context)


    #============================CHECKIN=====================================

# CheckIn List View
class CheckInListView(LoginRequiredMixin, ListView):
    model = CheckIn
    template_name = 'checkins.html'
    context_object_name = 'checkins'

# CheckIn Detail View
class CheckInDetailView(LoginRequiredMixin, DetailView):
    model = CheckIn
    template_name = 'checkin_details.html'
    context_object_name = 'checkin'

# CheckIn Create View
class CheckInCreateView(LoginRequiredMixin, CreateView):
    model = CheckIn
    template_name = 'checkin_create_update.html'
    fields = ['student', 'room', 'checked_in']
    success_url = reverse_lazy('checkin-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can create check-ins
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to create a check-in.")
        return super().dispatch(request, *args, **kwargs)

# CheckIn Update View
class CheckInUpdateView(LoginRequiredMixin, UpdateView):
    model = CheckIn
    template_name = 'checkin_create_update.html'
    fields = ['student', 'room', 'checked_in']
    success_url = reverse_lazy('checkin-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can update check-ins
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to update a check-in.")
        return super().dispatch(request, *args, **kwargs)

# CheckIn Delete View
class CheckInDeleteView(LoginRequiredMixin, DeleteView):
    model = CheckIn
    template_name = 'checkin_confirm_delete.html'
    success_url = reverse_lazy('checkin-list')

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can delete check-ins
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to delete a check-in.")
        return super().dispatch(request, *args, **kwargs)  


#===========================COMPLAINT=============================


class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaints.html'
    context_object_name = 'complaints'

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    template_name = 'complaints_create_update_form.html'
    fields = ['description']  # Only show the description field
    success_url = reverse_lazy('complaint-list')

    def form_valid(self, form):
        if not hasattr(self.request.user, 'student'):
            raise ValueError("The logged-in user does not have an associated Student instance.")
        form.instance.student = self.request.user
        return super().form_valid(form)

class ComplaintUpdateView(LoginRequiredMixin, UpdateView):
    model = Complaint
    template_name = 'complaints_create_update_form.html'
    fields = ['description']  # Only show the description field
    success_url = reverse_lazy('complaint-list')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'student') or self.get_object().student != request.user.student:
            raise PermissionDenied("You do not have permission to update this complaint.")
        return super().dispatch(request, *args, **kwargs)

class ComplaintDetailView(LoginRequiredMixin, DetailView):
    model = Complaint
    template_name = 'complaints_details.html'
    context_object_name = 'complaint'

class ComplaintDeleteView(LoginRequiredMixin, DeleteView):
    model = Complaint
    template_name = 'emergency_confirm_delete.html'
    success_url = reverse_lazy('complaint-list')

class HousekeeperComplaintUpdateView(LoginRequiredMixin, UpdateView):
    model = Complaint
    template_name = 'housekeeper_complaint_update.html'
    fields = ['status']  # Only allow updating the status
    success_url = reverse_lazy('complaint-list')


    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in ['housekeeper', 'admin']:
            raise PermissionDenied("You do not have permission to update the status of this complaint.")
        return super().dispatch(request, *args, **kwargs)




#================================EMMERGENCY=============================================


class EmergencyListView(LoginRequiredMixin, ListView):
    model = Emergency
    template_name = 'emergencies.html'
    context_object_name = 'emergencies'

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can view the emergency list
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)



class EmergencyCreateView(LoginRequiredMixin, CreateView):
    model = Emergency
    template_name = 'emergency_create_update.html'
    fields = ['emergency_type', 'details']  # Exclude student field from the form
    success_url = reverse_lazy('student-dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create an emergency.")

        if request.user.role != 'student':
            raise PermissionDenied("You do not have permission to create an emergency.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.request.user  # Assign the logged-in user to the student field
        return super().form_valid(form)

    

class EmergencyDetailView(LoginRequiredMixin, DetailView):
    model = Emergency
    template_name = 'emergency_details.html'
    context_object_name = 'emergency'

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can view emergency details
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

class EmergencyUpdateView(LoginRequiredMixin, UpdateView):
    model = Emergency
    template_name = 'emergency_create_update.html'
    fields = ['status']  # Only allow updating the status

    def dispatch(self, request, *args, **kwargs):
        # Only admins and housekeepers can update the status
        if request.user.role not in ['admin', 'housekeeper']:
            raise PermissionDenied("You do not have permission to update this emergency.")
        return super().dispatch(request, *args, **kwargs)

class EmergencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Emergency
    template_name = 'emergency_confirm_delete.html'
    success_url = reverse_lazy('emergency-list')

    def dispatch(self, request, *args, **kwargs):
        # No one can delete emergencies
        raise PermissionDenied("You do not have permission to delete this emergency.")