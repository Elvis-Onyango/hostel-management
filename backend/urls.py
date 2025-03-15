from django.urls import path
from .views import (
    HostelListView, HostelDetailView, HostelCreateView, HostelUpdateView, HostelDeleteView,
    BlockListView, BlockDetailView, BlockCreateView, BlockUpdateView, BlockDeleteView,
    WingListView, WingDetailView, WingCreateView, WingUpdateView, WingDeleteView,
    RoomListView, RoomDetailView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView,
    HousekeeperListView, HousekeeperDetailView, HousekeeperCreateView, HousekeeperUpdateView, HousekeeperDeleteView,
    CheckInListView, CheckInDetailView, CheckInCreateView, Landing,ComplaintDeleteView,
    ComplaintListView, ComplaintCreateView,student_dashboard,CheckInDeleteView,
    EmergencyListView, EmergencyCreateView,housekeeper_dashboard,ComplaintUpdateView,
    CheckInUpdateView,CustomLoginView,ComplaintDetailView,EmergencyDetailView,
    EmergencyUpdateView,EmergencyDeleteView, HousekeeperComplaintUpdateView
)



urlpatterns = [
    # Landing URLs
    path('',Landing.as_view(), name = 'home'),
    path('login/', CustomLoginView.as_view(), name='login'),

    # Hostel URLs
    path('hostels/', HostelListView.as_view(), name='hostel-list'),
    path('hostels/<int:pk>/', HostelDetailView.as_view(), name='hostel-detail'),
    path('hostels/new/', HostelCreateView.as_view(), name='hostel-create'),
    path('hostels/<int:pk>/update/', HostelUpdateView.as_view(), name='hostel-update'),
    path('hostels/<int:pk>/delete/', HostelDeleteView.as_view(), name='hostel-delete'),

    # Block URLs
    path('blocks/', BlockListView.as_view(), name='block-list'),
    path('blocks/<int:pk>/', BlockDetailView.as_view(), name='block-detail'),
    path('blocks/new/', BlockCreateView.as_view(), name='block-create'),
    path('blocks/<int:pk>/update/', BlockUpdateView.as_view(), name='block-update'),
    path('blocks/<int:pk>/delete/', BlockDeleteView.as_view(), name='block-delete'),

    # Wing URLs
    path('wings/', WingListView.as_view(), name='wing-list'),
    path('wings/<int:pk>/', WingDetailView.as_view(), name='wing-detail'),
    path('wings/new/', WingCreateView.as_view(), name='wing-create'),
    path('wings/<int:pk>/update/', WingUpdateView.as_view(), name='wing-update'),
    path('wings/<int:pk>/delete/', WingDeleteView.as_view(), name='wing-delete'),

    # Room URLs
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/new/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/<int:pk>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room-delete'),

    # Student URLs
    path('student-dashboard/', student_dashboard ,name = 'student-dashboard'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/new/', StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),

    # Housekeeper URLs
    path('housekeeper-dashboard/',housekeeper_dashboard, name= 'housekeeper-dashboard'),
    path('housekeepers/', HousekeeperListView.as_view(), name='housekeeper-list'),
    path('housekeepers/<int:pk>/', HousekeeperDetailView.as_view(), name='housekeeper-detail'),
    path('housekeepers/new/', HousekeeperCreateView.as_view(), name='housekeeper-create'),
    path('housekeepers/<int:pk>/update/', HousekeeperUpdateView.as_view(), name='housekeeper-update'),
    path('housekeepers/<int:pk>/delete/', HousekeeperDeleteView.as_view(), name='housekeeper-delete'),
    path('complaint/<int:pk>/update-status/', HousekeeperComplaintUpdateView.as_view(), name='housekeeper-complaint-update'),

    # CheckIn URLs
    path('checkins/', CheckInListView.as_view(), name='checkin-list'),
    path('checkins/<int:pk>/', CheckInDetailView.as_view(), name='checkin-detail'),
    path('checkins/new/', CheckInCreateView.as_view(), name='checkin-create'),
    path('checkin/<int:pk>/update', CheckInUpdateView.as_view(), name= 'checkin-update'),
    path('checkin/<int:pk>/delete', CheckInDeleteView.as_view(), name= 'checkin-delete'),

    # Complaint URLs
    path('complaints/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaints/new/', ComplaintCreateView.as_view(), name='complaint-create'),
    path('complaints/<int:pk>/', ComplaintDetailView.as_view(), name='complaint-detail'),
    path('complaints/<int:pk>/update',ComplaintUpdateView.as_view(), name= 'complaint-update'),
    path('complaints/<int:pk>/delete', ComplaintDeleteView.as_view(), name= 'complaint-delete'),


    # Emergency URLs
    path('emergencies/', EmergencyListView.as_view(), name='emergency-list'),
    path('emergencies/new/', EmergencyCreateView.as_view(), name='emergency-create'),
    path('emergency/<int:pk>/', EmergencyDetailView.as_view(), name='emergency-detail'),
    path('emergency/<int:pk>/update', EmergencyUpdateView.as_view(), name= 'emergency-update'),
    path('emergency/<int:pk>/delete', EmergencyDeleteView.as_view(), name= 'emergency-delete')
]
