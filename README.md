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


Kullanılabilir Endpoint’ler

Kullanıcı Yönetimi

1. Personel Giriş Yap

	•	Endpoint: /api/personel_login/login/
	•	Yöntem: POST
	•	Body:
{
  "username": "personel_kullanici_adi",
  "password": "sifre"
}
