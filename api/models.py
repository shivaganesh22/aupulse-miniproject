from django.db import models,IntegrityError
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
# Create your models here.
class BatchModel(models.Model):
    start = models.DateField()
    end = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start} - {self.end}"
    class Meta:
        unique_together = ('start', 'end')
class BranchModel(models.Model):
    batch = models.ForeignKey(BatchModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.batch} *** {self.name}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['batch', 'name'], name='unique_branch_name')
        ]

class SectionModel(models.Model):
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.branch} - {self.name}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['branch', 'name'], name='unique_section_name')
        ]

class SemesterModels(models.Model):
    batch = models.ForeignKey(BatchModel, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.batch} ----- {self.year} - {self.semester}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['batch', 'year', 'semester'], name='unique_batch_year_semester')
        ]
class StudentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    section=models.ForeignKey(SectionModel,on_delete=models.CASCADE)
    hall_ticket=models.CharField(max_length=10,unique=True)
    date_of_birth=models.DateField(null=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    mother_name=models.CharField(max_length=100,null=True,blank=True)
    profile=models.ImageField(upload_to='profiles/students')
    address=models.TextField(null=True,blank=True)
    phone_number=models.CharField(max_length=10)
    parent_phone_number=models.CharField(max_length=10)
    status=models.BooleanField(default=True)
    def __str__(self):
        return self.hall_ticket+" *** "+self.first_name
class FacultyModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date_of_birth=models.DateField(null=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    profile=models.ImageField(upload_to='profiles/faculty',null=True)
    phone_number=models.CharField(max_length=10)
    # email=models.EmailField()
    department=models.CharField(max_length=50)
    status=models.BooleanField(default=True)
    def __str__(self):
        return self.user.username+" *** "+self.user.email
class TimingModel(models.Model):
    name=models.CharField(max_length=10)
    batch=models.ForeignKey(BatchModel,on_delete=models.CASCADE)
    start=models.TimeField()
    end=models.TimeField()
    def __str__(self):
        return self.name+"  "+str(self.start)+'-'+str(self.end)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'batch'], name='unique_name_per_batch'),
            UniqueConstraint(fields=['start', 'end', 'batch'], name='unique_time_slot_per_batch')
        ]

class SubjectModel(models.Model):
    semester=models.ForeignKey(SemesterModels,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    branch=models.ForeignKey(BranchModel,on_delete=models.CASCADE)
    is_lab=models.BooleanField(default=False)
    def __str__(self):
        return str (self.semester)+" **** "+str(self.name)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['name','is_lab', 'semester'], name='unique_branch_name_semester')
        ]
# class PeriodModel(models.Model):
#     section=models.ForeignKey(SectionModel,on_delete=models.CASCADE)
#     subject=models.ForeignKey(SubjectModel,on_delete=models.CASCADE)
#     faculty=models.ForeignKey(FacultyModel,on_delete=models.CASCADE)
#     def __str__ (self):
#         return str(self.section)+" *** "+str(self.subject)+' *** '+str(self.faculty)
class TimetableModel(models.Model):
    section=models.ForeignKey(SectionModel,on_delete=models.CASCADE)
    timing=models.ForeignKey(TimingModel,on_delete=models.CASCADE)
    subject=models.ForeignKey(SubjectModel,on_delete=models.CASCADE)
    faculty=models.ForeignKey(FacultyModel,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    date=models.DateField()
    def __str__(self):
        return str(self.section)+" *** "+str(self.timing)+' *** '+str(self.subject)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['timing', 'section','date','subject'], name='unique_timing_date_period')
        ]
class PasswordChange(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return str(self.user)+ "  "+self.token
class AttendanceModel(models.Model):
    student=models.ForeignKey(StudentModel,on_delete=models.CASCADE)
    period=models.ForeignKey(TimetableModel,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    def __str__(self) :
        return str(self.student)+ "  "+str(self.period)+" "+str(self.status)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['student', 'period'], name='unique_period_student')
        ]