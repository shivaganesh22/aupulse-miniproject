from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from datetime import datetime, timedelta
from .serializers import *
from django.contrib.auth import authenticate
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
#Classes
class BatchView(viewsets.ModelViewSet):
    queryset = BatchModel.objects.all()
    serializer_class = BatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BatchFilter

class BranchView(viewsets.ModelViewSet):
    queryset = BranchModel.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BranchFilter

class SectionView(viewsets.ModelViewSet):
    queryset = SectionModel.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionFilter

class SemesterView(viewsets.ModelViewSet):
    queryset = SemesterModels.objects.all()
    serializer_class = SemesterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SemesterFilter

class TimingView(viewsets.ModelViewSet):
    queryset = TimingModel.objects.all()
    serializer_class = TimingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimingFilter

class SubjectView(viewsets.ModelViewSet):
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter

# class PeriodView(viewsets.ModelViewSet):
#     queryset = PeriodModel.objects.all()
#     serializer_class = PeriodSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = PeriodFilter
class TimetableDisplay(viewsets.ModelViewSet):
    queryset = TimetableModel.objects.all()
    serializer_class = TimetableDisplaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimetableFilter
    
class TimetableView(viewsets.ModelViewSet):
    queryset = TimetableModel.objects.all()
    serializer_class = TimetableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimetableFilter

    def create(self, request, *args, **kwargs):
        add_every_week = request.data.get('add_every_week', False)
        till_date = request.data.get('till_date', None)
        date = request.data.get('date', None)

        if add_every_week and till_date and date:
            try:
                till_date = datetime.strptime(till_date, '%Y-%m-%d').date()
                date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

            current_date = date
            while current_date <= till_date:
                # Create timetable instance for each week until till_date
                timetable_data = request.data.copy()
                timetable_data['date'] = current_date.strftime('%Y-%m-%d')
                serializer = self.get_serializer(data=timetable_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                current_date += timedelta(days=7)  # Move to the next week
            
            return Response({'message': 'Timetables created successfully.'}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
class CreateStudentView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    def post(self, request):
        user_serializer=UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user=user_serializer.save()
            student_data = request.data.copy()  
            student_data['user'] = user.id
            serializer = StudentSerializer(data=student_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                user.delete()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        serializer=StudentSerializer(StudentModel.objects.all(),many=True)
        return Response(serializer.data)
class UpdateStudentView(APIView):
    def post(self, request, id):
        try:
            student = StudentModel.objects.get(id=id)
        except StudentModel.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update only specific fields
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, id):
        try:
            student = StudentSerializer(StudentModel.objects.get(id=id))
            return Response(student.data, status=status.HTTP_200_OK)
        except StudentModel.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        try:
            std=StudentModel.objects.get(id=id)
            user = User.objects.get(id=std.user.id)
            user.delete()
            return Response({"msg":"Deleted"}, status=status.HTTP_200_OK)
        except StudentModel.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
    
class CreateFacultyView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = FacultyFilter
    def post(self, request):
        user_serializer=UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user=user_serializer.save()
            student_data = request.data.copy()  
            student_data['user'] = user.id
            serializer = FacultySerializer(data=student_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            user.delete()
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        serializer=FacultySerializer(FacultyModel.objects.all(),many=True)
        return Response(serializer.data)
class UpdateFacultyView(APIView):
    def post(self, request, id):
        try:
            faculty = FacultyModel.objects.get(id=id)
        except FacultyModel.DoesNotExist:
            return Response({'error': 'Faculty not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update only specific fields
        serializer = FacultySerializer(faculty, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, id):
        try:
            faculty = FacultySerializer(FacultyModel.objects.get(id=id))
            return Response(faculty.data, status=status.HTTP_200_OK)
        except FacultyModel.DoesNotExist:
            return Response({'error': 'Faculty not found.'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, id):
        try:
            std=FacultyModel.objects.get(id=id)
            user = User.objects.get(id=std.user.id)
            user.delete()
            return Response({"msg":"Deleted"}, status=status.HTTP_200_OK)
        except StudentModel.DoesNotExist:
            return Response({'error': 'Faculty not found.'}, status=status.HTTP_404_NOT_FOUND)
from rest_framework import serializers
class AdminLoginView(APIView):
    def post(self,request):
        serializer=AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user=authenticate(username=serializer.data["username"].upper(),password=serializer.data["password"])
            if user is not None and user.is_superuser:
                token,created=Token.objects.get_or_create(user=user)
                return Response({"token":token.key})
            else :
                raise serializers.ValidationError({"error":"Invalid Credentials"})
        else:
            return  Response({"error":"Enter valid details"}, status=status.HTTP_404_NOT_FOUND)
import uuid
from django.core.mail import send_mail
def sendMail(subject,message,email):
    send_mail(subject,message,'aupulse@gmail.com',email)
class ForgotPasswordView(APIView):
    def post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user=User.objects.get(username=serializer.data["username"].upper())
                token=uuid.uuid4()
                PasswordChange.objects.filter(user=user).delete()
                sendMail("Password Reset",f"Dear {user.username} click below link to reset password\nhttps://aupulse-api.vercel.app/resetpassword/?token={token}",[user.email])
                PasswordChange(user=user,token=token).save()
                return Response({"msg":"Mail sent"},status=status.HTTP_200_OK)
            except:
                return Response({"error":"No user exists with username"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return  Response({"error":"Enter valid details"}, status=status.HTTP_404_NOT_FOUND)
class ChangePasswordView(APIView):
    authentication_classes=[TokenAuthentication]
    def get(self,r):
        user=r.auth.user
        token=uuid.uuid4()
        PasswordChange.objects.filter(user=user).delete()
        sendMail("Password Reset",f"Dear {user.username} click below link to reset password\nhttps://aupulse-api.vercel.app/resetpassword/?token={token}",[user.email])
        PasswordChange(user=user,token=token).save()
        return Response({"msg":"Mail sent"},status=status.HTTP_200_OK)
