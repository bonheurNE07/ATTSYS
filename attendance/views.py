from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import AttendanceRecord
from .forms import AttendanceRecordForm

# List view for attendance records
class AttendanceRecordListView(ListView):
    model = AttendanceRecord
    template_name = 'attendance/attendance_record_list.html'
    context_object_name = 'attendance_records'
    paginate_by = 10  # Add pagination, 10 records per page

    def get_queryset(self):
        # Customize the queryset to filter by user roles if needed
        return AttendanceRecord.objects.all().order_by('-date')
