# Personel ve Yetkili Yönetim API'si

Bu proje, personel giriş-çıkış takibi, izin yönetimi ve yetkili onay işlemlerini gerçekleştirmek için geliştirilmiş bir API'yi içerir. Django REST Framework kullanılarak oluşturulmuştur.

---

## Kurulum

1. **Proje Depolarını Klonlayın:**
   ```bash
   git clone <repo-url>  
   cd <project-directory>  
python -m venv venv  
source venv/bin/activate  # Windows için: venv\Scripts\activate  
pip install -r requirements.txt  
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  


****Kullanılabilir Endpoint’ler****  

**Kullanıcı Yönetimi**  

1. Personel Giriş Yap  

	•	**Endpoint**: /api/personel_login/login/  
	•	**Yöntem**: POST  
	•	**Body**:  
`{  
  "username": "personel_kullanici_adi",  
  "password": "sifre"  
}`  
 
	•	**Dönüş**:  
	•	**Başarılı giriş**:  
`{  
  "message": "Login successful"  
}`  
2. ****Yetkili Giriş Yap****  

	•	**Endpoint**: /api/yetkili_login/login/  
	•	**Yöntem**: POST  
	•	**Body**:  
`{  
  "username": "yetkili_kullanici_adi",  
  "password": "sifre"  
}`  
3. ****Çıkış Yap****  

	•	**Endpoint**: /api/user_logout/  
	•	**Yöntem**: GET  
	•	**Dönüş**: Kullanıcıyı çıkış yapar ve ana sayfaya yönlendirir.  
 
******Giriş-Çıkış Takibi******  
1. **Tüm Kullanıcıların veya Kendi Verilerinin Listelenmesi**  

	•	**Endpoint**: /api/attendance/  
	•	**Yöntem**: GET  
	•	**Açıklama**:  
	•	Admin: Tüm personelin giriş-çıkış bilgilerini görebilir.  
	•	Personel: Sadece kendi giriş-çıkış bilgilerini görebilir.  
	•	**Dönüş**:  

`[  
  {  
    "user": "kullanici_adi",  
    "date": "2024-11-30",  
    "late": 15  # Geç kalma süresi dakika cinsinden  
  },
  ...
]`  
2. ****Giriş veya Çıkış Kaydı Oluştur****  

	•	**Endpoint**: /api/attendance/  
	•	**Yöntem**: POST  
	•	**Body**:  

`{  
  "check_in": "2024-11-30T09:30:00",  # ISO 8601 formatında tarih ve saat  
  "check_out": "2024-11-30T18:00:00"  # (isteğe bağlı)  
}`  

****İzin Yönetimi****  

1. **İzin Talebi Oluştur**  

	•	**Endpoint**: /api/leave_requests/  
	•	**Yöntem**: POST  
	•	**Body**:  
`{    
  "start_date": "2024-12-01",    
  "end_date": "2024-12-05",    
  "reason": "Yıllık izin talebi"    
}`  
2. ****İzin Taleplerini Görüntüle****  

	•	**Endpoint**: /api/leave_requests/  
	•	**Yöntem**: GET  
	•	**Dönüş**:    

`[  
  {  
    "id": 1,  
    "user": "kullanici_adi",  
    "start_date": "2024-12-01",  
    "end_date": "2024-12-05",  
    "reason": "Yıllık izin talebi",  
    "approved": false  
  },
  ...
]`  
******Yetkili İzin Onayı******  

1. ****İzin Onayla veya Reddet****  

	•	**Endpoint**: /api/leave_request_approval/<id>/approve_or_reject_leave/  
	•	**Yöntem**: POST  
	•	**Body**:    
`{  
  "action": "approve"  # veya "reject"  
}`  


 Kullanıcı Rolleri  

	1.	Admin:
	•	Tüm kullanıcıların giriş-çıkış ve izin bilgilerini görüntüleyebilir.
	•	Yeni kullanıcılar oluşturabilir.
	2.	Personel:
	•	Kendi giriş-çıkış ve izin bilgilerini görebilir.
	•	İzin talebinde bulunabilir.
	3.	Yetkili:
	•	İzin taleplerini onaylayabilir veya reddedebilir.