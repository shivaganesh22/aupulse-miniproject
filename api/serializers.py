from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=BatchModel
        fields="__all__"
    def validate(self, data):
        # Check if start time is before end time
        if data['start'] >= data['end']:
            raise serializers.ValidationError("Start date must be before end date.")
        return data
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model=BranchModel
        fields="__all__"
    def validate_name(self, value):
        upper_value = value.upper()
        return upper_value
    
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=SectionModel
        fields="__all__"
    def validate_name(self, value):
        upper_value = value.upper()
        return upper_value

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model=SemesterModels
        fields="__all__"

class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingModel
        fields = "__all__"
    def validate_name(self,value):
        return value.title()
    def validate(self, data):
        # Check if start time is before end time
        if data['start'] >= data['end']:
            raise serializers.ValidationError("Start time must be before end time.")

        # Check for unique name within the same batch
        name = data.get('name')
        batch = data.get('batch')
        # if self.instance:
        #     # If updating, exclude the current instance from the duplicate check
        #     if TimingModel.objects.exclude(pk=self.instance.pk).filter(name=name, batch=batch).exists():
        #         raise serializers.ValidationError("Period name already exists for this batch.")
        # else:
        #     if TimingModel.objects.filter(name=name, batch=batch).exists():
        #         raise serializers.ValidationError("Period name already exists for this batch.")

        # Check for overlapping periods within the same batch
        if TimingModel.objects.exclude(pk=self.instance.pk if self.instance else None).filter(
                batch=batch, start__lt=data['end'], end__gt=data['start']).exists():
            raise serializers.ValidationError("This time period overlaps with an existing period for this batch.")

        return data
    
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubjectModel
        fields="__all__"
    def validate_name(self, value):
        upper_value = value.title()
        return upper_value
# class PeriodSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=PeriodModel
#         fields="__all__"
class TimetableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=TimetableModel
        fields="__all__"




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        normalized_email = value.lower()
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return normalized_email
    def validate_username(self, value):
        normalized_email = value.upper()
        if User.objects.filter(username=normalized_email).exists():
            raise serializers.ValidationError("This username is already in use.")
        return normalized_email

    def create(self, validated_data):
        validated_data['username'] = validated_data['username'].upper()
        validated_data['email'] = validated_data['email'].lower()
        user = User.objects.create_user(**validated_data)
        return user
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'
    def validate_hall_ticket(self, value):
        upper_value = value.upper()
        if self.instance:
            # If updating, exclude the current instance from the duplicate check
            if StudentModel.objects.exclude(pk=self.instance.pk).filter(hall_ticket=upper_value).exists():
                raise serializers.ValidationError("Student with this hall ticket already exists")
        else:
            if StudentModel.objects.filter(hall_ticket=upper_value).exists():
                raise serializers.ValidationError("Student with this hall ticket already exists")
        return upper_value
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyModel
        fields ='__all__'
class TimetableDisplaySerializer(serializers.ModelSerializer):
    timing=TimingSerializer()
    subject=SubjectSerializer()
    faculty=FacultySerializer()
    class Meta:
        model=TimetableModel
        fields="__all__"
class AdminLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    username=serializers.CharField()
from datetime import date
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceModel
        fields = '__all__'
    def validate(self, data):
        period = data.get('period')
        if self.instance is None:
            if period.status:
                raise serializers.ValidationError("Attendance already taken for this period.")
        if period.date > date.today():
            raise serializers.ValidationError("Period date cannot be in the future.")
        return data
class AttendanceDisplaySerializer(serializers.ModelSerializer):
    student=StudentSerializer()
    period=TimetableDisplaySerializer()
   
    class Meta:
        model=AttendanceModel
        fields="__all__"