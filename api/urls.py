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
router.register('period', PeriodView)
router.register('timetable', TimetableView)

urlpatterns = [
    path('', include(router.urls)),
    path('student/',CreateStudentView.as_view()),
    path('student/<int:id>/',UpdateStudentView.as_view()),
    path('faculty/',CreateFacultyView.as_view()),
    path('faculty/<int:id>/',UpdateFacultyView.as_view()),
]
