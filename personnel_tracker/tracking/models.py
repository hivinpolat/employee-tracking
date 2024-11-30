from time import time
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime, time
from django.db import models
from django.utils import timezone
from decimal import Decimal


# Kullanıcı Modeli
class CustomUser(AbstractUser):
    """
    Özel Kullanıcı Modeli: Django'nun varsayılan kullanıcı modelini genişletir.
    Yıllık izin bakiyesi ve gruplar/user_permissions için farklı related_name'ler tanımlanmıştır.
    """
    annual_leave_balance = models.DecimalField(
        max_digits=5,  # Maksimum 4 basamaklı sayı + 2 ondalık
        decimal_places=2,  # 2 ondalık basamak
        default=15,  # Varsayılan yıllık izin bakiyesi
    )

    # 'groups' alanına related_name parametresi eklenerek çakışma önleniyor
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Varsayılan 'user_set' yerine özel bir isim
        blank=True
    )

    # 'user_permissions' alanına related_name parametresi eklenerek çakışma önleniyor
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Varsayılan 'user_set' yerine özel bir isim
        blank=True
    )


# Giriş-Çıkış Takip Modeli
class Attendance(models.Model):
    """
    Çalışanların giriş ve çıkış kayıtlarını takip eden model.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # Kullanıcı silinirse ilgili kayıtlar da silinir
    )
    date = models.DateField(
        default=timezone.now,  # Varsayılan olarak bugünün tarihi
    )
    check_in = models.DateTimeField(
        null=True,  # Zorunlu değil
        blank=True,  # Formlarda boş geçilebilir
    )
    check_out = models.DateTimeField(
        null=True,  # Zorunlu değil
        blank=True,  # Formlarda boş geçilebilir
    )

    def __str__(self):
        """
        Kullanıcı ve tarihe göre okunabilir bir temsil döndürür.
        """
        return f"{self.user} - {self.date}"

    def is_late(self):
        """
        Çalışan geç mi geldi? Eğer geç geldiyse kaç dakika geç kaldığını döndürür.
        """
        if self.check_in:
            # Beklenen giriş saati
            expected_time = time(9, 0)  # 09:00 AM
            # Giriş saati beklenen saatten sonra mı?
            if self.check_in.time() > expected_time:
                # Geç kalınan süreyi dakika cinsinden hesapla
                late_minutes = (
                                       datetime.combine(self.date, self.check_in.time()) -
                                       datetime.combine(self.date, expected_time)
                               ).seconds // 60
                return late_minutes
        return 0

    def save(self, *args, **kwargs):
        """
        Kayıt kaydedilmeden önce çalışanın geç kalması durumunda yıllık izinden gün düşer.
        """
        late_minutes = self.is_late()
        if late_minutes > 0:
            # Geç kalınan süreyi gün cinsine çevir (8 saatlik iş günü üzerinden)
            late_days = Decimal(late_minutes) / (60 * 8)
            print(f"{self.user} is late by {late_days} days")  # Geç kalma bilgisi
            self.user.annual_leave_balance -= late_days  # Yıllık izin bakiyesinden düş
            self.user.save()  # Kullanıcıyı güncelle
        super().save(*args, **kwargs)  # Normal kayıt işlemini devam ettir


# İzin Talepleri Modeli
class LeaveRequest(models.Model):
    """
    Çalışanların izin taleplerini takip eden model.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # Kullanıcı silinirse ilgili izin talepleri de silinir
    )
    start_date = models.DateField()  # İznin başlama tarihi
    end_date = models.DateField()  # İznin bitiş tarihi
    reason = models.TextField()  # İzin talebinin gerekçesi
    approved = models.BooleanField(
        default=False,  # Varsayılan olarak onaylanmamış
    )

    def __str__(self):
        """
        Kullanıcı ve izin tarihlerini gösteren okunabilir bir temsil döndürür.
        """
        return f"Leave Request for {self.user.username} from {self.start_date} to {self.end_date}"

    def is_approved(self):
        """
        İzin talebinin durumu: Eğer çalışanın yıllık izni 3 günden azsa, yetkiliye bildirim yapılabilir.
        """
        if self.user.annual_leave_balance <= 3:
            # Yetkiliye bildirim yapılması için uygun bir yer olabilir
            pass
