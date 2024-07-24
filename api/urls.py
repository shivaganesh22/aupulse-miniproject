from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import *
router = DefaultRouter()
router.register('batch', BatchView)
router.register('branch', BranchView)
router.register('section', SectionView)
router.register('semester', SemesterView)
router.register('timing', TimingView)
router.register('subject', SubjectView)
# router.register('period', PeriodView)
router.register('timetable', TimetableView)
router.register('timetabledisplay', TimetableDisplay,basename='timetabledisplay')
router.register('attendancedisplay', AttendanceDisplay,basename='attendancedisplay')

urlpatterns = [
    path('', include(router.urls)),
    path('student/',CreateStudentView.as_view()),
    path('student/<int:id>/',UpdateStudentView.as_view()),
    path('faculty/',CreateFacultyView.as_view()),
    path('faculty/<int:id>/',UpdateFacultyView.as_view()),
    path('login/admin/',AdminLoginView.as_view()),
    path('password/change/',ChangePasswordView.as_view()),
    path('password/reset/',ForgotPasswordView.as_view()),
    path('attendance/',AttendanceView.as_view()),
]
