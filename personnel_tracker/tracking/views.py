from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .models import Attendance
from .serializers import UserSerializer, AttendanceSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LeaveRequest, CustomUser
from .serializers import LeaveRequestSerializer
from rest_framework.permissions import IsAuthenticated


# Personel Login
class UserLoginViewSet(viewsets.ViewSet):
    """
    Personelin giriş yapabilmesi için API endpoint.
    """

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        """
        Kullanıcı giriş işlemini gerçekleştirir.
        - Yetkili olmayan kullanıcılar giriş yapabilir.
        """
        username = request.data.get("username")  # Kullanıcı adını al
        password = request.data.get("password")  # Şifreyi al
        user = authenticate(request, username=username, password=password)  # Kullanıcı doğrulama

        if user is not None:
            # Kullanıcı 'Yetkili' grubunda değilse giriş yapabilir
            if not user.groups.filter(name="Yetkili").exists():
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Yetkili Login
class YetkiliLoginViewSet(viewsets.ViewSet):
    """
    Yetkili personelin giriş yapabilmesi için API endpoint.
    """

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        """
        Yetkili giriş işlemini gerçekleştirir.
        - Sadece 'Yetkili' grubundaki kullanıcılar giriş yapabilir.
        """
        username = request.data.get("username")  # Kullanıcı adını al
        password = request.data.get("password")  # Şifreyi al
        user = authenticate(request, username=username, password=password)  # Kullanıcı doğrulama

        if user is not None:
            # Kullanıcı 'Yetkili' grubundaysa giriş yapabilir
            if user.groups.filter(name="Yetkili").exists():
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Personel Logout
def user_logout(request):
    """
    Kullanıcı çıkış yapar ve API ana sayfasına yönlendirilir.
    """
    logout(request)
    return redirect("/api")


# Kullanıcı ViewSet
class UserViewSet(viewsets.ModelViewSet):
    """
    Tüm kullanıcıları listelemek ve yönetmek için ViewSet.
    """
    queryset = CustomUser.objects.all()  # Tüm kullanıcıları al
    serializer_class = UserSerializer  # Kullanıcılar için serializer


# Giriş-Çıkış Takibi ViewSet
class AttendanceViewSet(viewsets.ModelViewSet):
    """
    Giriş-çıkış kayıtlarını görüntülemek ve yönetmek için ViewSet.
    """
    permission_classes = [IsAuthenticated]  # Sadece giriş yapmış kullanıcılar erişebilir
    queryset = Attendance.objects.all()  # Varsayılan olarak tüm kayıtları al
    serializer_class = AttendanceSerializer  # Attendance için serializer

    def list(self, request):
        """
        Giriş-çıkış kayıtlarını listeler.
        - Admin tüm kayıtları görebilir.
        - Diğer kullanıcılar sadece kendi kayıtlarını görebilir.
        """
        # Kullanıcı admin ise tüm kayıtları görür
        if request.user.is_staff:
            attendance_data = Attendance.objects.all()
        else:
            # Kullanıcı kendi kayıtlarını görür
            attendance_data = Attendance.objects.filter(user=request.user)

        attendance_report = []

        # Kayıtları rapor formatına dönüştür
        for attendance in attendance_data:
            attendance_report.append({
                'user': attendance.user.username,
                'date': attendance.date,
                'late': attendance.is_late(),
            })

        return Response(attendance_report, status=status.HTTP_200_OK)


# İzin Talepleri ViewSet
class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    İzin taleplerini yönetmek için ViewSet.
    """
    queryset = LeaveRequest.objects.all()  # Tüm izin taleplerini al
    serializer_class = LeaveRequestSerializer  # LeaveRequest için serializer


# İzin Taleplerini Onaylama/Red ViewSet
class LeaveRequestApprovalViewSet(viewsets.ViewSet):
    """
    Yetkili personelin izin taleplerini onaylayıp reddedebileceği API endpoint.
    """
    permission_classes = [IsAuthenticated]  # Sadece giriş yapmış kullanıcılar erişebilir

    @action(detail=True, methods=["post"], url_path="approve_or_reject_leave")
    def approve_or_reject_leave(self, request, pk=None):
        """
        İzin taleplerini onaylamak veya reddetmek için bir işlem.
        - Talep ID'sine göre işlem yapılır.
        - 'approve' ya da 'reject' işlemleri desteklenir.
        """
        user = request.user

        # Yetkili grubu kontrolü (gerekirse bu kısım aktif edilebilir)
        # if not user.groups.filter(name="Yetkili").exists():
        #     return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

        # Talep ID'sine göre izin talebini getir
        try:
            leave_request = LeaveRequest.objects.get(id=pk)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "Leave request not found"}, status=status.HTTP_404_NOT_FOUND)

        # İstekten eylemi al (approve/reject)
        action = request.data.get("action")

        if action == "approve":
            leave_request.approved = True  # Talep onaylandı
            leave_request.save()
            print(leave_request.approved)
            return Response({"message": "Leave request approved"}, status=status.HTTP_200_OK)

        elif action == "reject":
            leave_request.approved = False  # Talep reddedildi
            leave_request.save()
            return Response({"message": "Leave request rejected"}, status=status.HTTP_200_OK)

        # Geçersiz eylem durumu
        return Response({"error": "Invalid action, use 'approve' or 'reject'"}, status=status.HTTP_400_BAD_REQUEST)
