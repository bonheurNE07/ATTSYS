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

class AttendanceRecordDetailView(DetailView):
    model = AttendanceRecord
    template_name = 'attendance/attendance_record_detail.html'
    context_object_name = 'attendance_record'


# Create view for a new attendance record
class AttendanceRecordCreateView(CreateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = 'attendance/attendance_record_form.html'
    success_url = reverse_lazy('attendance:attendance_record_list')  # Redirect to the list after creation

    def form_valid(self, form):
        return super().form_valid(form)
