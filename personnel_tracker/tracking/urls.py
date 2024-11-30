from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    UserViewSet,
    AttendanceViewSet,
    LeaveRequestViewSet,
    UserLoginViewSet,
    YetkiliLoginViewSet,
    user_logout,
    LeaveRequestApprovalViewSet,
)

# REST Framework DefaultRouter
# DefaultRouter, ViewSet'ler için otomatik URL yönlendirmesi sağlar.
router = DefaultRouter()

# Kullanıcılarla ilgili CRUD işlemleri için endpoint.
router.register(r'users', UserViewSet)

# Giriş-çıkış kayıtlarını yönetmek için endpoint.
router.register(r'attendance', AttendanceViewSet)

# İzin taleplerini yönetmek için endpoint.
router.register(r'leave_requests', LeaveRequestViewSet)

# Personel için login endpoint.
router.register(r'personel_login', UserLoginViewSet, basename='personel-login')

# Yetkililer için login endpoint.
router.register(r'yetkili_login', YetkiliLoginViewSet, basename='yetkili-login')

# İzin taleplerinin onay/red işlemleri için endpoint.
router.register(r'leave_request_approval', LeaveRequestApprovalViewSet, basename="leave_request_approval")

# Router'dan gelen otomatik URL'ler.
urlpatterns = router.urls

# Ekstra URL'ler
# Kullanıcı çıkışı için manuel bir URL tanımı.
urlpatterns += [
    path('user_logout/', user_logout, name='user_logout'),  # Kullanıcı logout işlemi için endpoint.
]
