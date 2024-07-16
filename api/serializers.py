from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=BatchModel
        fields="__all__"
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

    def validate_name(self, value):
        upper_value = value.title()
        if self.instance:
            # If updating, exclude the current instance from the duplicate check
            if TimingModel.objects.exclude(pk=self.instance.pk).filter(name=upper_value).exists():
                raise serializers.ValidationError("Period already exists")
        else:
            if TimingModel.objects.filter(name=upper_value).exists():
                raise serializers.ValidationError("Period already exists")
        return upper_value


    def validate(self, data):
        # Check if start time is before end time
        if data['start'] >= data['end']:
            raise serializers.ValidationError("Start time must be before end time.")

        # Check for overlapping periods
        if TimingModel.objects.exclude(pk=self.instance.pk if self.instance else None).filter(
                start__lt=data['end'], end__gt=data['start']).exists():
            raise serializers.ValidationError("This time period overlaps with an existing period.")
        
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
class AdminLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
