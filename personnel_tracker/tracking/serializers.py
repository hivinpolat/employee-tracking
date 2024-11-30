from rest_framework import serializers
from .models import CustomUser, Attendance, LeaveRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'annual_leave_balance']


class AttendanceSerializer(serializers.ModelSerializer):
    late_minutes = serializers.ReadOnlyField()  # Make this field read-only

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'date', 'check_in', 'check_out', 'late_minutes']


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'user', 'start_date', 'end_date', 'reason', 'approved']
