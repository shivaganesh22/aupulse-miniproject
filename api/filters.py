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

# class PeriodFilter(django_filters.FilterSet):
#     class Meta:
#         model = PeriodModel
#         fields = '__all__'

class TimetableFilter(django_filters.FilterSet):
    subject_semester = django_filters.NumberFilter(field_name='subject__semester')
    class Meta:
        model = TimetableModel
        fields = '__all__'
