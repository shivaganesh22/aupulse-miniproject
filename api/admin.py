from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(BatchModel)
admin.site.register(BranchModel)
admin.site.register(SectionModel)
admin.site.register(SemesterModels)

admin.site.register(StudentModel)
admin.site.register(FacultyModel)

admin.site.register(TimingModel)
admin.site.register(SubjectModel)
# admin.site.register(PeriodModel)
admin.site.register(TimetableModel)
admin.site.register(PasswordChange)
admin.site.register(AttendanceModel)