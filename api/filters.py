import django_filters
from .models import *

class BatchFilter(django_filters.FilterSet):
    class Meta:
        model = BatchModel
        fields = '__all__'

class BranchFilter(django_filters.FilterSet):
    class Meta:
        model = BranchModel
        fields = '__all__'

class SectionFilter(django_filters.FilterSet):
    class Meta:
        model = SectionModel
        fields = '__all__'

class SemesterFilter(django_filters.FilterSet):
    class Meta:
        model = SemesterModels
        fields = '__all__'

class TimingFilter(django_filters.FilterSet):
    class Meta:
        model = TimingModel
        fields = '__all__'

class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = SubjectModel
        fields = '__all__'
class ImageFieldFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass
class StudentFilter(django_filters.FilterSet):
    profile = ImageFieldFilter(field_name='profile', lookup_expr='exact')
    class Meta:
        model = StudentModel
        fields ='__all__'
class FacultyFilter(django_filters.FilterSet):
    profile = ImageFieldFilter(field_name='profile', lookup_expr='exact')
    class Meta:
        model = FacultyModel
        fields ='__all__'
class AttendanceFilter(django_filters.FilterSet):
    student_status = django_filters.NumberFilter(field_name='student__status')
    date_range = django_filters.DateFromToRangeFilter(field_name='period__date')
    date = django_filters.DateFilter(field_name='period__date')
    section = django_filters.NumberFilter(field_name='period__section')
    semester = django_filters.NumberFilter(field_name='period__subject__semester')
    class Meta:
        model = AttendanceModel
        fields ='__all__'

# class PeriodFilter(django_filters.FilterSet):
#     class Meta:
#         model = PeriodModel
#         fields = '__all__'

class TimetableFilter(django_filters.FilterSet):
    subject_semester = django_filters.NumberFilter(field_name='subject__semester')
    date_range = django_filters.DateFromToRangeFilter(field_name='date')
    class Meta:
        model = TimetableModel
        fields = '__all__'
