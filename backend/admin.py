from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Hostel, Block, Wing, Room, Student, Housekeeper, CheckIn, Complaint, Emergency, User

# Custom admin display for User model
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Roles & Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)

# Inline for Block and Wing in HostelAdmin
class BlockInline(admin.TabularInline):
    model = Block
    extra = 1  # Number of empty forms to display

class WingInline(admin.TabularInline):
    model = Wing
    extra = 1

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_blocks', 'has_wings')
    search_fields = ('name',)
    list_filter = ('has_blocks', 'has_wings')
    inlines = [BlockInline, WingInline]  # Add inline editing for blocks and wings

# Inline for Room in BlockAdmin and WingAdmin
class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostel')
    search_fields = ('name', 'hostel__name')
    inlines = [RoomInline]  # Add inline editing for rooms

@admin.register(Wing)
class WingAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostel')
    search_fields = ('name', 'hostel__name')
    inlines = [RoomInline]  # Add inline editing for rooms

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'hostel', 'block', 'wing', 'capacity', 'occupied', 'room_type')
    list_filter = ('hostel', 'block', 'wing', 'room_type')
    search_fields = ('number', 'hostel__name', 'block__name', 'wing__name')
    actions = ['mark_as_fully_occupied']

    def mark_as_fully_occupied(self, request, queryset):
        # Custom admin action to mark selected rooms as fully occupied
        queryset.update(occupied=models.F('capacity'))
    mark_as_fully_occupied.short_description = "Mark selected rooms as fully occupied"

# Custom Inline for CheckIn in StudentAdmin
class CheckInInline(admin.TabularInline):
    model = CheckIn
    extra = 1
    fk_name = 'student'  # Specify the ForeignKey field name

    def get_queryset(self, request):
        # Filter CheckIn instances based on the Student's user field
        qs = super().get_queryset(request)
        if hasattr(request, '_obj_'):
            student = request._obj_
            return qs.filter(student=student.user)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limit the student field to the current student's user
        if db_field.name == "student" and hasattr(request, '_obj_'):
            student = request._obj_
            kwargs["queryset"] = User.objects.filter(id=student.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_number', 'hostel', 'room')
    search_fields = ('user__username', 'registration_number')
    list_filter = ('hostel',)
    inlines = [CheckInInline]  # Add inline editing for check-ins

    def get_inline_instances(self, request, obj=None):
        # Pass the current student object to the inline
        if obj:
            request._obj_ = obj
        return super().get_inline_instances(request, obj)

@admin.register(Housekeeper)
class HousekeeperAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostel', 'block', 'wing')
    search_fields = ('user__username', 'hostel__name', 'block__name', 'wing__name')
    list_filter = ('hostel',)

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'checked_in', 'timestamp')
    search_fields = ('student__username', 'room__number')
    list_filter = ('checked_in', 'timestamp')
    date_hierarchy = 'timestamp'  # Add a date-based hierarchy filter

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('student', 'description', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('student__username', 'description')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        # Custom admin action to mark selected complaints as resolved
        queryset.update(status='resolved')
    mark_as_resolved.short_description = "Mark selected complaints as resolved"

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('student', 'emergency_type', 'details', 'timestamp')
    search_fields = ('student__username', 'emergency_type', 'details')
    list_filter = ('emergency_type', 'timestamp')
    date_hierarchy = 'timestamp'  # Add a date-based hierarchy filter